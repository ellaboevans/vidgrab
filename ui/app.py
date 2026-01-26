import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QProgressBar, QFileDialog, QListWidget, QListWidgetItem, QMessageBox,
    QHBoxLayout
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QColor

from core.engine import DownloadEngine
from core.hooks import progress_hook_factory
from core.queue import QueueManager


# ---------------- Worker Thread ----------------
class DownloadWorker(QThread):
    progress = pyqtSignal(int)
    finished_one = pyqtSignal(bool)
    started_one = pyqtSignal()

    def __init__(self, queue_item, output_dir):
        super().__init__()
        self.item = queue_item
        self.output_dir = output_dir
        self._is_running = True

    def run(self):
        def on_progress(percent):
            if self._is_running:
                self.progress.emit(percent)

        def on_done(filename):
            pass

        engine = DownloadEngine(
            self.output_dir,
            hooks=[progress_hook_factory(on_progress, on_done)]
        )

        try:
            self.item.status = "Downloading"
            self.started_one.emit()
            
            # Check if we should stop before starting
            if not self._is_running:
                self.item.status = "Cancelled"
                self.finished_one.emit(False)
                return
            
            engine.download(self.item.url)
            
            # Check again after download completes
            if self._is_running:
                self.item.status = "Completed"
                self.finished_one.emit(True)
            else:
                self.item.status = "Cancelled"
                self.finished_one.emit(False)
        except Exception as e:
            if self._is_running:
                self.item.status = "Failed"
                self.finished_one.emit(False)

    def stop(self):
        """Signal the worker to stop"""
        self._is_running = False


# ---------------- Metadata Worker ----------------
class MetadataWorker(QThread):
    title_fetched = pyqtSignal(str)

    def __init__(self, url):
        super().__init__()
        self.url = url

    def run(self):
        try:
            import yt_dlp
            ydl_opts = {
                "quiet": True,
                "skip_download": True,
                "extract_flat": True,
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                title = info.get("title", self.url)
                self.title_fetched.emit(title)
        except Exception:
            self.title_fetched.emit(self.url)


# ---------------- Main GUI ----------------
class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setMinimumSize(600, 480)

        layout = QVBoxLayout()

        self.queue = QueueManager()
        self.total_items = 0
        self.completed_items = 0
        self.current_worker = None
        self.metadata_workers = []  # Track active metadata workers
        self.is_downloading = False

        # URL input
        layout.addWidget(QLabel("YouTube URL"))
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste video or playlist URL")
        layout.addWidget(self.url_input)

        # Folder chooser
        self.folder_label = QLabel("Download folder")
        layout.addWidget(self.folder_label)
        self.folder_btn = QPushButton("Choose Folder")
        self.folder_btn.clicked.connect(self.choose_folder)
        layout.addWidget(self.folder_btn)

        # Buttons
        btn_layout = QHBoxLayout()
        self.add_btn = QPushButton("Add to Queue")
        self.start_btn = QPushButton("Start Downloads")
        self.stop_btn = QPushButton("Stop")
        self.add_btn.clicked.connect(self.add_to_queue)
        self.start_btn.clicked.connect(self.start_queue)
        self.stop_btn.clicked.connect(self.stop_downloads)
        self.stop_btn.setEnabled(False)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Status
        self.status_label = QLabel("Idle")
        layout.addWidget(self.status_label)

        # Download list
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.setLayout(layout)
        self.output_dir = ""

    def closeEvent(self, event):
        """Clean up threads before closing"""
        # Stop all metadata workers with timeout
        for worker in self.metadata_workers:
            if worker.isRunning():
                worker.quit()
                if not worker.wait(2000):  # 2 second timeout
                    worker.terminate()
                    worker.wait()
        
        # Stop the current download worker with timeout
        if self.current_worker and self.current_worker.isRunning():
            self.current_worker.stop()
            if not self.current_worker.wait(5000):  # 5 second timeout
                self.current_worker.terminate()
                self.current_worker.wait()
        
        event.accept()

    # ---------------- Folder ----------------
    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select download folder")
        if folder:
            self.output_dir = folder
            self.folder_label.setText(f"Download folder: {folder}")

    # ---------------- Queue ----------------
    def add_to_queue(self):
        url = self.url_input.text().strip()
        if not url:
            return

        # Temporarily use URL as title until metadata is fetched
        item_index = self.list_widget.count()
        self.queue.add(url, url)
        list_item = QListWidgetItem(f"⏳ Waiting: Fetching title...")
        list_item.setForeground(QColor("gray"))
        self.list_widget.addItem(list_item)

        # Fetch metadata in background
        worker = MetadataWorker(url)
        worker.title_fetched.connect(
            lambda title, row=item_index, w=worker: self.on_title_ready(row, title, w)
        )
        self.metadata_workers.append(worker)
        worker.start()
        self.url_input.clear()

    def on_title_ready(self, row, title, worker):
        self.queue.queue[row].title = title
        self.list_widget.item(row).setText(f"⏳ Waiting: {title}")
        # Wait for thread to finish and remove it
        worker.wait()
        if worker in self.metadata_workers:
            self.metadata_workers.remove(worker)

    # ---------------- Queue Processing ----------------
    def start_queue(self):
        if not self.output_dir:
            QMessageBox.warning(self, "Missing folder", "Please choose a download folder first")
            return
        if not self.queue.has_next():
            QMessageBox.information(self, "Queue empty", "Please add at least one URL to the queue")
            return

        self.total_items = len(self.queue.queue)
        self.completed_items = 0
        self.is_downloading = True
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.start_next_download()

    def start_next_download(self):
        item = self.queue.next_item()
        if not item:
            self.status_label.setText("All downloads completed")
            self.progress_bar.setValue(100)
            self.start_btn.setEnabled(True)
            return

        index = self.queue.current_index + 1
        self.status_label.setText(f"Downloading {index} of {self.total_items}")
        self.progress_bar.setValue(int((self.completed_items / self.total_items) * 100))

        self.current_worker = DownloadWorker(item, self.output_dir)
        self.current_worker.progress.connect(lambda p, row=self.queue.current_index: self.update_item_progress(row, p))
        self.current_worker.started_one.connect(lambda row=self.queue.current_index: self.set_item_status(row, "In Progress"))
        self.current_worker.finished_one.connect(self.on_item_finished)
        self.current_worker.start()

    def set_item_status(self, row, status):
        item = self.list_widget.item(row)
        title = self.queue.queue[row].title
        if status == "In Progress":
            item.setText(f"▶️ {status}: {title}")
            item.setForeground(QColor("blue"))
        elif status == "Completed":
            item.setText(f"✅ {title}")
            item.setForeground(QColor("green"))
        elif status == "Failed":
            item.setText(f"❌ {title}")
            item.setForeground(QColor("red"))

    def update_item_progress(self, row, percent):
        item = self.list_widget.item(row)
        title = self.queue.queue[row].title
        item.setText(f"▶️ In Progress: {title} ({percent}%)")

    def on_item_finished(self, success):
        row = self.queue.current_index
        self.completed_items += 1
        self.set_item_status(row, "Completed" if success else "Failed")

        # Update overall progress
        overall_percent = int((self.completed_items / self.total_items) * 100)
        self.progress_bar.setValue(overall_percent)

        if self.is_downloading and self.queue.has_next():
            self.start_next_download()
        else:
            self.status_label.setText("All downloads completed")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.progress_bar.setValue(100)
            self.is_downloading = False

    def stop_downloads(self):
        """Stop current download and pause the queue"""
        self.is_downloading = False
        self.status_label.setText("Downloads stopped")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        # Stop the current worker gracefully
        if self.current_worker and self.current_worker.isRunning():
            self.current_worker.stop()
            # Wait with timeout to prevent freezing
            if not self.current_worker.wait(5000):  # 5 second timeout
                self.current_worker.terminate()
                self.current_worker.wait()


# ---------------- App Entry ----------------
def main():
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec())

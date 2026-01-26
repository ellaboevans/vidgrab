import sys
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QProgressBar,
    QFileDialog,
    QListWidget,
    QListWidgetItem,
    QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal

from core.engine import DownloadEngine
from core.hooks import progress_hook_factory
from core.queue import QueueManager


# ---------------- Worker Thread ----------------
class DownloadWorker(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)
    finished_one = pyqtSignal(bool)
    started_one = pyqtSignal()  # signal when download starts

    def __init__(self, queue_item, output_dir):
        super().__init__()
        self.item = queue_item
        self.output_dir = output_dir

    def run(self):
        def on_progress(percent):
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
            engine.download(self.item.url)
            self.item.status = "Completed"
            self.finished_one.emit(True)
        except Exception:
            self.item.status = "Failed"
            self.finished_one.emit(False)


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
        self.setMinimumSize(600, 420)

        layout = QVBoxLayout()

        self.queue = QueueManager()
        self.metadata_workers = []  # store active metadata threads

        self.total_items = 0
        self.completed_items = 0

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
        self.add_btn = QPushButton("Add to Queue")
        self.start_btn = QPushButton("Start Downloads")
        self.add_btn.clicked.connect(self.add_to_queue)
        self.start_btn.clicked.connect(self.start_queue)
        layout.addWidget(self.add_btn)
        layout.addWidget(self.start_btn)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Idle")
        layout.addWidget(self.status_label)

        # Download list
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.setLayout(layout)
        self.output_dir = ""

    # ---------------- Folder selection ----------------
    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select download folder")
        if folder:
            self.output_dir = folder
            self.folder_label.setText(f"Download folder: {folder}")

    # ---------------- Queue management ----------------
    def add_to_queue(self):
        url = self.url_input.text().strip()
        if not url:
            return

        # Add placeholder QueueItem with temporary title
        self.queue.add(url, title="Fetching title...")
        list_item = QListWidgetItem(f"Waiting: Fetching title...")
        self.list_widget.addItem(list_item)
        row = self.list_widget.count() - 1

        # Start metadata worker
        worker = MetadataWorker(url)
        worker.title_fetched.connect(
            lambda title, r=row, w=worker: self.on_title_ready_and_cleanup(r, title, w)
        )
        self.metadata_workers.append(worker)
        worker.start()

        self.url_input.clear()

    def on_title_ready_and_cleanup(self, row, title, worker):
        # Update the QueueItem and list widget
        self.queue.queue[row].title = title
        self.list_widget.item(row).setText(f"Waiting: {title}")

        # Clean up thread
        if worker in self.metadata_workers:
            self.metadata_workers.remove(worker)
        worker.quit()
        worker.wait()

    # ---------------- Start downloading ----------------
    def start_queue(self):
        if not self.output_dir:
            QMessageBox.warning(self, "Missing folder", "Please choose a download folder first")
            return

        if not self.queue.has_next():
            QMessageBox.information(self, "Queue empty", "Please add at least one URL to the queue")
            return

        self.total_items = len(self.queue.queue)
        self.completed_items = 0
        self.start_btn.setEnabled(False)
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

        self.worker = DownloadWorker(item, self.output_dir)
        self.worker.progress.connect(self.update_overall_progress)
        self.worker.started_one.connect(
            lambda: self.list_widget.item(self.queue.current_index)
            .setText(f"In Progress: {item.title}")
        )
        self.worker.finished_one.connect(self.on_item_finished)
        self.worker.start()

    def on_item_finished(self, success):
        row = self.queue.current_index
        status = "Completed" if success else "Failed"
        self.list_widget.item(row).setText(f"{status}: {self.queue.queue[row].title}")

        self.completed_items += 1

        if self.queue.has_next():
            self.start_next_download()
        else:
            self.status_label.setText("All downloads completed")
            self.progress_bar.setValue(100)
            self.start_btn.setEnabled(True)

    # ---------------- Progress calculation ----------------
    def update_overall_progress(self, video_percent):
        overall = ((self.completed_items + (video_percent / 100)) / self.total_items) * 100
        self.progress_bar.setValue(int(overall))


# ---------------- App Entry ----------------
def main():
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec())

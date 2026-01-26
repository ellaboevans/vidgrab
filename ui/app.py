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
            engine.download(self.item.url)
            self.item.status = "Completed"
            self.finished_one.emit(True)
        except Exception:
            self.item.status = "Failed"
            self.finished_one.emit(False)


# ---------------- Main GUI ----------------
class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setMinimumSize(600, 420)

        layout = QVBoxLayout()

        self.queue = QueueManager()

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

        # Status
        self.status_label = QLabel("Idle")
        layout.addWidget(self.status_label)

        # Download list
        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.setLayout(layout)
        self.output_dir = ""

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select download folder")
        if folder:
            self.output_dir = folder
            self.folder_label.setText(f"Download folder: {folder}")

    def start_download(self):
        url = self.url_input.text().strip()
        if not url or not self.output_dir:
            QMessageBox.warning(self, "Missing info", "Please enter URL and select a folder")
            return

        self.download_btn.setEnabled(False)
        self.progress_bar.setValue(0)
        self.list_widget.clear()

        self.worker = DownloadWorker(url, self.output_dir)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.status.connect(self.status_label.setText)
        self.worker.video_done.connect(self.add_completed_video)
        self.worker.finished.connect(self.download_finished)
        self.worker.start()

    def add_completed_video(self, filename):
        item = QListWidgetItem(f"Completed: {filename}")
        self.list_widget.addItem(item)

    def download_finished(self):
        self.download_btn.setEnabled(True)

    def add_to_queue(self):
        url = self.url_input.text().strip()
        if not url:
            return

        self.queue.add(url)
        self.list_widget.addItem(f"Waiting: {url}")
        self.url_input.clear()

    def start_queue(self):
        if not self.queue.has_next():
            return
        self.start_next_download()

    def start_next_download(self):
        item = self.queue.next_item()
        if not item:
            self.status_label.setText("All downloads completed")
            return

        row = self.queue.current_index

        # 🔥 UPDATE LIST ITEM WHEN DOWNLOAD STARTS
        self.list_widget.item(row).setText(f"In progress: {item.url}")

        self.status_label.setText("Downloading...")
        self.progress_bar.setValue(0)

        self.worker = DownloadWorker(item, self.output_dir)
        self.worker.progress.connect(self.progress_bar.setValue)
        self.worker.finished_one.connect(self.on_item_finished)
        self.worker.start()

    def on_item_finished(self, success):
        row = self.queue.current_index
        status = "Completed" if success else "Failed"
        self.list_widget.item(row).setText(f"{status}: {self.queue.queue[row].url}")

        if self.queue.has_next():
            self.start_next_download()
        else:
            self.status_label.setText("All downloads completed")

# ---------------- App Entry ----------------
def main():
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec())

import sys
import subprocess
import json
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QProgressBar, QFileDialog
)
from PyQt6.QtCore import QThread, pyqtSignal

# --------- Worker Thread for Downloading ---------
class DownloadWorker(QThread):
    progress_signal = pyqtSignal(dict)
    finished_signal = pyqtSignal(dict)

    def __init__(self, url, output_dir):
        super().__init__()
        self.url = url
        self.output_dir = output_dir

    def run(self):
        # Run downloader.py as subprocess and parse JSON output
        cmd = [
            sys.executable,  # use the same Python interpreter
            str(Path(__file__).parent / "downloader.py"),
            self.url,
            self.output_dir
        ]

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

        for line in process.stdout:
            line = line.strip()
            try:
                data = json.loads(line)
                if data.get("type") in ["progress", "done"]:
                    self.progress_signal.emit(data)
            except json.JSONDecodeError:
                continue

        process.wait()
        self.finished_signal.emit({"type": "finished"})


# --------- Main GUI Window ---------
class DownloaderGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setMinimumSize(500, 200)

        # Layout
        layout = QVBoxLayout()

        # URL input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter YouTube URL here...")
        layout.addWidget(self.url_input)

        # Output folder selector
        self.folder_label = QLabel("Select download folder")
        layout.addWidget(self.folder_label)

        self.select_folder_btn = QPushButton("Choose Folder")
        self.select_folder_btn.clicked.connect(self.select_folder)
        layout.addWidget(self.select_folder_btn)

        # Download button
        self.download_btn = QPushButton("Download")
        self.download_btn.clicked.connect(self.start_download)
        layout.addWidget(self.download_btn)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("Idle")
        layout.addWidget(self.status_label)

        self.setLayout(layout)
        self.output_dir = str(Path.home() / "Downloads")  # default

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Download Folder", str(Path.home()))
        if folder:
            self.output_dir = folder
            self.folder_label.setText(f"Download folder: {folder}")

    def start_download(self):
        url = self.url_input.text().strip()
        if not url:
            self.status_label.setText("Please enter a valid URL!")
            return

        self.download_btn.setEnabled(False)
        self.status_label.setText("Starting download...")

        self.worker = DownloadWorker(url, self.output_dir)
        self.worker.progress_signal.connect(self.update_progress)
        self.worker.finished_signal.connect(self.download_finished)
        self.worker.start()

    def update_progress(self, data):
        if data["type"] == "progress":
            downloaded = data.get("downloaded_bytes", 0)
            total = data.get("total_bytes") or data.get("total_bytes_estimate") or 1
            percent = int(downloaded / total * 100) if total else 0
            self.progress_bar.setValue(percent)
            self.status_label.setText(f"Downloading: {percent}%")
        elif data["type"] == "done":
            self.progress_bar.setValue(100)
            filename = data.get("filename", "Unknown")
            self.status_label.setText(f"Download complete: {filename}")

    def download_finished(self, data):
        self.download_btn.setEnabled(True)
        # Only set Idle if not already marked as done
        if self.status_label.text().startswith("Downloading"):
            self.status_label.setText("Download finished")


# --------- Run App ---------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DownloaderGUI()
    window.show()
    sys.exit(app.exec())

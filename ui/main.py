# ui/main.py

import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QProgressBar, QFileDialog,
    QListWidget, QListWidgetItem, QMessageBox
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import yt_dlp

# ---------------- Worker Thread ----------------
class DownloadWorker(QThread):
    progress_update = pyqtSignal(int)  # progress of current video (0-100)
    status_update = pyqtSignal(str)    # status text
    video_update = pyqtSignal(str)     # current video title
    finished_all = pyqtSignal()        # when all downloads are done
    video_done = pyqtSignal(str, str)  # (video title, status)

    def __init__(self, url, output_dir):
        super().__init__()
        self.url = url
        self.output_dir = output_dir

    def run(self):
        ydl_opts = {
            'outtmpl': os.path.join(self.output_dir, '%(playlist_index)s - %(title)s.%(ext)s'),
            'noplaylist': False,  # allow playlists
            'progress_hooks': [self.hook],
            'ignoreerrors': True,
            'format': 'bestvideo+bestaudio/best',
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                self.status_update.emit("Starting download...")
                info = ydl.extract_info(self.url, download=True)

                # handle playlist or single video
                if 'entries' in info:  # playlist
                    total = len(info['entries'])
                    for idx, entry in enumerate(info['entries'], start=1):
                        if entry is None:
                            continue
                        title = entry.get('title', 'Unknown')
                        self.video_update.emit(f"{idx}/{total}: {title}")
                        # individual video progress handled by hook
                else:  # single video
                    title = info.get('title', 'Unknown')
                    self.video_update.emit(title)

            self.finished_all.emit()
        except Exception as e:
            self.status_update.emit(f"Error: {str(e)}")
            self.finished_all.emit()

    def hook(self, d):
        if d['status'] == 'downloading':
            if d.get('total_bytes') and d.get('downloaded_bytes'):
                percent = int(d['downloaded_bytes'] / d['total_bytes'] * 100)
                self.progress_update.emit(percent)
        elif d['status'] == 'finished':
            self.progress_update.emit(100)
            self.video_done.emit(d.get('filename', 'Unknown'), "Completed")


# ---------------- Main GUI ----------------
class YouTubeDownloader(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(300, 300, 600, 400)

        layout = QVBoxLayout()

        self.url_label = QLabel("YouTube URL:")
        self.url_input = QLineEdit()
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)

        self.folder_label = QLabel("Save Folder:")
        self.folder_input = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_folder)
        layout.addWidget(self.folder_label)
        layout.addWidget(self.folder_input)
        layout.addWidget(self.browse_button)

        self.download_button = QPushButton("Download")
        self.download_button.clicked.connect(self.start_download)
        layout.addWidget(self.download_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        layout.addWidget(self.progress_bar)

        self.status_label = QLabel("Status: Idle")
        layout.addWidget(self.status_label)

        self.video_list = QListWidget()
        layout.addWidget(self.video_list)

        self.setLayout(layout)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_input.setText(folder)

    def start_download(self):
        url = self.url_input.text().strip()
        folder = self.folder_input.text().strip()
        if not url or not folder:
            QMessageBox.warning(self, "Warning", "Please enter URL and select folder")
            return

        self.download_button.setEnabled(False)
        self.progress_bar.setValue(0)
        self.status_label.setText("Status: Starting...")

        self.video_list.clear()
        self.worker = DownloadWorker(url, folder)
        self.worker.progress_update.connect(self.update_progress)
        self.worker.status_update.connect(self.update_status)
        self.worker.video_update.connect(self.update_current_video)
        self.worker.video_done.connect(self.update_video_list)
        self.worker.finished_all.connect(self.download_finished)
        self.worker.start()

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_status(self, text):
        self.status_label.setText(f"Status: {text}")

    def update_current_video(self, text):
        self.status_label.setText(f"Downloading: {text}")

    def update_video_list(self, filename, status):
        item = QListWidgetItem(f"{filename} - {status}")
        self.video_list.addItem(item)

    def download_finished(self):
        self.status_label.setText("Status: All downloads completed!")
        self.download_button.setEnabled(True)


# ---------------- Run App ----------------
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeDownloader()
    window.show()
    sys.exit(app.exec())

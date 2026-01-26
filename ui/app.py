import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QProgressBar, QFileDialog, QListWidget, QListWidgetItem, QMessageBox,
    QHBoxLayout, QDialog
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QColor

import subprocess
from core.engine import DownloadEngine
from core.hooks import progress_hook_factory
from core.queue import QueueManager
from core.settings import SettingsManager
from core.logger import log_error, log_info, AppLogger
from core.validators import URLValidator
from core.queue_persistence import QueuePersistence
from ui.settings_dialog import SettingsDialog


# ---------------- Worker Thread ----------------
class DownloadWorker(QThread):
    progress = pyqtSignal(int)
    finished_one = pyqtSignal(bool, str)  # success, error_message
    started_one = pyqtSignal()

    def __init__(self, queue_item, output_dir, quality="best", format="mp4"):
        super().__init__()
        self.item = queue_item
        self.output_dir = output_dir
        self.quality = quality
        self.format = format
        self._is_running = True
        self.error_message = ""

    def run(self):
        def on_progress(percent):
            if self._is_running:
                self.progress.emit(percent)

        def on_done(filename):
            pass

        engine = DownloadEngine(
            self.output_dir,
            hooks=[progress_hook_factory(on_progress, on_done)],
            quality=self.quality,
            format=self.format
        )

        try:
            self.item.status = "Downloading"
            self.started_one.emit()
            log_info(f"Starting download: {self.item.url}")
            
            # Check if we should stop before starting
            if not self._is_running:
                self.item.status = "Cancelled"
                self.finished_one.emit(False, "Download cancelled by user")
                return
            
            engine.download(self.item.url)
            
            # Check again after download completes
            if self._is_running:
                self.item.status = "Completed"
                log_info(f"Download completed: {self.item.title}")
                self.finished_one.emit(True, "")
            else:
                self.item.status = "Cancelled"
                self.finished_one.emit(False, "Download cancelled by user")
        except Exception as e:
            error_msg = f"Download failed: {str(e)}"
            log_error(f"Error downloading {self.item.url}: {str(e)}", exc_info=True)
            if self._is_running:
                self.item.status = "Failed"
                self.error_message = error_msg
                self.finished_one.emit(False, error_msg)

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

        # Initialize settings and queue persistence
        self.settings_manager = SettingsManager()
        self.settings = self.settings_manager.get()
        self.queue_persistence = QueuePersistence()

        self.queue = QueueManager()
        
        # Load saved queue if exists
        self.queue_persistence.load_queue(self.queue)
        
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
        self.logs_btn = QPushButton("View Logs")
        self.settings_btn = QPushButton("Settings")
        self.add_btn.clicked.connect(self.add_to_queue)
        self.start_btn.clicked.connect(self.start_queue)
        self.stop_btn.clicked.connect(self.stop_downloads)
        self.logs_btn.clicked.connect(self.view_logs)
        self.settings_btn.clicked.connect(self.open_settings)
        self.stop_btn.setEnabled(False)
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addStretch()
        btn_layout.addWidget(self.logs_btn)
        btn_layout.addWidget(self.settings_btn)
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
        # Load default folder from settings
        self.output_dir = self.settings.download_folder
        
        # Populate UI with loaded queue items
        self._populate_queue_ui()

    def _populate_queue_ui(self):
        """Populate the queue list widget with loaded queue items"""
        for item in self.queue.queue:
            if item.status == "Completed":
                color = QColor("green")
                icon = "✅"
            elif item.status == "Failed":
                color = QColor("red")
                icon = "❌"
            elif item.status == "Cancelled":
                color = QColor("gray")
                icon = "⏹️"
            else:  # Waiting, Downloading
                color = QColor("gray")
                icon = "⏳"
            
            list_item = QListWidgetItem(f"{icon} {item.status}: {item.title}")
            list_item.setForeground(color)
            self.list_widget.addItem(list_item)

    def closeEvent(self, event):
        """Clean up threads and save state before closing"""
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
        
        # Save queue before closing
        self.queue_persistence.save_queue(self.queue)
        log_info("Application closed")
        
        event.accept()

    # ---------------- Settings & Logs ----------------
    def open_settings(self):
        """Open settings dialog"""
        dialog = SettingsDialog(self, self.settings_manager)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Reload settings after they're saved
            self.settings = self.settings_manager.get()
            self.output_dir = self.settings.download_folder
            self.folder_label.setText(f"Download folder: {self.output_dir}")

    def view_logs(self):
        """Open log file in default text editor"""
        try:
            log_file = AppLogger().get_log_file()
            if log_file.exists():
                # Open with default application
                if sys.platform == "darwin":  # macOS
                    subprocess.run(["open", str(log_file)])
                elif sys.platform == "win32":  # Windows
                    subprocess.run(["notepad", str(log_file)])
                else:  # Linux
                    subprocess.run(["xdg-open", str(log_file)])
                log_info(f"Opened log file: {log_file}")
            else:
                QMessageBox.information(self, "No Logs", "No log file found yet. Logs will be created after the first download.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open log file: {str(e)}")
            log_error(f"Error opening log file: {str(e)}", exc_info=True)

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
            QMessageBox.warning(self, "Empty URL", "Please paste a URL before adding to queue")
            return

        # Validate URL format
        is_valid, error_msg = URLValidator.is_valid_youtube_url(url)
        if not is_valid:
            QMessageBox.warning(self, "Invalid URL", error_msg)
            log_error(f"Invalid URL attempted: {url}")
            return

        # Check for duplicates
        is_duplicate, existing_title = URLValidator.is_duplicate(url, self.queue.queue)
        if is_duplicate:
            QMessageBox.information(
                self,
                "Already in Queue",
                f"This URL is already in your queue:\n{existing_title}"
            )
            log_info(f"Duplicate URL detected: {url}")
            return

        log_info(f"Adding URL to queue: {url}")

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

        self.current_worker = DownloadWorker(
            item,
            self.output_dir,
            quality=self.settings.video_quality,
            format=self.settings.format
        )
        self.current_worker.progress.connect(lambda p, row=self.queue.current_index: self.update_item_progress(row, p))
        self.current_worker.started_one.connect(lambda row=self.queue.current_index: self.set_item_status(row, "In Progress"))
        self.current_worker.finished_one.connect(self.on_item_finished)
        self.current_worker.start()

    def set_item_status(self, row, status, error_msg=""):
        item = self.list_widget.item(row)
        queue_item = self.queue.queue[row]
        title = queue_item.title
        
        if status == "In Progress":
            item.setText(f"▶️ {status}: {title}")
            item.setForeground(QColor("blue"))
        elif status == "Completed":
            item.setText(f"✅ {title}")
            item.setForeground(QColor("green"))
        elif status == "Failed":
            queue_item.error_message = error_msg
            retry_text = f" (Retry {queue_item.retry_count}/{queue_item.max_retries})" if queue_item.retry_count > 0 else ""
            item.setText(f"❌ {title}{retry_text}")
            item.setForeground(QColor("red"))
        elif status == "Cancelled":
            item.setText(f"⏹️ {title}")
            item.setForeground(QColor("gray"))

    def update_item_progress(self, row, percent):
        item = self.list_widget.item(row)
        title = self.queue.queue[row].title
        item.setText(f"▶️ In Progress: {title} ({percent}%)")

    def on_item_finished(self, success, error_msg=""):
        row = self.queue.current_index
        queue_item = self.queue.queue[row]
        
        if success:
            self.completed_items += 1
            self.set_item_status(row, "Completed")
            log_info(f"Successfully downloaded: {queue_item.title}")
        else:
            # Try to retry if we haven't exceeded max retries
            if queue_item.retry_count < queue_item.max_retries:
                queue_item.retry_count += 1
                self.set_item_status(row, "Failed", error_msg)
                log_warning(f"Download failed, retrying ({queue_item.retry_count}/{queue_item.max_retries}): {queue_item.title}")
                
                # Show error to user
                QMessageBox.warning(
                    self,
                    "Download Failed",
                    f"Failed to download: {queue_item.title}\n\nError: {error_msg}\n\nRetrying ({queue_item.retry_count}/{queue_item.max_retries})..."
                )
                
                # Retry this item
                if self.is_downloading:
                    self.start_next_download()
                return
            else:
                self.completed_items += 1
                self.set_item_status(row, "Failed", error_msg)
                log_error(f"Download failed after {queue_item.max_retries} retries: {queue_item.title}")
                
                # Show final error to user
                QMessageBox.critical(
                    self,
                    "Download Failed",
                    f"Failed to download: {queue_item.title}\n\nError: {error_msg}\n\nMax retries exceeded."
                )

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

import sys
from typing import Optional
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton,
    QProgressBar, QFileDialog, QListWidget, QListWidgetItem, QMessageBox,
    QHBoxLayout, QDialog, QSpacerItem, QSizePolicy, QFrame, QMenu
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
from PyQt6.QtGui import QColor, QKeySequence

import subprocess
from core.engine import DownloadEngine
from core.hooks import progress_hook_factory
from core.queue import QueueManager
from core.settings import SettingsManager
from core.logger import log_error, log_info, log_warning, get_logger
from core.validators import URLValidator
from core.queue_persistence import QueuePersistence
from core.types import ItemStatus
from core.download_session import DownloadSession
from ui.settings_dialog import SettingsDialog
from ui.splash_screen import show_splash, hide_splash
from ui.theme import load_stylesheet, Colors
from ui.notifications import show_notification


# ---------------- Worker Thread ----------------
class DownloadWorker(QThread):
    progress = pyqtSignal(int, str)  # percent, detail_string
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
        def on_progress(percent, detail=""):
            if self._is_running:
                self.progress.emit(percent, detail)

        def on_done(filename):
            pass

        engine = DownloadEngine(
            self.output_dir,
            hooks=[progress_hook_factory(on_progress, on_done)],
            quality=self.quality,
            format=self.format
        )

        try:
            self.item.status = ItemStatus.DOWNLOADING
            self.started_one.emit()
            log_info(f"Starting download: {self.item.url}")
            
            # Check if we should stop before starting
            if not self._is_running:
                self.item.status = ItemStatus.CANCELLED
                self.finished_one.emit(False, "Download cancelled by user")
                return
            
            engine.download(self.item.url)
            
            # Check again after download completes
            if self._is_running:
                self.item.status = ItemStatus.COMPLETED
                log_info(f"Download completed: {self.item.title}")
                self.finished_one.emit(True, "")
            else:
                self.item.status = ItemStatus.CANCELLED
                self.finished_one.emit(False, "Download cancelled by user")
        except Exception as e:
            error_msg = f"Download failed: {str(e)}"
            log_error(f"Error downloading {self.item.url}: {str(e)}", exc_info=True)
            if self._is_running:
                self.item.status = ItemStatus.FAILED
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
        self.setWindowTitle("VidGrab")
        self.setMinimumSize(700, 550)

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(16, 16, 16, 16)

        # Initialize settings and queue persistence
        self.settings_manager = SettingsManager()
        self.settings = self.settings_manager.get()
        self.queue_persistence = QueuePersistence()

        self.queue = QueueManager()
        
        # Load saved queue if exists
        self.queue_persistence.load_queue(self.queue)
        
        # Initialize download session (None when not downloading)
        self.session: Optional[DownloadSession] = None
        self.metadata_workers = []  # Track active metadata workers

        # URL input section
        url_label = QLabel("YouTube URL")
        url_label.setObjectName("sectionHeader")
        layout.addWidget(url_label)
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Paste video or playlist URL")
        layout.addWidget(self.url_input)

        # Folder chooser section with shaded background
        folder_label_header = QLabel("Download Folder")
        folder_label_header.setObjectName("sectionHeader")
        layout.addWidget(folder_label_header)
        
        # Create frame with background for folder display
        folder_frame = QFrame()
        folder_frame.setObjectName("folderFrame")
        folder_frame_layout = QHBoxLayout()
        folder_frame_layout.setContentsMargins(0, 0, 0, 0)
        
        self.folder_label = QLabel(self.settings.download_folder)
        self.folder_label.setStyleSheet(f"color: {Colors.TEXT_SECONDARY}; font-size: 11px; background: transparent;")
        self.folder_label.setWordWrap(True)
        
        self.folder_btn = QPushButton("Browse")
        self.folder_btn.setMaximumWidth(100)
        self.folder_btn.clicked.connect(self.choose_folder)
        
        folder_frame_layout.addWidget(self.folder_label)
        folder_frame_layout.addStretch()
        folder_frame_layout.addWidget(self.folder_btn)
        folder_frame.setLayout(folder_frame_layout)
        layout.addWidget(folder_frame)

        # Spacing
        layout.addSpacing(4)

        # Action buttons
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)
        
        self.add_btn = QPushButton("Add to Queue")
        self.start_btn = QPushButton("Start Downloads")
        self.start_btn.setObjectName("primaryButton")
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setObjectName("dangerButton")
        self.clear_queue_btn = QPushButton("Clear Queue")
        self.open_folder_btn = QPushButton("Open Folder")
        
        self.add_btn.clicked.connect(self.add_to_queue)
        self.start_btn.clicked.connect(self.start_queue)
        self.stop_btn.clicked.connect(self.stop_downloads)
        self.clear_queue_btn.clicked.connect(self.clear_queue)
        self.open_folder_btn.clicked.connect(self.open_download_folder)
        self.stop_btn.setEnabled(False)
        
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.addWidget(self.clear_queue_btn)
        btn_layout.addWidget(self.open_folder_btn)
        btn_layout.addStretch()
        
        # Settings and logs buttons (right side)
        self.logs_btn = QPushButton("Logs")
        self.settings_btn = QPushButton("Settings")
        self.logs_btn.clicked.connect(self.view_logs)
        self.settings_btn.clicked.connect(self.open_settings)
        self.logs_btn.setMaximumWidth(80)
        self.settings_btn.setMaximumWidth(80)
        
        btn_layout.addWidget(self.logs_btn)
        btn_layout.addWidget(self.settings_btn)
        layout.addLayout(btn_layout)

        # Progress bar with percentage display
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        self.progress_bar.setFormat("%p%")  # Show percentage
        layout.addWidget(self.progress_bar)

        # Status
        self.status_label = QLabel("Idle")
        self.status_label.setObjectName("statusLabel")
        layout.addWidget(self.status_label)

        # Download list header
        queue_header = QLabel("Download Queue")
        queue_header.setObjectName("sectionHeader")
        layout.addWidget(queue_header)

        # Download list
        self.list_widget = QListWidget()
        self.list_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.list_widget.customContextMenuRequested.connect(self.show_queue_context_menu)
        layout.addWidget(self.list_widget)

        self.setLayout(layout)
        # Load default folder from settings
        self.output_dir = self.settings.download_folder
        
        # Populate UI with loaded queue items
        self._populate_queue_ui()

    def _populate_queue_ui(self):
        """Populate the queue list widget with loaded queue items"""
        for item in self.queue.queue:
            if item.status == ItemStatus.COMPLETED:
                color = QColor(Colors.STATUS_COMPLETED)
                icon = "✅"
            elif item.status == ItemStatus.FAILED:
                color = QColor(Colors.STATUS_FAILED)
                icon = "❌"
            elif item.status == ItemStatus.CANCELLED:
                color = QColor(Colors.STATUS_CANCELLED)
                icon = "⏹️"
            else:  # Waiting, Downloading
                color = QColor(Colors.STATUS_WAITING)
                icon = "⏳"
            
            list_item = QListWidgetItem(f"{icon} {item.status.value}: {item.title}")
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
        if self.session and self.session.current_worker and self.session.current_worker.isRunning():
            self.session.current_worker.stop()
            if not self.session.current_worker.wait(5000):  # 5 second timeout
                self.session.current_worker.terminate()
                self.session.current_worker.wait()
        
        # Save queue before closing
        self.queue_persistence.save_queue(self.queue)
        log_info("Application closed")
        
        event.accept()

    # ---------------- Queue Management ----------------
    def clear_queue(self):
        """Clear all items from queue"""
        if not self.queue.queue:
            QMessageBox.information(self, "Queue Empty", "The queue is already empty")
            return
        
        reply = QMessageBox.question(
            self,
            "Clear Queue",
            f"Are you sure you want to clear all {len(self.queue.queue)} items from the queue?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.queue.queue.clear()
            self.queue.current_index = -1
            self.list_widget.clear()
            self.queue_persistence.clear_saved_queue()
            self.status_label.setText("Queue cleared")
            log_info("Queue cleared by user")

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
            log_file = get_logger().get_log_file()
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
            self.folder_label.setText(folder)

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
        list_item = QListWidgetItem("⏳ Waiting: Fetching title...")
        list_item.setForeground(QColor(Colors.STATUS_WAITING))
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

        # Create new session for this batch of downloads
        self.session = DownloadSession(queue_items=self.queue.queue)
        self.session.is_running = True
        self.start_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.start_next_download()

    def start_next_download(self):
        item = self.queue.next_item()
        if not item:
            self.status_label.setText("All downloads completed")
            self.progress_bar.setValue(100)
            self.start_btn.setEnabled(True)
            if self.session:
                self.session.reset()
            return

        index = self.queue.current_index + 1
        if self.session:
            self.status_label.setText(f"Downloading {index} of {self.session.total_items}")
            self.progress_bar.setValue(self.session.progress_percent)

        worker = DownloadWorker(
            item,
            self.output_dir,
            quality=self.settings.video_quality,
            format=self.settings.format
        )
        if self.session:
            self.session.current_worker = worker
        
        worker.progress.connect(lambda p, d, row=self.queue.current_index: self.update_item_progress(row, p, d))
        worker.started_one.connect(lambda row=self.queue.current_index: self.set_item_status(row, ItemStatus.DOWNLOADING))
        worker.finished_one.connect(self.on_item_finished)
        worker.start()

    def set_item_status(self, row, status, error_msg=""):
        item = self.list_widget.item(row)
        queue_item = self.queue.queue[row]
        title = queue_item.title
        
        if status == ItemStatus.DOWNLOADING:
            item.setText(f"▶️ Downloading: {title}")
            item.setForeground(QColor(Colors.STATUS_DOWNLOADING))
        elif status == ItemStatus.COMPLETED:
            item.setText(f"✅ {title}")
            item.setForeground(QColor(Colors.STATUS_COMPLETED))
        elif status == ItemStatus.FAILED:
            queue_item.error_message = error_msg
            retry_text = f" (Retry {queue_item.retry_count}/{queue_item.max_retries})" if queue_item.retry_count > 0 else ""
            item.setText(f"❌ {title}{retry_text}")
            item.setForeground(QColor(Colors.STATUS_FAILED))
        elif status == ItemStatus.CANCELLED:
            item.setText(f"⏹️ {title}")
            item.setForeground(QColor(Colors.STATUS_CANCELLED))

    def update_item_progress(self, row, percent, detail=""):
        item = self.list_widget.item(row)
        title = self.queue.queue[row].title
        detail_str = f" — {detail}" if detail else ""
        item.setText(f"▶️ {title} ({percent}%){detail_str}")
        # Update main progress bar with current download percentage
        self.progress_bar.setValue(percent)

    def on_item_finished(self, success, error_msg=""):
        row = self.queue.current_index
        queue_item = self.queue.queue[row]
        
        if success:
            if self.session:
                self.session.mark_item_done()
            self.set_item_status(row, ItemStatus.COMPLETED)
            log_info(f"Successfully downloaded: {queue_item.title}")
            # Show notification
            show_notification("Download Complete", f"✅ {queue_item.title}", sound=True)
        else:
            # Try to retry if we haven't exceeded max retries
            if queue_item.retry_count < queue_item.max_retries:
                queue_item.retry_count += 1
                self.set_item_status(row, ItemStatus.FAILED, error_msg)
                log_warning(f"Download failed, retrying ({queue_item.retry_count}/{queue_item.max_retries}): {queue_item.title}")
                
                # Show error to user
                QMessageBox.warning(
                    self,
                    "Download Failed",
                    f"Failed to download: {queue_item.title}\n\nError: {error_msg}\n\nRetrying ({queue_item.retry_count}/{queue_item.max_retries})..."
                )
                
                # Retry this item
                if self.session and self.session.is_running:
                    self.start_next_download()
                return
            else:
                if self.session:
                    self.session.mark_item_done()
                self.set_item_status(row, ItemStatus.FAILED, error_msg)
                log_error(f"Download failed after {queue_item.max_retries} retries: {queue_item.title}")
                
                # Show final error to user
                QMessageBox.critical(
                    self,
                    "Download Failed",
                    f"Failed to download: {queue_item.title}\n\nError: {error_msg}\n\nMax retries exceeded."
                )

        # Update overall progress
        if self.session:
            self.progress_bar.setValue(self.session.progress_percent)

        if self.session and self.session.is_running and self.queue.has_next():
            self.start_next_download()
        else:
            self.status_label.setText("All downloads completed")
            self.start_btn.setEnabled(True)
            self.stop_btn.setEnabled(False)
            self.progress_bar.setValue(100)
            if self.session:
                self.session.reset()
            # Show completion notification
            show_notification("All Downloads Complete", "✅ All items have been processed", sound=True)

    def stop_downloads(self):
        """Stop current download and pause the queue"""
        if self.session:
            self.session.is_running = False
        self.status_label.setText("Downloads stopped")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        # Stop the current worker gracefully
        if self.session and self.session.current_worker and self.session.current_worker.isRunning():
            self.session.current_worker.stop()
            # Wait with timeout to prevent freezing
            if not self.session.current_worker.wait(5000):  # 5 second timeout
                self.session.current_worker.terminate()
                self.session.current_worker.wait()

    def show_queue_context_menu(self, position):
        """Show right-click context menu for queue items"""
        item = self.list_widget.itemAt(position)
        if not item:
            return
        
        row = self.list_widget.row(item)
        queue_item = self.queue.queue[row]
        
        menu = QMenu(self)
        
        # Copy URL action
        copy_action = menu.addAction("Copy URL")
        copy_action.triggered.connect(lambda: self.copy_queue_item_url(row))
        
        # Copy title action
        copy_title_action = menu.addAction("Copy Title")
        copy_title_action.triggered.connect(lambda: self.copy_queue_item_title(row))
        
        menu.addSeparator()
        
        # Remove item action
        remove_action = menu.addAction("Remove from Queue")
        remove_action.triggered.connect(lambda: self.remove_queue_item(row))
        
        # Show menu at cursor position
        menu.exec(self.list_widget.mapToGlobal(position))

    def copy_queue_item_url(self, row):
        """Copy queue item URL to clipboard"""
        from PyQt6.QtGui import QClipboard
        clipboard = QApplication.clipboard()
        queue_item = self.queue.queue[row]
        clipboard.setText(queue_item.url)
        log_info(f"Copied URL to clipboard: {queue_item.url}")

    def copy_queue_item_title(self, row):
        """Copy queue item title to clipboard"""
        from PyQt6.QtGui import QClipboard
        clipboard = QApplication.clipboard()
        queue_item = self.queue.queue[row]
        clipboard.setText(queue_item.title)
        log_info(f"Copied title to clipboard: {queue_item.title}")

    def remove_queue_item(self, row):
        """Remove item from queue"""
        self.queue.queue.pop(row)
        self.list_widget.takeItem(row)
        log_info(f"Removed item at index {row} from queue")

    def open_download_folder(self):
        """Open the download folder in file explorer"""
        try:
            folder = self.output_dir
            if not folder:
                QMessageBox.warning(self, "No folder", "Download folder not set")
                return
            
            # Open folder with native file manager
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", folder])
            elif sys.platform == "win32":  # Windows
                subprocess.run(["explorer", folder])
            else:  # Linux
                subprocess.run(["xdg-open", folder])
            
            log_info(f"Opened download folder: {folder}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Could not open folder: {str(e)}")
            log_error(f"Error opening folder: {str(e)}", exc_info=True)

    def keyPressEvent(self, event):
        """Handle keyboard shortcuts"""
        if event.key() == Qt.Key.Key_A and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            # Ctrl+A: Add to queue
            self.url_input.setFocus()
            self.add_to_queue()
        elif event.key() == Qt.Key.Key_S and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            # Ctrl+S: Start downloads
            self.start_queue()
        elif event.key() == Qt.Key.Key_Q and event.modifiers() == Qt.KeyboardModifier.ControlModifier:
            # Ctrl+Q: Quit application
            self.close()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        """Handle window close and cleanup"""
        # Stop any running download workers
        if self.session and self.session.current_worker and self.session.current_worker.isRunning():
            self.session.current_worker.stop()
            self.session.current_worker.wait(5000)
        
        # Wait for metadata workers to finish
        for worker in self.metadata_workers:
            if worker.isRunning():
                worker.wait(1000)
        
        # Save queue before closing
        self.queue_persistence.save_queue(self.queue)
        log_info("Application closing, queue saved")
        event.accept()


# ---------------- App Entry ----------------
def main():
    app = QApplication(sys.argv)
    
    # Apply stylesheet
    stylesheet = load_stylesheet()
    app.setStyleSheet(stylesheet)
    log_info("Stylesheet applied")
    
    # Show splash screen while loading
    splash = show_splash(app)
    log_info("Splash screen shown")
    
    # Create main window (but don't show it yet)
    window = YouTubeDownloader()
    log_info("Main window created")
    
    # Hide splash and show main window after delay
    hide_splash(splash, window, delay_ms=3000)
    
    sys.exit(app.exec())

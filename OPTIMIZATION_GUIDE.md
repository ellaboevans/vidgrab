# Implementation Guide: 3 High-Impact Optimizations

This guide walks through implementing the 3 optimizations recommended in CODE_REVIEW.md. Total time: ~2 hours.

---

## Optimization #1: Status Enum (40 min)

### Why This First?
The other optimizations depend on having a proper status type. Start here.

### Step 1: Update core/types.py

Replace the file with:

```python
from dataclasses import dataclass
from enum import Enum

class ItemStatus(str, Enum):
    """Queue item status states (compatible with string for JSON serialization)"""
    WAITING = "Waiting"
    DOWNLOADING = "Downloading"
    COMPLETED = "Completed"
    FAILED = "Failed"
    CANCELLED = "Cancelled"

@dataclass
class QueueItem:
    url: str
    title: str
    status: ItemStatus = ItemStatus.WAITING
    error_message: str = ""
    retry_count: int = 0
    max_retries: int = 3
```

**Why `str` mixin?** So `ItemStatus.COMPLETED == "Completed"` is True. Makes JSON serialization seamless.

### Step 2: Update core/queue_persistence.py

In the `load_queue()` method, update the status field:

```python
# Line 61 - Change from:
status=item_data.get("status", "Waiting"),

# To:
status=ItemStatus(item_data.get("status", ItemStatus.WAITING.value)),
```

This converts the stored string back to an enum.

In `save_queue()` method, the `.value` property converts enum to string:

```python
# Line 24 - Already works correctly because ItemStatus is a str Enum
"status": item.status.value,  # Or just: item.status (both work)
```

### Step 3: Update ui/app.py

Replace all hardcoded status strings with enum references. Use Find & Replace:

**Find & Replace patterns:**

```
"Waiting"           → ItemStatus.WAITING
"Downloading"       → ItemStatus.DOWNLOADING
"Completed"         → ItemStatus.COMPLETED
"Failed"            → ItemStatus.FAILED
"Cancelled"         → ItemStatus.CANCELLED
```

**Specific locations to update:**

1. Line 195-206 (`_populate_queue_ui()` method):
```python
# Before:
if item.status == "Completed":
    color = QColor("green")
    icon = "✅"
elif item.status == "Failed":
    color = QColor("red")
    icon = "❌"

# After:
if item.status == ItemStatus.COMPLETED:
    color = QColor("green")
    icon = "✅"
elif item.status == ItemStatus.FAILED:
    color = QColor("red")
    icon = "❌"
```

2. Lines 53, 59, 67, 71 (DownloadWorker.run()):
```python
# Before: self.item.status = "Downloading"
# After:  self.item.status = ItemStatus.DOWNLOADING
```

3. Lines 388-401 (set_item_status method):
```python
# Replace all status string comparisons with enum
if status == "In Progress":  # This one doesn't match directly (see note below)
```

**Note on "In Progress":** This status isn't in the enum because it's a UI-only state. Change to use `ItemStatus.DOWNLOADING`:

```python
def set_item_status(self, row, status_enum, error_msg=""):
    """Update UI display for an item's status"""
    item = self.list_widget.item(row)
    queue_item = self.queue.queue[row]
    title = queue_item.title
    
    if status_enum == ItemStatus.DOWNLOADING:  # Changed from "In Progress"
        item.setText(f"▶️ {status_enum.value}: {title}")
        item.setForeground(QColor("blue"))
    elif status_enum == ItemStatus.COMPLETED:
        item.setText(f"✅ {title}")
        item.setForeground(QColor("green"))
    elif status_enum == ItemStatus.FAILED:
        retry_text = f" (Retry {queue_item.retry_count}/{queue_item.max_retries})" if queue_item.retry_count > 0 else ""
        item.setText(f"❌ {title}{retry_text}")
        item.setForeground(QColor("red"))
    elif status_enum == ItemStatus.CANCELLED:
        item.setText(f"⏹️ {title}")
        item.setForeground(QColor("gray"))
```

4. Line 30 (queue_persistence.py) - Update comparison:
```python
# Before: if item.status != "Completed"
# After:  if item.status != ItemStatus.COMPLETED
```

### Step 4: Test

Run the app and verify:
1. ✅ Queue loads and displays correctly
2. ✅ Download completes and status shows green ✅
3. ✅ Failed download shows red ❌
4. ✅ Settings dialog opens (didn't break anything)
5. ✅ Queue saves on close and loads on reopen

**Commit message:** `feat: replace magic status strings with ItemStatus enum`

---

## Optimization #2: Download State Machine (60 min)

Now that we have proper status types, encapsulate download session state.

### Step 1: Create core/download_session.py

Create a new file:

```python
from dataclasses import dataclass, field
from typing import Optional
from core.types import QueueItem, ItemStatus

@dataclass
class DownloadSession:
    """
    Encapsulates the state of a download batch.
    Prevents state desynchronization between UI and queue.
    """
    queue_items: list[QueueItem]
    total_items: int = 0
    completed_items: int = 0
    failed_items: int = 0
    is_running: bool = False
    
    def __post_init__(self):
        """Initialize counters from queue items"""
        self.total_items = len(self.queue_items)
        # Count pre-existing completed/failed items
        for item in self.queue_items:
            if item.status == ItemStatus.COMPLETED:
                self.completed_items += 1
            elif item.status == ItemStatus.FAILED:
                self.failed_items += 1
    
    @property
    def progress_percent(self) -> int:
        """Overall progress as percentage (0-100)"""
        if self.total_items == 0:
            return 0
        completed_or_failed = self.completed_items + self.failed_items
        return int((completed_or_failed / self.total_items) * 100)
    
    @property
    def items_remaining(self) -> int:
        """Number of items not yet started/completed"""
        return self.total_items - self.completed_items - self.failed_items
    
    @property
    def is_done(self) -> bool:
        """True if all items are completed or failed"""
        return self.items_remaining == 0
    
    def mark_completed(self):
        """Mark current item as successfully completed"""
        self.completed_items += 1
    
    def mark_failed(self):
        """Mark current item as failed"""
        self.failed_items += 1
    
    def reset(self):
        """Reset the session for a new batch"""
        self.is_running = False
        self.completed_items = 0
        self.failed_items = 0
```

### Step 2: Update ui/app.py

Replace the scattered state variables (lines 129-133):

```python
# OLD CODE (delete these lines):
# self.total_items = 0
# self.completed_items = 0
# self.current_worker = None
# self.metadata_workers = []
# self.is_downloading = False

# NEW CODE (add this import at the top):
from core.download_session import DownloadSession

# In __init__, add this instead:
self.session: Optional[DownloadSession] = None
self.current_worker = None
self.metadata_workers = []  # Keep for metadata workers
```

Update `start_queue()` method (line 345-358):

```python
def start_queue(self):
    if not self.output_dir:
        QMessageBox.warning(self, "Missing folder", "Please choose a download folder first")
        return
    if not self.queue.has_next():
        QMessageBox.information(self, "Queue empty", "Please add at least one URL to the queue")
        return

    # Create session instead of tracking scattered variables
    self.session = DownloadSession(self.queue.queue)
    self.session.is_running = True
    self.start_btn.setEnabled(False)
    self.stop_btn.setEnabled(True)
    self.start_next_download()
```

Update `start_next_download()` method (line 360-381):

```python
def start_next_download(self):
    item = self.queue.next_item()
    if not item:
        self.session.is_running = False
        self.status_label.setText("All downloads completed")
        self.progress_bar.setValue(100)
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        return

    index = self.queue.current_index + 1
    self.status_label.setText(f"Downloading {index} of {self.session.total_items}")
    self.progress_bar.setValue(self.session.progress_percent)

    self.current_worker = DownloadWorker(
        item,
        self.output_dir,
        quality=self.settings.video_quality,
        format=self.settings.format
    )
    self.current_worker.progress.connect(lambda p, row=self.queue.current_index: self.update_item_progress(row, p))
    self.current_worker.started_one.connect(lambda row=self.queue.current_index: self.set_item_status(row, ItemStatus.DOWNLOADING))
    self.current_worker.finished_one.connect(self.on_item_finished)
    self.current_worker.start()
```

Update `on_item_finished()` method (line 408-457):

```python
def on_item_finished(self, success, error_msg=""):
    row = self.queue.current_index
    queue_item = self.queue.queue[row]
    
    if success:
        self.session.mark_completed()
        self.set_item_status(row, ItemStatus.COMPLETED)
        log_info(f"Successfully downloaded: {queue_item.title}")
    else:
        # Try to retry if we haven't exceeded max retries
        if queue_item.retry_count < queue_item.max_retries:
            queue_item.retry_count += 1
            self.set_item_status(row, ItemStatus.FAILED, error_msg)
            log_warning(f"Download failed, retrying ({queue_item.retry_count}/{queue_item.max_retries}): {queue_item.title}")
            
            QMessageBox.warning(
                self,
                "Download Failed",
                f"Failed to download: {queue_item.title}\n\nError: {error_msg}\n\nRetrying ({queue_item.retry_count}/{queue_item.max_retries})..."
            )
            
            if self.session.is_running:
                self.start_next_download()
            return
        else:
            self.session.mark_failed()
            self.set_item_status(row, ItemStatus.FAILED, error_msg)
            log_error(f"Download failed after {queue_item.max_retries} retries: {queue_item.title}")
            
            QMessageBox.critical(
                self,
                "Download Failed",
                f"Failed to download: {queue_item.title}\n\nError: {error_msg}\n\nMax retries exceeded."
            )

    # Update overall progress using session
    self.progress_bar.setValue(self.session.progress_percent)

    if self.session.is_running and not self.session.is_done:
        self.start_next_download()
    else:
        self.session.is_running = False
        self.status_label.setText("All downloads completed")
        self.start_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.progress_bar.setValue(100)

def stop_downloads(self):
    """Stop current download and pause the queue"""
    if self.session:
        self.session.is_running = False
    self.status_label.setText("Downloads stopped")
    self.start_btn.setEnabled(True)
    self.stop_btn.setEnabled(False)
    
    if self.current_worker and self.current_worker.isRunning():
        self.current_worker.stop()
        if not self.current_worker.wait(5000):
            self.current_worker.terminate()
            self.current_worker.wait()
```

### Step 3: Test

1. ✅ Start downloads - session should be created
2. ✅ Progress bar updates smoothly
3. ✅ Pause/resume doesn't break state
4. ✅ All items complete - session marks done
5. ✅ Failed items are tracked correctly

**Commit message:** `refactor: encapsulate download state in DownloadSession`

---

## Optimization #3: Logger Singleton (20 min)

Replace the fragile logger creation pattern.

### Step 1: Update core/logger.py

Replace the entire file:

```python
import logging
import logging.handlers
from pathlib import Path

class LoggerSingleton:
    """Thread-safe logger singleton - ensures only one handler instance"""
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = logging.getLogger("VidGrab")
            cls._instance.setLevel(logging.DEBUG)
        return cls._instance
    
    def __init__(self):
        """Initialize handlers only once"""
        if LoggerSingleton._initialized:
            return
        
        # Create log directory
        log_dir = Path.home() / ".vidgrab" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Remove any existing handlers (cleanup for reloads)
        for handler in self._instance.handlers[:]:
            self._instance.removeHandler(handler)
        
        # File handler - rotating
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / "app.log",
            maxBytes=5 * 1024 * 1024,  # 5MB
            backupCount=5  # Keep 5 old files
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers
        self._instance.addHandler(file_handler)
        self._instance.addHandler(console_handler)
        
        LoggerSingleton._initialized = True


# Initialize the singleton once
_logger = LoggerSingleton()


def get_logger():
    """Get the global logger instance"""
    return _logger


def log_debug(msg, *args):
    _logger.debug(msg, *args)


def log_info(msg, *args):
    _logger.info(msg, *args)


def log_warning(msg, *args):
    _logger.warning(msg, *args)


def log_error(msg, *args, exc_info=False):
    _logger.error(msg, *args, exc_info=exc_info)


def log_critical(msg, *args):
    _logger.critical(msg, *args)


# Helper class for accessing log file (for "View Logs" feature)
class AppLogger:
    """Wrapper for getting log file path"""
    def get_log_file(self):
        return Path.home() / ".vidgrab" / "logs" / "app.log"
```

### Step 2: Verify Imports

Check that all imports of `AppLogger` still work:

```python
# In ui/app.py, line 270:
from core.logger import AppLogger

# This still works - it's now a wrapper class for convenience
log_file = AppLogger().get_log_file()
```

### Step 3: Test

1. ✅ App starts - check ~/.vidgrab/logs/app.log exists
2. ✅ Download completes - logs are recorded
3. ✅ View Logs button works
4. ✅ No duplicate handlers (check by running app twice in same process)

**Commit message:** `refactor: fix logger singleton pattern - prevent handler duplication`

---

## Verification Checklist

After all 3 optimizations, verify:

### Functionality
- [ ] App starts without errors
- [ ] Queue loads from saved state
- [ ] Add URL → metadata fetches → displays title
- [ ] Start downloads → progress updates → files save
- [ ] Stop button pauses downloads
- [ ] Settings dialog saves and applies
- [ ] View Logs opens log file
- [ ] Close app → queue persists

### Code Quality
- [ ] No `import *` statements
- [ ] All status values use `ItemStatus` enum
- [ ] No magic strings for status
- [ ] Logger only initializes once
- [ ] Download state is in `DownloadSession`
- [ ] Type hints are correct (`from typing import Optional`)

### Performance
- [ ] App starts quickly (~1 second)
- [ ] UI doesn't freeze during download
- [ ] Progress bar updates smoothly (not 100+ updates/sec)

---

## Estimated Time Breakdown

| Task | Time |
|------|------|
| Status Enum | 40 min |
| Download State Machine | 60 min |
| Logger Singleton | 20 min |
| Testing | 30 min |
| **Total** | **150 min** (~2.5 hours) |

---

## If You Get Stuck

1. **Enum not serializing?** → Check that `ItemStatus` inherits from `str` (it should)
2. **Logger still creating handlers?** → Make sure you replaced the entire file
3. **State desync issues?** → Add a `__repr__` to `DownloadSession` and print it in `on_item_finished()`
4. **Queue not loading?** → Add debug logging to `queue_persistence.py` to see what's in the JSON

---

## Next Steps After These 3

Once complete, consider:
1. **Add pause/resume** - Now trivial with `DownloadSession.is_running` flag
2. **Add duplicate detection in UI** - Move logic into a signal to prevent re-adds
3. **Add unit tests** - `QueueManager` and `DownloadSession` are now testable in isolation


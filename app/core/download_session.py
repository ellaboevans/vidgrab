from dataclasses import dataclass, field
from typing import Optional
from PyQt6.QtCore import QObject
from core.types import QueueItem


@dataclass
class DownloadSession(QObject):
    """Encapsulates download state for a batch of queue items"""
    queue_items: list = field(default_factory=list)
    total_items: int = 0
    completed_items: int = 0
    is_running: bool = False
    current_worker: Optional[QObject] = None
    
    def __post_init__(self):
        super().__init__()
        self.total_items = len(self.queue_items)
    
    @property
    def progress_percent(self) -> int:
        """Calculate overall progress as percentage"""
        if self.total_items == 0:
            return 0
        return int((self.completed_items / self.total_items) * 100)
    
    @property
    def items_remaining(self) -> int:
        """Return number of items not yet completed"""
        return self.total_items - self.completed_items
    
    def mark_item_done(self):
        """Increment completed item counter"""
        self.completed_items += 1
    
    def reset(self):
        """Reset session state after completion"""
        self.is_running = False
        self.completed_items = 0
        self.current_worker = None

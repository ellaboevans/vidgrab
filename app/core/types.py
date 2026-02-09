from dataclasses import dataclass
from enum import Enum

class ItemStatus(str, Enum):
    """Queue item status states"""
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
    download_type: str = "auto"

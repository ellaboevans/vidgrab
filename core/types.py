from dataclasses import dataclass

@dataclass
class QueueItem:
    url: str
    title: str
    status: str = "Waiting" # Waiting | Downloading | Completed | Failed | Cancelled
    error_message: str = ""
    retry_count: int = 0
    max_retries: int = 3
from dataclasses import dataclass

@dataclass
class QueueItem:
    url: str
    status: str = "Waiting" # Waiting | Downloading | Completed | Failed
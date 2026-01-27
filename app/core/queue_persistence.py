import json
from pathlib import Path
from core.queue import QueueManager
from core.types import QueueItem
from core.logger import log_info, log_error


class QueuePersistence:
    """Handle saving and loading queue to/from disk"""
    
    def __init__(self):
        self.queue_dir = Path.home() / ".vidgrab"
        self.queue_file = self.queue_dir / "queue.json"
        self.queue_dir.mkdir(parents=True, exist_ok=True)
    
    def save_queue(self, queue_manager: QueueManager) -> bool:
        """Save queue to file"""
        try:
            # Filter out completed items, keep everything else
            items_to_save = [
                {
                    "url": item.url,
                    "title": item.title,
                    "status": item.status,
                    "error_message": item.error_message,
                    "retry_count": item.retry_count,
                    "max_retries": item.max_retries,
                }
                for item in queue_manager.queue
                if item.status != "Completed"  # Don't persist completed items
            ]
            
            with open(self.queue_file, 'w') as f:
                json.dump(items_to_save, f, indent=2)
            
            log_info(f"Queue saved: {len(items_to_save)} items")
            return True
        except Exception as e:
            log_error(f"Failed to save queue: {str(e)}", exc_info=True)
            return False
    
    def load_queue(self, queue_manager: QueueManager) -> bool:
        """Load queue from file"""
        try:
            if not self.queue_file.exists():
                log_info("No saved queue found")
                return False
            
            with open(self.queue_file, 'r') as f:
                items_data = json.load(f)
            
            if not items_data:
                log_info("Saved queue is empty")
                return False
            
            # Restore queue items
            for item_data in items_data:
                item = QueueItem(
                    url=item_data.get("url", ""),
                    title=item_data.get("title", ""),
                    status=item_data.get("status", "Waiting"),
                    error_message=item_data.get("error_message", ""),
                    retry_count=item_data.get("retry_count", 0),
                    max_retries=item_data.get("max_retries", 3),
                )
                queue_manager.queue.append(item)
            
            log_info(f"Queue loaded: {len(items_data)} items")
            return True
        except Exception as e:
            log_error(f"Failed to load queue: {str(e)}", exc_info=True)
            return False
    
    def clear_saved_queue(self) -> bool:
        """Clear the saved queue file"""
        try:
            if self.queue_file.exists():
                self.queue_file.unlink()
                log_info("Saved queue cleared")
            return True
        except Exception as e:
            log_error(f"Failed to clear queue: {str(e)}")
            return False

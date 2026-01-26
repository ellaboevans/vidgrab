from core.types import QueueItem

class QueueManager:
    def __init__(self):
        self.queue: list[QueueItem] = []
        self.current_index = -1

    def add(self, url: str):
        self.queue.append(QueueItem(url=url))

    def has_next(self)-> bool:
        return self.current_index + 1 < len(self.queue)

    def next_item(self) -> QueueItem | None:
        if self.has_next():
            self.current_index += 1
            return self.queue[self.current_index]
        return None

    def reset(self):
        self.current_index = -1
"""Queue Object (FIFO: First In, First Out)."""
class Queue:
    def __init__(self, items=None):
        self.items = list(items or [])  # index 0 is the FRONT, last index is the REAR.

    def enqueue(self, value):
        self.items.append(value)        # add at the rear

    def dequeue(self):
        return self.items.pop(0) if self.items else None   # remove from the front

    def peek(self):
        return self.items[0] if self.items else None        # look at the front

    def is_empty(self):
        return not self.items

    def size(self):
        return len(self.items)

    def clear(self):
        self.items.clear()

        
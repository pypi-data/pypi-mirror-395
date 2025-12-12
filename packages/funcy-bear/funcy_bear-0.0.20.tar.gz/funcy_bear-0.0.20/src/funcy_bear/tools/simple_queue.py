"""A simple queue implementation."""

from __future__ import annotations

from .general_base import BaseCollection, PopDirection, PushDirection


class SimpooQueue[T](BaseCollection[T]):
    """A simple queue implementation with a silly name to differentiate it."""

    default_pop_dir: PopDirection = "top"
    default_push_dir: PushDirection = "bottom"

    @property
    def queue(self) -> list[T]:
        """Get the internal queue list."""
        return self.collection

    @queue.setter
    def queue(self, value: list[T]) -> None:
        """Set the internal queue list."""
        self.collection = value

    def enq00(self, item: T) -> None:  # THIS IS HERE FOR FUN, LEAVE ME ALONE!
        """Enqueue an item to the queue with a silly name."""
        self.push(item)

    def put(self, item: T) -> None:
        """Enqueue an item to the queue."""
        self.push(item)

    def enqueue(self, item: T) -> None:
        """Enqueue an item to the queue."""
        self.push(item)

    def get(self) -> T:  # pyright: ignore[reportIncompatibleMethodOverride]
        """Dequeue an item from the queue."""
        return self.pop()

    def dequeue(self) -> T:
        """Dequeue an item from the queue."""
        return self.pop()

    def peek(self, left: bool = True) -> T:
        """Peek at the left (front) or right (back) item of the queue without removing it. Raises IndexError if the queue is empty."""
        if self.is_empty:
            raise IndexError("Peek from an empty queue")
        return self._peek_bottom() if left else self._peek_top()

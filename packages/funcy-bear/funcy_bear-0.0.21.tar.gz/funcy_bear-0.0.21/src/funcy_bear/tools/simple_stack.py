"""A Simple Stack implementation."""

from __future__ import annotations

from .general_base import BaseCollection


class SimpleStack[T](BaseCollection[T]):
    """A simple stack implementation."""

    default_push: str = "top"
    default_pop: str = "top"

    @property
    def stack(self) -> list[T]:
        """Get the internal stack list."""
        return self.collection

    @stack.setter
    def stack(self, value: list[T]) -> None:
        """Set the internal stack list."""
        self.collection = value

    def peek(self) -> T:
        """Peek at the top item of the stack without removing it. Raises IndexError if the stack is empty."""
        if self.is_empty:
            raise IndexError("Peek from an empty stack")
        return self.stack[-1]

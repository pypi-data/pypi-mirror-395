"""A double-ended queue (deque) implementation using a simple stack as the base called a Deq00."""

from .general_base import PopDirection, PushDirection  # noqa: TC001
from .simple_stack import SimpleStack


class Deq00[T](SimpleStack[T]):
    """A double-ended queue (deque) implementation using a simple stack as the base."""

    default_push_dir: PushDirection = "top"
    default_pop_dir: PopDirection = "top"

    def pushleft(self, item: T) -> None:
        """Push an item onto the left (bottom) of the deque."""
        self._push_bottom(item)

    def pushright(self, item: T) -> None:
        """Push an item onto the right (top) of the deque."""
        self.push(item)

    def popleft(self) -> T:
        """Pop an item from the left (bottom) of the deque."""
        return self._pop_from_bottom()

    def popright(self) -> T:
        """Pop an item from the right (top) of the deque."""
        return self._pop_from_top()

    def extendleft(self, items: list[T]) -> None:
        """Extend the deque with a list of items to the left."""
        for item in reversed(items):
            self.pushleft(item)

    def extend(self, items: list[T], left: bool = False) -> None:
        """Extend the deque with a list of items to the left or right."""
        super().extend(items) if not left else self.extendleft(items)

    def rotate(self, n: int = 1) -> None:
        """Rotate the deque n steps to the right. If n is negative, rotate to the left."""
        n = n % self.size if self.size > 0 else 0
        if n == 0:
            return
        temp: list[T] = [*self.stack[-n:], *self.stack[:-n]]
        self.stack = temp

    def reverse(self) -> None:
        """Reverse the order of items in the deque."""
        self.stack.reverse()

    def peek(self, left: bool = False) -> T:
        """Peek at the left (bottom) or right (top) item of the deque without removing it. Raises IndexError if the deque is empty."""
        if self.is_empty:
            raise IndexError("Peek from an empty deque")
        return self._peek_bottom() if left else self._peek_top()

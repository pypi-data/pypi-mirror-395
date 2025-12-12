"""A collection base implementation."""

from __future__ import annotations

from abc import ABC
from typing import TYPE_CHECKING, Any, Literal

from funcy_bear.protocols.general import CollectionProtocol

if TYPE_CHECKING:
    from collections.abc import Generator

PushDirection = PopDirection = Literal["top", "bottom"]


class BaseCollection[T](ABC, CollectionProtocol):
    """A simple collection base implementation."""

    default_push_dir: PushDirection = "top"
    default_pop_dir: PopDirection = "top"

    def __init__(self, data: T | None = None) -> None:
        """Initialize an empty collection."""
        self._collection: list[T] = []
        if data is not None:
            self.push(data)

    def push(self, item: T) -> None:
        """Push an item onto the collection."""
        self._push_top(item) if self.default_push_dir == "top" else self._push_bottom(item)

    def extend(self, items: list[T]) -> None:
        """Extend the collection with a list of items."""
        for item in items:
            self.push(item)

    def pop(self) -> T:
        """Pop an item off the collection. Raises IndexError if the collection is empty."""
        return self._pop_from_top() if self.default_pop_dir == "top" else self._pop_from_bottom()

    def drain(self, start: int = 0, end: int | None = None) -> list[T]:
        """Drain a slice of items from the collection and return them as a list.

        Args:
            start (int): The starting index of the slice. Defaults to 0.
            end (int | None): The ending index of the slice. Defaults to None.

        Returns:
            list[T]: The drained items.
        """
        drained_items = self.collection[start:end]
        del self.collection[start:end]
        return drained_items

    def drain_left(self, n: int) -> list[T]:
        """Drain n items from the left (bottom) of the collection and return them as a list.

        Args:
            n (int): The number of items to drain.

        Returns:
            list[T]: The drained items.
        """
        return self.drain(0, n)

    def drain_right(self, n: int) -> list[T]:
        """Drain n items from the right (top) of the collection and return them as a list.

        Args:
            n (int): The number of items to drain.

        Returns:
            list[T]: The drained items.
        """
        return self.drain(-n, None)

    def get(self, index: int) -> T:
        """Get an item from the collection by index."""
        return self.collection[index]

    def has(self, item: T) -> bool:
        """Check if the stack contains the given item."""
        return item in self.collection

    def remove(self, item: T) -> None:
        """Remove the first occurrence of a value from the collection."""
        self.collection.remove(item)

    def clear(self) -> None:
        """Clear all items from the collection."""
        self._collection.clear()

    def copy(self) -> list[T]:
        """Get a copy of the current collection."""
        return self._collection.copy()

    def join(self, d: str = ", ") -> str:
        """Join the collection items into a single string with the given delimiter.

        Args:
            d (str): The delimiter to use between items. Defaults to ", ".

        Returns:
            str: The joined string of collection items.
        """
        return d.join(map(str, self.copy())) or ""

    def _pop(self, index: int) -> T:
        """Pop an item at the given index from the collection. Raises IndexError if the collection is empty."""
        if self.is_empty:
            raise IndexError(f"pop from empty {self.name.lower()}")
        return self.collection.pop(index)

    def _peek_top(self) -> T:
        """Peek at the top item of the collection without removing it. Raises IndexError if the collection is empty."""
        if self.is_empty:
            raise IndexError(f"peek from empty {self.name.lower()}")
        return self.get(-1)

    def _peek_bottom(self) -> T:
        """Peek at the bottom item of the collection without removing it. Raises IndexError if the collection is empty."""
        if self.is_empty:
            raise IndexError(f"peek from empty {self.name.lower()}")
        return self.get(0)

    def _pop_from_top(self) -> T:
        """Pop an item off the collection. Raises IndexError if the collection is empty."""
        if self.is_empty:
            raise IndexError(f"pop from empty {self.name.lower()}")
        return self._pop(-1)

    def _pop_from_bottom(self) -> T:
        """Pop an item from the bottom of the collection. Raises IndexError if the collection is empty."""
        if self.is_empty:
            raise IndexError(f"pop from empty {self.name.lower()}")
        return self._pop(0)

    def _push_top(self, item: T) -> None:
        """Push an item onto the top of the collection."""
        self.collection.append(item)

    def _push_bottom(self, item: T) -> None:
        """Push an item onto the bottom of the collection."""
        self.collection.insert(0, item)

    @property
    def is_empty(self) -> bool:
        """Check if the collection is empty."""
        return len(self.collection) == 0

    @property
    def not_empty(self) -> bool:
        """Check if the collection is not empty."""
        return not self.is_empty

    @property
    def size(self) -> int:
        """Get the current size of the collection."""
        return len(self.collection)

    @property
    def collection(self) -> list[T]:
        """Get the current collection."""
        return self._collection

    @collection.setter
    def collection(self, value: list[T]) -> None:
        """Set the current collection."""
        self._collection = value

    @property
    def name(self) -> str:
        """Get the name of the collection class."""
        return self.__class__.__name__

    def __contains__(self, item: T) -> bool:
        """Check if an item is in the collection."""
        return item in self.collection

    def __bool__(self) -> bool:
        """Check if the collection is not empty."""
        return self.not_empty

    def __getitem__(self, index: int) -> T:
        """Get an item from the collection by index."""
        return self.collection[index]

    def __setitem__(self, index: int, value: T) -> None:
        """Set an item in the collection by index."""
        self.collection[index] = value

    def __slice__(self, start: int | None = None, end: int | None = None, step: int | None = None) -> list[T]:
        """Get a slice of the collection."""
        return self.collection[slice(start, end, step)]

    def __len__(self) -> int:
        """Get the current size of the collection."""
        return self.size

    def __iter__(self) -> Generator[T, Any]:
        """Iterate over the collection from bottom to top."""
        yield from self.collection

    def __repr__(self) -> str:
        """Get the string representation of the collection."""
        return f"{self.name} ({self.size} items)"

    def __str__(self) -> str:
        """Get the string representation of the collection."""
        return f"{self.name} with {self.size} items"

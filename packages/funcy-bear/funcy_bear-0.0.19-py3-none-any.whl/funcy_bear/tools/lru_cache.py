"""An LRU (least-recently used) cache implementation."""

from collections import OrderedDict
from collections.abc import Hashable, Iterator, MutableMapping
from typing import Any


class LRUCache[K, V](MutableMapping):
    """A least-recently used (LRU) cache with a fixed cache size."""

    def __init__(self, capacity: int | None = None, strict: bool = True) -> None:
        """Initialize the LRUCache with an optional capacity.

        Args:
            capacity (int, optional): The maximum number of items the cache can hold. Defaults to INFINITE.
            strict (bool, optional): If True, raises an error when a non-hashable key is used. Defaults to True.
        """
        from funcy_bear.ops.math import INFINITE  # noqa: PLC0415

        self.capacity: int | float = capacity or INFINITE
        self.cache: OrderedDict[K, V] = OrderedDict()
        self.strict: bool = strict

    def get[D](self, key: K, default: D | None = None) -> V | D | None:
        """Get an item from the cache, returning default if not found.

        Args:
            key (K): The key to look up in the cache.
            default (D | None, optional): The value to return if the key is not found. Defaults to None.

        Returns:
            V | D | None: The value associated with the key, or the default value if not found.
        """
        value: V | None = self.cache.get(key)

        if value is not None:
            self.cache.move_to_end(key, last=True)
            return value
        return default

    def set(self, key: K, value: V) -> None:
        """A hashable key must be provided, if not cache will not work properly.

        Args:
            key (K): The key to set in the cache.
            value (V): The value to associate with the key.
        """
        if not isinstance(key, Hashable):
            if not self.strict:
                return  # Ignore non-hashable keys if strict mode is off
            raise TypeError(f"Key {key} of type {type(key)} is not hashable and cannot be used in LRUCache.")

        if key in self.cache:
            self.cache[key] = value
            self.cache.move_to_end(key, last=True)
        else:
            self.cache[key] = value
            if self.length > self.capacity:  # Evict least-recently used item if over capacity
                self.cache.popitem(last=False)

    @property
    def lru(self) -> list[K]:
        """Get a list of keys in the cache from least-recently used to most-recently used."""
        return list(self.cache.keys())

    @property
    def length(self) -> int:
        """Get the current number of items in the cache."""
        return len(self.cache)

    def clear(self) -> None:
        """Clear all items from the cache."""
        self.cache.clear()

    def __len__(self) -> int:
        return self.length

    def __contains__(self, key: object) -> bool:
        return key in self.cache

    def __setitem__(self, key: K, value: V) -> None:
        self.set(key, value)

    def __delitem__(self, key: K) -> None:
        del self.cache[key]

    def __getitem__(self, key: Any) -> V:
        value: V | None = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __iter__(self) -> Iterator[K]:
        return iter(self.cache)

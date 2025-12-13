from __future__ import annotations

from typing import Any

import pytest

from funcy_bear.tools import LRUCache
from funcy_bear.tools.freezing import FrozenDict, freeze, thaw


def test_lru_cache_respects_capacity_and_recency() -> None:
    cache: LRUCache[str, int] = LRUCache(capacity=2)
    cache.set("a", 1)
    cache.set("b", 2)

    # Access 'a' so it becomes most recently used
    assert cache.get("a") == 1

    cache.set("c", 3)  # Should evict 'b'

    assert "a" in cache
    assert "c" in cache
    assert "b" not in cache
    assert cache.length == 2


def test_lru_cache_accepts_frozen_keys_from_freeze_helpers() -> None:
    cache: LRUCache[FrozenDict, str] = LRUCache(capacity=2)

    original: dict[str, Any] = {"alpha": [1, 2], "beta": {"nested": True}}
    key: FrozenDict = freeze(original)
    cache.set(key, "payload")

    # same structure, new object; freezing should normalize it to equivalent key
    equivalent_key: FrozenDict = freeze({"alpha": [1, 2], "beta": {"nested": True}})
    assert cache.get(equivalent_key) == "payload"

    cache.set(freeze({"alpha": [3]}), "other")
    assert cache.length == 2


def test_lru_cache_get_with_default_and_missing_key() -> None:
    cache: LRUCache[str, int] = LRUCache()

    assert cache.get("missing") is None
    assert cache.get("missing", default=5) == 5

    cache.set("present", 42)
    assert cache["present"] == 42

    with pytest.raises(KeyError):
        _ = cache["absent"]


def test_lru_cache_rejects_unhashable_keys() -> None:
    cache: LRUCache[object, int] = LRUCache()

    with pytest.raises(TypeError):
        cache.set(["not", "hashable"], 1)  # type: ignore[list-item]


def test_lru_cache_delete_and_clear() -> None:
    cache: LRUCache[str, int] = LRUCache()
    cache["x"] = 10
    cache["y"] = 20

    del cache["x"]
    assert "x" not in cache
    assert cache.length == 1

    cache.clear()
    assert cache.length == 0


def test_freeze_and_thaw_round_trip_nested_structures() -> None:
    data: dict[str, Any] = {"alpha": [1, {"beta": {1, 2}}], "gamma": {"delta": "value"}}

    frozen: FrozenDict = freeze(data)
    assert isinstance(frozen, FrozenDict)
    assert frozen["alpha"][1]["beta"] == frozenset({1, 2})

    thawed: dict = thaw(frozen)
    assert thawed == data
    assert thawed is not data  # ensure new objects were created

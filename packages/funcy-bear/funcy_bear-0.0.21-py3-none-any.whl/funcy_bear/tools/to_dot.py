"""Provide dot notation access to nested dictionaries."""

from __future__ import annotations

from collections.abc import MutableMapping
from functools import cached_property
from typing import TYPE_CHECKING, Any, Literal, Self, overload

from lazy_bear import LazyLoader

from .freezing import freeze, immutable_method

if TYPE_CHECKING:
    from collections.abc import Iterator
    import copy
    import json as _json

    from funcy_bear.constants.type_constants import LitFalse, LitTrue, NoReturnCall
else:
    _json = LazyLoader("json")
    copy = LazyLoader("copy")


class DotDict(MutableMapping):
    """A dictionary that supports dot notation access to nested dictionaries.

    Example:
        >>> d = DotDict({"a": {"b": {"c": 1}}})
        >>> d.a.b.c
        1
        >>> d["a"]["b"]["c"]
        1
        >>> d.a.b.c = 2
        >>> d.a.b.c
        2
        >>> d["a"]["b"]["c"]
        2
    """

    _data: dict[str, Any]
    __slots__: tuple[Literal["_data"]] = ("_data",)

    def __init__(self, data: dict[str, Any] | None = None) -> None:
        """Initialize the DotDict with an optional dictionary."""
        _data: dict[str, Any] = {}
        for key, value in (data or {}).items():
            if isinstance(value, dict):
                _data[key] = DotDict(value)
            else:
                _data[key] = value
        object.__setattr__(self, "_data", _data)

    def __copy__(self) -> DotDict:
        """Return a shallow copy of the DotDict."""
        return self.copy()

    def __deepcopy__(self, memo: dict[int, Any] | None = None) -> DotDict:
        """Return a deep copy of the DotDict."""
        if memo is None:
            memo = {}
        copied_data: dict[str, Any] = copy.deepcopy(self._data, memo)
        return DotDict(copied_data)

    def copy(self) -> DotDict:
        """Return a shallow copy of the DotDict."""
        return DotDict(self.as_dict())

    def clear(self) -> None:
        """Clear all items from the DotDict."""
        self._data.clear()

    @classmethod
    def _as_dict(
        cls,
        data: dict[str, Any],
        json: bool = False,
        indent: int = 4,
        sort_keys: bool = False,
    ) -> dict[str, Any] | str:
        """Return a standard dictionary representation of the DotDict."""

        def convert(value: Any) -> Any:
            if isinstance(value, cls):
                return {k: convert(v) for k, v in value._data.items()}
            if isinstance(value, dict):
                return {k: convert(v) for k, v in value.items()}
            return value

        result: dict[str, Any] = {k: convert(v) for k, v in data.items()}
        if json:
            return _json.dumps(result, indent=indent, sort_keys=sort_keys)
        return result

    @overload
    def as_dict(self, json: LitFalse = False, indent: int = 4, sort_keys: bool = False) -> dict[str, Any]: ...
    @overload
    def as_dict(self, json: LitTrue, indent: int = 4, sort_keys: bool = False) -> str: ...
    def as_dict(self, json: bool = False, indent: int = 4, sort_keys: bool = False) -> dict[str, Any] | str:
        """Return a standard dictionary representation of the class."""
        return self._as_dict(
            self._data,
            json=json,
            indent=indent,
            sort_keys=sort_keys,
        )

    def freeze(self) -> FrozenDotDict:
        """Return a frozen (immutable) version of the dictionary."""
        return FrozenDotDict(self.as_dict())

    @classmethod
    def to_dot(cls, data: dict[str, Any]) -> Self:
        """Convert a standard dictionary to a DotDict."""
        dot: Self = cls()
        _data: dict[str, Any] = {}
        for key, value in data.items():
            if isinstance(value, dict):
                _data[key] = cls.to_dot(value)
            else:
                _data[key] = value
        object.__setattr__(dot, "_data", _data)
        return dot

    def __getattr__(self, key: str) -> Any:
        """Get an item using dot notation."""
        try:
            value = self._data[key]
            if isinstance(value, dict):
                return DotDict(value)
            return value
        except KeyError as e:
            raise AttributeError(f"'DotDict' object has no attribute '{key}'") from e

    def __setattr__(self, key: str, value: Any) -> None:
        """Set an item using dot notation."""
        if key == "_data":
            super().__setattr__(key, value)
        else:
            self._data[key] = value

    def __delattr__(self, key: str) -> None:
        """Delete an item using dot notation."""
        try:
            del self._data[key]
        except KeyError as e:
            raise AttributeError(f"'DotDict' object has no attribute '{key}'") from e

    def __getitem__(self, key: str) -> Any:
        """Get an item using dictionary notation."""
        value = self._data[key]
        if isinstance(value, dict):
            return DotDict(value)
        return value

    def __setitem__(self, key: str, value: Any) -> None:
        """Set an item using dictionary notation."""
        self._data[key] = value

    def __delitem__(self, key: str) -> None:
        """Delete an item using dictionary notation."""
        del self._data[key]

    def __iter__(self) -> Iterator[str]:
        """Return an iterator over the keys of the dictionary."""
        return iter(self._data)

    def __len__(self) -> int:
        """Return the number of items in the dictionary."""
        return len(self._data)

    def __bool__(self) -> bool:
        """Return True if the DotDict is not empty."""
        return bool(self._data)

    def __repr__(self) -> str:
        """Return a string representation of the DotDict."""
        return f"{self.__class__.__name__}({self.as_dict()})"


class FrozenDotDict(DotDict):
    """A frozen (immutable) version of DotDict."""

    __slots__: tuple[Literal["_data"]] = ("_data",)

    def __init__(self, data: dict[str, Any] | None = None) -> None:
        """Initialize the FrozenDotDict with an optional dictionary."""
        _data: dict[str, Any] = {}
        for key, value in (data or {}).items():
            if isinstance(value, dict):
                _data[key] = FrozenDotDict(value)
            else:
                _data[key] = value
        object.__setattr__(self, "_data", freeze(_data))

    def flatten_to_hashable(
        self,
        data: dict[str, Any] | None = None,
        sort_keys: bool = True,
    ) -> tuple[tuple[Any, ...], ...]:
        """Flatten the FrozenDotDict to a hashable tuple of tuples.

        Args:
            data (dict[str, Any] | None): The data to flatten. If None, use the current instance.
            sort_keys (bool): Whether to sort the keys in the output.

        Returns:
            tuple[tuple[Any, ...], ...]: A hashable representation of the FrozenDotDict.
        """
        local_data: dict[str, Any] = self.as_dict() if data is None else data
        items: list[list[str | Any]] = []
        for key, value in sorted(local_data.items()):
            if isinstance(value, dict):
                items.append([key, self.flatten_to_hashable(value)])
            else:
                items.append([key, value])
        if sort_keys:
            items.sort()
        return freeze(items)  # converts to tuple of tuples

    @cached_property
    def hashable(self) -> int:
        """Return a cached hashable representation of the FrozenDotDict."""
        return hash(self.flatten_to_hashable())

    def __hash__(self) -> int:
        """Return the hash of the FrozenDotDict."""
        return self.hashable

    __frozen__ = True
    __setattr__: NoReturnCall = immutable_method("FrozenDotDict")
    __delattr__: NoReturnCall = immutable_method("FrozenDotDict")
    __setitem__: NoReturnCall = immutable_method("FrozenDotDict")
    __delitem__: NoReturnCall = immutable_method("FrozenDotDict")
    clear: NoReturnCall = immutable_method("FrozenDotDict")


__all__ = ["DotDict", "FrozenDotDict"]


# if __name__ == "__main__":
#     data = {
#         "collection": {
#             "item1": {"name": "Item 1", "value": 10},
#             "item2": {"name": "Item 2", "value": {"subvalue": 20}},
#         },
#     }
#     dot_data: FrozenDotDict = FrozenDotDict.to_dot(data)
#     as_a_dict = dot_data.as_dict()
#     print(">>>> as_a_dict = dot_data.as_dict()")
#     print(as_a_dict)
#     print(">>>> dot_data = FrozenDotDict.to_dot(data)")
#     print(dot_data)

#     value = dot_data.collection.item1.name
#     print(">>>> value = dot_data.collection.item1.name")
#     print(value)  # Output: Item 1
#     item_value = dot_data["collection"]["item1"]["name"]
#     print(">>>> item_value = dot_data['collection']['item1']['name']")
#     print(item_value)  # Output: Item 1
#     print(f"Value is the same: {value == item_value}")

#     print(">>>> dot_data.counter = 0")

#     dot_data.counter = 0
#     print(dot_data.counter)  # Output: 0
#     print(">>>> dot_data.counter += 1")
#     dot_data.counter += 1
#     print(dot_data.counter)  # Output: 1

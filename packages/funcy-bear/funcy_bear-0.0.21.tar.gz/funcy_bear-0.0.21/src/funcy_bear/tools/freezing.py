"""Utilities for making objects immutable and hashable."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, NoReturn

from funcy_bear.exceptions import ImmutableTypeError
from funcy_bear.protocols.general import FrozenClass

if TYPE_CHECKING:
    from collections.abc import Callable

    from funcy_bear.constants.type_constants import NoReturnCall


def immutable_method(name: str = "FrozenDict") -> Callable[..., NoReturn]:
    """Generate a method that raises TypeError when called."""

    def immutable(*args, **kws) -> NoReturn:  # noqa: ARG001
        """Disable any method that would modify the dict."""
        raise ImmutableTypeError(name)

    return immutable


class FrozenDict(dict, FrozenClass):
    """An immutable dictionary.

    This is used to generate stable hashes for queries that contain dicts.
    Usually, Python dicts are not hashable because they are mutable. This
    class removes the mutability and implements the ``__hash__`` method.
    """

    __frozen__: bool = True
    clear: NoReturnCall = immutable_method()
    setdefault: NoReturnCall = immutable_method()  # type: ignore[override]
    popitem: NoReturnCall = immutable_method()
    update: NoReturnCall = immutable_method()  # type: ignore[override]
    pop: NoReturnCall = immutable_method()  # type: ignore[override]

    __setitem__: NoReturnCall = immutable_method()
    __delitem__: NoReturnCall = immutable_method()

    def __hash__(self) -> int:  # type: ignore[override]
        """Calculate the has by hashing a tuple of all dict items"""
        return hash(tuple(sorted(self.items())))


type FreezableTypes = dict | list | set
type ThawTypes = FrozenDict | tuple | frozenset


def freeze(obj: FreezableTypes | object | FrozenClass) -> FrozenDict | tuple | frozenset | object:
    """Freeze an object by making it immutable and thus hashable.

    Args:
        obj (AllowableTypes): The object to freeze. Can be a dict, list, or set.

    Returns:
        FrozenDict | tuple | frozenset | object: The frozen version of the object.

    Note:
        This function only handles dicts, lists, and sets. All other objects are returned as
        is without modification.

        if the object is already a frozen class (i.e., it implements the ``FrozenClass`` protocol
        and has ``__frozen__`` set to True), it is returned as is.
        If the input is a dict, it is converted to a ``FrozenDict``.
        If the input is a list, it is converted to a tuple.
        If the input is a set, it is converted to a ``frozenset``.
        Other types are returned unchanged.
    """
    if isinstance(obj, FrozenClass) and obj.__frozen__:
        return obj
    if isinstance(obj, dict):
        return FrozenDict((k, freeze(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return tuple(freeze(el) for el in obj)
    if isinstance(obj, set):
        return frozenset(obj)
    return obj


def thaw(obj: ThawTypes | Any) -> FreezableTypes:
    """Thaw a frozen object back to its mutable form.

    Args:
        obj (Any): The object to thaw. Can be a FrozenDict, tuple, or frozenset.

    Returns:
        Any: The thawed version of the object.

    Note:
        This function only handles FrozenDicts, tuples, and frozensets. All other objects
        are returned as is without modification.
        If the input is a FrozenDict, it is converted to a dict.
        If the input is a tuple, it is converted to a list.
        If the input is a frozenset, it is converted to a set.
        Other types are returned unchanged.
    """
    if isinstance(obj, FrozenDict):
        return {k: thaw(v) for k, v in obj.items()}
    if isinstance(obj, tuple):
        return [thaw(el) for el in obj]
    if isinstance(obj, frozenset):
        return set(obj)
    return obj

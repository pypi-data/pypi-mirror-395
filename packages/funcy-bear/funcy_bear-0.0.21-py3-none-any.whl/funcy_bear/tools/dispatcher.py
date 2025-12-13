"""A generalized dispatcher for data, using FP principles."""

from collections.abc import Callable, Hashable  # noqa: I001
from functools import wraps
from typing import Any, NamedTuple, ParamSpec, TypeVar

from funcy_bear.sentinels import MISSING

from .freezing import FrozenDict, freeze
from funcy_bear.constants.type_constants import TruthReturnedCall  # noqa: TC001


class DispatchEntry(NamedTuple):
    """A dispatch entry mapping a condition to a handler."""

    conditions: tuple[TruthReturnedCall, ...]
    kwargs: FrozenDict


class CacheKey(NamedTuple):
    """A cache key for the dispatcher."""

    arg_type: type
    arg_value: Hashable


class Registry(dict[DispatchEntry, Callable]):
    """A registry mapping keys to handler functions."""


T = TypeVar("T")
P = ParamSpec("P")


class Dispatcher:
    """A dispatcher that maps a conditional function to a handler function.

    Multiple ways to use the dispatcher:
        1. By keyword argument (default):
           @dispatcher.dispatcher()
           def func(obj, ...):
               ...
           foo = func(obj="bar")  # Dispatches on 'obj' argument
        2. By positional argument:
           @dispatcher.dispatcher()
           def func(arg1, arg2, ...):
               ...
           foo = func("bar", arg2=...)  # Dispatches on first positional argument
    """

    def __init__(self, arg: str = "obj", capacity: int = 256) -> None:
        """Initialize the dispatcher with an empty registry.

        Args:
            arg: The name of the argument to dispatch on (default: "obj")
            capacity: The maximum size of the LRU cache for resolved handlers (default: 256)
        """
        from funcy_bear.tools.lru_cache import LRUCache  # noqa: PLC0415

        self._arg: str = arg
        self._registry: Registry = Registry()
        self._cache: LRUCache[CacheKey, tuple[Callable, dict]] = LRUCache(capacity=capacity, strict=False)

    def register(self, *conditions: TruthReturnedCall, **kws) -> Callable:
        """Register a handler function for the given conditions.

        Args:
            *conditions: Predicate callables that return a truthy value when the handler should fire
                These callables should accept a single argument and return a boolean-like value.
            **kws: Additional keyword arguments to pass to the handler function
        """

        def decorator(func: Callable[P, T]) -> Callable[P, T]:
            self._cache.clear()
            entry = DispatchEntry(conditions=conditions, kwargs=freeze(kws))
            self._registry[entry] = func

            @wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def dispatcher(self) -> Callable:
        """Decorator to dispatch the function based on registered conditions.

        We let the decorated function handle missing arguments so nothing crashes here.

        We cache the resolved handler for each unique argument type and value combination
        to speed up repeated calls with the same argument.
        """

        def decorator(func: Callable[P, T]) -> Callable[P, T]:
            @wraps(func)
            def wrapper(*args: P.args, **kwargs: P.kwargs) -> T:
                arg: Any = kwargs.get(self._arg, args[0] if args else MISSING)
                if arg is MISSING:
                    return func(*args, **kwargs)
                cache_key = CacheKey(type(arg), freeze(arg))
                cached: tuple[Callable, dict] | None = self._cache.get(cache_key)
                if cached is not None:
                    c: tuple[Callable, dict] = cached
                    return c[0](*args, **{**c[1], **kwargs})
                for entry, handler in self._registry.items():
                    if all(cond(arg) for cond in entry.conditions):
                        self._cache[cache_key] = (handler, entry.kwargs)
                        return handler(*args, **{**entry.kwargs, **kwargs})
                return func(*args, **kwargs)

            return wrapper

        return decorator

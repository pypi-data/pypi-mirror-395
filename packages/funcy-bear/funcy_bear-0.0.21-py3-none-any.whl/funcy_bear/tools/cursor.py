"""A simple cursor to track position in a collection."""

from collections.abc import Iterator, Sequence
from typing import TYPE_CHECKING, Any, Final

from funcy_bear.protocols.general import CollectionProtocol
from funcy_bear.sentinels import SentinelDict, SentinelTuple
from lazy_bear import LazyLoader

if TYPE_CHECKING:
    from funcy_bear.ops.func_stuffs import has_attrs
    from funcy_bear.ops.math.general import clamp, neg
else:
    clamp, neg = LazyLoader("funcy_bear.ops.math.general").to("clamp", "neg")
    has_attrs = LazyLoader("funcy_bear.ops.func_stuffs").to("has_attrs")

SENTINEL_TUPLE: Final = SentinelTuple()
SENTINEL_DICT: Final = SentinelDict()


class BaseCursor[Collection_T: Sequence | CollectionProtocol, ReturnType: Any]:
    """A simple cursor to track position in a collection."""

    def __init__(
        self,
        collection: type[Collection_T],
        *,
        constrained: bool = True,
        default: Any | None = None,
        args: Any = SENTINEL_TUPLE,
        kwargs: Any = SENTINEL_DICT,
    ) -> None:
        """A simple cursor to track position in a collection.

        Args:
            collection (type[Collection_T]): The collection type to use for the cursor.
            _constrained (bool, optional): Whether to constrain the cursor within bounds. Defaults to True.
            default (Any | None, optional): The default value to return if the collection is empty. Defaults to None.
            *args: Arguments to pass to the collection constructor if a type is provided.
            **kwargs: Keyword arguments to pass to the collection constructor if a type is provided.
        """
        self._factory: type[Collection_T] = collection
        self._collection: Collection_T | None = None

        self._args: tuple[Any, ...] = args if args is not SENTINEL_TUPLE else ()
        self._kwargs: dict[str, Any] = kwargs if kwargs is not SENTINEL_DICT else {}
        self._constrained: bool = constrained
        self._default: Any = default
        self._index: int = 0

    @property
    def collection(self) -> Collection_T:
        """Get the current collection."""
        if self._collection is None:
            self._collection = self._factory(*self._args, **self._kwargs)
        return self._collection

    @property
    def current(self) -> ReturnType:
        """Get the current item in the collection."""
        return self.collection[self.index] if self.not_empty else self._default

    @property
    def index(self) -> int:
        """Get the current index of the cursor."""
        if self._constrained:
            return self.clamped(self._index)
        return self._index

    @index.setter
    def index(self, value: int) -> None:  # noqa: ARG002
        raise ValueError("Index cannot be set directly, use move() instead.")

    def set_index(self, value: int) -> None:
        """Set the current index of the cursor."""
        self._set_index(value)

    def move(self, offset: int, tail: bool = False, head: bool = False) -> None:
        """Move the cursor by the given offset."""
        self._move(offset=offset, tail=tail, head=head)

    def tick(self) -> None:
        """Move the cursor forward by one."""
        self._move(1)

    def tock(self) -> None:
        """Move the cursor backward by one."""
        self._move(neg(1))

    def head(self) -> None:
        """Move the cursor to the beginning of the collection."""
        self._move(head=True)

    def tail(self) -> None:
        """Move the cursor to the end of the collection."""
        self._move(tail=True)

    def _update(self, collection: Collection_T) -> None:
        """Update the collection and clamp the index to the new bounds."""
        self._collection = collection

    def _set_index(self, value: int) -> None:
        """Set the current index of the cursor."""
        self._index = value if not self._constrained else self.clamped(value)

    def _move(self, offset: int | None = None, tail: bool = False, head: bool = False) -> None:
        """Move the cursor by the given offset."""
        if head and tail:
            raise ValueError("Cannot move to both head and tail.")
        if not head and not tail and offset is not None:
            self._set_index(self.index + offset)
        elif head:
            self._set_index(self.lower)
        elif tail:
            self._set_index(self.upper)

    def offset(self, v: int) -> None:
        """Move the cursor by the given offset."""
        self._move(offset=v)

    def get(self, offset: int | None = None) -> ReturnType:
        """Get an item in the collection at the given offset from the current index."""
        if self._constrained:
            target_index: int = self.clamped(self.index + (offset if offset is not None else 0))
        else:
            target_index: int = self.index + (offset if offset is not None else 0)
        if hasattr(self.collection, "get") and isinstance(self.collection, CollectionProtocol):
            return self.collection.get(target_index) if self.not_empty else self._default
        return self.collection[target_index] if self.not_empty else self._default

    def peek(self, offset: int = 0, tail: bool = False, head: bool = False) -> ReturnType:
        """Peek at an item in the collection at the given offset from the current index."""
        if head and tail:
            raise ValueError("Cannot peek at both head and tail.")
        if head:
            target_index: int = self.lower
        elif tail:
            target_index = self.upper
        elif not self._constrained:
            try:
                return self.collection[self.index + offset]
            except IndexError:
                return self._default
        else:
            target_index = self.clamped(self.index + offset)
        return self.collection[target_index] if self.not_empty else self._default

    def reset(self) -> None:
        """Reset the cursor to the beginning of the collection."""
        self.head()

    def clear(self) -> None:
        """Clear all items from the collection."""
        collection: Collection_T = self.collection
        if hasattr(collection, "clear") and isinstance(collection, CollectionProtocol):
            collection.clear()
        self.reset()

    def clamped(self, v: int) -> int:
        """Clamp the given value to the bounds of the cursor."""
        return clamp(v, self.lower, self.upper)

    def copy(self) -> Collection_T:
        """Get a copy of the current collection."""
        if hasattr(self.collection, "copy") and isinstance(self.collection, CollectionProtocol):
            return self.collection.copy()
        raise NotImplementedError(f"Collection of type {type(self.collection)} does not support copy.")

    def push(self, item: ReturnType) -> None:
        """Add an item to the end of the collection."""
        attrs: dict[str, bool] = has_attrs(self.collection, ("push", "append", "add", "insert"), true_only=True)
        if not attrs:
            raise NotImplementedError(
                f"Collection of type {type(self.collection)} does not support push/append/add/insert."
            )
        getattr(self.collection, next(iter(attrs)))(item)

    def pop(self, index: int | None = None) -> ReturnType:
        """Remove and return an item from the collection.

        Args:
            index (int | None, optional): The index of the item to remove. If None, removes the item at the current cursor position. Defaults to None.

        Returns:
            ReturnType: The removed item.
        """
        if self.is_empty:
            raise IndexError("pop from empty collection")
        if self._constrained:
            target_index: int = self.clamped(self.index if index is None else index)
        else:
            target_index = self.index if index is None else index
        item: ReturnType = self.collection[target_index]
        if hasattr(self.collection, "remove") and isinstance(self.collection, CollectionProtocol):
            self.collection.remove(item)
        else:
            raise NotImplementedError(f"Collection of type {type(self.collection)} does not support pop.")
        return item

    @property
    def head_value(self) -> ReturnType:
        """Get the value at the head of the collection."""
        return self.peek(head=True)

    @property
    def tail_value(self) -> ReturnType:
        """Get the value at the tail of the collection."""
        return self.peek(tail=True)

    @property
    def lower(self) -> int:
        """Get the lower bound of the cursor."""
        return 0

    @property
    def upper(self) -> int:
        """Get the upper bound of the cursor."""
        return self.size - 1

    @property
    def size(self) -> int:
        """Get the size of the collection."""
        return len(self)

    @property
    def is_empty(self) -> bool:
        """Check if the collection is empty."""
        return self.size == 0

    @property
    def not_empty(self) -> bool:
        """Check if the collection is not empty."""
        return self.size > 0

    @property
    def within_bounds(self) -> bool:
        """Check if the current index is within the bounds of the collection."""
        return self.lower <= self.index <= self.upper

    def join(self, d: str = ", ") -> str:
        """Join the collection items into a single string with the given delimiter.

        Args:
            d (str): The delimiter to use between items. Defaults to ", ".

        Returns:
            str: The joined string of collection items.
        """
        if hasattr(self.collection, "join") and isinstance(self.collection, CollectionProtocol):
            return self.collection.join(d) if self.not_empty else ""
        raise NotImplementedError(f"Collection of type {type(self.collection)} does not support join.")

    def __len__(self) -> int:
        return len(self.collection)

    def __iter__(self) -> Iterator[ReturnType]:
        return iter(self.collection)

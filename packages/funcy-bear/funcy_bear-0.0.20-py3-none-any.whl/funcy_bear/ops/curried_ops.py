"""A collection of curried operations that can be applied to fields in a document."""

from collections.abc import Callable  # noqa: TC003
from contextlib import suppress
from operator import abs as _abs, mod as _mod, not_ as invert, pow as _pow
from typing import Any

from funcy_bear.injection import Deleter, Getter, Provide, Setter, inject_tools

from ._di_containers import CurryingContainer, FactoryContainer
from .math import clamp as _clamp


@inject_tools()
def delete(
    field: str,
    deleter: Deleter = Provide[CurryingContainer.deleter],
) -> None:
    """Delete a given field from the document.

    Args:
        field: The field to delete.
    """
    deleter(field)


@inject_tools()
def add(
    field: str,
    n: int,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Add ``n`` to a given field in the document.

    Args:
        field: The field to add to.
        n: The amount to add.
    """
    attr: Any = getter(field)
    if isinstance(attr, (int | float)):
        setter(field, attr + n)


@inject_tools()
def subtract(
    field: str,
    n: int,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Subtract ``n`` to a given field in the document.

    Args:
        field: The field to subtract from.
        n: The amount to subtract.
    """
    attr: Any = getter(field)
    if isinstance(attr, (int | float)):
        setter(field, attr - n)


@inject_tools()
def multiply(
    field: str,
    n: int,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Multiply a given field in the document by n.

    Args:
        field: The field to multiply.
        n: The amount to multiply by.
    """
    attr: Any = getter(field)
    if isinstance(attr, (int | float)):
        setter(field, attr * n)


@inject_tools()
def div(
    field: str,
    n: int,
    floor: bool,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Divide a given field in the document by n.

    Args:
        field: The field to divide.
        n: The amount to divide by. Must not be zero
        floor: If True, use floor division.
    """
    attr: Any = getter(field)
    if isinstance(attr, (int | float)) and n != 0:
        if floor:
            setter(field, attr // n)
        else:
            setter(field, attr / n)


@inject_tools()
def increment(
    field: str,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Increment a given field by 1."""
    attr: Any = getter(field)
    if isinstance(attr, (int | float)):
        setter(field, attr + 1)


@inject_tools()
def decrement(
    field: str,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Decrement a given field in the document by 1.

    Args:
        field: The field to decrement.
    """
    attr: Any = getter(field)
    if isinstance(attr, (int | float)):
        setter(field, attr - 1)


@inject_tools()
def setter(
    field: str,
    v: Any,
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Set a given field to ``val``.

    Args:
        field: The field to set.
        v: The value to set the field to.
    """
    setter(field, v)


@inject_tools()
def if_else(
    field: str,
    cond: Callable[[Any], bool],
    then: Callable[..., None],
    otherwise: Callable[..., None],
    getter: Getter = Provide[FactoryContainer.getter],
) -> Callable[[Any], None]:
    """Apply one of two operations based on the value of a field in the document.

    Args:
        field: The field to check.
        cond: A callable that takes the field's value and returns a boolean.
        then: The operation to apply if the condition is true.
        otherwise: The operation to apply if the condition is false.
    """

    def transform(doc: Any) -> None:
        if cond(getter(field, doc)):
            then(doc)
        else:
            otherwise(doc)

    return transform


@inject_tools()
def swapcase(
    field: str,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Swap the case of a string field.

    Args:
        field: The field to swap case.
    """
    attr: Any = getter(field)
    if isinstance(attr, str):
        setter(field, attr.swapcase())


@inject_tools()
def upper(
    field: str,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Convert a string field to uppercase.

    Args:
        field: The field to convert.
    """
    attr: Any = getter(field)
    if isinstance(attr, str):
        setter(field, attr.upper())


@inject_tools()
def lower(
    field: str,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Convert a string field to lowercase.

    Args:
        field: The field to convert.
    """
    attr: Any = getter(field)
    if isinstance(attr, str):
        setter(field, attr.lower())


@inject_tools()
def replace(
    field: str,
    old: str,
    new: str,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Replace occurrences of a substring in a string field.

    Args:
        field: The field to modify.
        old: The substring to replace.
        new: The substring to replace with.
    """
    attr: Any = getter(field)
    if isinstance(attr, str):
        setter(field, attr.replace(old, new))


@inject_tools()
def format(
    field: str,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
    **kwargs: Any,
) -> None:
    """Format a string field using the provided arguments.

    Args:
        field: The field to format.
        **kwargs: Keyword arguments for formatting.
    """
    attr = getter(field)
    if isinstance(attr, str) and kwargs.get("kwargs") and isinstance(kwargs["kwargs"], dict):
        extracted = kwargs.pop("kwargs")
        attr: str = attr.format(**extracted)
        setter(field, attr)
    else:
        setter(field, attr.format(**kwargs))


@inject_tools()
def pow(
    field: str,
    n: int,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Raise a given field in the document to the power of n.

    Args:
        field: The field to raise.
        n: The exponent.
    """
    attr: Any = getter(field)
    if isinstance(attr, (int | float)):
        setter(field, _pow(attr, n))


@inject_tools()
def clamp(
    field: str,
    min_value: int,
    max_value: int,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Clamp a given field in the document to be within min_value and max_value.

    Args:
        field: The field to clamp.
        min_value: The minimum value to clamp to.
        max_value: The maximum value to clamp to.
    """
    attr: Any = getter(field)
    if isinstance(attr, (int | float)):
        setter(field, _clamp(attr, min_value, max_value))


@inject_tools()
def mod(
    field: str,
    n: int,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Modulus a given field in the document by n.

    Args:
        field: The field to modulus.
        n: The amount to modulus by.
    """
    attr: Any = getter(field)
    if isinstance(attr, (int | float)) and n != 0:
        setter(field, _mod(attr, n))


@inject_tools()
def toggle(
    field: str,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Toggle a boolean field.

    Args:
        field: The field to toggle.
    """
    attr: Any = getter(field)
    if isinstance(attr, bool):
        setter(field, invert(attr))


@inject_tools()
def abs(
    field: str,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Set a field to its absolute value.

    Args:
        field: The field to set.
    """
    attr: Any = getter(field)
    if isinstance(attr, (int | float)):
        setter(field, _abs(attr))


@inject_tools()
def default(
    field: str,
    v: Any,
    replace_none: bool,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Set a field to a default value if it does not exist.

    Args:
        field: The field to set.
        v: The default value to set the field to.
        replace_none: If True, also replace None values.
    """
    try:
        current: Any = getter(field)
        if replace_none and current is None:
            setter(field, v)
    except (KeyError, AttributeError):
        setter(field, v)


@inject_tools()
def push(
    field: str,
    v: Any,
    index: int,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Push a value to a list field in the document at a specific index.

    Args:
        field: The field to push to.
        v: The value to push.
        index: The index to insert the value at. Defaults to -1 (the end of the list).
    """
    try:
        attr: Any = getter(field)
    except (KeyError, AttributeError):
        attr = setter(field, [], return_val=True)

    if isinstance(attr, list):
        if index == -1 or index >= len(attr):
            attr.append(v)
        else:
            attr.insert(index, v)


@inject_tools()
def append(
    field: str,
    v: Any,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Append a value to a list field in the document.

    Args:
        field: The field to append to.
        v: The value to append.
    """
    try:
        attr: Any = getter(field)
    except (KeyError, AttributeError):
        attr = setter(field, [], return_val=True)

    if isinstance(attr, list):
        attr.append(v)


@inject_tools()
def prepend(
    field: str,
    v: Any,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Prepend a value to a list field in the document.

    Args:
        field: The field to prepend to.
        v: The value to prepend.
    """
    try:
        attr: Any = getter(field)
    except (KeyError, AttributeError):
        attr = setter(field, [], return_val=True)
    if isinstance(attr, list):
        attr.insert(0, v)


@inject_tools()
def extend(
    field: str,
    vals: list,
    getter: Getter = Provide[CurryingContainer.getter],
    setter: Setter = Provide[CurryingContainer.setter],
) -> None:
    """Extend a list field in the document with another list.

    Args:
        field: The field to extend.
        vals: The list of values to extend with.
    """
    try:
        attr = getter(field)
    except (KeyError, AttributeError):
        setter(field, [])
        attr: list[Any] = []

    if isinstance(attr, list):
        attr.extend(vals)


@inject_tools()
def pop(
    field: str,
    index: int,
    getter: Getter = Provide[CurryingContainer.getter],
) -> None:
    """Pop a value from a list field in the document.

    Args:
        field: The field to pop from.
        index: The index to pop. Defaults to -1 (the last item).
    """
    with suppress(IndexError, KeyError, AttributeError):
        attr: Any = getter(field)
        if isinstance(attr, list) and -len(attr) <= index < len(attr):
            attr.pop(index)


# if __name__ == "__main__":
# from dataclasses import dataclass
# from typing import Any

# @dataclass
# class Sample:
#     name: str
#     age: int

# doc1: dict[str, Any] = {"name": "Alice", "age": 30}
# doc2 = Sample(name="Bob", age=25)

# print("Before:", doc1)
# print("Before:", doc2)

# increment_age = increment("age")

# increment_age(doc1)

# print("After increment:", doc1)

# increment("age")(doc2)

# upper("name")(doc1)
# upper("name")(doc2)

# print("After increment and upper:", doc1)
# print("After increment and upper:", doc2)

# decrement("age")(doc1)
# decrement("age")(doc1)
# decrement("age")(doc2)
# decrement("age")(doc2)

# print("After decrement:", doc1)
# print("After decrement:", doc2)

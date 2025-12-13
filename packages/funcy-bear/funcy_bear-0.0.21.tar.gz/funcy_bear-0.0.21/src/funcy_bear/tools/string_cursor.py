"""String cursor for scanning through a string one character at a time."""

from funcy_bear.ops.math.general import neg

from .cursor import BaseCursor


class StringCursor(BaseCursor[str, str]):
    """Cursor for scanning through a string one character at a time."""

    def __init__(self, text: str, *, allow_negative: bool = False) -> None:
        """Initialize cursor with text to scan."""
        if not isinstance(text, str):
            raise TypeError(f"Expected str, got {type(text).__name__}")
        super().__init__(str, constrained=False, default="", args=(text,))
        self.allow_neg: bool = allow_negative

    def tick(self) -> None:
        """Move the cursor forward by one."""
        self._move(1)

    def tock(self) -> None:
        """Move the cursor backward by one."""
        if not self.allow_neg and self.index == 0:
            return
        self._move(neg(1))

    def prev_char_equals(self, s: str) -> bool:
        """Check if previous character equals target character.

        Args:
            s: Target character to compare
        Returns:
            True if previous character equals s
        """
        if not self.allow_neg and self.index == 0:
            return False
        return self.peek(-1) == s

    def next_char_equals(self, s: str) -> bool:
        """Check if next character equals target character.

        Args:
            s: Target character to compare
        Returns:
            True if next character equals s
        """
        return self.peek(1) == s

    def is_char(self, s: str) -> bool:
        """Check if current character equals target character.

        Args:
            s: Target character to compare
        Returns:
            True if current character equals s
        """
        return self.peek(0) == s

    def n_char_equals(self, o: int, s: str) -> bool:
        """Check if character at offset equals target character.

        Args:
            o: Offset from current index
            s: Target character to compare

        Returns:
            True if character at offset equals s
        """
        if not self.allow_neg and self.index + o < 0:
            return False
        return self.peek(o) == s

    def head_equals(self, s: str) -> bool:
        """Check if the first character in the text equals target character.

        Args:
            s: Target character to compare
        Returns:
            True if first character equals s
        """
        return self.head_value == s if self.not_empty else False

    def tail_equals(self, s: str) -> bool:
        """Check if the last character in the text equals target character.

        Args:
            s: Target character to compare
        Returns:
            True if last character equals s
        """
        return self.tail_value == s if self.not_empty else False

    def matches_ahead(self, s: str) -> bool:
        """Check if string ahead matches target.

        Args:
            s: Target string to compare
        Returns:
            True if string ahead matches s
        Raises:
            IndexError: If there are not enough characters ahead to match
        """
        if self._index + len(s) > len(self.collection):
            return False
        return self.collection[self._index : self._index + len(s)] == s

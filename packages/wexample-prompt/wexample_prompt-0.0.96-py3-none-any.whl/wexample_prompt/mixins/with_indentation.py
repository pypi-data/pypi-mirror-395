from __future__ import annotations

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class WithIndentation:
    indentation_length: int | None = public_field(
        default=2, description="Number of characters to repeat for one indentation"
    )
    _indentation: int = 0

    @property
    def indentation(self) -> int:
        """Current indentation level."""
        return self._indentation

    @indentation.setter
    def indentation(self, value: int) -> None:
        self._indentation = value

    def indentation_down(self, number: int = 1) -> None:
        """Decrease indentation by a given number (default: 1)."""
        self._indentation -= number
        if self._indentation < 0:
            self._indentation = 0  # optional safety guard

    def indentation_up(self, number: int = 1) -> None:
        """Increase indentation by a given number (default: 1)."""
        self._indentation += number

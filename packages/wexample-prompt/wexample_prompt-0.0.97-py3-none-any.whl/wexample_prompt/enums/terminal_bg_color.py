"""Terminal background color codes using colorama."""

from __future__ import annotations

from enum import Enum

from colorama import Back


class TerminalBgColor(Enum):
    """Terminal background color codes using colorama constants."""

    # Standard background colors
    BLACK = Back.BLACK
    RED = Back.RED
    GREEN = Back.GREEN
    YELLOW = Back.YELLOW
    BLUE = Back.BLUE
    MAGENTA = Back.MAGENTA
    CYAN = Back.CYAN
    WHITE = Back.WHITE
    # Light/Bright background colors
    LIGHT_BLACK = Back.LIGHTBLACK_EX
    LIGHT_RED = Back.LIGHTRED_EX
    LIGHT_GREEN = Back.LIGHTGREEN_EX
    LIGHT_YELLOW = Back.LIGHTYELLOW_EX
    LIGHT_BLUE = Back.LIGHTBLUE_EX
    LIGHT_MAGENTA = Back.LIGHTMAGENTA_EX
    LIGHT_CYAN = Back.LIGHTCYAN_EX
    LIGHT_WHITE = Back.LIGHTWHITE_EX
    # Reset background
    DEFAULT = Back.RESET

    def __str__(self) -> str:
        """Return the background color code when converting to string."""
        return self.value

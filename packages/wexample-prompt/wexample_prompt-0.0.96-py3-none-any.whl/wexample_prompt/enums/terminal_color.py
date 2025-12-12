"""Terminal color and style codes using colorama."""

from __future__ import annotations

from enum import Enum

from colorama import Fore, Style


class TerminalColor(Enum):
    """Terminal color and style codes using colorama constants."""

    # Standard colors
    BLACK = Fore.BLACK
    RED = Fore.RED
    GREEN = Fore.GREEN
    YELLOW = Fore.YELLOW
    BLUE = Fore.BLUE
    MAGENTA = Fore.MAGENTA
    CYAN = Fore.CYAN
    WHITE = Fore.WHITE
    # Light/Bright colors
    LIGHT_BLACK = Fore.LIGHTBLACK_EX
    LIGHT_RED = Fore.LIGHTRED_EX
    LIGHT_GREEN = Fore.LIGHTGREEN_EX
    LIGHT_YELLOW = Fore.LIGHTYELLOW_EX
    LIGHT_BLUE = Fore.LIGHTBLUE_EX
    LIGHT_MAGENTA = Fore.LIGHTMAGENTA_EX
    LIGHT_CYAN = Fore.LIGHTCYAN_EX
    LIGHT_WHITE = Fore.LIGHTWHITE_EX
    # Special
    DEFAULT = Fore.RESET
    RESET = Style.RESET_ALL
    # Text styles
    BOLD = Style.BRIGHT
    DIM = Style.DIM

    def __str__(self) -> str:
        """Return the color/style code when converting to string."""
        return self.value

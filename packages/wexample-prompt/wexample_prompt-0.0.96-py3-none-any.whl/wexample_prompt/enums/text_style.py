from __future__ import annotations

from enum import Enum


class TextStyle(Enum):
    BOLD = "bold"
    ITALIC = "italic"
    UNDERLINE = "underline"
    STRIKETHROUGH = "strikethrough"
    DIM = "dim"
    REVERSE = "reverse"
    HIDDEN = "hidden"

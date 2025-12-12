"""Indentation style enumeration."""

from __future__ import annotations

from enum import Enum


class IndentationStyle(str, Enum):
    """Style of indentation rendering."""

    REPEAT = "repeat"
    """Repeat the indentation character × length for each level (default behavior)."""
    VERTICAL = "vertical"
    """Display one character per level, like IDE vertical lines (e.g., '│ │ │ ')."""

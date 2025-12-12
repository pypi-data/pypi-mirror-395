from __future__ import annotations

from enum import Enum


class ResponseType(Enum):
    """Types of prompt responses."""

    LIST = "list"
    MULTIPLE = "multiple"
    PLAIN = "plain"
    PROGRESS = "progress"
    PROPERTIES = "properties"
    SUGGESTIONS = "suggestions"
    TABLE = "table"
    TITLE = "title"
    TREE = "tree"

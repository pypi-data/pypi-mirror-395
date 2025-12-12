from __future__ import annotations

from enum import Enum


class ChoiceValue(Enum):
    ABORT = "abort"


class FilePickerMode(str, Enum):
    FILES = "files"
    DIRS = "dirs"
    BOTH = "both"

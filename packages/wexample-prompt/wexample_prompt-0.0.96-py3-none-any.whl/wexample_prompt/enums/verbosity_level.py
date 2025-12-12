from __future__ import annotations

from enum import IntEnum


class VerbosityLevel(IntEnum):
    """Verbosity levels for controlling output detail.

    Levels:
        QUIET (0): Only show critical messages and errors
        DEFAULT (1): Show normal output (default)
        MEDIUM (2): Show additional information and details
        MAXIMUM (3): Show all possible information including debug messages
    """

    QUIET = 0
    DEFAULT = 1
    MEDIUM = 2
    HIGH = 3
    MAXIMUM = 4

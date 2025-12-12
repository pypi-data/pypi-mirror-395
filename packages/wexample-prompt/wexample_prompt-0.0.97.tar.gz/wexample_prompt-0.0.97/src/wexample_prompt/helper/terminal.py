"""Text width calculation utilities for proper display width including emojis and OSC links."""

from __future__ import annotations

import wcwidth


def terminal_get_visible_width(text: str) -> int:
    """Calculate the visible width of text using wcwidth.

    This function properly handles:
    - Regular ASCII characters (width 1)
    - Emojis and other wide characters (width 2)
    - Zero-width characters (width 0)
    - ANSI escape codes and OSC hyperlinks (stripped automatically)

    Args:
        text: The text to measure

    Returns:
        The visible width in terminal columns
    """
    text = terminal_strip_sequences(text)

    width = wcwidth.wcswidth(text)
    # wcswidth returns -1 if the string contains non-printable characters
    # In that case, fall back to character-by-character calculation
    if width == -1:
        width = 0
        for char in text:
            char_width = wcwidth.wcwidth(char)
            # wcwidth returns -1 for control characters, treat as 0
            if char_width == -1:
                char_width = 0
            width += char_width

    return max(0, width)


def terminal_strip_sequences(text: str) -> str:
    """Strip CSI/OSC ANSI escape sequences so width calculations see only visible chars."""
    from wexample_helpers.const.terminal import OSC_SEQUENCE_RE
    from wexample_helpers.helpers.ansi import ansi_strip

    cleaned = ansi_strip(text)
    return OSC_SEQUENCE_RE.sub("", cleaned)

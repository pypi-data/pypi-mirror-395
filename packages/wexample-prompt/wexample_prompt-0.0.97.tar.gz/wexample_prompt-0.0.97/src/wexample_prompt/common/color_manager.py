from __future__ import annotations

from typing import TYPE_CHECKING

from colorama import init

from wexample_prompt.enums.terminal_bg_color import TerminalBgColor
from wexample_prompt.enums.terminal_color import TerminalColor

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_bg_color import TerminalBgColor
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.enums.text_style import TextStyle


class ColorManager:
    """Manages color application and terminal capabilities."""

    # Initialize colorama when class is loaded
    init()

    @classmethod
    def build_prefix(
        cls,
        color: TerminalColor | None = None,
        bg: TerminalBgColor | None = None,
        styles: list[TextStyle] | None = None,
    ) -> str:
        """Build ANSI prefix combining color and a list of TextStyle entries."""
        prefix = ""
        if color:
            prefix += str(color)
        if bg:
            prefix += str(bg)
        if styles:
            prefix += "".join(cls.get_style_ansi(s) for s in styles)
        return prefix

    @classmethod
    def colorize(
        cls,
        text: str,
        color: TerminalColor | None = None,
        style: TerminalColor | None = None,
        bg: TerminalBgColor | None = None,
        styles: list[TextStyle] | None = None,
    ) -> str:
        from colorama import Style

        # Backward compatibility: if caller passes single style via `style`
        # (which historically reused TerminalColor entries BOLD/DIM),
        # we still honor it. New code should use `styles` and/or `bg`.
        prefix = ""
        if color:
            prefix += str(color)
        if bg:
            prefix += str(bg)
        if styles:
            prefix += "".join(cls.get_style_ansi(s) for s in styles)
        if style:
            prefix += str(style)

        if prefix:
            return f"{prefix}{text}{Style.RESET_ALL}"
        return text

    @classmethod
    def get_style_ansi(cls, style: TextStyle) -> str:
        """Map TextStyle to ANSI code without reset."""
        from wexample_prompt.enums.text_style import TextStyle

        style_codes = {
            TextStyle.BOLD: "\u001b[1m",
            TextStyle.ITALIC: "\u001b[3m",
            TextStyle.UNDERLINE: "\u001b[4m",
            TextStyle.STRIKETHROUGH: "\u001b[9m",
            TextStyle.DIM: "\u001b[2m",
            TextStyle.REVERSE: "\u001b[7m",
            TextStyle.HIDDEN: "\u001b[8m",
        }
        return style_codes.get(style, "")

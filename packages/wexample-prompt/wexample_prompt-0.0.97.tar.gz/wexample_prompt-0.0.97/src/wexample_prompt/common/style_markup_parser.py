from __future__ import annotations

import re
from collections.abc import Iterable
from typing import TYPE_CHECKING

from wexample_prompt.enums.terminal_color import TerminalColor

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
    from wexample_prompt.enums.text_style import TextStyle

# Pattern to match directives: @type:params{content} or @type{content}
# Supports word characters, emojis, +, and special chars for backward compatibility
_STYLE_DIRECTIVE_PATTERN = re.compile(
    r"@([\w🔴🟥🟠🟧🟡🟨🟢🟩🔵🟦🟣🟪🟤⚫⚪🔷🔹🔶🔸+]+)(?::([^\{\}]+))?\{", re.IGNORECASE
)
_EMOJI_COLOR_MAP: dict[str, TerminalColor] = {
    "🔴": TerminalColor.RED,
    "🟥": TerminalColor.RED,
    "🟥️": TerminalColor.RED,
    "🟠": TerminalColor.LIGHT_RED,
    "🟧": TerminalColor.LIGHT_RED,
    "🟡": TerminalColor.YELLOW,
    "🟨": TerminalColor.YELLOW,
    "🟢": TerminalColor.GREEN,
    "🟩": TerminalColor.GREEN,
    "🔵": TerminalColor.BLUE,
    "🟦": TerminalColor.BLUE,
    "🟣": TerminalColor.MAGENTA,
    "🟪": TerminalColor.MAGENTA,
    "🟤": TerminalColor.LIGHT_BLACK,
    "⚫": TerminalColor.BLACK,
    "⚪": TerminalColor.WHITE,
    "🔷": TerminalColor.CYAN,
    "🔹": TerminalColor.CYAN,
    "🔶": TerminalColor.LIGHT_YELLOW,
    "🔸": TerminalColor.LIGHT_YELLOW,
}


def flatten_style_markup(
    text: str,
    *,
    default_color: TerminalColor | None = None,
    base_styles: Iterable[TextStyle] | None = None,
    joiner: str | None = " ",
) -> list[PromptResponseSegment]:
    """Parse markup and flatten multi-line output into a single list of segments.

    Parameters
    ----------
    text:
        The source string that may contain inline directives.
    default_color:
        Optional fallback color applied to segments without an explicit color.
    base_styles:
        Styles propagated to every generated segment unless overridden.
    joiner:
        String inserted between logical lines when the markup produced multiple
        lines. Set to ``None`` to keep them separate (no automatic joiner).
    """
    from wexample_prompt.common.prompt_response_segment import PromptResponseSegment

    segments: list[PromptResponseSegment] = []
    parsed_lines = parse_style_markup(
        text=text, default_color=default_color, base_styles=base_styles
    )

    for idx, line in enumerate(parsed_lines):
        if idx > 0 and joiner is not None:
            segments.append(PromptResponseSegment(text=joiner))
        segments.extend(line)
    return segments


def parse_style_markup(
    text: str,
    default_color: TerminalColor | None = None,
    base_styles: Iterable[TextStyle] | None = None,
) -> list[list[PromptResponseSegment]]:
    """
    Parse a text with custom markup like ``@color:red+bold{content}`` into
    prompt response segments grouped by lines.

    Supported directives:
      * ``@color:name+style{text}`` or ``@name+style{text}`` - Apply color and styles
      * ``@path{/path/to/file}`` or ``@path:short{/path/to/file}`` - Format file paths (clickable)
      * ``@time{format}`` or ``@time:format{timestamp}`` - Format timestamps

    Supported modifiers:
      * Any ``TerminalColor`` member name (case-insensitive, - or _ interchangeable).
      * Any ``TextStyle`` member name (case-insensitive).

    Multiple modifiers can be combined with ``+`` (eg ``@color:blue+bold``).
    Nested directives are supported.
    """
    lines: list[list[PromptResponseSegment]] = []
    current_segments: list[PromptResponseSegment] = []
    initial_styles = list(base_styles) if base_styles else []

    def push_text(
        value: str,
        active_color: TerminalColor | None,
        active_styles: Iterable[TextStyle],
    ) -> None:
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment

        nonlocal current_segments

        styles_list = list(active_styles)
        buffer: list[str] = []

        for ch in value:
            if ch == "\n":
                if buffer:
                    segment_text = "".join(buffer)
                    current_segments.append(
                        PromptResponseSegment(
                            text=segment_text,
                            color=active_color,
                            styles=list(styles_list),
                        )
                    )
                    buffer = []
                elif not current_segments:
                    current_segments.append(
                        PromptResponseSegment(
                            text="",
                            color=active_color,
                            styles=list(styles_list),
                        )
                    )

                lines.append(current_segments)
                current_segments = []
                continue

            buffer.append(ch)

        if buffer:
            segment_text = "".join(buffer)
            current_segments.append(
                PromptResponseSegment(
                    text=segment_text,
                    color=active_color,
                    styles=list(styles_list),
                )
            )

    def apply_tokens(
        tokens: str, active_color: TerminalColor | None, active_styles: list[TextStyle]
    ) -> tuple[TerminalColor | None, list[TextStyle]]:
        from wexample_prompt.enums.terminal_color import TerminalColor
        from wexample_prompt.enums.text_style import TextStyle

        updated_color = active_color
        styles_list = list(active_styles)

        for raw_token in tokens.split("+"):
            token = raw_token.strip()
            if not token:
                continue

            if token in _EMOJI_COLOR_MAP:
                updated_color = _EMOJI_COLOR_MAP[token]
                continue

            normalized = re.sub(r"[^0-9A-Z_]", "_", token, flags=re.IGNORECASE).upper()

            if normalized in TextStyle.__members__:
                style = TextStyle[normalized]
                if style not in styles_list:
                    styles_list.append(style)
                continue

            if normalized in TerminalColor.__members__:
                updated_color = TerminalColor[normalized]
                continue

        return updated_color, styles_list

    def extract_braced_content(source: str, start_index: int) -> tuple[str, int]:
        depth = 0
        i = start_index
        while i < len(source):
            if source[i] == "{":
                depth += 1
            elif source[i] == "}":
                if depth == 0:
                    return source[start_index:i], i + 1
                depth -= 1
            i += 1

        raise ValueError("Unmatched '{' in style markup.")

    def format_path(path: str, short: bool = False) -> str:
        """Format a file path, optionally making it clickable."""
        try:
            from wexample_helpers.helpers.cli import cli_make_clickable_path

            if short and "/" in path:
                # Show only filename for short format
                filename = path.rsplit("/", 1)[-1]
                return cli_make_clickable_path(path, short_title=filename)
            return cli_make_clickable_path(path)
        except ImportError:
            # Fallback if helper not available
            return path

    def format_time(content: str, fmt: str | None = None) -> str:
        """Format a timestamp or current time."""
        from datetime import datetime

        if fmt is None:
            fmt = "%H:%M:%S"

        # If content is empty, use current time
        if not content.strip():
            return datetime.now().strftime(fmt)

        # Try to parse content as timestamp
        try:
            # If it's a number, treat as unix timestamp
            timestamp = float(content)
            return datetime.fromtimestamp(timestamp).strftime(fmt)
        except ValueError:
            # If it's already formatted, return as-is
            return content

    def parse_section(
        section_text: str,
        active_color: TerminalColor | None,
        active_styles: list[TextStyle],
    ) -> None:
        index = 0
        while index < len(section_text):
            match = _STYLE_DIRECTIVE_PATTERN.search(section_text, index)
            if not match:
                remaining = section_text[index:]
                if remaining:
                    push_text(remaining, active_color, active_styles)
                return

            prefix = section_text[index : match.start()]
            if prefix:
                push_text(prefix, active_color, active_styles)

            directive_type = match.group(1).lower()
            directive_params = match.group(2) or ""

            try:
                content, next_index = extract_braced_content(section_text, match.end())
            except ValueError:
                # Treat the directive literally if it is malformed.
                push_text(section_text[match.start() :], active_color, active_styles)
                return

            # Handle special formatters (must be explicit directive types)
            if directive_type == "path":
                formatted = format_path(content, short=(directive_params == "short"))
                push_text(formatted, active_color, active_styles)
                index = next_index
                continue

            if directive_type == "time":
                formatted = format_time(content, directive_params or None)
                push_text(formatted, active_color, active_styles)
                index = next_index
                continue

            # Handle color/style directives (backward compatibility)
            # If directive_type is "color", use params as tokens
            # Otherwise, use directive_type itself as tokens (for @red{}, @🔵+bold{}, etc.)
            if directive_type == "color" and directive_params:
                tokens = directive_params
            else:
                # For @red{}, @🔵+bold{}, etc., the whole directive_type is the token
                tokens = directive_type

            child_color, child_styles = apply_tokens(
                tokens, active_color, active_styles
            )
            parse_section(content, child_color, child_styles)
            index = next_index

        return

    parse_section(text, default_color, initial_styles)

    if current_segments:
        lines.append(current_segments)

    return lines

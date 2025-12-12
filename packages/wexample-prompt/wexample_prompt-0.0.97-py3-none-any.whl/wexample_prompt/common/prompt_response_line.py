"""Prompt response line implementation."""

from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
    from wexample_prompt.const.types import LineMessage
    from wexample_prompt.enums.terminal_color import TerminalColor


@base_class
class PromptResponseLine(BaseClass):
    """A line of text composed of one or more segments with optional styling and layout."""

    segments: list[PromptResponseSegment] = public_field(
        factory=list, description="List of text segments that constitute a line"
    )

    @classmethod
    def create_from_string(
        cls, text: LineMessage, color: TerminalColor | None = None
    ) -> list[PromptResponseLine]:
        """
        Create a line from a single text string.
        """
        from wexample_prompt.common.style_markup_parser import parse_style_markup

        raw_inputs = [text] if isinstance(text, str) else list(text)
        lines: list[PromptResponseLine] = []
        for raw in raw_inputs:
            for segments in parse_style_markup(raw, default_color=color):
                lines.append(cls(segments=segments))

        return lines

    def render(self, context: PromptContext) -> str:
        """Render the line within the context width, wrapping segments as needed.
        Respect context.formatting: when False, do not reflow/wrap lines.
        """
        indentation = context.render_indentation()
        # If formatting is disabled, bypass wrapping logic entirely.
        if context.formatting is False:
            return self._render_no_formatting(context, indentation)

        max_content_width = self._compute_max_content_width(context, indentation)

        if not max_content_width:
            return self._render_unbounded(context, indentation)

        return self._render_wrapped(context, indentation, max_content_width)

    def _compute_max_content_width(
        self, context: PromptContext, indentation: str
    ) -> int | None:
        """Compute the maximum visible width available for content on a line, or None if unbounded."""
        if context.width:
            return context.get_available_width(context.width, minimum=0)
        return None

    def _render_no_formatting(self, context: PromptContext, indentation: str) -> str:
        """Render all segments on a single line, without wrapping."""
        rendered_segments = []
        for seg in self.segments:
            # Provide a very large remaining width to avoid splitting segments
            rendered, _ = seg.render(context, line_remaining_width=10**9)
            rendered_segments.append(rendered)
        return f"{indentation}{''.join(rendered_segments)}"

    def _render_unbounded(self, context: PromptContext, indentation: str) -> str:
        """Render without width restriction (no wrapping)."""
        rendered_segments = []
        for seg in self.segments:
            rendered, _ = seg.render(context, line_remaining_width=10**9)
            rendered_segments.append(rendered)
        return f"{indentation}{''.join(rendered_segments)}"

    def _render_wrapped(
        self, context: PromptContext, indentation: str, max_content_width: int
    ) -> str:
        """Render with wrapping according to max_content_width."""
        lines: list[str] = []
        current_line = ""
        remaining = max_content_width

        queue = list(self.segments)
        carry_over: PromptResponseSegment | None = None

        while queue or carry_over:
            if carry_over is not None:
                rendered, remainder = carry_over.render(context, remaining)
                current_line += rendered
                remaining -= self._visible_len(rendered)
                carry_over = remainder
            else:
                seg = queue.pop(0)
                rendered, remainder = seg.render(context, remaining)
                current_line += rendered
                remaining -= self._visible_len(rendered)
                carry_over = remainder

            if remaining <= 0 or (carry_over is not None and remaining == 0):
                lines.append(f"{indentation}{current_line}")
                current_line = ""
                remaining = max_content_width
                continue

            if carry_over is None and not queue:
                lines.append(f"{indentation}{current_line}")
                current_line = ""
                remaining = max_content_width

        if current_line:
            lines.append(f"{indentation}{current_line}")

        return "\n".join(lines)

    def _visible_len(self, s: str) -> int:
        from wexample_helpers.helpers.ansi import ansi_strip

        return len(ansi_strip(s))

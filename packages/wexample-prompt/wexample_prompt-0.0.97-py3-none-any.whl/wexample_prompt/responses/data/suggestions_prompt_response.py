"""Response for displaying suggestions with optional descriptions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.const.types import LineMessage
    from wexample_prompt.enums.verbosity_level import VerbosityLevel


@base_class
class SuggestionsPromptResponse(AbstractPromptResponse):
    """Display a list of suggestions with an introductory message."""

    @classmethod
    def create_suggestions(
        cls,
        message: LineMessage,
        suggestions: list[str],
        arrow_style: str = "→",
        verbosity: VerbosityLevel | None = None,
    ) -> SuggestionsPromptResponse:
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
        from wexample_prompt.enums.terminal_color import TerminalColor
        from wexample_prompt.enums.text_style import TextStyle

        # Build lines independent of context
        lines: list[PromptResponseLine] = []
        # Top spacer
        lines.append(PromptResponseLine(segments=[PromptResponseSegment(text="")]))

        # Message lines (support multi-line)
        message_lines = PromptResponseLine.create_from_string(message)
        for ml in message_lines:
            for seg in ml.segments:
                seg.color = TerminalColor.BLUE
                if TextStyle.BOLD not in seg.styles:
                    seg.styles.append(TextStyle.BOLD)
            lines.append(ml)

        # Suggestions (each on its own line; support multi-line suggestions too)
        for suggestion in suggestions:
            for sline in PromptResponseLine.create_from_string(suggestion):
                # Prepend arrow and keep parsed segments
                arrow_segment = PromptResponseSegment(
                    text=f"  {arrow_style} ",
                    color=TerminalColor.CYAN,
                )
                # Add bold to suggestion segments if they don't have color
                for seg in sline.segments:
                    if seg.color is None and TextStyle.BOLD not in seg.styles:
                        seg.styles.append(TextStyle.BOLD)

                lines.append(
                    PromptResponseLine(segments=[arrow_segment] + sline.segments)
                )

        # Bottom spacer
        lines.append(PromptResponseLine(segments=[PromptResponseSegment(text="")]))

        return cls(
            lines=lines,
            verbosity=verbosity,
        )

    @classmethod
    def get_example_class(cls) -> type:
        from wexample_prompt.example.response.data.suggestions_example import (
            SuggestionsExample,
        )

        return SuggestionsExample

from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.messages.abstract_message_response import (
    AbstractMessageResponse,
)

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.example.abstract_response_example import (
        AbstractResponseExample,
    )


@base_class
class ErrorPromptResponse(AbstractMessageResponse):
    SYMBOL: ClassVar[str] = "❌"

    @classmethod
    def create_error(
        cls: ErrorPromptResponse,
        message: str | None = None,
        exception: BaseException | None = None,
        color: TerminalColor | None = None,
        symbol: str | None = None,
        verbosity: VerbosityLevel | None = None,
    ) -> ErrorPromptResponse:
        from wexample_helpers.helpers.error import error_format

        from wexample_prompt.enums.terminal_color import TerminalColor

        # Build content: if there's an exception, create a red header line (symbol + message)
        # and append the formatted trace as raw lines (no added color) so its own formatting stays intact.
        if exception is not None:
            from wexample_prompt.common.prompt_response_line import PromptResponseLine
            from wexample_prompt.common.prompt_response_segment import (
                PromptResponseSegment,
            )

            header_text = (
                message
                if (message is not None and message != "")
                else "An error occurred"
            )

            # First line: symbol + header in red
            # Parse header_text to support color markups like @color:magenta+bold{...}
            effective_symbol = symbol or cls.SYMBOL

            # Parse the header text to extract color/style markups
            from wexample_prompt.common.style_markup_parser import flatten_style_markup

            header_segments: list[PromptResponseSegment] = []
            if effective_symbol:
                header_segments.append(
                    PromptResponseSegment(
                        text=f"{effective_symbol} ", color=(color or TerminalColor.RED)
                    )
                )

            # Parse header text with markup support, using default color if no markup specified
            parsed_segments = flatten_style_markup(
                header_text, default_color=(color or TerminalColor.RED), joiner=None
            )
            header_segments.extend(parsed_segments)

            lines: list[PromptResponseLine] = [
                PromptResponseLine(segments=header_segments)
            ]

            # Trace lines: preserve helper formatting (may include ANSI), no extra color
            formatted = error_format(exception)
            lines.extend(PromptResponseLine.create_from_string(formatted.splitlines()))
            return cls._create(lines=lines, verbosity=verbosity)

        else:
            text = (
                message
                if (message is not None and message != "")
                else "An error occurred"
            )
            return cls._create_symbol_message(
                text=text, color=(color or TerminalColor.RED), verbosity=verbosity
            )

    @classmethod
    def get_example_class(cls) -> type[AbstractResponseExample]:
        from wexample_prompt.example.response.messages.error_example import ErrorExample

        return ErrorExample

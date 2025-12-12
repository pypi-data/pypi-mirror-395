from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.messages.abstract_message_response import (
    AbstractMessageResponse,
)

if TYPE_CHECKING:
    from wexample_prompt.const.types import LineMessage
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.example.abstract_response_example import (
        AbstractResponseExample,
    )


@base_class
class WarningPromptResponse(AbstractMessageResponse):
    """Response for warning messages."""

    SYMBOL: ClassVar[str] = "⚠"

    @classmethod
    def create_warning(
        cls: WarningPromptResponse,
        message: LineMessage,
        color: TerminalColor | None = None,
        symbol: str | None = None,
        verbosity: VerbosityLevel | None = None,
    ) -> WarningPromptResponse:
        from wexample_prompt.enums.terminal_color import TerminalColor

        return cls._create_symbol_message(
            text=message,
            color=color or TerminalColor.YELLOW,
            symbol=symbol,
            verbosity=verbosity,
        )

    @classmethod
    def get_example_class(cls) -> type[AbstractResponseExample]:
        """Get the example class for warning messages."""
        from wexample_prompt.example.response.messages.warning_example import (
            WarningExample,
        )

        return WarningExample

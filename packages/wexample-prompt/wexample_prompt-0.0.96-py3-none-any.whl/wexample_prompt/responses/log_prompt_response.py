from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.const.types import LineMessage
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.example.abstract_response_example import (
        AbstractResponseExample,
    )


@base_class
class LogPromptResponse(AbstractPromptResponse):
    """Response for log messages."""

    @classmethod
    def apply_prefix_to_kwargs(
        cls, prefix: str, args: tuple, kwargs: dict
    ) -> tuple[tuple, dict]:
        """Apply prefix to message parameter.

        Args:
            prefix: The formatted prefix to apply (e.g., "[child] ")
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Tuple of (modified_args, modified_kwargs)
        """
        # Handle message parameter
        if "message" in kwargs:
            kwargs["message"] = prefix + kwargs["message"]
        elif len(args) > 0 and isinstance(args[0], str):
            # Handle positional message argument
            args = (prefix + args[0],) + args[1:]

        return args, kwargs

    @classmethod
    def create_log(
        cls: LogPromptResponse,
        message: LineMessage,
        color: TerminalColor | None = None,
        verbosity: VerbosityLevel | None = None,
    ) -> LogPromptResponse:
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.enums.terminal_color import TerminalColor

        return cls(
            lines=PromptResponseLine.create_from_string(
                text=message, color=color or TerminalColor.WHITE
            ),
            verbosity=verbosity,
        )

    @classmethod
    def get_example_class(cls) -> type[AbstractResponseExample]:
        from wexample_prompt.example.response.log_example import LogExample

        return LogExample

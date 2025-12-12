from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.const.types import LineMessage
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.example.abstract_response_example import (
        AbstractResponseExample,
    )


@base_class
class EchoPromptResponse(AbstractPromptResponse):
    """A basic response with no style"""

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
    def create_echo(
        cls: EchoPromptResponse,
        message: LineMessage,
        verbosity: VerbosityLevel | None = None,
    ) -> EchoPromptResponse:
        from wexample_prompt.common.prompt_response_line import PromptResponseLine

        return cls(
            lines=PromptResponseLine.create_from_string(
                text=message,
            ),
            verbosity=verbosity,
        )

    @classmethod
    def get_example_class(cls) -> type[AbstractResponseExample]:
        from wexample_prompt.example.response.echo_example import EchoExample

        return EchoExample

    def render(self, context: PromptContext | None = None) -> str | None:
        from wexample_prompt.common.prompt_context import PromptContext

        context = PromptContext.create_if_none(context=context)
        context.colorized = False

        return super().render(
            context=context,
        )

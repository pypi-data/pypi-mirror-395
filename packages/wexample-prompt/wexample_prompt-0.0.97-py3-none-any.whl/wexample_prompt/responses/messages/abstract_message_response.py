from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.const.types import LineMessage
    from wexample_prompt.enums.terminal_color import TerminalColor


@base_class
class AbstractMessageResponse(AbstractPromptResponse):
    # Symbol to display before the message, override in subclasses
    SYMBOL: ClassVar[str] = ""

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
        # Determine the effective symbol (explicit symbol in kwargs > class default)
        effective_symbol = kwargs.get("symbol", cls.SYMBOL)

        # Build the final prefix: prefix + symbol (if any) + space
        final_prefix = prefix
        if effective_symbol:
            final_prefix = f"{prefix}{effective_symbol} "
            # Remove the symbol from kwargs so it won't be added again in _create_symbol_message
            kwargs["symbol"] = ""

        # Handle message parameter
        if "message" in kwargs:
            kwargs["message"] = final_prefix + kwargs["message"]
        elif len(args) > 0 and isinstance(args[0], str):
            # Handle positional message argument
            args = (final_prefix + args[0],) + args[1:]

        return args, kwargs

    @classmethod
    def _create_symbol_message(
        cls,
        text: LineMessage,
        color: TerminalColor,
        symbol: str | None = None,
        **kwargs,
    ) -> AbstractMessageResponse:
        """Create a message with a symbol"""
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment

        # Determine effective symbol (explicit > class default)
        effective_symbol = symbol if symbol is not None else cls.SYMBOL

        # Build lines from message handling multi-line inputs like PromptResponseLine.create_from_string
        raw_lines = PromptResponseLine.create_from_string(text=text, color=color)

        # Prepend symbol (if any) to the first line only
        if effective_symbol and raw_lines:
            first = raw_lines[0]
            first.segments.insert(
                0, PromptResponseSegment(text=f"{effective_symbol} ", color=color)
            )

        return cls._create(lines=raw_lines, **kwargs)

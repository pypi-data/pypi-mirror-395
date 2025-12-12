from __future__ import annotations

from typing import TYPE_CHECKING

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
class ListPromptResponse(AbstractMessageResponse):
    """Display items as a bulleted list, supporting nested indentation via leading spaces."""

    @classmethod
    def apply_prefix_to_kwargs(
        cls, prefix: str, args: tuple, kwargs: dict
    ) -> tuple[tuple, dict]:
        """Apply prefix to items parameter.

        Args:
            prefix: The formatted prefix to apply (e.g., "[child] ")
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Tuple of (modified_args, modified_kwargs)
        """
        # Handle items parameter
        if "items" in kwargs and isinstance(kwargs["items"], list):
            kwargs["items"] = [
                prefix + item if isinstance(item, str) else item
                for item in kwargs["items"]
            ]

        return args, kwargs

    @classmethod
    def create_list(
        cls,
        items: list[str],
        bullet: str = "•",
        color: TerminalColor | None = None,
        verbosity: VerbosityLevel | None = None,
    ) -> ListPromptResponse:
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment

        lines: list[PromptResponseLine] = []

        for item in items:
            # Determine indentation level by counting leading double-spaces
            indent_level = 0
            content = item
            while content.startswith("  "):
                indent_level += 1
                content = content[2:]

            # If the content already starts with the bullet, strip it
            if content.startswith(f"{bullet} "):
                content = content[len(bullet) + 1 :]

            bullet_text = ("  " * indent_level) + f"{bullet} "

            bullet_segment = PromptResponseSegment(text=bullet_text, color=color)

            # Parse content for inline formatting (@color, @path, @time, etc.)
            from wexample_prompt.common.style_markup_parser import flatten_style_markup

            content_segments = flatten_style_markup(
                content, default_color=color, joiner=None
            )

            # Combine bullet with parsed content segments
            all_segments = [bullet_segment] + content_segments
            lines.append(PromptResponseLine(segments=all_segments))

        return cls(lines=lines, verbosity=verbosity)

    @classmethod
    def get_example_class(cls) -> type[AbstractResponseExample]:
        from wexample_prompt.example.response.data.list_example import ListExample

        return ListExample

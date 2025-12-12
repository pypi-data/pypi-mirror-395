from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.responses.messages.abstract_message_response import (
    AbstractMessageResponse,
)

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.enums.verbosity_level import VerbosityLevel


@base_class
class AbstractTitleResponse(AbstractMessageResponse):
    """Base class for title-like responses that render:
    "❯ <text> ⫻⫻⫻⫻⫻⫻⫻⫻⫻⫻" with configurable fill character and width.
    """

    DEFAULT_PREFIX: ClassVar[str] = "❯"
    DEFAULT_CHARACTER: ClassVar[str] = "⫻"

    @classmethod
    def apply_prefix_to_kwargs(
        cls, prefix: str, args: tuple, kwargs: dict
    ) -> tuple[tuple, dict]:
        """Apply prefix before the DEFAULT_PREFIX symbol for title responses.

        For titles, we want: [prefix] ❯ text
        Not: ❯ [prefix] text

        Args:
            prefix: The formatted prefix to apply (e.g., "[child] ")
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Tuple of (modified_args, modified_kwargs)
        """
        # Store the prefix in kwargs so it can be prepended to DEFAULT_PREFIX during creation
        kwargs["_context_prefix"] = prefix

        return args, kwargs

    character: str | None = public_field(
        default=DEFAULT_CHARACTER,
        description="Character used to fill the remaining line",
    )
    fill_segment: PromptResponseSegment = public_field(
        description="The trailing fill characters segment"
    )
    prefix_segment: PromptResponseSegment = public_field(
        description="The prefix segment displayed before the title text"
    )
    text_segment: PromptResponseSegment = public_field(
        description="The title text segment"
    )
    width: int | None = public_field(
        default=None, description="Optional fixed width; if not set uses context width"
    )

    @classmethod
    def _create_title(
        cls,
        text: str,
        color: TerminalColor | None = None,
        character: str | None = None,
        width: int | None = None,
        verbosity: VerbosityLevel = None,
        **kwargs,
    ) -> AbstractTitleResponse:
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment

        # Extract context prefix if provided (added by apply_prefix_to_kwargs)
        _context_prefix = kwargs.pop("_context_prefix", None)

        # Prepend context prefix if provided (e.g., "[child] ❯ " instead of "❯ ")
        prefix_text = (
            f"{_context_prefix}{cls.DEFAULT_PREFIX} "
            if _context_prefix
            else f"{cls.DEFAULT_PREFIX} "
        )

        prefix = PromptResponseSegment(
            text=prefix_text,
            color=color,
        )

        # Parse text to support color markups like @color:cyan+bold{...}
        from wexample_prompt.common.style_markup_parser import flatten_style_markup

        # Parse the text with markup support, using default color if no markup specified
        text_segments = flatten_style_markup(
            f"{text} ", default_color=color, joiner=None  # Add trailing space as before
        )

        # For backward compatibility, store the first text segment as text_segment
        # (used for width calculation in render)
        text_seg = (
            text_segments[0]
            if text_segments
            else PromptResponseSegment(
                text=f"{text} ",
                color=color,
            )
        )

        fill = PromptResponseSegment(
            text="",
            color=color,
        )

        # Build segments list: prefix + parsed text segments + fill
        segments = [prefix] + text_segments + [fill]

        return cls(
            prefix_segment=prefix,
            text_segment=text_seg,
            fill_segment=fill,
            width=width,
            character=character or cls.DEFAULT_CHARACTER,
            lines=[PromptResponseLine(segments=segments)],
            verbosity=verbosity,
        )

    def render(self, context: PromptContext | None = None) -> str | None:
        from wexample_prompt.common.prompt_context import PromptContext
        from wexample_prompt.helper.terminal import terminal_get_visible_width

        context = PromptContext.create_if_none(context=context)

        # Prefer provided context, else defer to super to resolve any defaulting
        width = self.width or context.get_width()
        # Compute remaining space after prefix + text and indentation
        remaining = context.get_available_width(width, minimum=0)

        # Calculate width of all segments except fill
        # (prefix + all text segments, which may be multiple if markup was parsed)
        for segment in self.lines[0].segments:
            if segment is not self.fill_segment:
                remaining -= terminal_get_visible_width(segment.text)

        target_width = max(0, remaining)
        fill_pattern = self.character or self.DEFAULT_CHARACTER
        if target_width:
            pattern_width = terminal_get_visible_width(fill_pattern)
            if pattern_width <= 0:
                fill_pattern = self.DEFAULT_CHARACTER
                pattern_width = terminal_get_visible_width(fill_pattern) or 1

            repeats = target_width // pattern_width if pattern_width else 0
            fill_text = fill_pattern * repeats
            visible = repeats * pattern_width

            if visible < target_width:
                fill_text += " " * (target_width - visible)
        else:
            fill_text = ""

        self.fill_segment.text = fill_text

        return super().render(context=context)

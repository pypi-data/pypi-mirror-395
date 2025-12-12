from __future__ import annotations

from typing import TYPE_CHECKING, ClassVar

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
from wexample_prompt.common.style_markup_parser import flatten_style_markup
from wexample_prompt.responses.messages.abstract_message_response import (
    AbstractMessageResponse,
)

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.example.abstract_response_example import (
        AbstractResponseExample,
    )


@base_class
class SeparatorPromptResponse(AbstractMessageResponse):
    """Response for log messages."""

    DEFAULT_CHARACTER: ClassVar[str] = "-"
    character: str | None = public_field(
        default=DEFAULT_CHARACTER, description="The character to repeat"
    )
    label: str | None = public_field(
        default=None, description="A label to display on the separator right"
    )
    label_segments: list[PromptResponseSegment] = public_field(
        factory=list,
        description="Segments used to render the optional label.",
    )
    separator_response_segment: PromptResponseSegment | None = public_field(
        default=None,
        description="The line segment used by render process",
    )
    width: int | None = public_field(
        default=None, description="A fixed width, use context width if not provided"
    )

    def __attrs_post_init__(self) -> None:
        parent = super()
        if hasattr(parent, "__attrs_post_init__"):
            parent.__attrs_post_init__()

        if not self.separator_response_segment:
            from wexample_prompt.common.prompt_response_segment import (
                PromptResponseSegment,
            )

            character = self.character or self.DEFAULT_CHARACTER
            self.separator_response_segment = PromptResponseSegment(text=character)

        if not self.lines:
            from wexample_prompt.common.prompt_response_line import PromptResponseLine

            self.lines = [
                PromptResponseLine(segments=[self.separator_response_segment])
            ]
        else:
            first_line = self.lines[0]
            if self.separator_response_segment not in first_line.segments:
                first_line.segments.insert(0, self.separator_response_segment)

    @classmethod
    def create_separator(
        cls: SeparatorPromptResponse,
        label: str | None = None,
        width: int | None = None,
        color: TerminalColor | None = None,
        character: str | None = None,
        verbosity: VerbosityLevel | None = None,
    ) -> SeparatorPromptResponse:
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment

        segments: list[PromptResponseSegment] = []

        separator_response_segment = PromptResponseSegment(text="-", color=color)
        segments.append(separator_response_segment)

        label_segments: list[PromptResponseSegment] = []
        if label:
            label_segments = flatten_style_markup(
                label, default_color=color, joiner=" "
            )
            # Prepend spacing before label
            label_segments.insert(0, PromptResponseSegment(text=" ", color=color))
            segments.extend(label_segments)

        return cls(
            separator_response_segment=separator_response_segment,
            label_segments=label_segments,
            label=label,
            width=width,
            character=character or SeparatorPromptResponse.DEFAULT_CHARACTER,
            lines=[PromptResponseLine(segments=segments)],
            verbosity=verbosity,
        )

    @classmethod
    def get_example_class(cls) -> type[AbstractResponseExample]:
        from wexample_prompt.example.response.titles.separator_example import (
            SeparatorExample,
        )

        return SeparatorExample

    def render(self, context: PromptContext | None = None) -> str | None:
        from wexample_helpers.helpers.ansi import ansi_strip

        from wexample_prompt.helper.terminal import terminal_get_visible_width

        width = self.width or context.get_width()
        length = context.get_available_width(width, minimum=0)
        if self.label_segments:
            length -= sum(
                terminal_get_visible_width(ansi_strip(seg.text))
                for seg in self.label_segments
            )

        separator_segment = self.separator_response_segment
        if separator_segment is None:
            from wexample_prompt.common.prompt_response_segment import (
                PromptResponseSegment,
            )

            separator_segment = PromptResponseSegment(
                text="", color=getattr(self, "color", None)
            )
            self.separator_response_segment = separator_segment
            if self.lines:
                self.lines[0].segments.insert(0, separator_segment)
        character = self.character or self.DEFAULT_CHARACTER
        separator_segment.text = length * character

        return super().render(
            context=context,
        )

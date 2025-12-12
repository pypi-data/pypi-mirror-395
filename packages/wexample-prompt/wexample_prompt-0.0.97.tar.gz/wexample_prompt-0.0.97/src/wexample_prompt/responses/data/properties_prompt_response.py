from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.common.prompt_response_line import PromptResponseLine
    from wexample_prompt.enums.verbosity_level import VerbosityLevel


@base_class
class PropertiesPromptResponse(AbstractPromptResponse):
    """Render a dictionary of properties as a formatted block, with optional title.

    The visual width adapts to the provided render context. Lines are generated during
    render, so the response remains context-agnostic until displayed.
    """

    nested_indent: int = public_field(
        default=2,
        description="Indentation inside the properties list, when rendering sub list of items",
    )
    properties: dict[str, Any] = public_field(
        factory=dict, description="The list of properties to display"
    )
    title: str | None = public_field(
        default=None, description="The title of the properties list"
    )

    @classmethod
    def create_properties(
        cls,
        properties: dict[str, Any],
        title: str | None = None,
        nested_indent: int = 2,
        verbosity: VerbosityLevel | None = None,
    ) -> PropertiesPromptResponse:
        return cls(
            lines=[],  # Lines will be built in render() because we neet context with to create them.
            properties=properties,
            title=title,
            nested_indent=nested_indent,
            verbosity=verbosity,
        )

    @classmethod
    def get_example_class(cls) -> type:
        from wexample_prompt.example.response.data.properties_example import (
            PropertiesExample,
        )

        return PropertiesExample

    @staticmethod
    def _create_border_line(width: int) -> PromptResponseLine:
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment

        return PromptResponseLine(
            segments=[PromptResponseSegment(text=f"{'-' * width}")]
        )

    @staticmethod
    def _format_properties(
        properties: dict[str, Any],
        key_width: int,
        indent: int,
        current_indent: int = 0,
    ) -> list[str]:
        lines: list[str] = []
        indent_str = " " * current_indent
        for key, value in properties.items():
            if isinstance(value, dict):
                lines.append(f"{indent_str}{str(key)}:")
                lines.extend(
                    PropertiesPromptResponse._format_properties(
                        value, key_width, indent, current_indent + indent
                    )
                )
            else:
                key_str = str(key).ljust(key_width)
                lines.append(f"{indent_str}{key_str} : {str(value)}")
        return lines

    def render(self, context: PromptContext | None = None) -> str | None:
        """Render the properties into lines using the provided context width."""
        from wexample_prompt.common.prompt_context import PromptContext
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment

        if not self.properties:
            return ""

        context = PromptContext.create_if_none(context=context)

        # Determine content width by aligning with available visible width (indent-aware)
        indentation_visible_width = context.get_indentation_visible_width()
        total_width = context.get_width()
        content_width = max(10, total_width - indentation_visible_width)

        max_key_width = 0

        def scan_keys(obj: dict[str, Any]) -> None:
            nonlocal max_key_width
            for k, v in obj.items():
                max_key_width = max(max_key_width, len(str(k)))
                if isinstance(v, dict):
                    scan_keys(v)

        scan_keys(self.properties)

        content_lines = self._format_properties(
            self.properties, max_key_width, self.nested_indent
        )

        # Maintain a leading spacer line so the block visually separates like other responses.
        lines: list[PromptResponseLine] = [
            PromptResponseLine(segments=[PromptResponseSegment(text="")])
        ]

        if self.title:
            title_len = len(self.title)
            left_pad = max(0, (content_width - title_len) // 2)
            right_pad = max(0, content_width - title_len - left_pad)
            lines.append(
                PromptResponseLine(
                    segments=[
                        PromptResponseSegment(text="-" * left_pad),
                        PromptResponseSegment(text=f" {self.title} "),
                        PromptResponseSegment(text="-" * max(0, right_pad - 2)),
                    ]
                )
            )
        else:
            lines.append(self._create_border_line(content_width))

        for content in content_lines:
            # Parse content for inline formatting
            from wexample_prompt.common.style_markup_parser import flatten_style_markup

            content_segments = flatten_style_markup(content, joiner=None)

            # Add leading space and parsed content
            all_segments = [PromptResponseSegment(text=" ")] + content_segments
            lines.append(PromptResponseLine(segments=all_segments))

        lines.append(self._create_border_line(content_width))

        # Replace and delegate to base to apply verbosity and segment rendering
        self.lines = lines
        return super().render(context=context)

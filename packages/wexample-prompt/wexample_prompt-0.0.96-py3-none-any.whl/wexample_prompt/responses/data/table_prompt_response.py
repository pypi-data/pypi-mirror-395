"""Table response for displaying data in a formatted table layout."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.common.prompt_response_line import PromptResponseLine
    from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
    from wexample_prompt.enums.verbosity_level import VerbosityLevel


@base_class
class TablePromptResponse(AbstractPromptResponse):
    """Response for displaying data in a table layout with borders and formatting."""

    data: list[list[Any]] = public_field(
        description="Table body rows: list of rows, each row a list of cell values"
    )
    headers: list[str] | None = public_field(
        default=None, description="Optional list of column headers"
    )
    title: str | None = public_field(default=None, description="Optional table title")

    @classmethod
    def create_table(
        cls,
        data: list[list[Any]],
        headers: list[str] | None = None,
        title: str | None = None,
        verbosity: VerbosityLevel | None = None,
    ) -> TablePromptResponse:
        return cls(
            lines=[], data=data, headers=headers, title=title, verbosity=verbosity
        )

    @classmethod
    def get_example_class(cls) -> type:
        from wexample_prompt.example.response.data.table_example import TableExample

        return TableExample

    @staticmethod
    def _calculate_max_widths(rows: list[list[Any]]) -> list[int]:
        if not rows:
            return []
        num_columns = max(len(row) for row in rows)
        max_widths = [0] * num_columns
        for row in rows:
            for i in range(num_columns):
                cell = str(row[i]) if i < len(row) else ""
                # Use visible width instead of len()
                visible_width = TablePromptResponse._get_visible_width(cell)
                max_widths[i] = max(max_widths[i], visible_width)
        return max_widths

    @staticmethod
    def _create_border_line(width: int) -> PromptResponseLine:
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment

        return PromptResponseLine(
            segments=[PromptResponseSegment(text="+" + "-" * width + "+")]
        )

    @staticmethod
    def _format_row(row: list[Any], widths: list[int]) -> list[PromptResponseSegment]:
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment
        from wexample_prompt.common.style_markup_parser import flatten_style_markup

        segments = [PromptResponseSegment(text="|")]
        for i in range(len(widths)):
            cell = str(row[i]) if i < len(row) else ""

            # Parse cell content for inline formatting
            cell_segments = flatten_style_markup(cell, joiner=None)

            # Calculate actual text length (without markup and ANSI codes)
            cell_text_length = sum(
                len(TablePromptResponse._strip_ansi(seg.text)) for seg in cell_segments
            )
            padding = max(0, widths[i] - cell_text_length)

            # Add leading space
            segments.append(PromptResponseSegment(text=" "))
            # Add parsed cell content
            segments.extend(cell_segments)
            # Add padding and closing pipe
            segments.append(PromptResponseSegment(text=" " * padding + " |"))

        return segments

    @staticmethod
    def _get_visible_width(text: str) -> int:
        """Get visible width of text, excluding ANSI escape sequences and markup."""
        from wexample_prompt.common.style_markup_parser import flatten_style_markup
        from wexample_prompt.helper.terminal import terminal_get_visible_width

        # Parse markup to get segments
        segments = flatten_style_markup(text, joiner=None)
        # Strip ANSI codes from each segment and sum visible widths (using wcwidth)
        total_width = 0
        for seg in segments:
            clean_text = TablePromptResponse._strip_ansi(seg.text)
            total_width += terminal_get_visible_width(clean_text)
        return total_width

    @staticmethod
    def _strip_ansi(text: str) -> str:
        """Strip ANSI escape sequences from text."""
        import re

        # Remove ANSI escape sequences (including hyperlinks)
        ansi_escape = re.compile(r"\x1b\[[0-9;]*m|\x1b\]8;;[^\x1b]*\x1b\\")
        return ansi_escape.sub("", text)

    def render(self, context: PromptContext | None = None) -> str | None:
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment

        if not self.data and not self.headers:
            return ""

        all_rows: list[list[Any]] = []
        if self.headers:
            all_rows.append(self.headers)
        all_rows.extend(self.data)

        max_widths = self._calculate_max_widths(all_rows)
        total_width = sum(max_widths) + (len(max_widths) * 3) - 1

        # Ensure total_width is at least as wide as the title
        if self.title:
            min_width_for_title = len(self.title) + 4  # +4 for "+ " and " +"
            if total_width < min_width_for_title:
                # Distribute extra space across columns
                extra_space = min_width_for_title - total_width
                space_per_column = extra_space // len(max_widths)
                remainder = extra_space % len(max_widths)

                for i in range(len(max_widths)):
                    max_widths[i] += space_per_column
                    if i < remainder:
                        max_widths[i] += 1

                total_width = sum(max_widths) + (len(max_widths) * 3) - 1

        lines: list[PromptResponseLine] = []
        lines.append(PromptResponseLine(segments=[PromptResponseSegment(text="")]))

        if self.title:
            title_padding = max(0, (total_width - len(self.title)) // 2)
            title_line = PromptResponseLine(
                segments=[
                    PromptResponseSegment(text="+" + "-" * title_padding),
                    PromptResponseSegment(text=f" {self.title} "),
                    PromptResponseSegment(
                        text="-" * (total_width - title_padding - len(self.title) - 2)
                        + "+"
                    ),
                ]
            )
            lines.append(title_line)
        else:
            lines.append(self._create_border_line(total_width))

        if self.headers:
            header_segments = self._format_row(self.headers, max_widths)
            lines.append(PromptResponseLine(segments=header_segments))
            lines.append(self._create_border_line(total_width))

        for row in self.data:
            row_segments = self._format_row(row, max_widths)
            lines.append(PromptResponseLine(segments=row_segments))

        lines.append(self._create_border_line(total_width))
        lines.append(PromptResponseLine(segments=[PromptResponseSegment(text="")]))

        self.lines = lines
        return super().render(context=context)

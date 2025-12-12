"""Abstract base class for interactive prompt responses."""

from __future__ import annotations

from typing import Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse


@base_class
class AbstractInteractivePromptResponse(AbstractPromptResponse):
    """Base for interactive responses with common terminal helpers."""

    reset_on_finish: bool = public_field(
        default=False,
        description="If True, clears the prompt block from the terminal after a selection or abort.",
    )
    _answer: Any = None

    @staticmethod
    def _partial_clear(printed_lines: int) -> None:
        if printed_lines > 0:
            print(f"\033[{printed_lines}F\033[J", end="", flush=True)

    @staticmethod
    def _read_key() -> str:
        import readchar

        return readchar.readkey()

    def get_answer(self) -> Any:
        return self._answer

    def _print_render(self, context) -> int:
        """Render the content and return the number of terminal rows consumed.

        Counts visual rows by considering terminal width and visible text width
        (ANSI stripped). This ensures _partial_clear erases the correct height
        even when lines wrap.
        """
        import shutil

        from wexample_helpers.helpers.ansi import ansi_display_width

        rendered = super().render(context=context)
        if rendered is None:
            return 0
        print(rendered, flush=True)

        # Determine columns from context or fallback to terminal/env
        try:
            cols = (
                int(getattr(context, "get_width", lambda: 0)())
                or shutil.get_terminal_size().columns
            )
        except Exception:
            cols = 80
        cols = max(1, cols)

        rows = 0
        for line in rendered.split("\n"):
            width = ansi_display_width(line)
            if width <= 0:
                rows += 1
            else:
                rows += (width + cols - 1) // cols  # ceil(width/cols)
        return rows

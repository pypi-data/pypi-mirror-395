from __future__ import annotations

import shutil
import sys
from typing import TYPE_CHECKING, Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.output.abstract_prompt_output_handler import (
    AbstractPromptOutputHandler,
)

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )


@base_class
class PromptStdoutOutputHandler(AbstractPromptOutputHandler):
    def erase(
        self,
        response: AbstractPromptResponse,
    ) -> Any:
        sys.stdout.write(self._render_erase(response))
        sys.stdout.flush()

    def print(
        self,
        response: AbstractPromptResponse,
        context: PromptContext | None = None,
    ) -> Any:
        rendered_response = response.render(context=context)
        if rendered_response:
            # Equivalent of print
            # Use stdout directly for consistency with erase()
            sys.stdout.write(rendered_response + "\n")
            sys.stdout.flush()

        return rendered_response

    def _render_erase(self, response: AbstractPromptResponse) -> str:
        from wexample_helpers.helpers.ansi import ansi_display_width

        content = response.rendered_content
        if not content:
            return ""

        # Compute how many visual rows were used, accounting for wrapping.
        cols = max(1, shutil.get_terminal_size(fallback=(80, 24)).columns)
        lines = content.split("\n")

        total_rows = 0
        for line in lines:
            w = ansi_display_width(line)
            rows = max(1, (w + cols - 1) // cols)
            total_rows += rows

        parts: list[str] = []
        # Move cursor up from the trailing newline printed by print().
        parts.append("\x1b[F")
        for i in range(total_rows):
            parts.append("\r\x1b[2K")  # Clear entire line
            if i < total_rows - 1:
                parts.append("\x1b[1A")  # Move up one visual row

        parts.append("\r")
        return "".join(parts)

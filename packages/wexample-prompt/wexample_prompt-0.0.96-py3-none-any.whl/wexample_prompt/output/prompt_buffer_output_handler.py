from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.private_field import private_field
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
class PromptBufferOutputHandler(AbstractPromptOutputHandler):
    """Output handler that buffers responses instead of writing to stdout.

    - Stores the original response objects in `buffer` (preserving legacy behavior).
    - Returns the rendered string (aligned with current handlers like PromptStdoutOutputHandler).
    """

    _buffer_rendered: list[str | None] = private_field(
        factory=list,
        description="Rendered strings for buffered responses (None if not rendered).",
    )
    _buffer_responses: list[AbstractPromptResponse] = private_field(
        factory=list,
        description="Original response objects buffered in order.",
    )

    @property
    def rendered(self) -> list[str | None]:
        return self._buffer_rendered

    @property
    def rendered_str(self) -> str:
        return "".join([str(s) for s in self._buffer_rendered])

    @property
    def responses(self) -> list[AbstractPromptResponse]:
        return self._buffer_responses

    def append_rendered(self, text: str) -> None:
        self._buffer_rendered.append(text)

    def clear(self) -> None:
        self._buffer_responses = []
        self._buffer_rendered = []

    def erase(
        self,
        response: AbstractPromptResponse,
    ) -> Any:
        pass

    def flush(self) -> list[str | None]:
        rendered = self.rendered
        self.clear()
        return rendered

    def print(
        self,
        response: AbstractPromptResponse,
        context: PromptContext | None = None,
    ) -> Any:
        # Preserve legacy: store the response object
        self._buffer_responses.append(response)

        # Align with new API: return the rendered output
        rendered_response = response.render(context=context)
        if rendered_response is not None:
            self.append_rendered(rendered_response)

        return rendered_response

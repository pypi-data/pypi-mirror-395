from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.mixins.with_io_methods import WithIoMethods
from wexample_prompt.responses.interactive.abstract_interactive_prompt_response import (
    AbstractInteractivePromptResponse,
)

if TYPE_CHECKING:
    from collections.abc import Callable

    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.example.abstract_response_example import (
        AbstractResponseExample,
    )
    from wexample_prompt.output.prompt_buffer_output_handler import (
        PromptBufferOutputHandler,
    )


@base_class
class ScreenPromptResponse(WithIoMethods, AbstractInteractivePromptResponse):
    """A simple screen-like interactive response that repeatedly invokes a user-provided
    callback, allowing the callback to draw text lines, sleep, and request reload/close.
    """

    callback: Callable[[ScreenPromptResponse], Any] = public_field(
        description="Function called repeatedly with this response instance to draw and control flow.",
    )
    height: int = public_field(
        default=30,
        description="Approx height in lines reserved for this response block.",
    )
    reset_on_finish: bool = public_field(
        default=False,
        description="If True, clears printed block when finishing (close).",
    )
    _closed: bool = False
    _io_buffer: PromptBufferOutputHandler | None = None
    _reload_requested: bool = False

    @classmethod
    def create_screen(
        cls,
        callback: Callable[[ScreenPromptResponse], Any],
        *,
        height: int = 30,
        reset_on_finish: bool = False,
        verbosity: VerbosityLevel | None = None,
    ) -> ScreenPromptResponse:
        return cls(
            callback=callback,
            height=height,
            reset_on_finish=reset_on_finish,
            verbosity=verbosity,
        )

    @classmethod
    def get_example_class(cls) -> type[AbstractResponseExample]:
        from wexample_prompt.example.response.interactive.screen_example import (
            ScreenExample,
        )

        return ScreenExample

    # Drawing helpers for the callback
    def clear(self) -> None:
        self.lines = []

    def close(self) -> None:
        self._closed = True

    def print(self, text: str) -> None:
        self._io_buffer.append_rendered(str(text))

    def reload(self) -> None:
        self._reload_requested = True

    def render(self, context: PromptContext | None = None) -> str | None:
        from time import sleep

        from wexample_prompt.common.io_manager import IoManager
        from wexample_prompt.common.prompt_context import PromptContext
        from wexample_prompt.output.prompt_buffer_output_handler import (
            PromptBufferOutputHandler,
        )

        # Wait first rendering to build nested io manager.
        if self._io_buffer is None:
            self._io_buffer = PromptBufferOutputHandler()
            self.io = IoManager(output=self._io_buffer)

        context = PromptContext.create_if_none(context=context)

        printed_lines = 0
        # First frame: let the callback populate content
        try:
            self._reload_requested = False
            self.callback(self)
            self._render_buffer()
        except Exception as e:
            # If callback errors, close gracefully
            self._closed = True
            raise e

        while True:
            # Clear previous frame area
            self._partial_clear(printed_lines)
            self._io_buffer.clear()

            # Render and print current lines
            printed_lines = self._print_render(context=context)

            if self._closed:
                if self.reset_on_finish and printed_lines > 0:
                    self._partial_clear(printed_lines)
                return None

            # Prepare next frame
            self._reload_requested = False
            try:
                self.callback(self)
            except Exception as e:
                self._closed = True
                raise e

            # If callback didn't request reload and not closed, avoid busy loop
            if not self._reload_requested and not self._closed:
                sleep(0.05)

            self._render_buffer()

    def _render_buffer(self) -> None:
        from wexample_prompt.common.prompt_response_line import PromptResponseLine

        # Consume buffered output as a single string, split into lines
        rendered = self._io_buffer.flush()
        # Normalize to lines
        for raw_line in rendered:
            if raw_line is None:
                continue
            for line in PromptResponseLine.create_from_string(raw_line):
                self.lines.append(line)

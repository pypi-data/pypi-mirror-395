"""Mixin for managing file picker prompt responses."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.choice import FilePickerMode
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.const.types import LineMessage
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.responses.interactive.file_picker_prompt_response import (
        FilePickerPromptResponse,
    )


class FilePickerPromptResponseManagerMixin:
    """Mixin class for managing file picker prompt responses."""

    def file_picker(
        self: IoManager,
        question: LineMessage = "Select a file:",
        base_dir: str | None = None,
        abort: bool | str | None = None,
        mode: FilePickerMode = FilePickerMode.BOTH,
        allow_parent_selection: bool = False,
        verbosity: VerbosityLevel | None = None,
        reset_on_finish: bool = False,
        context: PromptContext | None = None,
        predefined_answer: Any = None,
        **kwargs: Kwargs,
    ) -> FilePickerPromptResponse:
        from wexample_prompt.responses.interactive.file_picker_prompt_response import (
            FilePickerPromptResponse,
        )

        response = FilePickerPromptResponse.create_file_picker(
            question=question,
            base_dir=base_dir,
            abort=abort,
            mode=mode,
            verbosity=(
                verbosity if verbosity is not None else self.default_response_verbosity
            ),
            allow_parent_selection=allow_parent_selection,
            reset_on_finish=reset_on_finish,
            predefined_answer=predefined_answer,
        )

        return self.print_response(
            response=response,
            context=FilePickerPromptResponse.rebuild_context_for_kwargs(
                context=context, parent_kwargs=kwargs
            ),
        )

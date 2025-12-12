"""Response for displaying and handling file picker prompts."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.enums.choice import FilePickerMode
from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.interactive.choice_prompt_response import (
    ChoicePromptResponse,
)

if TYPE_CHECKING:
    from wexample_prompt.const.types import LineMessage
    from wexample_prompt.enums.verbosity_level import VerbosityLevel


@base_class
class FilePickerPromptResponse(ChoicePromptResponse):
    """Response for displaying a file picker interface."""

    abort_option: bool | str | None = public_field(
        default=None,
        description="Abort configuration forwarded to inner ChoicePromptResponse (bool or custom label).",
    )
    allow_parent_selection: bool = public_field(
        default=False,
        description="If True, include '..' as a selectable entry at the top; otherwise hide it.",
    )
    base_dir: str = public_field(
        description="Base directory to browse from; defaults to current working directory if not provided"
    )
    mode: FilePickerMode = public_field(
        default=FilePickerMode.BOTH,
        description="Filter entries: files, dirs, or both (default). Affects visibility, not just selection.",
    )

    @classmethod
    def create_file_picker(
        cls,
        base_dir: str | None = None,
        question: LineMessage = "Select a file:",
        abort: bool | str | None = None,
        mode: FilePickerMode = FilePickerMode.BOTH,
        allow_parent_selection: bool = False,
        reset_on_finish: bool = False,
        predefined_answer: Any = None,
        verbosity: VerbosityLevel | None = None,
    ) -> FilePickerPromptResponse:
        base = base_dir or os.getcwd()

        # Build mapping with ".." first, then folders (with icon), then files
        dirs: dict[str, str] = {}
        files: dict[str, str] = {}
        try:
            for element in os.listdir(base):
                full_path = os.path.join(base, element)
                if os.path.isdir(full_path):
                    if mode in (FilePickerMode.BOTH, FilePickerMode.DIRS):
                        dirs[element] = f"📁 {element}"
                else:
                    if mode in (FilePickerMode.BOTH, FilePickerMode.FILES):
                        files[element] = element
        except Exception:
            pass

        merged: dict[str, str] = {}
        if allow_parent_selection:
            merged[".."] = ".."
        for name in sorted(dirs.keys(), key=str.casefold):
            merged[name] = dirs[name]
        for name in sorted(files.keys(), key=str.casefold):
            merged[name] = files[name]

        # Build parent Choice response using mapping (key=value, value=title)
        parent_response = ChoicePromptResponse.create_choice(
            question=question,
            choices=merged,
            default=None,
            abort=abort,
            verbosity=verbosity,
            reset_on_finish=reset_on_finish,
            predefined_answer=predefined_answer,
        )

        return cls(
            # Do not copy lines; ChoicePromptResponse.ask rebuilds lines each frame
            choices=parent_response.choices,
            default=parent_response.default,
            inquirer_kwargs=parent_response.inquirer_kwargs,
            question=parent_response.question,
            question_lines=parent_response.question_lines,
            base_dir=base,
            mode=mode,
            abort_option=abort,
            verbosity=verbosity,
            reset_on_finish=reset_on_finish,
            predefined_answer=predefined_answer,
        )

    @classmethod
    def get_example_class(cls) -> type:
        from wexample_prompt.example.response.interactive.file_picker_example import (
            FilePickerExample,
        )

        return FilePickerExample

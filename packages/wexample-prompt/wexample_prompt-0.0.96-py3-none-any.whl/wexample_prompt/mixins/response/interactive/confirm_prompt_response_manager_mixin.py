"""Mixin for managing confirmation dialogs."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.const.types import LineMessage
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.responses.interactive.confirm_prompt_response import (
        ConfirmPromptResponse,
    )


class ConfirmPromptResponseManagerMixin:
    """Mixin class for managing confirmation dialog prompt responses."""

    def confirm(
        self: IoManager,
        question: LineMessage = "Please confirm:",
        choices: dict[str, tuple] | None = None,
        default: str | None = None,
        width: int | None = None,
        verbosity: VerbosityLevel | None = None,
        reset_on_finish: bool = False,
        context: PromptContext | None = None,
        predefined_answer: Any = None,
        **kwargs: Any,
    ) -> ConfirmPromptResponse:
        from wexample_prompt.responses.interactive.confirm_prompt_response import (
            ConfirmPromptResponse,
        )

        response = ConfirmPromptResponse.create_confirm(
            question=question,
            choices=choices,
            default=default,
            width=width,
            verbosity=(
                verbosity if verbosity is not None else self.default_response_verbosity
            ),
            reset_on_finish=reset_on_finish,
            predefined_answer=predefined_answer,
        )

        return self.print_response(
            response=response,
            context=ConfirmPromptResponse.rebuild_context_for_kwargs(
                context=context, parent_kwargs=kwargs
            ),
        )

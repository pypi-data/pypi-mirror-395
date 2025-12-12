"""Mixin for handling interactive screen response in IoManager."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from collections.abc import Callable

    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.responses.interactive.screen_prompt_response import (
        ScreenPromptResponse,
    )


class ScreenPromptResponseManagerMixin:
    def screen(
        self: IoManager,
        *,
        callback: Callable[[ScreenPromptResponse], Any],
        height: int = 30,
        verbosity: VerbosityLevel | None = None,
        reset_on_finish: bool = False,
        context: PromptContext | None = None,
        **kwargs: Kwargs,
    ) -> ScreenPromptResponse:
        from wexample_prompt.responses.interactive.screen_prompt_response import (
            ScreenPromptResponse,
        )

        response = ScreenPromptResponse.create_screen(
            callback=callback,
            height=height,
            verbosity=(
                verbosity if verbosity is not None else self.default_response_verbosity
            ),
            reset_on_finish=reset_on_finish,
        )

        return self.print_response(
            response=response,
            context=ScreenPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )

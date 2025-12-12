"""Mixin for managing progress prompt responses."""

from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_prompt.enums.terminal_color import TerminalColor

if TYPE_CHECKING:
    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.progress.progress_handle import ProgressHandle
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.responses.interactive.progress_prompt_response import (
        ProgressPromptResponse,
    )


class ProgressPromptResponseManagerMixin:
    """Mixin class for managing progress prompt responses."""

    def progress(
        self: IoManager,
        total: int = 100,
        current: float | int | str = 0,
        width: int | None = None,
        label: str | None = None,
        show_percentage: bool = False,
        verbosity: VerbosityLevel | None = None,
        context: PromptContext | None = None,
        print_response: bool = True,
        color: TerminalColor | None = None,
        **kwargs: Kwargs,
    ) -> ProgressPromptResponse:
        from wexample_prompt.responses.interactive.progress_prompt_response import (
            ProgressPromptResponse,
        )

        response = ProgressPromptResponse.create_progress(
            total=total,
            current=current,
            width=width,
            label=label,
            color=color,
            show_percentage=show_percentage,
            verbosity=(
                verbosity if verbosity is not None else self.default_response_verbosity
            ),
        )

        # We may need to initialize a hidden progress handle.
        if print_response:
            # The first print is done without progress handle.
            response = self.print_response(
                response=response,
                context=ProgressPromptResponse.rebuild_context_for_kwargs(
                    context=context,
                    parent_kwargs=kwargs,
                ),
            )
        else:
            rebuilt_context = ProgressPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            )
            effective_context = self.create_context(context=rebuilt_context)
            response.init_handle(context=effective_context)

        # The first print is done without progress handle.
        response.get_handle().output = self.output
        return response

    def progress_handle_create_or_update(
        self: IoManager, progress: ProgressHandle | None = None, **kwargs
    ) -> ProgressHandle:

        if progress is not None:
            progress.update(**kwargs)
            return progress
        else:
            return self.progress(**kwargs).get_handle()

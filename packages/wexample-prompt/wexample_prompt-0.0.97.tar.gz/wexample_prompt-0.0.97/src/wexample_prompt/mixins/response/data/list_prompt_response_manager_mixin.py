from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.responses.data.list_prompt_response import ListPromptResponse


class ListPromptResponseManagerMixin:
    def list(
        self: IoManager,
        items: list[str],
        bullet: str = "•",
        color: TerminalColor | None = None,
        verbosity: VerbosityLevel | None = None,
        context: PromptContext | None = None,
        **kwargs: Kwargs,
    ) -> ListPromptResponse:
        from wexample_prompt.responses.data.list_prompt_response import (
            ListPromptResponse,
        )

        response = ListPromptResponse.create_list(
            items=items,
            bullet=bullet,
            color=color,
            verbosity=(
                verbosity if verbosity is not None else self.default_response_verbosity
            ),
        )

        return self.print_response(
            response=response,
            context=ListPromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )

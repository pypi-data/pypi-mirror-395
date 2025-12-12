from __future__ import annotations

from typing import TYPE_CHECKING, cast

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.const.types import LineMessage
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )


class TitlePromptResponseManagerMixin:
    def title(
        self: IoManager,
        text: LineMessage,
        color: TerminalColor | None = None,
        character: str | None = None,
        width: int | None = None,
        verbosity: VerbosityLevel | None = None,
        context: PromptContext | None = None,
        **kwargs: Kwargs,
    ) -> AbstractPromptResponse:
        from wexample_prompt.common.io_manager import IoManager
        from wexample_prompt.responses.titles.title_prompt_response import (
            TitlePromptResponse,
        )

        response = TitlePromptResponse.create_title(
            text=text,
            color=color,
            character=character,
            width=width,
            verbosity=(
                verbosity if verbosity is not None else self.default_response_verbosity
            ),
        )

        return cast("IoManager", self).print_response(
            response=response,
            context=TitlePromptResponse.rebuild_context_for_kwargs(
                context=context, parent_kwargs=kwargs
            ),
        )

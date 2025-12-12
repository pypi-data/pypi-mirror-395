from __future__ import annotations

import sys
from typing import TYPE_CHECKING

from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.responses.messages.error_prompt_response import (
        ErrorPromptResponse,
    )


class ErrorPromptResponseManagerMixin:
    def error(
        self: IoManager,
        message: str | None = None,
        exception: BaseException | None = None,
        color: TerminalColor | None = None,
        verbosity: VerbosityLevel | None = None,
        context: PromptContext | None = None,
        symbol: str | None = None,
        fatal: bool = False,
        **kwargs: Kwargs,
    ) -> ErrorPromptResponse:
        from wexample_prompt.responses.messages.error_prompt_response import (
            ErrorPromptResponse,
        )

        response = ErrorPromptResponse.create_error(
            message=message,
            exception=exception,
            color=color,
            symbol=symbol,
            verbosity=(
                verbosity if verbosity is not None else self.default_response_verbosity
            ),
        )

        printed_response = self.print_response(
            response=response,
            context=ErrorPromptResponse.rebuild_context_for_kwargs(
                context=context, parent_kwargs=kwargs
            ),
        )

        if fatal:
            sys.exit(1)

        return printed_response

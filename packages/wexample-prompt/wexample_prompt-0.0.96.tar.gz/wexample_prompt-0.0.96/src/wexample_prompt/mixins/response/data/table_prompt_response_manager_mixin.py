"""Mixin for handling table responses in IoManager."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.responses.data.table_prompt_response import TablePromptResponse


class TablePromptResponseManagerMixin:
    """Mixin for IoManager to handle table responses."""

    def table(
        self: IoManager,
        data: list[list[Any]],
        headers: list[str] | None = None,
        title: str | None = None,
        verbosity: VerbosityLevel | None = None,
        context: PromptContext | None = None,
        **kwargs: Kwargs,
    ) -> TablePromptResponse:
        from wexample_prompt.responses.data.table_prompt_response import (
            TablePromptResponse,
        )

        response = TablePromptResponse.create_table(
            data=data,
            headers=headers,
            title=title,
            verbosity=(
                verbosity if verbosity is not None else self.default_response_verbosity
            ),
        )

        return self.print_response(
            response=response,
            context=TablePromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )

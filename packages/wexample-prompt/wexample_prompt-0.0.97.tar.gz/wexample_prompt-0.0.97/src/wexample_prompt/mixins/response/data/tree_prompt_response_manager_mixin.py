"""Mixin for handling tree responses in IoManager."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.responses.data.tree_prompt_response import TreePromptResponse


class TreePromptResponseManagerMixin:
    """Mixin for IoManager to handle tree responses."""

    def tree(
        self: IoManager,
        data: dict[str, Any],
        verbosity: VerbosityLevel | None = None,
        context: PromptContext | None = None,
        **kwargs: Kwargs,
    ) -> TreePromptResponse:
        from wexample_prompt.responses.data.tree_prompt_response import (
            TreePromptResponse,
        )

        response = TreePromptResponse.create_tree(
            data=data,
            verbosity=(
                verbosity if verbosity is not None else self.default_response_verbosity
            ),
        )

        return self.print_response(
            response=response,
            context=TreePromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )

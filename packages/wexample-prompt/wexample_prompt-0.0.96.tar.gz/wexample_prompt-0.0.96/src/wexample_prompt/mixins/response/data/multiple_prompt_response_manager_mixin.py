"""Mixin for managing multiple prompt responses."""

from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_prompt.common.prompt_context import PromptContext
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )
    from wexample_prompt.responses.data.multiple_prompt_response import (
        MultiplePromptResponse,
    )


class MultiplePromptResponseManagerMixin:
    """Mixin for managing multiple prompt responses in IoManager."""

    def multiple(
        self: IoManager,
        responses: list[AbstractPromptResponse],
        verbosity: VerbosityLevel | None = None,
        context: PromptContext | None = None,
        **kwargs,
    ) -> MultiplePromptResponse:
        """Create a multiple prompt response."""
        from wexample_prompt.responses.data.multiple_prompt_response import (
            MultiplePromptResponse,
        )

        response = MultiplePromptResponse.create_multiple(
            responses=responses,
            verbosity=(
                verbosity if verbosity is not None else self.default_response_verbosity
            ),
        )

        return self.print_response(
            response=response,
            context=MultiplePromptResponse.rebuild_context_for_kwargs(
                context=context,
                parent_kwargs=kwargs,
            ),
        )

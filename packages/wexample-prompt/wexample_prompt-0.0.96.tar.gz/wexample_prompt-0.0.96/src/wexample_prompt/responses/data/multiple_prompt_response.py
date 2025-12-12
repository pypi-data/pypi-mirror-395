from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.responses.abstract_prompt_response import AbstractPromptResponse

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.verbosity_level import VerbosityLevel


@base_class
class MultiplePromptResponse(AbstractPromptResponse):
    """A response that groups multiple responses and renders them in sequence.

    This class allows grouping multiple prompt responses of different types into a
    single response object. When rendered or printed, each contained response is
    processed in order.

    Attributes:
        responses: List of prompt responses to be rendered together.
    """

    responses: list[AbstractPromptResponse] = public_field(
        factory=list,
        description="List of prompt responses to be rendered together",
    )

    @classmethod
    def create_multiple(
        cls: type[MultiplePromptResponse],
        responses: list[AbstractPromptResponse] | None = None,
        verbosity: VerbosityLevel | None = None,
    ) -> MultiplePromptResponse:
        """Create a new MultiplePromptResponse from a list of responses."""
        responses = responses or []

        # Work on deep copies to avoid mutating shared instances across calls.
        cloned_responses: list[AbstractPromptResponse] = []
        for response in responses:
            cloned = response.clone()
            cloned.verbosity = verbosity
            cloned_responses.append(cloned)

        return cls(
            responses=cloned_responses,
            verbosity=verbosity,
        )

    @classmethod
    def get_example_class(cls) -> type:
        from wexample_prompt.example.response.data.multiple_example import (
            MultipleExample,
        )

        return MultipleExample

    def append_response(
        self, response: AbstractPromptResponse
    ) -> MultiplePromptResponse:
        """Append a single response and return self for chaining."""
        self.responses.append(response)
        return self

    def extend_responses(
        self, responses: list[AbstractPromptResponse]
    ) -> MultiplePromptResponse:
        """Extend responses with a list and return self for chaining."""
        self.responses.extend(responses)
        return self

    def render(self, context: PromptContext | None = None) -> str | None:
        """Render all contained responses in sequence.

        Returns:
            The concatenated rendered string, skipping None parts.
        """
        from wexample_prompt.common.prompt_context import PromptContext

        context = PromptContext.create_if_none(context=context)

        if not self._verbosity_context_allows_display(context=context):
            return None

        rendered_parts: list[str] = []
        for response in self.responses:
            part = response.render(context=context)
            if part is not None:
                rendered_parts.append(part)

        self._rendered_content = "\n".join(rendered_parts) if rendered_parts else None
        return self._rendered_content

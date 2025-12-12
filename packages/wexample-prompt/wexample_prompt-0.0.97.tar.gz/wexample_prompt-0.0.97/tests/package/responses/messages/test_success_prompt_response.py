"""Tests for SuccessPromptResponse."""

from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_prompt.testing.abstract_prompt_message_response_test import (
    AbstractPromptMessageResponseTest,
)

if TYPE_CHECKING:
    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )


class TestSuccessPromptResponse(AbstractPromptMessageResponseTest):
    """Test cases for SuccessPromptResponse."""

    __test__ = True  # Re-enable test collection for concrete test class

    def get_expected_lines(self) -> int:
        return 1  # Success messages are single line

    def _assert_specific_format(self, rendered: str) -> None:
        # Success messages should include the success symbol
        self._assert_contains_text(rendered, "✅")

    def _create_test_kwargs(self, kwargs=None) -> Kwargs:
        kwargs = kwargs or {}
        kwargs.setdefault("message", self._test_message)
        return kwargs

    def _get_response_class(self) -> type[AbstractPromptResponse]:
        from wexample_prompt.responses.messages.success_prompt_response import (
            SuccessPromptResponse,
        )

        return SuccessPromptResponse

"""Base class for testing prompt responses."""

from __future__ import annotations

from wexample_prompt.testing.abstract_prompt_response_test import (
    AbstractPromptResponseTest,
)


class AbstractPromptMessageResponseTest(AbstractPromptResponseTest):
    __test__ = False  # Prevent pytest from discovering this abstract class

    def test_multiline_message_is_rendered(self) -> None:
        """All message responses should correctly render multi-line messages."""
        response = self._create_test_response({"message": self._test_message_multiline})
        self._asset_response_render_is_multiline(response)

    # Common tests for all message-type responses
    def test_single_line_by_default(self) -> None:
        """Message responses are typically single-line; if expected is 1, ensure no extra newlines."""
        response = self._create_test_response({"message": self._test_message})
        rendered = response.render()
        if self.get_expected_lines() == 1:
            # No newline characters expected for single-line messages
            self.assertNotIn("\n", rendered)

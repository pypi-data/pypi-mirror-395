"""Base class for testing title prompt responses."""

from __future__ import annotations

from wexample_prompt.testing.abstract_prompt_response_test import (
    AbstractPromptResponseTest,
)


class AbstractTitlePromptResponseTest(AbstractPromptResponseTest):
    """Base class for testing title prompt responses."""

    __test__ = False  # Prevent pytest from discovering this abstract class

    def get_expected_lines(self) -> int:
        """Return the expected number of lines in the rendered response."""
        return 3  # Title messages have empty lines before and after

    def test_custom_fill_char(self) -> None:
        """Test response with custom fill character."""
        character = "."
        response = self._create_test_response(character=character)
        response.render()

        self._assert_common_response_structure(response)
        self._assert_contains_text(response.rendered_content, self._test_message)
        self.assertIn(character, response.rendered_content)

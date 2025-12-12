from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.response.abstract_title_example import AbstractTitleExample


@base_class
class SubtitleExample(AbstractTitleExample):
    """Example usage of SubtitlePromptResponse with comprehensive formatting tests."""

    def example_class(self):
        from wexample_prompt.responses.titles.subtitle_prompt_response import (
            SubtitlePromptResponse,
        )

        return SubtitlePromptResponse.create_subtitle(
            text=self.get_test_message() + " (from response)"
        )

    def example_extended(self) -> None:
        self._class_with_methods.subtitle(
            text=self.get_test_message() + " (class method)"
        )

    def example_manager(self) -> None:
        self.io.subtitle(text=self.get_test_message())

    def get_io_method(self):
        """Return the IO method for this title type."""
        return self.io.subtitle

    def get_response_name(self) -> str:
        """Return the response name for this title type."""
        return "subtitle"

    def get_test_message(self) -> str:
        return "Test subtitle"

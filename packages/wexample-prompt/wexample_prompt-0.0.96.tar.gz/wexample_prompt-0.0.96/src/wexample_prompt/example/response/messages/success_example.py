from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.response.abstract_simple_message_example import (
    AbstractSimpleMessageExample,
)


@base_class
class SuccessExample(AbstractSimpleMessageExample):
    """Example usage of SuccessPromptResponse with comprehensive formatting tests."""

    def example_class(self):
        from wexample_prompt.responses.messages.success_prompt_response import (
            SuccessPromptResponse,
        )

        return SuccessPromptResponse.create_success(
            message=self.get_test_message(),
        )

    def example_extended(self) -> None:
        self._class_with_methods.success(message=self.get_test_message())

    def example_manager(self) -> None:
        self.io.success(message=self.get_test_message())

    def get_io_method(self):
        """Return the IO method for this message type."""
        return self.io.success

    def get_response_name(self) -> str:
        """Return the response name for this message type."""
        return "success"

    def get_test_message(self) -> str:
        return "Test success message"

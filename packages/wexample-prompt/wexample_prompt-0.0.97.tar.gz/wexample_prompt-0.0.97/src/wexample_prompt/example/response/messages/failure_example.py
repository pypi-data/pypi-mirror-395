from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.response.abstract_simple_message_example import (
    AbstractSimpleMessageExample,
)


@base_class
class FailureExample(AbstractSimpleMessageExample):
    """Example usage of FailurePromptResponse with comprehensive formatting tests."""

    def example_class(self):
        from wexample_prompt.responses.messages.failure_prompt_response import (
            FailurePromptResponse,
        )

        return FailurePromptResponse.create_failure(
            message=self.get_test_message(),
        )

    def example_extended(self) -> None:
        self._class_with_methods.failure(message=self.get_test_message())

    def example_manager(self) -> None:
        self.io.failure(message=self.get_test_message())

    def get_io_method(self):
        """Return the IO method for this message type."""
        return self.io.failure

    def get_response_name(self) -> str:
        """Return the response name for this message type."""
        return "failure"

    def get_test_message(self) -> str:
        return "Test failure message"

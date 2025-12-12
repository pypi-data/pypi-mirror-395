from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.response.abstract_simple_message_example import (
    AbstractSimpleMessageExample,
)


@base_class
class LogExample(AbstractSimpleMessageExample):
    """Example usage of LogPromptResponse with various formatting."""

    def example_class(self):
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse

        return LogPromptResponse.create_log(
            message=self.get_test_message(),
        )

    def example_extended(self) -> None:
        self._class_with_methods.log(message=self.get_test_message())

    def example_manager(self) -> None:
        self.io.log(message=self.get_test_message())

    def get_test_message(self) -> str:
        return "Test log message"

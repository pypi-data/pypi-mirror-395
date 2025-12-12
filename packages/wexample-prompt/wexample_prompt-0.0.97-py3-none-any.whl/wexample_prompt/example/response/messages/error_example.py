from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.response.abstract_simple_message_example import (
    AbstractSimpleMessageExample,
)


@base_class
class ErrorExample(AbstractSimpleMessageExample):
    """Example usage of ErrorPromptResponse with comprehensive formatting tests and edge cases."""

    @staticmethod
    def generate_long_error() -> str:
        """Generate long error message."""
        return "@🔴+bold{Critical Error:} " + (
            "This is a very long error message that contains detailed information about what went wrong. "
            * 5
        )

    @staticmethod
    def generate_long_path() -> str:
        """Generate long file path."""
        return (
            "/home/user/projects/some_project/build/output/deploy/"
            "very/very/very/long/subdirectory/structure/with/files/and/more/files/"
            "and/even/more/nested/paths/that/should/wrap/properly.txt"
        )

    def edge_case_indentation(self) -> None:
        """Test edge cases: indentation."""
        self.io.error(message="@🔴+bold{Error at level 0}", indentation=0)

        self.io.indentation = 3
        self.io.error(message="@🔴+bold{Error at indentation level 3}")

        self.io.error(
            message="@🔴+bold{Error at indentation level 3 + 5}", indentation=5
        )
        self.io.indentation = 0

    def edge_case_limits(self) -> None:
        """Test edge cases: limits (long error messages)."""
        # Long error message
        self.io.error(message=self.generate_long_error())

        # Error with long path
        self.io.error(message="@🔴+bold{Path error:} " + self.generate_long_path())

    def edge_case_nesting(self) -> None:
        """Test edge cases: nested error contexts."""
        self.io.log("@color:cyan{Starting outer function}")
        self.io.indentation += 1
        self.io.error("@🔴+bold{Error at level 1}")

        self.io.indentation += 1
        self.io.error("@🟠+bold{Error at level 2}")

        self.io.indentation += 1
        self.io.error("@🔴+bold{Error at level 3}")
        self.io.indentation = 0

    def edge_case_with_exception(self) -> None:
        """Test edge cases: errors with exceptions."""

        def make_error() -> None:
            def inner() -> None:
                raise ValueError("Test exception from example")

            def middle() -> None:
                inner()

            middle()

        try:
            make_error()
        except Exception as e:
            self.io.error(
                message="@color:magenta+bold{Error with exception}",
                exception=e,
            )

    def example_class(self):
        from wexample_prompt.responses.messages.error_prompt_response import (
            ErrorPromptResponse,
        )

        return ErrorPromptResponse.create_error(
            message=self.get_test_message(),
        )

    def example_extended(self) -> None:
        self._class_with_methods.error(message=self.get_test_message())

    def example_manager(self) -> None:
        self.io.error(message=self.get_test_message())

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        # Get base examples from AbstractSimpleMessageExample
        base_examples = super().get_examples()

        # Add error-specific examples
        error_specific = [
            {
                "title": "Edge Case: With Exception",
                "description": "Error with exception and traceback",
                "callback": self.edge_case_with_exception,
            },
        ]

        return base_examples + error_specific

    def get_io_method(self):
        """Return the IO method for this message type."""
        return self.io.error

    def get_response_name(self) -> str:
        """Return the response name for this message type."""
        return "error"

    def get_test_message(self) -> str:
        return "Test error message"

"""Example usage of MultiplePromptResponse."""

from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample
from wexample_prompt.responses.data.multiple_prompt_response import (
    MultiplePromptResponse,
)


@base_class
class MultipleExample(AbstractResponseExample):
    """Example usage of MultiplePromptResponse."""

    def dynamic_multiple(self) -> MultiplePromptResponse | None:
        """Show building responses dynamically."""
        from wexample_prompt.responses.data.list_prompt_response import (
            ListPromptResponse,
        )
        from wexample_prompt.responses.data.multiple_prompt_response import (
            MultiplePromptResponse,
        )
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse

        response = MultiplePromptResponse.create_multiple(
            responses=[LogPromptResponse.create_log("Initial response")],
            # context=self.io.create_context(),
        )

        # Add more responses
        response.append_response(
            ListPromptResponse.create_list(items=["Dynamic item 1"])
        )
        response.extend_responses(
            [
                LogPromptResponse.create_log("Added later"),
                ListPromptResponse.create_list(items=["Dynamic item 2"]),
            ]
        )

        return response

    def example_all_message_types(self) -> MultiplePromptResponse | None:
        """Show all different message types together."""
        from wexample_prompt.responses.echo_prompt_response import EchoPromptResponse
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse
        from wexample_prompt.responses.messages.error_prompt_response import (
            ErrorPromptResponse,
        )
        from wexample_prompt.responses.messages.info_prompt_response import (
            InfoPromptResponse,
        )
        from wexample_prompt.responses.messages.success_prompt_response import (
            SuccessPromptResponse,
        )
        from wexample_prompt.responses.messages.warning_prompt_response import (
            WarningPromptResponse,
        )

        responses = [
            LogPromptResponse.create_log("Log message"),
            EchoPromptResponse.create_echo("Echo message"),
            InfoPromptResponse.create_info("Info message"),
            SuccessPromptResponse.create_success("Success message"),
            WarningPromptResponse.create_warning("Warning message"),
            ErrorPromptResponse.create_error("Error message"),
        ]
        return self.io.multiple(responses=responses)

    def example_class(self, indentation: int | None = None):
        """Example using the class directly."""
        from wexample_prompt.responses.data.list_prompt_response import (
            ListPromptResponse,
        )
        from wexample_prompt.responses.data.multiple_prompt_response import (
            MultiplePromptResponse,
        )
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse

        responses = [
            LogPromptResponse.create_log("First response"),
            ListPromptResponse.create_list(items=["Item 1", "Item 2"]),
            LogPromptResponse.create_log("Last response"),
        ]
        return MultiplePromptResponse.create_multiple(
            responses=responses,
        )

    def example_complex_structure(self) -> MultiplePromptResponse | None:
        """Complex structure with titles, lists, and messages."""
        from wexample_prompt.responses.data.list_prompt_response import (
            ListPromptResponse,
        )
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse
        from wexample_prompt.responses.titles.subtitle_prompt_response import (
            SubtitlePromptResponse,
        )
        from wexample_prompt.responses.titles.title_prompt_response import (
            TitlePromptResponse,
        )

        responses = [
            TitlePromptResponse.create_title("Project Report"),
            SubtitlePromptResponse.create_subtitle("Summary"),
            LogPromptResponse.create_log("Project completed successfully"),
            SubtitlePromptResponse.create_subtitle("Files Modified"),
            ListPromptResponse.create_list(
                items=[
                    "📄 README.md",
                    "📄 setup.py",
                    "📁 src/",
                    "  📄 main.py",
                    "  📄 utils.py",
                ]
            ),
            SubtitlePromptResponse.create_subtitle("Statistics"),
            ListPromptResponse.create_list(
                items=[
                    "@color:green{✓} 15 tests passed",
                    "@color:yellow{⚠} 2 warnings",
                    "@color:cyan{ℹ} 100% coverage",
                ]
            ),
        ]
        return self.io.multiple(responses=responses)

    def example_extended(self) -> None:
        """Example using PromptContext."""
        from wexample_prompt.responses.data.list_prompt_response import (
            ListPromptResponse,
        )
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse

        responses = [
            LogPromptResponse.create_log("First response"),
            ListPromptResponse.create_list(items=["Item 1", "Item 2"]),
            LogPromptResponse.create_log("Last response"),
        ]
        self._class_with_methods.multiple(responses=responses)

    def example_manager(self) -> None:
        """Example using the IoManager."""
        from wexample_prompt.responses.data.list_prompt_response import (
            ListPromptResponse,
        )
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse

        responses = [
            LogPromptResponse.create_log("First response"),
            ListPromptResponse.create_list(items=["Item 1", "Item 2"]),
            LogPromptResponse.create_log("Last response"),
        ]
        self.io.multiple(responses=responses)

    def example_with_formatting(self) -> MultiplePromptResponse | None:
        """Multiple responses with inline formatting."""
        from wexample_prompt.responses.data.list_prompt_response import (
            ListPromptResponse,
        )
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse

        responses = [
            LogPromptResponse.create_log(
                "@color:green+bold{Success}: Operation completed"
            ),
            ListPromptResponse.create_list(
                items=[
                    "@color:cyan{File}: @path:short{/home/user/file1.txt}",
                    "@color:cyan{File}: @path:short{/home/user/file2.txt}",
                ]
            ),
            LogPromptResponse.create_log("@color:yellow{Time}: @time{}"),
        ]
        return self.io.multiple(responses=responses)

    def example_with_nesting(self) -> MultiplePromptResponse | None:
        """Multiple responses with nested parent/child."""
        from wexample_prompt.example.helpers.nesting_demo_classes import ParentTask
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse

        responses = [
            LogPromptResponse.create_log(
                "@color:yellow+bold{Nesting in Multiple Response}"
            ),
        ]

        # Add nesting demo
        parent = ParentTask(io=self.io)
        parent.execute(method_name="log")

        return self.io.multiple(responses=responses)

    def example_with_separators(self) -> MultiplePromptResponse | None:
        """Multiple responses with separators."""
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse
        from wexample_prompt.responses.titles.separator_prompt_response import (
            SeparatorPromptResponse,
        )

        responses = [
            LogPromptResponse.create_log("Section 1: Introduction"),
            LogPromptResponse.create_log("This is the first section"),
            SeparatorPromptResponse.create_separator(),
            LogPromptResponse.create_log("Section 2: Details"),
            LogPromptResponse.create_log("This is the second section"),
            SeparatorPromptResponse.create_separator(label="End"),
        ]
        return self.io.multiple(responses=responses)

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List[Dict[str, Any]]: List of example configurations
        """
        return [
            {
                "title": "Simple Multiple",
                "description": "Display multiple responses in sequence",
                "callback": self.simple_multiple,
            },
            {
                "title": "Mixed Types",
                "description": "Display different types of responses together",
                "callback": self.mixed_types,
            },
            {
                "title": "With Formatting",
                "description": "Multiple responses with inline formatting (@color, @path, @time)",
                "callback": self.example_with_formatting,
            },
            {
                "title": "With Nesting",
                "description": "Multiple responses with parent/child nesting",
                "callback": self.example_with_nesting,
            },
            {
                "title": "All Message Types",
                "description": "Show all different message types (log, echo, info, success, warning, error)",
                "callback": self.example_all_message_types,
            },
            {
                "title": "With Separators",
                "description": "Multiple responses with separator lines",
                "callback": self.example_with_separators,
            },
            {
                "title": "Complex Structure",
                "description": "Complex structure with titles, subtitles, lists, and formatted messages",
                "callback": self.example_complex_structure,
            },
            {
                "title": "Dynamic Multiple",
                "description": "Build multiple responses dynamically",
                "callback": self.dynamic_multiple,
            },
        ]

    def mixed_types(self) -> MultiplePromptResponse | None:
        """Show different response types together."""
        from wexample_prompt.responses.data.list_prompt_response import (
            ListPromptResponse,
        )
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse

        responses = [
            LogPromptResponse.create_log("Log response"),
            ListPromptResponse.create_list(
                items=["List item 1", "List item 2"],
            ),
            LogPromptResponse.create_log("Another log response"),
        ]
        return self.io.multiple(responses=responses)

    def simple_multiple(self) -> MultiplePromptResponse | None:
        """Show a simple multiple response example."""
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse

        responses = [
            LogPromptResponse.create_log("First message"),
            LogPromptResponse.create_log("Second message"),
            LogPromptResponse.create_log("Third message"),
        ]
        return self.io.multiple(responses=responses)

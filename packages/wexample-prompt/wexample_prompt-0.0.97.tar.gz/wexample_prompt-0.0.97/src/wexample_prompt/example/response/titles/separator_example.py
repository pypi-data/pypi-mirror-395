from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class SeparatorExample(AbstractResponseExample):
    """Example usage of SeparatorPromptResponse with comprehensive formatting tests."""

    def example_class(self):
        from wexample_prompt.responses.titles.separator_prompt_response import (
            SeparatorPromptResponse,
        )

        return SeparatorPromptResponse.create_separator("From response")

    def example_extended(self) -> None:
        self._class_with_methods.separator(label="Class method")

    def example_indented(self) -> None:
        """Separator with indentation."""
        from wexample_prompt.enums.terminal_color import TerminalColor

        # Different indentation levels
        self.io.separator(label="Normal separator", indentation=0)
        self.io.separator(label="Indented separator (level 3)", indentation=3)
        self.io.separator(label="Indented separator (level 5)", indentation=5)

        # Colored indentation
        self.io.separator(
            label="@color:cyan{Colored separator with indentation}",
            indentation=3,
            indentation_text_color=TerminalColor.CYAN,
        )

    def example_long_text(self) -> None:
        """Separator with long text."""
        self.io.separator(
            label="This is a very long separator label that contains a lot of text"
        )
        self.io.separator(
            label="@color:magenta+bold{Very Long Formatted Separator} with lots of text"
        )

    def example_manager(self) -> None:
        self.io.separator()

    def example_nesting(self) -> None:
        """Separator with nested parent/child classes."""
        from wexample_prompt.example.helpers.nesting_demo_classes import ParentTask

        self.io.separator(label="@color:yellow+bold{Nesting Demo}")
        parent = ParentTask(io=self.io)
        parent.execute(method_name="log")

    def example_simple(self) -> None:
        """Simple separator without label."""
        self.io.separator()
        self.io.separator(label="Simple Separator")

    def example_with_emojis(self) -> None:
        """Separator with emojis."""
        self.io.separator(label="🎉 Success Section")
        self.io.separator(label="⚠️ Warning Section")
        self.io.separator(label="🚀 Deployment Section")
        self.io.separator(label="✅ Completed Section")

    def example_with_formatting(self) -> None:
        """Separator with color and bold formatting."""
        self.io.separator(label="@color:cyan+bold{Cyan Bold Separator}")
        self.io.separator(label="@color:yellow{Yellow Separator}")
        self.io.separator(label="@🔵+bold{Blue Emoji Separator}")

    def example_with_paths(self) -> None:
        """Separator with file paths."""
        self.io.separator(
            label="Processing: @path:short{/home/user/documents/report.pdf}"
        )
        self.io.separator(label="@color:green{✓ Saved to} @path:short{/tmp/output.log}")

    def example_with_time(self) -> None:
        """Separator with time formatters."""
        self.io.separator(label="Build started at @time{}")
        self.io.separator(label="@color:cyan{Deployment} - @time:%H:%M:%S{}")

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Simple",
                "description": "Simple separator without/with label",
                "callback": self.example_simple,
            },
            {
                "title": "With Formatting",
                "description": "Separator with colors and bold",
                "callback": self.example_with_formatting,
            },
            {
                "title": "With Emojis",
                "description": "Separator with various emojis",
                "callback": self.example_with_emojis,
            },
            {
                "title": "Long Text",
                "description": "Separator with long text",
                "callback": self.example_long_text,
            },
            {
                "title": "With Paths",
                "description": "Separator with file paths (@path)",
                "callback": self.example_with_paths,
            },
            {
                "title": "With Time",
                "description": "Separator with time formatters (@time)",
                "callback": self.example_with_time,
            },
            {
                "title": "Nesting",
                "description": "Separator with parent/child nesting",
                "callback": self.example_nesting,
            },
            {
                "title": "Indented",
                "description": "Separator with various indentation levels",
                "callback": self.example_indented,
            },
        ]

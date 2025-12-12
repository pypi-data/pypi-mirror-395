"""Abstract base class for title examples (title, subtitle, separator)."""

from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class AbstractTitleExample(AbstractResponseExample):
    """Base class for title examples with standard formatting tests."""

    def example_indented(self) -> None:
        """Title with indentation."""
        from wexample_prompt.enums.terminal_color import TerminalColor

        method = self.get_io_method()
        name = self.get_response_name()

        # Different indentation levels
        method(text=f"Normal {name}", indentation=0)
        method(text=f"Indented {name} (level 3)", indentation=3)
        method(text=f"Indented {name} (level 5)", indentation=5)

        # Colored indentation
        method(
            text=f"@color:cyan{{Colored {name} with indentation}}",
            indentation=3,
            indentation_text_color=TerminalColor.CYAN,
        )

    def example_long_text(self) -> None:
        """Title with long text."""
        method = self.get_io_method()
        method(
            text="This is a very long title that contains a lot of text to test how the system handles wrapping"
        )
        method(
            text="@color:magenta+bold{Very Long Formatted Title} with lots of text that might wrap around"
        )

    def example_nesting(self) -> None:
        """Title with nested parent/child classes."""
        from wexample_prompt.example.helpers.nesting_demo_classes import ParentTask

        method = self.get_io_method()
        method(text="@color:yellow+bold{Nesting Demo}")
        parent = ParentTask(io=self.io)
        parent.execute(method_name=self.get_response_name())

    def example_simple(self) -> None:
        """Simple title without formatting."""
        method = self.get_io_method()
        name = self.get_response_name()
        method(text=f"Simple {name}")

    def example_with_emojis(self) -> None:
        """Title with emojis."""
        method = self.get_io_method()
        method(text="🎉 Success Title")
        method(text="⚠️ Warning Title")
        method(text="🚀 Deployment Title")
        method(text="✅ Completed Title")

    def example_with_formatting(self) -> None:
        """Title with color and bold formatting."""
        method = self.get_io_method()
        method(text="@color:cyan+bold{Cyan Bold Title}")
        method(text="@color:yellow{Yellow Title}")
        method(text="@🔵+bold{Blue Emoji Title}")

    def example_with_paths(self) -> None:
        """Title with file paths."""
        method = self.get_io_method()
        method(text="Processing: @path:short{/home/user/documents/report.pdf}")
        method(text="@color:green{✓ Saved to} @path:short{/tmp/output.log}")

    def example_with_time(self) -> None:
        """Title with time formatters."""
        method = self.get_io_method()
        method(text="Build started at @time{}")
        method(text="@color:cyan{Deployment} - @time:%H:%M:%S{}")

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Simple",
                "description": "Simple title without formatting",
                "callback": self.example_simple,
            },
            {
                "title": "With Formatting",
                "description": "Title with colors and bold",
                "callback": self.example_with_formatting,
            },
            {
                "title": "With Emojis",
                "description": "Title with various emojis",
                "callback": self.example_with_emojis,
            },
            {
                "title": "Long Text",
                "description": "Title with long text that might wrap",
                "callback": self.example_long_text,
            },
            {
                "title": "With Paths",
                "description": "Title with file paths (@path)",
                "callback": self.example_with_paths,
            },
            {
                "title": "With Time",
                "description": "Title with time formatters (@time)",
                "callback": self.example_with_time,
            },
            {
                "title": "Nesting",
                "description": "Title with parent/child nesting",
                "callback": self.example_nesting,
            },
            {
                "title": "Indented",
                "description": "Title with various indentation levels",
                "callback": self.example_indented,
            },
        ]

    def get_io_method(self) -> None:
        """Return the IO method for this title type. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement get_io_method()")

    def get_response_name(self) -> str:
        """Return the response name for this title type. Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement get_response_name()")

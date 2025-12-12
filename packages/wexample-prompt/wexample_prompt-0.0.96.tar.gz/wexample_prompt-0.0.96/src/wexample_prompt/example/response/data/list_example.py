from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class ListExample(AbstractResponseExample):
    def example_class(self):
        from wexample_prompt.responses.data.list_prompt_response import (
            ListPromptResponse,
        )

        return ListPromptResponse.create_list(
            items=self.get_test_items(),
        )

    def example_colored(self) -> None:
        """List with colors."""
        from wexample_prompt.enums.terminal_color import TerminalColor

        self.io.list(
            items=["Success item 1", "Success item 2"], color=TerminalColor.GREEN
        )
        self.io.list(
            items=["Warning item 1", "Warning item 2"], color=TerminalColor.YELLOW
        )
        self.io.list(items=["Error item 1", "Error item 2"], color=TerminalColor.RED)

    def example_custom_bullets(self) -> None:
        """List with custom bullet characters."""
        self.io.list(items=["Arrow item 1", "Arrow item 2", "Arrow item 3"], bullet="→")
        self.io.list(items=["Check item 1", "Check item 2", "Check item 3"], bullet="✓")
        self.io.list(items=["Star item 1", "Star item 2", "Star item 3"], bullet="★")

    def example_edge_cases(self) -> None:
        """List with edge cases."""
        self.io.list(
            items=[
                "",  # Empty item
                "Single char: X",
                "Special chars: <>&\"'`[]{}()±×÷≠≈∞",
                "  Deeply nested",
                "    Very deeply nested",
                "      Extremely deeply nested",
            ]
        )

    def example_extended(self) -> None:
        self._class_with_methods.list(items=self.get_test_items())

    def example_formatted_items(self) -> None:
        """List items with inline formatting."""
        self.io.list(
            items=[
                "@color:green+bold{Completed} task",
                "@color:yellow{In progress} task",
                "@color:red{Failed} task",
                "Task with @path:short{/home/user/file.txt}",
                "Task at @time{}",
            ]
        )

    def example_long_items(self) -> None:
        """List with long items that may wrap."""
        self.io.list(
            items=[
                "Short item",
                "This is a very long item that contains a lot of text and will probably wrap to multiple lines depending on the terminal width",
                "Another short item",
                "  Nested long item: "
                + "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 3,
            ]
        )

    def example_manager(self) -> None:
        self.io.list(items=self.get_test_items())

    def example_mixed_content(self) -> None:
        """List with mixed content types."""
        self.io.list(
            items=[
                "📁 Project Structure",
                "  📄 README.md",
                "  📄 setup.py",
                "  📁 src/",
                "    📄 __init__.py",
                "    📄 main.py",
                "  📁 tests/",
                "    📄 test_main.py",
            ]
        )

    def example_nested(self) -> None:
        """List with multiple nesting levels."""
        self.io.list(
            items=[
                "Root level 1",
                "  Level 1.1",
                "    Level 1.1.1",
                "    Level 1.1.2",
                "  Level 1.2",
                "Root level 2",
                "  Level 2.1",
                "    Level 2.1.1",
            ]
        )

    def example_nesting(self) -> None:
        """List with nested parent/child classes demonstrating automatic indentation."""
        from wexample_prompt.example.helpers.nesting_demo_classes import ParentTask

        self.io.list(
            items=["@color:yellow+bold{Nesting Demo: Parent/Child/Grandchild}"]
        )
        parent = ParentTask(io=self.io)
        parent.execute(method_name="list")

    def example_simple(self) -> None:
        """Simple flat list."""
        self.io.list(
            items=[
                "First item",
                "Second item",
                "Third item",
            ]
        )

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Simple",
                "description": "Simple flat list",
                "callback": self.example_simple,
            },
            {
                "title": "Nested",
                "description": "List with multiple nesting levels",
                "callback": self.example_nested,
            },
            {
                "title": "Custom Bullets",
                "description": "Lists with custom bullet characters (→, ✓, ★)",
                "callback": self.example_custom_bullets,
            },
            {
                "title": "Colored",
                "description": "Lists with different colors",
                "callback": self.example_colored,
            },
            {
                "title": "Formatted Items",
                "description": "List items with inline formatting (@color, @path, @time)",
                "callback": self.example_formatted_items,
            },
            {
                "title": "Mixed Content",
                "description": "List with emojis and file structure",
                "callback": self.example_mixed_content,
            },
            {
                "title": "Long Items",
                "description": "List with long items that wrap",
                "callback": self.example_long_items,
            },
            {
                "title": "Nesting",
                "description": "Parent/child classes with automatic indentation",
                "callback": self.example_nesting,
            },
            {
                "title": "Edge Cases",
                "description": "Empty items, special chars, deep nesting",
                "callback": self.example_edge_cases,
            },
        ]

    def get_test_items(self) -> list[str]:
        return [
            "Item A",
            "  Sub-item A1",
            "  Sub-item A2",
            "Item B",
        ]

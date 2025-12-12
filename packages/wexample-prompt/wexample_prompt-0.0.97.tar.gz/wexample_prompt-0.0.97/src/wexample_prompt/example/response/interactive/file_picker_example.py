"""Example usage of FilePickerPromptResponse."""

from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class FilePickerExample(AbstractResponseExample):
    """Example usage of FilePickerPromptResponse."""

    def example_class(self, indentation: int | None = None):
        """Example using the class directly."""
        from wexample_prompt.responses.interactive.file_picker_prompt_response import (
            FilePickerPromptResponse,
        )

        return FilePickerPromptResponse.create_file_picker(
            question="Select a file:",
            base_dir=None,  # Will use current working directory
            predefined_answer="some_file",
        )

    def example_extended(self) -> None:
        """Example using PromptContext."""
        self._class_with_methods.file_picker(
            question="Select a file:", predefined_answer="some_file"
        )

    def example_manager(self) -> None:
        """Example using the IoManager."""
        self.io.file_picker(question="Select a file:", predefined_answer="some_file")

    def example_nesting(self) -> None:
        """File picker with parent/child nesting."""
        from wexample_prompt.example.helpers.nesting_demo_classes import ParentTask

        self.io.file_picker(
            question="@color:yellow+bold{Nesting Demo} - Select file:",
            predefined_answer="example.txt",
        )
        parent = ParentTask(io=self.io)
        parent.execute(method_name="log")

    def example_simple(self) -> None:
        """Simple file picker in current directory."""
        self.io.file_picker(question="Select a file:", predefined_answer="README.md")

    def example_specific_dir(self) -> None:
        """File picker in specific directory."""
        import os

        self.io.file_picker(
            question="Select from /tmp:",
            base_dir="/tmp",
            predefined_answer=(
                os.listdir("/tmp")[0] if os.listdir("/tmp") else "file.txt"
            ),
        )

    def example_with_emojis(self) -> None:
        """File picker with emojis."""
        self.io.file_picker(
            question="📁 Select a Python file:", predefined_answer="main.py"
        )

    def example_with_formatting(self) -> None:
        """File picker with inline formatting."""
        self.io.file_picker(
            question="@color:cyan+bold{Select configuration file}:",
            predefined_answer="config.yml",
        )

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Simple",
                "description": "Simple file picker in current directory",
                "callback": self.example_simple,
            },
            {
                "title": "With Formatting",
                "description": "File picker with inline formatting (@color)",
                "callback": self.example_with_formatting,
            },
            {
                "title": "With Emojis",
                "description": "File picker with emojis",
                "callback": self.example_with_emojis,
            },
            {
                "title": "Specific Directory",
                "description": "File picker in specific directory (/tmp)",
                "callback": self.example_specific_dir,
            },
            {
                "title": "Nesting",
                "description": "File picker with parent/child nesting",
                "callback": self.example_nesting,
            },
        ]

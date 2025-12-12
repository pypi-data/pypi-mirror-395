"""Example for table response."""

from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class TableExample(AbstractResponseExample):
    """Example for table response."""

    def example_class(self, indentation: int | None = None):
        """Example using class with context."""
        from wexample_prompt.responses.data.table_prompt_response import (
            TablePromptResponse,
        )

        headers = ["Name", "Age", "City"]
        data = [
            ["John", "30", "New York"],
            ["Jane", "25", "San Francisco"],
            ["Bob", "35", "Chicago"],
        ]
        return TablePromptResponse.create_table(
            data=data,
            headers=headers,
            title="Employee List",
        )

    def example_extended(self) -> None:
        """Example using context."""
        headers = ["Name", "Age", "City"]
        data = [
            ["John", "30", "New York"],
            ["Jane", "25", "San Francisco"],
            ["Bob", "35", "Chicago"],
        ]
        self._class_with_methods.table(
            data=data,
            headers=headers,
            title="Employee List",
        )

    def example_long_content(self) -> None:
        """Table with long content that wraps."""
        self.io.table(
            headers=["Command", "Description"],
            data=[
                [
                    "git commit",
                    "This is a very long description that contains a lot of text and will probably wrap to multiple lines",
                ],
                [
                    "docker run",
                    "Run a command in a new container with various options and parameters",
                ],
            ],
            title="Commands",
        )

    def example_manager(self) -> None:
        """Example using IoManager directly."""
        headers = ["Name", "Age", "City"]
        data = [
            ["John", "30", "New York"],
            ["Jane", "25", "San Francisco"],
            ["Bob", "35", "Chicago"],
        ]
        self.io.table(
            data=data,
            headers=headers,
            title="Employee List",
        )

    def example_many_columns(self) -> None:
        """Table with many columns."""
        self.io.table(
            headers=["ID", "Name", "Email", "Role", "Department", "Status"],
            data=[
                ["1", "Alice", "alice@example.com", "Dev", "Engineering", "Active"],
                ["2", "Bob", "bob@example.com", "Designer", "Design", "Active"],
                ["3", "Charlie", "charlie@example.com", "Manager", "Product", "Away"],
            ],
            title="Team Members",
        )

    def example_many_rows(self) -> None:
        """Table with many rows."""
        data = [[str(i), f"Item {i}", f"Value {i}"] for i in range(1, 16)]
        self.io.table(headers=["ID", "Name", "Value"], data=data, title="Large Dataset")

    def example_nesting(self) -> None:
        """Table with parent/child nesting."""
        from wexample_prompt.example.helpers.nesting_demo_classes import ParentTask

        self.io.table(
            headers=["Demo", "Type"],
            data=[["@color:yellow+bold{Nesting}", "Table"]],
            title="Nesting Demo",
        )
        parent = ParentTask(io=self.io)
        parent.execute(method_name="log")

    def example_simple(self) -> None:
        """Simple table."""
        self.io.table(
            headers=["ID", "Name", "Status"],
            data=[
                ["1", "Task A", "Done"],
                ["2", "Task B", "In Progress"],
                ["3", "Task C", "Pending"],
            ],
            title="Tasks",
        )

    def example_with_emojis(self) -> None:
        """Table with emojis."""
        self.io.table(
            headers=["Service", "Status", "Uptime"],
            data=[
                ["🌐 Web Server", "🟢 Online", "99.9%"],
                ["🗄️ Database", "🟢 Online", "99.8%"],
                ["📧 Mail Server", "🟡 Degraded", "95.2%"],
                ["🔍 Search", "🔴 Offline", "0%"],
            ],
            title="System Status",
        )

    def example_with_formatting(self) -> None:
        """Table with inline formatting."""
        self.io.table(
            headers=["Name", "Status", "Progress"],
            data=[
                ["Build", "@color:green+bold{✓ Success}", "100%"],
                ["Tests", "@color:yellow{⚠ Running}", "75%"],
                ["Deploy", "@color:red{✗ Failed}", "0%"],
            ],
            title="Pipeline Status",
        )

    def example_with_indentation(self) -> None:
        """Tables at different indentation levels."""
        self.io.log("@color:cyan+bold{Tables at different levels:}")

        self.io.table(
            headers=["Col1", "Col2"],
            data=[["A", "B"], ["C", "D"]],
            title="Level 0",
            indentation=0,
        )

        self.io.table(
            headers=["Col1", "Col2"],
            data=[["A", "B"], ["C", "D"]],
            title="Level 1",
            indentation=1,
        )

        self.io.table(
            headers=["Col1", "Col2"],
            data=[["A", "B"], ["C", "D"]],
            title="Level 3",
            indentation=3,
        )

    def example_with_paths(self) -> None:
        """Table with file paths."""
        self.io.table(
            headers=["File", "Size", "Modified"],
            data=[
                [
                    "@path:short{/home/user/documents/report.pdf}",
                    "2.5 MB",
                    "@time:%Y-%m-%d{1699000000}",
                ],
                [
                    "@path:short{/home/user/projects/app/main.py}",
                    "15 KB",
                    "@time:%Y-%m-%d{1699100000}",
                ],
                [
                    "@path:short{/etc/nginx/nginx.conf}",
                    "8 KB",
                    "@time:%Y-%m-%d{1699200000}",
                ],
            ],
            title="Recent Files",
        )

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Simple",
                "description": "Simple table",
                "callback": self.example_simple,
            },
            {
                "title": "With Formatting",
                "description": "Table with inline formatting (@color)",
                "callback": self.example_with_formatting,
            },
            {
                "title": "Many Columns",
                "description": "Table with many columns",
                "callback": self.example_many_columns,
            },
            {
                "title": "Many Rows",
                "description": "Table with many rows",
                "callback": self.example_many_rows,
            },
            {
                "title": "With Emojis",
                "description": "Table with emojis",
                "callback": self.example_with_emojis,
            },
            {
                "title": "With Paths",
                "description": "Table with file paths (@path, @time)",
                "callback": self.example_with_paths,
            },
            {
                "title": "Long Content",
                "description": "Table with long content that wraps",
                "callback": self.example_long_content,
            },
            {
                "title": "With Indentation",
                "description": "Tables at different indentation levels",
                "callback": self.example_with_indentation,
            },
            {
                "title": "Nesting",
                "description": "Table with parent/child nesting",
                "callback": self.example_nesting,
            },
        ]

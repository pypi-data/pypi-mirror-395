"""Example for properties response."""

from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class PropertiesExample(AbstractResponseExample):
    """Example for properties response."""

    def example_class(self, indentation: int | None = None):
        """Example using class with context."""
        from wexample_prompt.responses.data.properties_prompt_response import (
            PropertiesPromptResponse,
        )

        properties = {
            "name": "John Doe",
            "age": 30,
            "contact": {
                "email": "john@example.com",
                "phone": "123-456-7890",
            },
        }

        return PropertiesPromptResponse.create_properties(
            properties=properties,
            title="User Information",
        )

    def example_complex_structure(self) -> None:
        """Complex nested structure."""
        self.io.properties(
            properties={
                "project": {
                    "name": "MyApp",
                    "version": "2.1.0",
                    "author": {
                        "name": "John Doe",
                        "email": "john@example.com",
                    },
                },
                "dependencies": {
                    "python": "3.11+",
                    "packages": {
                        "django": "4.2.0",
                        "celery": "5.3.0",
                        "redis": "4.5.0",
                    },
                },
                "deployment": {
                    "environment": "production",
                    "servers": {
                        "web": ["web1.example.com", "web2.example.com"],
                        "db": "db.example.com",
                    },
                },
            },
            title="Project Configuration",
        )

    def example_extended(self) -> None:
        """Example using context."""
        properties = {
            "status": "success",
            "duration": "2.5s",
            "details": {
                "processed": 100,
                "failed": 0,
            },
        }
        self._class_with_methods.properties(
            properties=properties,
            title="Operation Results",
        )

    def example_long_values(self) -> None:
        """Properties with long values."""
        self.io.properties(
            properties={
                "description": "This is a very long description that contains a lot of text and will probably wrap to multiple lines depending on the terminal width",
                "path": "/home/user/very/long/path/to/some/directory/with/many/subdirectories/file.txt",
                "url": "https://example.com/very/long/url/with/many/segments/and/parameters?param1=value1&param2=value2&param3=value3",
            },
            title="Long Values",
        )

    def example_manager(self) -> None:
        """Example using IoManager directly."""
        properties = {
            "server": "localhost",
            "port": 8080,
            "config": {
                "debug": True,
                "log_level": "INFO",
            },
        }
        self.io.properties(
            properties=properties,
            title="Server Configuration",
        )

    def example_mixed_types(self) -> None:
        """Properties with different value types."""
        self.io.properties(
            properties={
                "string": "Hello World",
                "integer": 42,
                "float": 3.14159,
                "boolean": True,
                "none": None,
                "list": [1, 2, 3],
                "nested": {
                    "key1": "value1",
                    "key2": 123,
                },
            },
            title="Mixed Data Types",
        )

    def example_nested(self) -> None:
        """Properties with nested dictionaries."""
        self.io.properties(
            properties={
                "server": "production",
                "database": {
                    "host": "db.example.com",
                    "port": 5432,
                    "name": "app_db",
                },
                "cache": {
                    "type": "redis",
                    "host": "cache.example.com",
                    "ttl": 3600,
                },
            },
            title="Application Configuration",
        )

    def example_nesting(self) -> None:
        """Properties with parent/child nesting."""
        from wexample_prompt.example.helpers.nesting_demo_classes import ParentTask

        self.io.properties(
            properties={"demo": "@color:yellow+bold{Nesting Demo}"},
            title="Properties with Nesting",
        )
        parent = ParentTask(io=self.io)
        parent.execute(method_name="log")

    def example_simple(self) -> None:
        """Simple flat properties."""
        self.io.properties(
            properties={
                "name": "Alice",
                "role": "Developer",
                "status": "Active",
            },
            title="User Profile",
        )

    def example_with_emojis(self) -> None:
        """Properties with emojis."""
        self.io.properties(
            properties={
                "📊 Stats": {
                    "✅ Passed": 150,
                    "❌ Failed": 5,
                    "⏭️ Skipped": 10,
                },
                "📁 Files": {
                    "📄 Total": 1250,
                    "🔒 Protected": 45,
                    "🔓 Public": 1205,
                },
            },
            title="Test Results",
        )

    def example_with_formatting(self) -> None:
        """Properties with inline formatting."""
        self.io.properties(
            properties={
                "status": "@color:green+bold{✓ Online}",
                "uptime": "@color:cyan{99.9%}",
                "last_deploy": "@time:%Y-%m-%d{1699000000}",
                "config_file": "@path:short{/etc/app/config.yml}",
            },
            title="Server Status",
        )

    def example_with_indentation(self) -> None:
        """Properties with different indentation levels."""
        self.io.log("@color:cyan+bold{Properties at different indentation levels:}")

        # Level 0
        self.io.properties(
            properties={
                "level": "0 (no indentation)",
                "name": "Root",
            },
            title="Level 0",
            indentation=0,
        )

        # Level 1
        self.io.properties(
            properties={
                "level": "1 (indented once)",
                "name": "Child",
            },
            title="Level 1",
            indentation=1,
        )

        # Level 3
        self.io.properties(
            properties={
                "level": "3 (indented 3 times)",
                "name": "Deep Child",
            },
            title="Level 3",
            indentation=3,
        )

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Simple",
                "description": "Simple flat properties",
                "callback": self.example_simple,
            },
            {
                "title": "Nested",
                "description": "Properties with nested dictionaries",
                "callback": self.example_nested,
            },
            {
                "title": "With Formatting",
                "description": "Properties with inline formatting (@color, @path, @time)",
                "callback": self.example_with_formatting,
            },
            {
                "title": "Mixed Types",
                "description": "Properties with different value types",
                "callback": self.example_mixed_types,
            },
            {
                "title": "With Emojis",
                "description": "Properties with emojis",
                "callback": self.example_with_emojis,
            },
            {
                "title": "Long Values",
                "description": "Properties with long values that wrap",
                "callback": self.example_long_values,
            },
            {
                "title": "Nesting",
                "description": "Properties with parent/child nesting",
                "callback": self.example_nesting,
            },
            {
                "title": "With Indentation",
                "description": "Properties at different indentation levels",
                "callback": self.example_with_indentation,
            },
            {
                "title": "Complex Structure",
                "description": "Complex nested structure",
                "callback": self.example_complex_structure,
            },
        ]

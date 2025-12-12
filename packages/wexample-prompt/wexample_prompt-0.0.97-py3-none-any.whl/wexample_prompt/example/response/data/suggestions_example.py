"""Example for suggestions response."""

from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class SuggestionsExample(AbstractResponseExample):
    """Example for suggestions response."""

    def example_class(self, indentation: int | None = None):
        """Example using class with context."""
        from wexample_prompt.responses.data.suggestions_prompt_response import (
            SuggestionsPromptResponse,
        )

        message = "Here are some useful commands"
        suggestions = [
            "command1 --arg value",
            "command2",
            "command3 --flag",
        ]
        return SuggestionsPromptResponse.create_suggestions(
            message=message,
            suggestions=suggestions,
        )

    def example_extended(self) -> None:
        """Example using context."""
        message = "Here are some useful commands"
        suggestions = [
            "command1 --arg value",
            "command2",
            "command3 --flag",
        ]
        self._class_with_methods.suggestions(
            message=message,
            suggestions=suggestions,
        )

    def example_long_suggestions(self) -> None:
        """Suggestions with long commands."""
        self.io.suggestions(
            message="Docker commands:",
            suggestions=[
                "docker run -d -p 8080:80 --name myapp nginx:latest",
                "docker-compose up -d --build --remove-orphans",
                "docker exec -it myapp /bin/bash",
            ],
        )

    def example_manager(self) -> None:
        """Example using IoManager directly."""
        message = "Here are some useful commands"
        suggestions = [
            "command1 --arg value",
            "command2",
            "command3 --flag",
        ]
        self.io.suggestions(
            message=message,
            suggestions=suggestions,
        )

    def example_many_suggestions(self) -> None:
        """Many suggestions to test scrolling/wrapping."""
        self.io.suggestions(
            message="Available Python packages:",
            suggestions=[
                "django",
                "flask",
                "fastapi",
                "requests",
                "numpy",
                "pandas",
                "matplotlib",
                "scikit-learn",
                "tensorflow",
                "pytorch",
            ],
        )

    def example_nesting(self) -> None:
        """Suggestions with parent/child nesting."""
        from wexample_prompt.example.helpers.nesting_demo_classes import ParentTask

        self.io.suggestions(
            message="@color:yellow+bold{Nesting Demo}", suggestions=["demo1", "demo2"]
        )
        parent = ParentTask(io=self.io)
        parent.execute(method_name="log")

    def example_simple(self) -> None:
        """Simple suggestions."""
        self.io.suggestions(
            message="Available commands:",
            suggestions=[
                "start",
                "stop",
                "restart",
            ],
        )

    def example_with_emojis(self) -> None:
        """Suggestions with emojis."""
        self.io.suggestions(
            message="Quick actions:",
            suggestions=[
                "🚀 Deploy to production",
                "🧪 Run tests",
                "📊 View analytics",
                "🔧 Configure settings",
            ],
        )

    def example_with_formatting(self) -> None:
        """Suggestions with inline formatting."""
        self.io.suggestions(
            message="@color:cyan+bold{Git commands}:",
            suggestions=[
                "@color:green{git commit} -m 'message'",
                "@color:green{git push} origin main",
                "@color:green{git pull} --rebase",
            ],
        )

    def example_with_indentation(self) -> None:
        """Suggestions at different indentation levels."""
        self.io.log("@color:cyan+bold{Suggestions at different levels:}")

        self.io.suggestions(
            message="Level 0:", suggestions=["option1", "option2"], indentation=0
        )

        self.io.suggestions(
            message="Level 1:", suggestions=["option1", "option2"], indentation=1
        )

        self.io.suggestions(
            message="Level 3:", suggestions=["option1", "option2"], indentation=3
        )

    def example_with_paths(self) -> None:
        """Suggestions with file paths."""
        self.io.suggestions(
            message="Recent files:",
            suggestions=[
                "@path:short{/home/user/documents/report.pdf}",
                "@path:short{/home/user/projects/myapp/src/main.py}",
                "@path:short{/etc/nginx/nginx.conf}",
            ],
        )

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Simple",
                "description": "Simple suggestions",
                "callback": self.example_simple,
            },
            {
                "title": "With Formatting",
                "description": "Suggestions with inline formatting (@color)",
                "callback": self.example_with_formatting,
            },
            {
                "title": "Long Suggestions",
                "description": "Suggestions with long commands",
                "callback": self.example_long_suggestions,
            },
            {
                "title": "With Paths",
                "description": "Suggestions with file paths (@path)",
                "callback": self.example_with_paths,
            },
            {
                "title": "With Emojis",
                "description": "Suggestions with emojis",
                "callback": self.example_with_emojis,
            },
            {
                "title": "Many Suggestions",
                "description": "Many suggestions to test display",
                "callback": self.example_many_suggestions,
            },
            {
                "title": "With Indentation",
                "description": "Suggestions at different indentation levels",
                "callback": self.example_with_indentation,
            },
            {
                "title": "Nesting",
                "description": "Suggestions with parent/child nesting",
                "callback": self.example_nesting,
            },
        ]

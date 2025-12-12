"""Reusable nesting demo classes for examples."""

from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.helpers.output_message_mixin import OutputMessageMixin
from wexample_prompt.mixins.with_io_methods import WithIoMethods


@base_class
class ParentTask(OutputMessageMixin, WithIoMethods):
    """Parent task demonstrating basic nesting."""

    def execute(self, method_name: str = "log") -> None:
        """Execute parent task.

        Args:
            method_name: IO method to use (log, list, etc.)
        """
        self._output_message(method_name, "Parent task started")
        self._output_message(method_name, "Processing parent operations...")

        # Create child with automatic indentation
        child = ChildTask(parent_io_handler=self)
        child.execute(method_name)

        self._output_message(method_name, "Parent task completed")


@base_class
class ChildTask(OutputMessageMixin, WithIoMethods):
    """Child task with prefix."""

    def execute(self, method_name: str = "log") -> None:
        """Execute child task.

        Args:
            method_name: IO method to use (log, list, etc.)
        """
        self._output_message(method_name, "Child task started", prefix=True)
        self._output_message(method_name, "Processing child operations...", prefix=True)

        # Create grandchild with automatic indentation
        grandchild = GrandchildTask(parent_io_handler=self)
        grandchild.execute(method_name)

        self._output_message(method_name, "Child task completed", prefix=True)

    def get_io_context_prefix(self) -> str:
        return "child"


@base_class
class GrandchildTask(OutputMessageMixin, WithIoMethods):
    """Grandchild task with custom indentation style and prefix format."""

    def execute(self, method_name: str = "log") -> None:
        """Execute grandchild task.

        Args:
            method_name: IO method to use (log, list, etc.)
        """
        self._output_message(
            method_name, "Grandchild task started (vertical style)", prefix=True
        )
        self._output_message(
            method_name, "Processing grandchild operations...", prefix=True
        )
        self._output_message(method_name, "Grandchild task completed", prefix=True)

    def get_io_context_indentation_character(self) -> str:
        return "│"

    def get_io_context_indentation_style(self):
        from wexample_prompt.enums.indentation_style import IndentationStyle

        return IndentationStyle.VERTICAL

    def get_io_context_indentation_text_color(self):
        from wexample_prompt.enums.terminal_color import TerminalColor

        return TerminalColor.CYAN

    def get_io_context_prefix(self) -> str:
        return "grandchild"

    def get_io_context_prefix_format(self) -> str:
        return "({prefix}) "  # Custom format with parentheses

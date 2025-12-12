"""Example usage of ProgressPromptResponse."""

from __future__ import annotations

import time
from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.enums.terminal_color import TerminalColor
from wexample_prompt.example.abstract_response_example import AbstractResponseExample


def step1() -> None:
    """First step: Initialize system."""
    time.sleep(0.2)


def step2() -> None:
    """Second step: Process data."""
    time.sleep(0.4)


def step3() -> None:
    """Third step: Cleanup."""
    time.sleep(0.2)


@base_class
class ProgressExample(AbstractResponseExample):
    """Example usage of progress responses."""

    def edge_case_indentation(self) -> None:
        """Test edge cases: indentation."""
        response = self.io.progress(
            label="@color:cyan{Level 0}", total=100, indentation=0
        )
        handle = response.get_handle()
        handle.update(current=50)
        handle.finish()

        self.io.indentation = 3
        response = self.io.progress(
            label="@color:yellow{Level 3 indentation}",
            total=100,
            color=TerminalColor.MAGENTA,
        )
        handle = response.get_handle()
        handle.update(current=50)
        handle.finish()

        response = self.io.progress(
            label="@color:magenta{Level 3 + 5 indentation}", total=100, indentation=5
        )
        handle = response.get_handle()
        handle.update(current=50)
        handle.finish()
        self.io.indentation = 0

    def edge_case_limits(self) -> None:
        """Test edge cases: limits (long labels)."""
        # Very long label
        response = self.io.progress(
            label="@color:cyan{This is a very long progress label that contains lots of text and should test wrapping behavior}",
            total=100,
        )
        handle = response.get_handle()
        for cur in (25, 50, 75, 100):
            time.sleep(0.02)
            handle.update(current=cur)

    def edge_case_nesting(self) -> None:
        """Test edge cases: nested progress bars."""
        response = self.io.progress(label="@color:cyan+bold{Main Task}", total=3)
        root = response.get_handle()

        stages = ["Compilation", "Testing", "Packaging"]

        for stage_idx, stage_name in enumerate(stages):
            self.io.indentation += 1
            stage_handle = root.create_range_handle(to_step=1, virtual_total=5)

            for step in range(1, 6):
                time.sleep(0.01)
                stage_handle.advance(
                    step=1, label=f"@color:yellow{{{stage_name}: step {step}/5}}"
                )

            stage_handle.finish(label=f"@color:green+bold{{{stage_name} complete}}")
            self.io.indentation -= 1

        root.finish(label="@🟢+bold{Build complete}")

    def example_class(self, indentation: int | None = None):
        """Example using the response class directly."""
        from wexample_prompt.responses.interactive.progress_prompt_response import (
            ProgressPromptResponse,
        )

        return ProgressPromptResponse.create_progress(
            total=5,
            current=3,
            label="Processing",
        )

    def example_extended(self) -> None:
        """Example using a context class."""
        self._class_with_methods.progress(total=5, current=3, label="Processing")

    def example_manager(self) -> None:
        """Example using the IoManager."""
        self.io.progress(
            total=5,
            current=3,
            label="Processing",
        )

    def example_nested_progress(self) -> None:
        """Nested progress bars with parent/child."""
        from wexample_prompt.enums.terminal_color import TerminalColor
        from wexample_prompt.example.helpers.nesting_demo_classes import ParentTask

        response = self.io.progress(
            label="@color:yellow+bold{Main task}", total=3, color=TerminalColor.RED
        )
        handle = response.get_handle()

        for i in range(1, 4):
            time.sleep(0.1)
            handle.update(current=i, label=f"@color:yellow+bold{{Step {i}/3}}")

        handle.finish(label="@color:green+bold{Main task complete}")

        parent = ParentTask(io=self.io)
        parent.execute(method_name="log")

    def example_simple(self) -> None:
        """Simple progress bar."""
        from wexample_prompt.enums.terminal_color import TerminalColor

        response = self.io.progress(
            label="Processing", total=100, color=TerminalColor.CYAN
        )
        handle = response.get_handle()
        for i in range(0, 101, 20):
            time.sleep(0.05)
            handle.update(current=i)
        handle.finish()

    def example_with_emojis(self) -> None:
        """Progress bar with emojis."""
        from wexample_prompt.enums.terminal_color import TerminalColor

        response = self.io.progress(
            label="🚀 Deploying...", total=100, color=TerminalColor.YELLOW
        )
        handle = response.get_handle()
        for i in range(0, 101, 25):
            time.sleep(0.05)
            handle.update(current=i)
        handle.finish(label="✅ Deployment successful")

    def example_with_formatting(self) -> None:
        """Progress bar with inline formatting."""
        from wexample_prompt.enums.terminal_color import TerminalColor

        response = self.io.progress(
            label="@color:cyan+bold{Downloading} files...",
            total=100,
            color=TerminalColor.BLUE,
        )
        handle = response.get_handle()
        for i in range(0, 101, 10):
            time.sleep(0.03)
            handle.update(current=i)
        handle.finish(label="@color:green+bold{✓ Download complete}")

    def example_with_percentage(self) -> None:
        """Progress bar showing percentage instead of current/total."""
        from wexample_prompt.enums.terminal_color import TerminalColor

        response = self.io.progress(
            label="Uploading",
            total=100,
            show_percentage=True,
            color=TerminalColor.MAGENTA,
        )
        handle = response.get_handle()
        for i in range(0, 101, 10):
            time.sleep(0.03)
            handle.update(current=i)
        handle.finish(label="@color:green{Upload complete}")

    def example_with_steps(self) -> None:
        """Progress bar with step updates."""
        from wexample_prompt.enums.terminal_color import TerminalColor

        response = self.io.progress(
            label="Building project", total=5, color=TerminalColor.GREEN
        )
        handle = response.get_handle()

        steps = ["Compiling", "Linking", "Testing", "Packaging", "Done"]
        for i, step in enumerate(steps):
            time.sleep(0.1)
            handle.update(current=i + 1, label=f"@color:yellow{{{step}}}")
        handle.finish(label="@color:green+bold{Build complete}")

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Simple",
                "description": "Simple progress bar",
                "callback": self.example_simple,
            },
            {
                "title": "With Formatting",
                "description": "Progress bar with inline formatting (@color)",
                "callback": self.example_with_formatting,
            },
            {
                "title": "With Emojis",
                "description": "Progress bar with emojis",
                "callback": self.example_with_emojis,
            },
            {
                "title": "With Steps",
                "description": "Progress bar with step-by-step updates",
                "callback": self.example_with_steps,
            },
            {
                "title": "With Percentage",
                "description": "Progress bar showing percentage",
                "callback": self.example_with_percentage,
            },
            {
                "title": "Nested Progress",
                "description": "Nested progress with parent/child",
                "callback": self.example_nested_progress,
            },
            {
                "title": "Edge Case: Limits",
                "description": "Long labels in progress bars",
                "callback": self.edge_case_limits,
            },
            {
                "title": "Edge Case: Indentation",
                "description": "Progress with various indentation levels",
                "callback": self.edge_case_indentation,
            },
            {
                "title": "Edge Case: Nesting",
                "description": "Nested progress bars",
                "callback": self.edge_case_nesting,
            },
        ]

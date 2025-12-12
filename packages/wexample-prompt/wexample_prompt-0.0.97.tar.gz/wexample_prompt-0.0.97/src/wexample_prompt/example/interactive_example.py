from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.example.example import Example

from wexample_prompt.mixins.with_io_methods import WithIoMethods

if TYPE_CHECKING:
    from wexample_prompt.example.interactive_executor import InteractiveExecutor


class InteractiveExample(Example, WithIoMethods):
    def after_execute(self) -> None:
        """Hook executed after example logic."""

    def before_execute(self) -> None:
        """Hook executed before example logic."""

    def bind_executor(self, executor: InteractiveExecutor) -> None:
        object.__setattr__(self, "executor", executor)
        self.set_parent_io_handler(executor)
        self.ensure_io_manager()

    def run(self) -> None:
        """Run the example with optional pre/post hooks."""
        self.before_execute()
        self.execute()
        self.after_execute()

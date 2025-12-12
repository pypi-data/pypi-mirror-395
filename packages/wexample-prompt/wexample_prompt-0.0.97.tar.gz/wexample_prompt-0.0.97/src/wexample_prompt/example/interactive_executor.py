from __future__ import annotations

from collections.abc import Iterable

from wexample_helpers.classes.example.executor import Executor

from wexample_prompt.mixins.with_io_methods import WithIoMethods


class InteractiveExecutor(Executor, WithIoMethods):
    """
    Executor variant that leverages the prompt IO manager to render progress,
    separators, and messages while running examples.
    """

    def __attrs_post_init__(self) -> None:
        super().__attrs_post_init__()
        self.set_parent_io_handler(None)
        self.ensure_io_manager()
        self._attach_examples_to_executor()

    def execute(self) -> None:
        examples_registry = self.get_registry("examples")
        matched = False

        for index, (key, example) in enumerate(
            examples_registry.get_all().items(), start=1
        ):
            if not self._should_run_example(key, example):
                continue

            matched = True
            self.title(text=key)

            runner = getattr(example, "run", None)
            if callable(runner):
                runner()
            else:
                example.execute()

        if self.filters and not matched:
            tokens: Iterable[str] = self.filters or ()
            filters = ", ".join(tokens)
            self.warning(message=f"No examples matched filters: {filters}")

    def _attach_examples_to_executor(self) -> None:
        """
        Bind every discovered example to this executor so they share the same IO manager.
        """
        examples_registry = self.get_registry("examples")

        for example in examples_registry.get_all().values():
            # Should be InteractiveExample
            example.bind_executor(self)

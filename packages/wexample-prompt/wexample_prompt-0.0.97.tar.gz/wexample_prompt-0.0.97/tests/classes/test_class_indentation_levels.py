from __future__ import annotations

from wexample_prompt.testing.abstract_prompt_test import AbstractPromptTest


class TestIoManager(AbstractPromptTest):
    __test__ = True  # Re-enable test collection for concrete test class

    def test_class_indentation_levels(self) -> None:
        from wexample_prompt.testing.resources.classes.class_indenation_level_one import (
            ClassIndentationLevelOne,
        )

        level_one = ClassIndentationLevelOne(io=self._io)
        level_one.print_deep_log_one()

        assert level_one is not None

    def test_nested_context_indentation_values(self) -> None:
        from wexample_prompt.testing.resources.classes.class_indenation_level_one import (
            ClassIndentationLevelOne,
        )
        from wexample_prompt.testing.resources.classes.class_indenation_level_three import (
            ClassIndentationLevelThree,
        )
        from wexample_prompt.testing.resources.classes.class_indenation_level_two import (
            ClassIndentationLevelTwo,
        )

        level_one = ClassIndentationLevelOne(io=self._io)
        context_one = level_one.create_io_context()
        assert context_one.get_indentation() == 0

        level_two = ClassIndentationLevelTwo(parent_io_handler=level_one)
        context_two = level_two.create_io_context()
        assert context_two.get_indentation() == context_one.get_indentation() + 1

        level_three = ClassIndentationLevelThree(parent_io_handler=level_two)
        context_three = level_three.create_io_context()
        assert context_three.get_indentation() == context_two.get_indentation() + 1

        self._io.indentation_up()
        resolved_context = self._io.create_context(context=context_three)
        assert resolved_context is not context_three
        assert resolved_context.indentation == context_three.get_indentation() + 1
        assert context_three.get_indentation() == 2

    def test_with_io_methods_preserves_explicit_context(self) -> None:
        from unittest.mock import MagicMock

        from wexample_prompt.testing.resources.classes.class_indenation_level_one import (
            ClassIndentationLevelOne,
        )
        from wexample_prompt.testing.resources.classes.class_indenation_level_two import (
            ClassIndentationLevelTwo,
        )

        level_one = ClassIndentationLevelOne(io=self._io)
        level_two = ClassIndentationLevelTwo(parent_io_handler=level_one)

        explicit_context = level_two.create_io_context()

        mock_log = MagicMock(return_value=None)
        level_two.io.log = mock_log

        level_two.log(message="test message", context=explicit_context)

        assert mock_log.call_count == 1
        _, kwargs = mock_log.call_args
        assert kwargs["context"] is explicit_context

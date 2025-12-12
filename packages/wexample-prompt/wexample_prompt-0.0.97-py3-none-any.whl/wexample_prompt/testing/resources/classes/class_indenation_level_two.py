from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.mixins.with_io_methods import WithIoMethods

if TYPE_CHECKING:
    pass


@base_class
class ClassIndentationLevelTwo(WithIoMethods):
    def print_deep_log_two(self) -> None:
        from wexample_prompt.enums.verbosity_level import VerbosityLevel
        from wexample_prompt.testing.resources.classes.class_indenation_level_three import (
            ClassIndentationLevelThree,
        )

        io_context = self.create_io_context()
        self.log(message="test deep log two", context=io_context)

        self.log(
            message="test deep log two",
            context=self.create_io_context(colorized=False),
        )

        level_three = ClassIndentationLevelThree(parent_io_handler=self)

        level_three.print_deep_log_three()

        self.separator("Try class level three in quiet mode")
        io_context.verbosity = VerbosityLevel.QUIET

        level_three = ClassIndentationLevelThree(parent_io_handler=self)

        level_three.print_deep_log_three()

        io_context.verbosity = VerbosityLevel.DEFAULT
        self.separator("Quiet end")

from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.mixins.with_io_manager import WithIoManager


@base_class
class ClassIndentationLevelOne(WithIoManager):
    def print_deep_log_one(self) -> None:
        from wexample_helpers.helpers.string import string_generate_lorem_ipsum

        from wexample_prompt.testing.resources.classes.class_indenation_level_two import (
            ClassIndentationLevelTwo,
        )

        self.io.log("test deep log one", context=self.create_io_context())
        self.io.log(string_generate_lorem_ipsum(1000), context=self.create_io_context())

        level_two = ClassIndentationLevelTwo(parent_io_handler=self)

        level_two.print_deep_log_two()

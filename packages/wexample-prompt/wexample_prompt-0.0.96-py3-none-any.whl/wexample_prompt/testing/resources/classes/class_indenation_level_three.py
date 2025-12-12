from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.mixins.with_io_methods import WithIoMethods

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_color import TerminalColor


@base_class
class ClassIndentationLevelThree(WithIoMethods, BaseClass):
    def get_io_context_indentation_character(self) -> str | None:
        return "·"

    def get_io_context_indentation_color(self) -> TerminalColor | None:
        from wexample_prompt.enums.terminal_color import TerminalColor

        return TerminalColor.BLUE

    def print_deep_log_three(self) -> None:
        from wexample_helpers.helpers.string import string_generate_lorem_ipsum

        self.io.log(message="test deep three LOG", context=self.create_io_context())

        self.log(
            message="test deep three LOG (shortcut)",
        )

        self.log(
            message="test deep three LOG (no color)",
            context=self.create_io_context(),
            colorized=False,
        )

        io_context = self.create_io_context()
        io_context.width = 100

        self.separator(
            label="Text width management",
            context=io_context,
        )

        self.io.log(string_generate_lorem_ipsum(1000), context=io_context)

        self.log(string_generate_lorem_ipsum(200), context=io_context, width=60)

        self.separator(width=60)

        self.echo(message="test deep three ECHO", context=self.create_io_context())

        self.echo(string_generate_lorem_ipsum(200), context=io_context, width=60)

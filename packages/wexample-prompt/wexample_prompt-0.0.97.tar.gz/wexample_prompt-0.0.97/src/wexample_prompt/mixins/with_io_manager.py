from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.terminal_bg_color import TerminalBgColor
    from wexample_prompt.enums.terminal_color import TerminalColor


@base_class
class WithIoManager(BaseClass):
    io: IoManager | None = public_field(
        default=None,
        description="The optional IO manager that could be shared with a parent.",
    )
    parent_io_handler: WithIoManager | None = public_field(
        default=None,
        description="A parent class that may share its IO and context (ex shared verbosity or indentation level).",
    )
    _owns_io: bool = private_field(
        default=False,
        description="Flag indicating whether this instance created its own IO manager.",
    )

    def __attrs_post_init__(self) -> None:
        self._execute_super_attrs_post_init_if_exists()

        if self.parent_io_handler is not None:
            self.set_parent_io_handler(self.parent_io_handler)
        elif self.io is not None:
            self._owns_io = False

    def create_io_context(self, **kwargs) -> PromptContext:
        from wexample_prompt.common.prompt_context import PromptContext

        io = self.ensure_io_manager()
        try:
            parent_handler = object.__getattribute__(self, "parent_io_handler")
        except AttributeError:
            parent_handler = None
        parent_context = (
            parent_handler.create_io_context() if parent_handler is not None else None
        )

        defaults = {
            "parent_context": parent_context,
            "indentation": self.get_io_context_indentation(
                parent_context=parent_context
            ),
            "indentation_character": self.get_io_context_indentation_character(),
            "indentation_text_color": self.get_io_context_indentation_text_color(),
            "indentation_bg_color": self.get_io_context_indentation_bg_color(),
            "indentation_style": self.get_io_context_indentation_style(),
            "colorized": self.get_io_context_colorized()
            or (
                parent_context.colorized
                if parent_context is not None
                else PromptContext.DEFAULT_COLORIZED
            ),
            "verbosity": (
                parent_context.verbosity
                if parent_context is not None
                else PromptContext.DEFAULT_VERBOSITY
            ),
            "width": self.get_io_context_indentation_width()
            or (parent_context.width if parent_context is not None else None)
            or (io.terminal_width if io else None),
        }

        defaults.update(kwargs)

        return PromptContext.create_from_kwargs(kwargs=defaults)

    def ensure_io_manager(self) -> IoManager:
        try:
            current_io = object.__getattribute__(self, "io")
        except AttributeError:
            current_io = None
        if current_io is not None:
            return current_io

        try:
            parent_handler = object.__getattribute__(self, "parent_io_handler")
        except AttributeError:
            parent_handler = None
        if parent_handler is not None:
            inherited = parent_handler.ensure_io_manager()
            object.__setattr__(self, "io", inherited)
            object.__setattr__(self, "_owns_io", False)
            return inherited

        created = self._create_io_manager()
        object.__setattr__(self, "io", created)
        object.__setattr__(self, "_owns_io", True)
        return created

    def get_io_context_colorized(self) -> bool | None:
        return None

    def get_io_context_indentation(
        self, *, parent_context: PromptContext | None = None
    ) -> int:
        if parent_context is not None:
            return parent_context.get_indentation() + 1

        try:
            parent_handler = object.__getattribute__(self, "parent_io_handler")
        except AttributeError:
            parent_handler = None
        if parent_handler is not None:
            context = parent_handler.create_io_context()
            return context.get_indentation() + 1

        return 0

    def get_io_context_indentation_bg_color(self) -> TerminalBgColor | None:
        return None

    def get_io_context_indentation_character(self) -> str | None:
        return None

    def get_io_context_indentation_style(self) -> None:
        return None  # Will inherit from parent or use default

    def get_io_context_indentation_text_color(self) -> TerminalColor | None:
        return None

    def get_io_context_indentation_width(self) -> int | None:
        return None

    def get_io_context_prefix(self) -> str | None:
        """Get the prefix to prepend to messages (e.g., '[child]')."""
        return None

    def get_io_context_prefix_format(self) -> str:
        """Get the format string for the prefix. Use {prefix} as placeholder.
        Default: '[{prefix}] '
        """
        return "[{prefix}] "

    def set_parent_io_handler(self, parent: WithIoManager | None) -> None:
        object.__setattr__(self, "parent_io_handler", parent)
        if parent is not None:
            inherited = parent.ensure_io_manager()
            object.__setattr__(self, "io", inherited)
            object.__setattr__(self, "_owns_io", False)
        else:
            object.__setattr__(self, "parent_io_handler", None)

    def use_io_manager(self, io: IoManager) -> IoManager:
        object.__setattr__(self, "io", io)
        object.__setattr__(self, "_owns_io", False)
        return io

    def _create_io_manager(self) -> IoManager:
        from wexample_prompt.common.io_manager import IoManager

        return IoManager()

    # Backwards compatibility for previous API
    def _init_io_manager(self) -> IoManager:
        return self.ensure_io_manager()

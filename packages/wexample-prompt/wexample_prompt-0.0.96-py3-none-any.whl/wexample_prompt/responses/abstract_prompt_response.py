from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import TYPE_CHECKING, Any

import attrs
from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.mixin.has_snake_short_class_name_class_mixin import (
    HasSnakeShortClassNameClassMixin,
)
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.enums.verbosity_level import VerbosityLevel

if TYPE_CHECKING:
    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.example.abstract_response_example import (
        AbstractResponseExample,
    )


@base_class
class AbstractPromptResponse(HasSnakeShortClassNameClassMixin):
    """Abstract base class for all prompt responses."""

    lines: list[PromptResponseLine] = public_field(
        factory=list,
        description="The list of lines of the response content",
    )
    verbosity: VerbosityLevel | None = public_field(
        default=None,
        description="The context verbosity, saying which response to render or not",
    )
    _rendered_content: str | None = None

    @classmethod
    def apply_prefix_to_kwargs(
        cls, prefix: str, args: tuple, kwargs: dict
    ) -> tuple[tuple, dict]:
        """Apply prefix to the appropriate parameters in kwargs/args.

        This method should be overridden by subclasses to handle their specific parameters.
        Default implementation does nothing.

        Args:
            prefix: The formatted prefix to apply (e.g., "[child] ")
            args: Positional arguments
            kwargs: Keyword arguments

        Returns:
            Tuple of (modified_args, modified_kwargs)
        """
        return args, kwargs

    @classmethod
    def get_class_name_suffix(cls) -> str | None:
        return "PromptResponse"

    @classmethod
    @abstract_method
    def get_example_class(cls) -> type[AbstractResponseExample]:
        cls._raise_not_implemented_error()

    @classmethod
    def rebuild_context_for_kwargs(
        cls,
        parent_kwargs: Kwargs,
        context: PromptContext | None = None,
    ) -> PromptContext:
        from wexample_prompt.common.prompt_context import PromptContext

        if not parent_kwargs:
            # Keep same context as we don't see a reason to recreate one.
            return context or PromptContext.create_from_kwargs({})

        if context:
            kwargs = PromptContext.create_kwargs_from_context(context=context)
            kwargs.update(parent_kwargs)
            parent_kwargs = kwargs

        return PromptContext.create_from_parent_context_and_kwargs(
            parent_context=context.parent_context if context else None,
            kwargs=parent_kwargs,
        )

    @classmethod
    def _create(
        cls: AbstractPromptResponse,
        lines: list[PromptResponseLine],
        **kwargs,
    ) -> AbstractPromptResponse:
        """Create a new response with the given lines."""
        return cls(lines=lines, **kwargs)

    @property
    def rendered_content(self) -> str | None:
        return self._rendered_content

    def clone(self, **overrides) -> AbstractPromptResponse:
        """Clone this response and all its child objects safely."""
        payload = self._clone_export()
        payload.update(overrides)
        return self.__class__(**payload)

    def render(self, context: PromptContext | None = None) -> str | None:
        """Render the complete response."""
        from wexample_prompt.common.prompt_context import PromptContext

        context = PromptContext.create_if_none(context=context)

        if not self._verbosity_context_allows_display(context=context):
            return None

        self._rendered_content = "\n".join(line.render(context) for line in self.lines)
        return self._rendered_content

    def reset(self) -> None:
        self._rendered_content = None

    def _clone_export(
        self,
        *,
        shallow: bool = False,
        per_field_copy: Mapping[str, Callable[[Any], Any]] | None = None,
    ) -> dict:
        from wexample_helpers.enums.field_visibility import FieldVisibility
        from wexample_helpers.helpers.variable import copy_shallow

        out = {}
        for a in attrs.fields(self.__class__):
            if not a.init:
                continue
            vis = a.metadata.get("visibility")
            if vis is not None and vis != FieldVisibility.PUBLIC.value:
                continue
            if a.name.startswith("_"):
                continue

            val = getattr(self, a.name)
            init_name = getattr(a, "alias", None) or a.name

            if per_field_copy and init_name in per_field_copy:
                out[init_name] = per_field_copy[init_name](val)
            elif shallow:
                out[init_name] = copy_shallow(val)
            else:
                out[init_name] = val
        return out

    def _verbosity_context_allows_display(self, context: PromptContext) -> bool:
        return (
            self.verbosity is None
            or context.verbosity is None
            or self.verbosity <= context.verbosity
        )

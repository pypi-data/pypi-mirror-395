from __future__ import annotations

from typing import TYPE_CHECKING, Any

from wexample_helpers.classes.abstract_method import abstract_method
from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )


@base_class
class AbstractPromptOutputHandler(BaseClass):
    @abstract_method
    def erase(
        self,
        response: AbstractPromptResponse,
    ) -> Any:
        self._raise_not_implemented_error()

    @abstract_method
    def print(
        self,
        response: AbstractPromptResponse,
        context: PromptContext | None = None,
    ) -> Any:
        self._raise_not_implemented_error()

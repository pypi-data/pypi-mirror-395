from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.common.prompt_response_line import PromptResponseLine
from wexample_prompt.enums.choice import ChoiceValue

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_response_line import PromptResponseLine
    from wexample_prompt.enums.choice import ChoiceValue


@base_class
class Choice(BaseClass):
    line: PromptResponseLine = public_field(
        description="The line that renders the choice"
    )
    title: str = public_field(description="The title of the choice")
    value: str | int | ChoiceValue = public_field(description="The value of the choice")

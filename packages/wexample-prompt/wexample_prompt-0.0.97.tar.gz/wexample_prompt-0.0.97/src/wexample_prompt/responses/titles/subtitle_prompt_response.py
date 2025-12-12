from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.responses.titles.abstract_title_response import (
    AbstractTitleResponse,
)

if TYPE_CHECKING:
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.example.abstract_response_example import (
        AbstractResponseExample,
    )


@base_class
class SubtitlePromptResponse(AbstractTitleResponse):
    DEFAULT_PREFIX = "  ❯"

    @classmethod
    def create_subtitle(
        cls: SubtitlePromptResponse,
        text: str,
        color: TerminalColor | None = None,
        character: str | None = None,
        width: int | None = None,
        verbosity: VerbosityLevel | None = None,
        **kwargs,
    ) -> SubtitlePromptResponse:
        from wexample_prompt.enums.terminal_color import TerminalColor

        return super()._create_title(
            text=text,
            color=color or TerminalColor.BLUE,
            character=character,
            width=width,
            verbosity=verbosity,
            **kwargs,
        )

    @classmethod
    def get_example_class(cls) -> type[AbstractResponseExample]:
        from wexample_prompt.example.response.titles.subtitle_example import (
            SubtitleExample,
        )

        return SubtitleExample

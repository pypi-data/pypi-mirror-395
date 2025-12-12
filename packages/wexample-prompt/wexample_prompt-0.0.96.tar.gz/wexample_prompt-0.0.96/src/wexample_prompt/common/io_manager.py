from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.enums.verbosity_level import VerbosityLevel
from wexample_prompt.mixins.response.data.list_prompt_response_manager_mixin import (
    ListPromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.data.multiple_prompt_response_manager_mixin import (
    MultiplePromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.data.properties_prompt_response_manager_mixin import (
    PropertiesPromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.data.suggestions_prompt_response_manager_mixin import (
    SuggestionsPromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.data.table_prompt_response_manager_mixin import (
    TablePromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.data.tree_prompt_response_manager_mixin import (
    TreePromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.echo_prompt_response_manager_mixin import (
    EchoPromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.interactive.choice_prompt_response_manager_mixin import (
    ChoicePromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.interactive.confirm_prompt_response_manager_mixin import (
    ConfirmPromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.interactive.file_picker_prompt_response_manager_mixin import (
    FilePickerPromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.interactive.progress_prompt_response_manager_mixin import (
    ProgressPromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.interactive.screen_prompt_response_manager_mixin import (
    ScreenPromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.log_prompt_response_manager_mixin import (
    LogPromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.messages.debug_prompt_response_manager_mixin import (
    DebugPromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.messages.error_prompt_response_manager_mixin import (
    ErrorPromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.messages.failure_prompt_response_manager_mixin import (
    FailurePromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.messages.info_prompt_response_manager_mixin import (
    InfoPromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.messages.success_prompt_response_manager_mixin import (
    SuccessPromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.messages.task_prompt_response_manager_mixin import (
    TaskPromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.messages.warning_prompt_response_manager_mixin import (
    WarningPromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.titles.separator_prompt_response_manager_mixin import (
    SeparatorPromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.titles.subtitle_prompt_response_manager_mixin import (
    SubtitlePromptResponseManagerMixin,
)
from wexample_prompt.mixins.response.titles.title_prompt_response_manager_mixin import (
    TitlePromptResponseManagerMixin,
)
from wexample_prompt.mixins.with_indentation import WithIndentation

if TYPE_CHECKING:
    from wexample_prompt.common.prompt_context import PromptContext
    from wexample_prompt.enums.verbosity_level import VerbosityLevel
    from wexample_prompt.output.abstract_prompt_output_handler import (
        AbstractPromptOutputHandler,
    )
    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )


@base_class
class IoManager(
    # Basics
    EchoPromptResponseManagerMixin,
    LogPromptResponseManagerMixin,
    # Messages
    InfoPromptResponseManagerMixin,
    DebugPromptResponseManagerMixin,
    WarningPromptResponseManagerMixin,
    ErrorPromptResponseManagerMixin,
    FailurePromptResponseManagerMixin,
    SuccessPromptResponseManagerMixin,
    TaskPromptResponseManagerMixin,
    # Titles
    SeparatorPromptResponseManagerMixin,
    TitlePromptResponseManagerMixin,
    SubtitlePromptResponseManagerMixin,
    # Data
    ListPromptResponseManagerMixin,
    MultiplePromptResponseManagerMixin,
    PropertiesPromptResponseManagerMixin,
    SuggestionsPromptResponseManagerMixin,
    TablePromptResponseManagerMixin,
    TreePromptResponseManagerMixin,
    # Interactive
    ChoicePromptResponseManagerMixin,
    FilePickerPromptResponseManagerMixin,
    ProgressPromptResponseManagerMixin,
    ScreenPromptResponseManagerMixin,
    ConfirmPromptResponseManagerMixin,
    # Parent classes
    WithIndentation,
    BaseClass,
):
    default_context_verbosity: VerbosityLevel = public_field(
        default=VerbosityLevel.DEFAULT,
        description="The overall verbosity level used in contexts.",
    )
    default_response_verbosity: VerbosityLevel = public_field(
        default=VerbosityLevel.DEFAULT,
        description="The default verbosity for every generated message.",
    )
    output: AbstractPromptOutputHandler = public_field(
        default=None,
        description="Manages what to do with the generated output (print, or store), "
        "by default print to stdout",
    )
    _terminal_width: int = private_field(
        default=None, description="The terminal with cached value."
    )

    def __attrs_post_init__(self) -> None:
        self._init_output()

    @classmethod
    def get_response_types(cls) -> list[type[AbstractPromptResponse]]:
        from wexample_prompt.responses.data.list_prompt_response import (
            ListPromptResponse,
        )
        from wexample_prompt.responses.data.multiple_prompt_response import (
            MultiplePromptResponse,
        )
        from wexample_prompt.responses.data.properties_prompt_response import (
            PropertiesPromptResponse,
        )
        from wexample_prompt.responses.data.suggestions_prompt_response import (
            SuggestionsPromptResponse,
        )
        from wexample_prompt.responses.data.table_prompt_response import (
            TablePromptResponse,
        )
        from wexample_prompt.responses.data.tree_prompt_response import (
            TreePromptResponse,
        )
        from wexample_prompt.responses.echo_prompt_response import EchoPromptResponse
        from wexample_prompt.responses.interactive.choice_prompt_response import (
            ChoicePromptResponse,
        )
        from wexample_prompt.responses.interactive.confirm_prompt_response import (
            ConfirmPromptResponse,
        )
        from wexample_prompt.responses.interactive.file_picker_prompt_response import (
            FilePickerPromptResponse,
        )
        from wexample_prompt.responses.interactive.progress_prompt_response import (
            ProgressPromptResponse,
        )
        from wexample_prompt.responses.interactive.screen_prompt_response import (
            ScreenPromptResponse,
        )
        from wexample_prompt.responses.log_prompt_response import LogPromptResponse
        from wexample_prompt.responses.messages.debug_prompt_response import (
            DebugPromptResponse,
        )
        from wexample_prompt.responses.messages.error_prompt_response import (
            ErrorPromptResponse,
        )
        from wexample_prompt.responses.messages.failure_prompt_response import (
            FailurePromptResponse,
        )
        from wexample_prompt.responses.messages.info_prompt_response import (
            InfoPromptResponse,
        )
        from wexample_prompt.responses.messages.success_prompt_response import (
            SuccessPromptResponse,
        )
        from wexample_prompt.responses.messages.task_prompt_response import (
            TaskPromptResponse,
        )
        from wexample_prompt.responses.messages.warning_prompt_response import (
            WarningPromptResponse,
        )
        from wexample_prompt.responses.titles.separator_prompt_response import (
            SeparatorPromptResponse,
        )
        from wexample_prompt.responses.titles.subtitle_prompt_response import (
            SubtitlePromptResponse,
        )
        from wexample_prompt.responses.titles.title_prompt_response import (
            TitlePromptResponse,
        )

        return [
            # Basics
            EchoPromptResponse,
            LogPromptResponse,
            InfoPromptResponse,
            # Messages
            DebugPromptResponse,
            WarningPromptResponse,
            ErrorPromptResponse,
            FailurePromptResponse,
            SuccessPromptResponse,
            TaskPromptResponse,
            # Titles
            SeparatorPromptResponse,
            TitlePromptResponse,
            SubtitlePromptResponse,
            # Data
            ListPromptResponse,
            MultiplePromptResponse,
            PropertiesPromptResponse,
            SuggestionsPromptResponse,
            TablePromptResponse,
            TreePromptResponse,
            # Interactive
            ChoicePromptResponse,
            FilePickerPromptResponse,
            ProgressPromptResponse,
            ScreenPromptResponse,
            ConfirmPromptResponse,
        ]

    @property
    def terminal_width(self) -> int:
        if self._terminal_width is None:
            self.reload_terminal_width()
        return self._terminal_width

    def create_context(self, context: PromptContext | None = None) -> PromptContext:
        from wexample_prompt.common.prompt_context import PromptContext

        base_context = PromptContext.create_if_none(context=context)
        context_kwargs = PromptContext.create_kwargs_from_context(context=base_context)

        base_indentation_length = (
            context_kwargs.get("indentation_length") or self.indentation_length
        )
        base_indentation = context_kwargs.get("indentation") or 0
        total_indentation = base_indentation + self.indentation

        context_kwargs["colorized"] = base_context.colorized
        context_kwargs["formatting"] = base_context.formatting
        context_kwargs["indentation"] = total_indentation
        context_kwargs["indentation_length"] = base_indentation_length
        verbosity = context_kwargs.get("verbosity")
        context_kwargs["verbosity"] = (
            verbosity if verbosity is not None else self.default_context_verbosity
        )

        width = context_kwargs.get("width")
        if width is None:
            context_kwargs["width"] = self.terminal_width - (
                total_indentation * base_indentation_length
            )

        return PromptContext.create_from_parent_context_and_kwargs(
            parent_context=base_context.parent_context,
            kwargs=context_kwargs,
        )

    def erase_response(
        self,
        response: AbstractPromptResponse,
    ) -> None:
        self.output.erase(response=response)

    def print_response(
        self,
        response: AbstractPromptResponse,
        context: PromptContext | None = None,
    ) -> AbstractPromptResponse:
        # Quiet mode.
        if response.verbosity == VerbosityLevel.QUIET:
            return response

        self.output.print(
            response=response, context=self.create_context(context=context)
        )

        return response

    def reload_terminal_width(self) -> int:
        import shutil

        self._terminal_width = shutil.get_terminal_size().columns
        return self._terminal_width

    def _init_output(self) -> None:
        from wexample_prompt.output.prompt_stdout_output_handler import (
            PromptStdoutOutputHandler,
        )

        self.output = (
            self.output if (self.output is not None) else PromptStdoutOutputHandler()
        )

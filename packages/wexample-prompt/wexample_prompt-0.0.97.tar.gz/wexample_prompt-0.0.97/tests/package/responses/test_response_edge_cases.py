from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from wexample_prompt.mixins.with_io_methods import WithIoMethods

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.common.prompt_context import PromptContext


LONG_TEXT = (
    "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque "
    "habitant morbi tristique senectus et netus et malesuada fames ac turpis "
    "egestas. "
) * 3


def test_data_responses_handle_long_text() -> None:
    from wexample_prompt.responses.data.list_prompt_response import ListPromptResponse
    from wexample_prompt.responses.data.multiple_prompt_response import (
        MultiplePromptResponse,
    )
    from wexample_prompt.responses.data.properties_prompt_response import (
        PropertiesPromptResponse,
    )
    from wexample_prompt.responses.data.suggestions_prompt_response import (
        SuggestionsPromptResponse,
    )
    from wexample_prompt.responses.data.table_prompt_response import TablePromptResponse
    from wexample_prompt.responses.data.tree_prompt_response import TreePromptResponse
    from wexample_prompt.responses.log_prompt_response import LogPromptResponse
    from wexample_prompt.responses.messages.info_prompt_response import (
        InfoPromptResponse,
    )

    responses = [
        ListPromptResponse.create_list(items=[LONG_TEXT, LONG_TEXT]),
        PropertiesPromptResponse.create_properties(properties={"key": LONG_TEXT}),
        SuggestionsPromptResponse.create_suggestions(
            message=LONG_TEXT, suggestions=[LONG_TEXT, LONG_TEXT]
        ),
        TablePromptResponse.create_table(
            headers=["A", "B"], data=[[LONG_TEXT, LONG_TEXT]]
        ),
        TreePromptResponse.create_tree(data={"root": {"child": LONG_TEXT}}),
        MultiplePromptResponse.create_multiple(
            responses=[
                LogPromptResponse.create_log(message=LONG_TEXT),
                InfoPromptResponse.create_info(message=LONG_TEXT),
            ]
        ),
    ]

    for response in responses:
        rendered = response.render(context=_make_context())
        assert rendered is not None
        assert LONG_TEXT.split()[0] in rendered


def test_interactive_responses_accept_predefined_answers(tmp_path) -> None:
    from wexample_prompt.enums.choice import FilePickerMode
    from wexample_prompt.responses.interactive.confirm_prompt_response import (
        ConfirmPromptResponse,
    )

    io = _make_io()

    # Choice
    response = io.choice(
        question=LONG_TEXT,
        choices=["alpha", "beta"],
        predefined_answer="alpha",
        reset_on_finish=True,
    )
    assert response.get_answer() == "alpha"

    # Confirm
    response = io.confirm(
        question=LONG_TEXT,
        choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
        predefined_answer="yes",
        reset_on_finish=True,
    )
    assert response.get_answer() == "yes"

    # File picker (point to temporary directory)
    file_path = tmp_path / "sample.txt"
    file_path.write_text("dummy")
    response = io.file_picker(
        question=LONG_TEXT,
        base_dir=str(tmp_path),
        mode=FilePickerMode.FILES,
        allow_parent_selection=True,
        predefined_answer=file_path.name,
        reset_on_finish=True,
    )
    assert response.get_answer() == file_path.name

    # Progress (ensure label with long text fits)
    response = io.progress(label=LONG_TEXT, total=10, current=5, print_response=False)
    rendered = response.render(context=_make_context())
    assert rendered is not None
    assert LONG_TEXT.split()[0] in rendered


def test_message_responses_handle_long_text() -> None:
    from wexample_prompt.responses.echo_prompt_response import EchoPromptResponse
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

    context = _make_context()
    cases: list[tuple[Callable[..., object], dict[str, object]]] = [
        (EchoPromptResponse.create_echo, {"message": LONG_TEXT}),
        (LogPromptResponse.create_log, {"message": LONG_TEXT}),
        (InfoPromptResponse.create_info, {"message": LONG_TEXT}),
        (DebugPromptResponse.create_debug, {"message": LONG_TEXT}),
        (WarningPromptResponse.create_warning, {"message": LONG_TEXT}),
        (ErrorPromptResponse.create_error, {"message": LONG_TEXT}),
        (FailurePromptResponse.create_failure, {"message": LONG_TEXT}),
        (SuccessPromptResponse.create_success, {"message": LONG_TEXT}),
        (TaskPromptResponse.create_task, {"message": LONG_TEXT}),
    ]

    for factory, kwargs in cases:
        rendered = factory(**kwargs).render(context=context)
        assert rendered is not None
        assert LONG_TEXT.split()[0] in rendered


def test_title_responses_handle_long_text() -> None:
    from wexample_prompt.responses.titles.separator_prompt_response import (
        SeparatorPromptResponse,
    )
    from wexample_prompt.responses.titles.subtitle_prompt_response import (
        SubtitlePromptResponse,
    )
    from wexample_prompt.responses.titles.title_prompt_response import (
        TitlePromptResponse,
    )

    rendered = TitlePromptResponse.create_title(text=LONG_TEXT).render(
        context=_make_context()
    )
    assert rendered is not None
    assert LONG_TEXT.split()[0] in rendered

    rendered = SubtitlePromptResponse.create_subtitle(text=LONG_TEXT).render(
        context=_make_context(1)
    )
    assert rendered is not None
    assert LONG_TEXT.split()[0] in rendered

    rendered = SeparatorPromptResponse.create_separator(label=LONG_TEXT).render(
        context=_make_context()
    )
    assert rendered is not None
    assert LONG_TEXT.split()[0] in rendered


def test_with_io_methods_propagates_indentation() -> None:
    class ParentWorker(WithIoMethods):
        def __attrs_post_init__(self) -> None:
            self.ensure_io_manager()

    class ChildWorker(WithIoMethods):
        def __attrs_post_init__(self) -> None:
            pass

    parent = ParentWorker()
    child = ChildWorker()
    child.set_parent_io_handler(parent)

    parent_context = parent.create_io_context()
    child_context = child.create_io_context()

    assert child_context.get_indentation() == parent_context.get_indentation() + 1

    parent.ensure_io_manager().indentation_up()
    deeper_context = child.create_io_context()
    assert deeper_context.get_indentation() == child_context.get_indentation()


def _make_context(indentation: int = 0) -> PromptContext:
    from wexample_prompt.common.prompt_context import PromptContext

    return PromptContext(indentation=indentation, formatting=True)


def _make_io() -> IoManager:
    from wexample_prompt.common.io_manager import IoManager
    from wexample_prompt.output.prompt_buffer_output_handler import (
        PromptBufferOutputHandler,
    )

    return IoManager(output=PromptBufferOutputHandler())


def _render(response) -> str:
    rendered = response.render(context=_make_context())
    assert rendered is not None
    return rendered

from __future__ import annotations


def test_progress_label_markup_renders_without_tokens() -> None:
    from wexample_prompt.responses.interactive.progress_prompt_response import (
        ProgressPromptResponse,
    )

    response = ProgressPromptResponse.create_progress(
        total=100,
        current=50,
        width=40,
        label="@color:magenta+bold{Stylish label}",
    )

    rendered = response.render()

    assert rendered is not None
    assert "@color" not in rendered
    assert "Stylish label" in rendered

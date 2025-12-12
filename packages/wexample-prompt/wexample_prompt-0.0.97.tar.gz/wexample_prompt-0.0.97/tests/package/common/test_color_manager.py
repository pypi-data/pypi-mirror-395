from __future__ import annotations


def test_build_prefix_empty() -> None:
    from wexample_prompt.common.color_manager import ColorManager

    assert ColorManager.build_prefix() == ""
    assert ColorManager.build_prefix(color=None, styles=[]) == ""


def test_build_prefix_with_color_and_styles() -> None:
    from wexample_prompt.common.color_manager import ColorManager
    from wexample_prompt.enums.terminal_color import TerminalColor
    from wexample_prompt.enums.text_style import TextStyle

    prefix = ColorManager.build_prefix(
        color=TerminalColor.RED, styles=[TextStyle.BOLD, TextStyle.UNDERLINE]
    )
    assert prefix.startswith(str(TerminalColor.RED))
    # Contains bold and underline codes (order of join preserved)
    assert "\033[1m" in prefix
    assert "\033[4m" in prefix
    # No reset in prefix
    assert "\033[0m" not in prefix

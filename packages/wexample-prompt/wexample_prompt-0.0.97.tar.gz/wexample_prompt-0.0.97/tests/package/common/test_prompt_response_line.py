from __future__ import annotations


class TestPromptResponseLine:
    def test_color_markup_with_styles_and_nesting(self) -> None:
        """Combined color + styles and nested directives should be parsed recursively."""
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.enums.terminal_color import TerminalColor
        from wexample_prompt.enums.text_style import TextStyle

        text = "@color:blue+bold{Outer @color:yellow+underline{Inner}\nNext}"
        lines = PromptResponseLine.create_from_string(text)

        assert len(lines) == 2
        outer_seg = lines[0].segments[0]
        inner_seg = lines[0].segments[1]

        assert outer_seg.text == "Outer "
        assert outer_seg.color is TerminalColor.BLUE
        assert TextStyle.BOLD in outer_seg.styles

        assert inner_seg.text == "Inner"
        assert inner_seg.color is TerminalColor.YELLOW
        assert TextStyle.BOLD in inner_seg.styles
        assert TextStyle.UNDERLINE in inner_seg.styles

        next_line_seg = lines[1].segments[0]
        assert next_line_seg.text == "Next"
        assert next_line_seg.color is TerminalColor.BLUE
        assert TextStyle.BOLD in next_line_seg.styles

    def test_create_basic_line(self) -> None:
        """Test creating a basic line with single segment."""
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment

        segment = PromptResponseSegment(text="Hello")
        line = PromptResponseLine(segments=[segment])
        assert len(line.segments) == 1
        assert line.segments[0].text == "Hello"

    def test_create_from_string_parses_color_markup(self) -> None:
        """Styled markup should produce distinct segments with proper colors."""
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.enums.terminal_color import TerminalColor

        text = "Hello @color:red{World}"
        lines = PromptResponseLine.create_from_string(text)

        assert len(lines) == 1
        assert len(lines[0].segments) == 2
        assert lines[0].segments[0].text == "Hello "
        assert lines[0].segments[0].color is None
        assert lines[0].segments[1].text == "World"
        assert lines[0].segments[1].color is TerminalColor.RED

    def test_create_from_string_splits_multiline(self) -> None:
        """Multi-line input should be split into distinct PromptResponseLine without embedded newlines."""
        from wexample_prompt.common.prompt_context import PromptContext
        from wexample_prompt.common.prompt_response_line import PromptResponseLine

        text = "Line A\nLine B\nLine C"
        lines = PromptResponseLine.create_from_string(text)

        assert len(lines) == 3
        rendered = [ln.render(context=PromptContext()) for ln in lines]
        assert rendered == ["Line A", "Line B", "Line C"]
        # No segment should contain newlines
        for ln in lines:
            for seg in ln.segments:
                assert "\n" not in seg.text

    def test_emoji_color_mapping(self) -> None:
        """Emoji tokens map to their corresponding terminal colors."""
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.enums.terminal_color import TerminalColor

        text = "@🔵{Blue}@🟢{Green}@🔴+bold{Red}"
        lines = PromptResponseLine.create_from_string(text)

        assert len(lines) == 1
        segments = lines[0].segments
        assert len(segments) == 3
        assert segments[0].color is TerminalColor.BLUE
        assert segments[1].color is TerminalColor.GREEN
        assert segments[2].color is TerminalColor.RED

    def test_line_to_string(self) -> None:
        """Test converting line to string."""
        from wexample_prompt.common.prompt_context import PromptContext
        from wexample_prompt.common.prompt_response_line import PromptResponseLine
        from wexample_prompt.common.prompt_response_segment import PromptResponseSegment

        segments = [
            PromptResponseSegment(text="Hello"),
            PromptResponseSegment(text=" World"),
        ]
        line = PromptResponseLine(segments=segments)
        assert line.render(context=PromptContext()) == "Hello World"

    def test_wrapping_is_per_line_not_across_lines(self) -> None:
        """Wrapping width must reset for each logical line produced by create_from_string."""
        from wexample_prompt.common.prompt_context import PromptContext
        from wexample_prompt.common.prompt_response_line import PromptResponseLine

        text = "AAAAAA\nBBBBBB"
        lines = PromptResponseLine.create_from_string(text)
        assert len(lines) == 2

        r1 = lines[0].render(context=PromptContext(width=3, formatting=True))
        r2 = lines[1].render(context=PromptContext(width=3, formatting=True))

        # Expect chunking independently per line
        assert r1 == "AAA\nAAA"
        assert r2 == "BBB\nBBB"

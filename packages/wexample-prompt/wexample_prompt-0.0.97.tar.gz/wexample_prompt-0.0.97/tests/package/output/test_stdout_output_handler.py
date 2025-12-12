"""Simple tests for StdoutOutputHandler."""

from __future__ import annotations

from wexample_prompt.testing.abstract_prompt_test import AbstractPromptTest


class TestLogPromptResponse(AbstractPromptTest):
    """Test cases for LogPromptResponse."""

    def test_print_writes_to_stdout_and_returns_response(self) -> None:
        from wexample_prompt.output.prompt_stdout_output_handler import (
            PromptStdoutOutputHandler,
        )

        # This is the default output handler
        assert isinstance(self._io.output, PromptStdoutOutputHandler)

        assert isinstance(self._io.echo("Test output handler").rendered_content, str)

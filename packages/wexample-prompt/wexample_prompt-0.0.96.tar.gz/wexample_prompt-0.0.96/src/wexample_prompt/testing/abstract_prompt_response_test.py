"""Base class for testing prompt responses."""

from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.abstract_method import abstract_method

from wexample_prompt.testing.abstract_prompt_test import AbstractPromptTest

if TYPE_CHECKING:
    from wexample_helpers.const.types import Kwargs

    from wexample_prompt.responses.abstract_prompt_response import (
        AbstractPromptResponse,
    )


class AbstractPromptResponseTest(AbstractPromptTest):
    __test__ = False  # Prevent pytest from discovering this abstract class

    @abstract_method
    def get_expected_lines(self) -> int:
        """Return the expected number of lines in the rendered response."""

    def test_manager_indentation(self) -> None:
        response = self._create_test_response()

        response = self._io.print_response(response=response)

        assert isinstance(response.rendered_content, str)
        assert not response.rendered_content.startswith("  ")

        self._io.indentation_up()

        response = self._io.print_response(response=response)

        assert isinstance(response.rendered_content, str)
        assert response.rendered_content.startswith("  ")

        self._io.indentation_up()

        response = self._io.print_response(response=response)

        assert isinstance(response.rendered_content, str)
        assert response.rendered_content.startswith("    ")

        self._io.indentation_down()
        self._io.indentation_down()

        response = self._io.print_response(response=response)

        assert isinstance(response.rendered_content, str)
        assert not response.rendered_content.startswith("  ")

    def test_no_color(self) -> None:
        from wexample_prompt.common.prompt_context import PromptContext

        response = self._create_test_response()
        response.render(context=PromptContext(colorized=False))

        self._assert_no_color_codes(response.rendered_content)

    def test_response_class(self) -> None:
        """Test response class behavior."""
        response = self._create_test_response()
        response.render()

        self._assert_common_response_structure(response)
        self._assert_contains_text(response.rendered_content, self._test_message)
        self._assert_specific_format(response.rendered_content)

    def test_verbosity_methods(self) -> None:
        from wexample_prompt.enums.verbosity_level import VerbosityLevel

        kwargs = self._create_test_kwargs()
        kwargs["verbosity"] = VerbosityLevel.QUIET
        quiet_required = self._create_test_response_from_method(response_kwargs=kwargs)
        kwargs["verbosity"] = VerbosityLevel.DEFAULT
        default_required = self._create_test_response_from_method(
            response_kwargs=kwargs
        )
        kwargs["verbosity"] = VerbosityLevel.MAXIMUM
        maximum_required = self._create_test_response_from_method(
            response_kwargs=kwargs
        )

        self._test_verbosity(
            quiet_required=quiet_required,
            default_required=default_required,
            maximum_required=maximum_required,
        )

    def test_verbosity_standalone(self) -> None:
        from wexample_prompt.enums.verbosity_level import VerbosityLevel

        quiet_required = self._create_test_response(verbosity=VerbosityLevel.QUIET)
        default_required = self._create_test_response(verbosity=VerbosityLevel.DEFAULT)
        maximum_required = self._create_test_response(verbosity=VerbosityLevel.MAXIMUM)

        self._test_verbosity(
            quiet_required=quiet_required,
            default_required=default_required,
            maximum_required=maximum_required,
        )

    def _assert_common_response_structure(
        self, response: AbstractPromptResponse
    ) -> None:
        """Assert common structure for rendered responses."""
        lines = response.rendered_content.split("\n")
        expected_lines = self.get_expected_lines()

        self.assertEqual(len(lines), expected_lines)

        # If more than one line, first should be empty
        if expected_lines > 1:
            self.assertEqual(lines[0].strip(), "")

    def _assert_no_color_codes(self, text: str) -> None:
        """Assert that a string contains no ANSI escape sequences (colors/styles)."""
        import re

        # Generic ANSI escape sequence regex (covers CSI, OSC, and single-char escapes)
        ansi_pattern = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
        assert not ansi_pattern.search(
            text
        ), f"Unexpected ANSI escape sequences found in: {text!r}"

    @abstract_method
    def _assert_specific_format(self, rendered: str) -> None:
        """Assert format specific to this response type."""

    def _create_test_kwargs(self, **kwargs) -> Kwargs:
        return kwargs

    def _create_test_response(
        self, response_kwargs: Kwargs | None = None, **kwargs
    ) -> AbstractPromptResponse:
        """Create a response using the class: LogPromptResponse.create_log(...)"""
        kwargs = response_kwargs or self._create_test_kwargs(kwargs=kwargs)
        response_class = self._get_response_class()
        method_name = f"create_{response_class.get_snake_short_class_name()}"
        return getattr(response_class, method_name)(**kwargs)

    def _create_test_response_from_method(
        self, response_kwargs: Kwargs | None = None, **kwargs
    ) -> AbstractPromptResponse:
        """Create a response using io manager: self._io.log(...)"""
        kwargs = response_kwargs or self._create_test_kwargs(kwargs=kwargs)
        method_name = self._get_response_class().get_snake_short_class_name()
        return getattr(self._io, method_name)(**kwargs)

    @abstract_method
    def _get_response_class(self) -> type[AbstractPromptResponse]:
        pass

    def _test_verbosity(
        self,
        quiet_required: AbstractPromptResponse,
        default_required: AbstractPromptResponse,
        maximum_required: AbstractPromptResponse,
    ) -> None:
        from wexample_prompt.common.prompt_context import PromptContext
        from wexample_prompt.enums.verbosity_level import VerbosityLevel

        # Contexts with different verbosity levels
        quiet_context = PromptContext(verbosity=VerbosityLevel.QUIET)
        default_context = PromptContext(verbosity=VerbosityLevel.DEFAULT)
        medium_context = PromptContext(verbosity=VerbosityLevel.MEDIUM)
        max_context = PromptContext(verbosity=VerbosityLevel.MAXIMUM)

        def assert_visibility(context, expectations) -> None:
            # expectations: list of tuples (response, should_be_visible)
            for response, should_be_visible in expectations:
                # Reset rendered when passing already rendered response.
                response.reset()

                response.render(context=context)
                if should_be_visible:
                    assert response.rendered_content is not None
                    self._assert_contains_text(
                        response.rendered_content, self._test_message
                    )
                else:
                    assert response.rendered_content is None

        # Quiet context: only QUIET-level responses should appear
        assert_visibility(
            quiet_context,
            [
                (quiet_required, True),
                (default_required, False),
                (maximum_required, False),
            ],
        )

        # Default context: QUIET and DEFAULT appear; MAXIMUM hidden
        assert_visibility(
            default_context,
            [
                (quiet_required, True),
                (default_required, True),
                (maximum_required, False),
            ],
        )

        # Medium context: QUIET, DEFAULT, MEDIUM appear; MAXIMUM hidden
        temp_kwargs = self._create_test_kwargs()
        temp_kwargs["verbosity"] = VerbosityLevel.MEDIUM
        medium_required = self._create_test_response(temp_kwargs)
        assert_visibility(
            medium_context,
            [
                (quiet_required, True),
                (default_required, True),
                (medium_required, True),
                (maximum_required, False),
            ],
        )

        # Maximum context: all appear
        assert_visibility(
            max_context,
            [
                (quiet_required, True),
                (default_required, True),
                (maximum_required, True),
            ],
        )

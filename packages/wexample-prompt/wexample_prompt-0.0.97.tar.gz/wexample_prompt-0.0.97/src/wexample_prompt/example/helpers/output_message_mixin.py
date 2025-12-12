"""Mixin for flexible output message handling across different response types."""

from __future__ import annotations

from typing import Any


class OutputMessageMixin:
    """Mixin providing flexible _output_message method for demo classes."""

    def _build_kwargs_for_response(
        self, response_class: type, message: str, **extra_kwargs: Any
    ) -> dict[str, Any]:
        """Build kwargs dict for a specific response class.

        Args:
            response_class: The response class
            message: The message content
            **extra_kwargs: Additional kwargs to merge

        Returns:
            Dict of kwargs appropriate for the response class
        """
        from wexample_prompt.responses.data.list_prompt_response import (
            ListPromptResponse,
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

        kwargs = extra_kwargs.copy()

        # Map response classes to their parameter names
        if issubclass(response_class, ListPromptResponse):
            kwargs["items"] = [message]
        elif issubclass(
            response_class,
            (TitlePromptResponse, SubtitlePromptResponse, SeparatorPromptResponse),
        ):
            kwargs["text"] = message
        else:
            # Default: most responses use 'message' parameter
            kwargs["message"] = message

        return kwargs

    def _output_message(
        self, method_name: str, message: str, prefix: bool = False, **extra_kwargs: Any
    ) -> None:
        """Output a message using the appropriate method with response-specific parameters.

        Args:
            method_name: IO method to use (log, list, etc.)
            message: The message content
            prefix: Whether to apply the context prefix (default: False)
            **extra_kwargs: Additional kwargs to pass to the method
        """
        from wexample_prompt.common.io_manager import IoManager

        # Get the response class for this method
        response_types = IoManager.get_response_types()
        response_class = None

        for resp_class in response_types:
            if resp_class.get_snake_short_class_name() == method_name:
                response_class = resp_class
                break

        if not response_class:
            # Fallback: try to call the method directly
            method = getattr(self, method_name, None)
            if method:
                method(message=message, prefix=prefix, **extra_kwargs)
            return

        # Build kwargs based on response class requirements
        kwargs = self._build_kwargs_for_response(
            response_class, message, **extra_kwargs
        )

        # Add prefix parameter
        kwargs["prefix"] = prefix

        # Call the method with the appropriate kwargs
        method = getattr(self, method_name)
        method(**kwargs)

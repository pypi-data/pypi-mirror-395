from __future__ import annotations

from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.mixins.with_io_manager import WithIoManager


@base_class
class WithIoMethods(WithIoManager):
    """
    Allow class to provide Io methods like .log(), .title() etc.
    """

    def __getattr__(self, name: str) -> Any:
        io_response = self._get_io_methods(name)
        if io_response is not None:
            return io_response
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )

    def _get_io_methods(self, name: str) -> Any:
        io = self.ensure_io_manager()

        if hasattr(io, name):
            attr = getattr(io, name)
            if callable(attr):

                def wrapper(*args, **kwargs):
                    if "context" not in kwargs or kwargs["context"] is None:
                        kwargs["context"] = self.create_io_context()

                    if kwargs.pop("prefix", False):
                        # Add prefix using the response class's apply_prefix_to_kwargs method
                        prefix = self.get_io_context_prefix()
                        if prefix:
                            prefix_format = self.get_io_context_prefix_format()
                            formatted_prefix = prefix_format.format(prefix=prefix)

                            # Get the response class from the method name
                            response_class = self._get_response_class_for_method(name)
                            if response_class:
                                args, kwargs = response_class.apply_prefix_to_kwargs(
                                    formatted_prefix, args, kwargs
                                )

                    return attr(*args, **kwargs)

                return wrapper
            return attr
        return None

    def _get_response_class_for_method(self, method_name: str):
        """Get the response class for a given IO method name.

        Args:
            method_name: The method name (e.g., 'log', 'list', 'echo')

        Returns:
            The response class or None if not found
        """
        from wexample_prompt.common.io_manager import IoManager

        # Get all response types from IoManager
        response_types = IoManager.get_response_types()

        # Find the response class that matches the method name
        for response_class in response_types:
            # Get the short name (e.g., 'log' from 'LogPromptResponse')
            short_name = response_class.get_snake_short_class_name()
            if short_name == method_name:
                return response_class

        return None

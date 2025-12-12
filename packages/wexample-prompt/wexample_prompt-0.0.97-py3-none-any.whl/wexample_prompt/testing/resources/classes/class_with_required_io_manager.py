from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.mixins.with_required_io_manager import WithRequiredIoManager


@base_class
class ClassWithRequiredIoManager(WithRequiredIoManager):
    """
    The minimal class with an io manager.
    """

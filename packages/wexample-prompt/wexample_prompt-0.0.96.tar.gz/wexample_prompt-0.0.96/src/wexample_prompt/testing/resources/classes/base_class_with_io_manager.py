from __future__ import annotations

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.mixins.with_io_manager import WithIoManager


@base_class
class ExtendedBaseClassWithIoManager(WithIoManager, BaseClass):
    """
    A Pydantic class with an io manager.
    """

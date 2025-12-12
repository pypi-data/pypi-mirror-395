from __future__ import annotations

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.mixins.with_io_methods import WithIoMethods


@base_class
class ClassWithIoMethods(WithIoMethods):
    """
    The minimal class with an io manager.
    """

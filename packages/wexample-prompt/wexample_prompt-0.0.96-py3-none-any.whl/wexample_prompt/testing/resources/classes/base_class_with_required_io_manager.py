from __future__ import annotations

from wexample_prompt.mixins.with_required_io_manager import WithRequiredIoManager


class BaseClassWithRequiredIoManager(WithRequiredIoManager):
    """
    A Pydantic class with an io manager.
    """

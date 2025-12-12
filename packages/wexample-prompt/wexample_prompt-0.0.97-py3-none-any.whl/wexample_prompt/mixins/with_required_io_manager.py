from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.mixins.with_io_manager import WithIoManager

if TYPE_CHECKING:
    from wexample_prompt.common.io_manager import IoManager


@base_class
class WithRequiredIoManager(WithIoManager):
    io: IoManager = public_field(
        description="The required IO manager that could be shared with a parent."
    )

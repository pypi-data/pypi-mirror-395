from __future__ import annotations

from typing import TYPE_CHECKING

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field

from wexample_prompt.common.progress.progress_handle import ProgressHandle

if TYPE_CHECKING:
    from wexample_prompt.common.progress.progress_handle import ProgressHandle
    from wexample_prompt.enums.terminal_color import TerminalColor


class RangeProgressHandle(BaseClass):
    """A handle that controls a specific sub-range of a parent ProgressHandle.

    It maps the child range [0..total] to the parent range [start..end].
    Percentages provided to update/advance are relative to this child range.
    """

    end: int = public_field(
        description="Exclusive end position (start + total) of the mapped range on the parent"
    )
    parent: ProgressHandle = public_field(
        description="The parent progress handle that this range controls"
    )
    start: int = public_field(
        description="Inclusive start position of the mapped range on the parent"
    )
    total: int = public_field(description="Total size of the child range (end - start)")

    def advance(
        self,
        step: float | int | str | None = None,
        **kwargs,
    ) -> str | None:
        from wexample_prompt.responses.interactive.progress_prompt_response import (
            ProgressPromptResponse,
        )

        step_norm = ProgressPromptResponse._normalize_value(self.total, step)
        cur_child = self._child_current()
        return self.update(current=cur_child + step_norm, **kwargs)

    def finish(self, **kwargs) -> str | None:
        return self.parent.update(current=self.end, **kwargs)

    def render(self) -> str:
        return self.parent.render()

    def update(
        self,
        current: float | int | str | None = None,
        label: str | None = None,
        color: TerminalColor | None = None,
        auto_render: bool = True,
    ) -> str | None:
        from wexample_prompt.responses.interactive.progress_prompt_response import (
            ProgressPromptResponse,
        )

        if current is not None:

            normalized = ProgressPromptResponse._normalize_value(self.total, current)
            mapped = self.start + max(0, min(self.total, normalized))
            return self.parent.update(
                current=mapped, label=label, color=color, auto_render=auto_render
            )
        else:
            # Only update label/color/render
            return self.parent.update(
                current=None, label=label, color=color, auto_render=auto_render
            )

    def _child_current(self) -> int:
        # Current child value derived from parent's current
        cur = max(self.start, min(self.end, self.parent.response.current))
        return max(0, min(self.total, cur - self.start))

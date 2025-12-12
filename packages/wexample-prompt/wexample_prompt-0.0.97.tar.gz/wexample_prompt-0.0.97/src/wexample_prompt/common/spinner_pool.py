from __future__ import annotations

import threading
import time
from typing import Any, ClassVar

from wexample_helpers.classes.base_class import BaseClass
from wexample_helpers.classes.field import public_field
from wexample_helpers.classes.private_field import private_field
from wexample_helpers.decorator.base_class import base_class


@base_class
class Spinner(BaseClass):
    """Simple cyclic spinner.

    Not thread-safe; guard with external lock when used via SpinnerPool.
    """

    frames: list[str] | None = public_field(
        default=None,
        description="Number of animation frames.",
    )
    interval: float = public_field(
        default=0.2,
        description="Duration of one interval in seconds.",
    )
    _interval: float = private_field(
        default=0.2,
        description="Computed duration of one interval in seconds.",
    )
    _last_time: float = private_field(
        default=None,
        description="Last time (monotonic seconds) at which the spinner advanced."
        "None means uninitialized; the first call to next() sets it and returns current frame.",
    )

    def __attrs_post_init__(self) -> None:
        from wexample_prompt.const.spinners import DEFAULT_SPINNER_FRAMES

        self.frames: list[str] = list(self.frames or DEFAULT_SPINNER_FRAMES)
        if not self.frames:
            self.frames = list(DEFAULT_SPINNER_FRAMES)
        self._idx: int = 0
        # Minimum time between frame advances (seconds).
        self._interval: float = max(0.0, float(self.interval)) or 0.2
        self._last_time: float | None = None

    def next(self) -> str:
        if not self.frames:
            return ""

        now = time.monotonic()

        # Initialize last_time on the first call, but do not advance immediately.
        if self._last_time is None:
            self._last_time = now
            return self.frames[self._idx]

        # Compute how many whole intervals have elapsed since we last advanced.
        elapsed = now - self._last_time
        if self._interval <= 0:
            steps = 1  # fallback: always advance
        else:
            steps = int(elapsed / self._interval)

        if steps > 0:
            self._idx = (self._idx + steps) % len(self.frames)
            # Move last_time forward by the number of whole intervals consumed
            # to keep remainder for smooth, time-based stepping.
            self._last_time += steps * self._interval

        return self.frames[self._idx]

    def reset(self) -> None:
        self._idx = 0
        self._last_time = None

    def set_frames(self, frames: list[str]) -> None:
        from wexample_prompt.const.spinners import DEFAULT_SPINNER_FRAMES

        self.frames = list(frames) if frames else list(DEFAULT_SPINNER_FRAMES)
        self._idx = 0
        # Reset timing so a new frame set starts fresh.
        self._last_time = None

    def set_interval(self, interval: float) -> None:
        """Set the time interval (in seconds) between spinner frame advances."""
        self._interval = max(0.0, float(interval)) or 0.2
        # Keep current phase; do not reset _last_time to avoid visible jump.


@base_class
class SpinnerPool(BaseClass):
    """Thread-safe pool for per-key spinners."""

    _lock: ClassVar[Any] = threading.RLock()
    _spinners: ClassVar[dict[str, Spinner]] = {}

    @classmethod
    def get(cls, key: str = "default") -> Spinner:
        with cls._lock:
            sp = cls._spinners.get(key)
            if sp is None:
                sp = Spinner()
                cls._spinners[key] = sp
            return sp

    @classmethod
    def next(cls, key: str = "default") -> str:
        with cls._lock:
            return cls.get(key).next()

    @classmethod
    def reset(cls, key: str = "default") -> None:
        with cls._lock:
            cls.get(key).reset()

    @classmethod
    def set_frames(cls, frames: list[str], key: str = "default") -> None:
        with cls._lock:
            cls.get(key).set_frames(frames)

    @classmethod
    def set_interval(cls, interval: float, key: str = "default") -> None:
        """Set the advance interval for a specific spinner (in seconds)."""
        with cls._lock:
            cls.get(key).set_interval(interval)

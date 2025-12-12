from __future__ import annotations

import subprocess
import time
from typing import Any

from wexample_helpers.decorator.base_class import base_class

from wexample_prompt.example.abstract_response_example import AbstractResponseExample


@base_class
class ScreenExample(AbstractResponseExample):
    """Example usage of ScreenPromptResponse with various demos."""

    def demo_process_monitor(self) -> None:
        """Screen demo showing top CPU processes (shell-based)."""
        from wexample_prompt.responses.interactive.screen_prompt_response import (
            ScreenPromptResponse,
        )

        start = time.time()

        def _proc_callback(response: ScreenPromptResponse) -> None:
            response.clear()
            response.print(
                "@color:magenta+bold{Top CPU processes (refresh 1s, ~3s total)}"
            )

            # Get processes sorted by CPU descending; keep header + 10 rows
            cmd = ["ps", "-eo", "pid,comm,pcpu,pmem,etime", "--sort=-pcpu"]
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            lines = [ln for ln in res.stdout.strip().splitlines() if ln.strip()]
            for ln in lines[:11]:
                response.print(f"@color:cyan{{{ln}}}")

            if time.time() - start >= 3:
                response.close()
                return

            time.sleep(1.0)
            response.reload()

        self.io.screen(callback=_proc_callback, height=14)

    def demo_with_progress_and_confirm(self) -> None:
        """Screen demo with progress bar and confirmation."""
        from wexample_prompt.responses.interactive.confirm_prompt_response import (
            ConfirmPromptResponse,
        )
        from wexample_prompt.responses.interactive.screen_prompt_response import (
            ScreenPromptResponse,
        )

        counter = {"n": 0}
        total = 50

        def _callback(response: ScreenPromptResponse) -> None:
            response.clear()

            response.print(f"@color:cyan+bold{{Some text}}, {counter['n']} times...")
            response.progress(
                total=total,
                current=counter["n"],
                label="@color:yellow{Demo progression...}",
            )
            response.log("@🟢{(Any io method works)}")

            if counter["n"] == 10:
                response.confirm(
                    question="@🔵+bold{Do you want to continue demo ?}",
                    choices=ConfirmPromptResponse.MAPPING_PRESET_YES_NO,
                    default="yes",
                )

                if response.get_answer() == "no":
                    response.close()
                    return

            time.sleep(0.01)
            counter["n"] += 1
            if counter["n"] > total:
                response.close()
            else:
                response.reload()

        self.io.screen(callback=_callback, height=10)

    def example_class(self):
        from wexample_prompt.responses.interactive.screen_prompt_response import (
            ScreenPromptResponse,
        )

        counter = {"n": 0}
        total = 10

        def _callback(response: ScreenPromptResponse) -> None:
            response.clear()
            response.print(f"Test screen iteration {counter['n']}/{total}")
            time.sleep(0.05)
            counter["n"] += 1
            if counter["n"] > total:
                response.close()
            else:
                response.reload()

        return ScreenPromptResponse.create_screen(
            callback=_callback,
            height=5,
        )

    def example_extended(self) -> None:
        counter = {"n": 0}
        total = 10

        def _callback(response) -> None:
            from time import sleep

            response.clear()
            response.print(f"Test screen (extended) {counter['n']}/{total}")
            sleep(0.05)
            counter["n"] += 1
            if counter["n"] > total:
                response.close()
            else:
                response.reload()

        self._class_with_methods.screen(callback=_callback, height=5)

    def example_manager(self) -> None:
        counter = {"n": 0}
        total = 10

        def _callback(response) -> None:
            from time import sleep

            response.clear()
            response.print(f"Test screen (manager) {counter['n']}/{total}")
            sleep(0.05)
            counter["n"] += 1
            if counter["n"] > total:
                response.close()
            else:
                response.reload()

        self.io.screen(callback=_callback, height=5)

    def get_examples(self) -> list[dict[str, Any]]:
        """Get list of examples.

        Returns:
            List of example configurations
        """
        return [
            {
                "title": "Basic Screen",
                "description": "Simple screen with iteration counter",
                "callback": self.example_manager,
            },
            {
                "title": "Screen with Progress & Confirm",
                "description": "Screen with progress bar and interactive confirmation",
                "callback": self.demo_with_progress_and_confirm,
            },
            {
                "title": "Process Monitor",
                "description": "Live process monitoring (top CPU)",
                "callback": self.demo_process_monitor,
            },
        ]

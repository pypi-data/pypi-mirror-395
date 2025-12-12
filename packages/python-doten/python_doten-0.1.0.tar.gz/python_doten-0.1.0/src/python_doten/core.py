from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Any


@dataclass
class Step:
    """A single unit of work inside a ten-run.

    `action` receives the current rep index (1..10) and may return any value.
    """

    name: str
    action: Callable[[int], Any]

    def run(self, rep: int) -> Any:
        return self.action(rep)


class TenRun:
    """Execute a single `Step` up to ten times.

    This is a very small abstraction around looping from 1 to 10 and collecting
    results. It is intentionally synchronous and simple.
    """

    def __init__(self, step: Step) -> None:
        self.step = step

    def execute(self, *, max_reps: int = 10) -> List[Any]:
        if max_reps <= 0:
            return []
        if max_reps > 10:
            max_reps = 10

        results: List[Any] = []
        for rep in range(1, max_reps + 1):
            results.append(self.step.run(rep))
        return results

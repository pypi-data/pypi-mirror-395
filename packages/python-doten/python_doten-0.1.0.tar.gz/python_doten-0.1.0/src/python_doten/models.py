from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass
class RoutineResult:
    """A simple container returned by `RoutineBase.run`.

    Attributes
    ----------
    name:
        The name of the routine.
    total_reps:
        How many repetitions were successfully completed.
    notes:
        Optional textual notes, often one per rep.
    """

    name: str
    total_reps: int
    notes: List[str] = field(default_factory=list)

    def summary(self) -> str:
        base = f"Routine '{self.name}' finished with {self.total_reps} reps."
        if not self.notes:
            return base
        return base + f" Notes: {len(self.notes)} items."

from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ..core import Step, TenRun
from ..models import RoutineResult
from ..routines import RoutineBase


@dataclass
class WorkoutRoutine(RoutineBase):
    """Text-only workout routine.

    This does not enforce any semantics beyond a label, it simply records ten
    "sets" or "reps" as strings.
    """

    label: str = "workout"

    def __init__(self, label: str = "workout") -> None:
        RoutineBase.__init__(self, name=label)
        self.label = label

    def run(self) -> RoutineResult:
        notes: List[str] = []

        def record(rep: int) -> str:
            note = f"{self.label}-set-{rep}"
            notes.append(note)
            return note

        step = Step(name=self.label, action=record)
        ten = TenRun(step)
        ten.execute()
        return RoutineResult(name=self.name, total_reps=len(notes), notes=notes)

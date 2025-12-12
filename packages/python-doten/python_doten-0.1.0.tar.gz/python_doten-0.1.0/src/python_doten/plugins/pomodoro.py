from __future__ import annotations

from dataclasses import dataclass
from typing import List

from ..core import Step, TenRun
from ..models import RoutineResult
from ..routines import RoutineBase


@dataclass
class PomodoroRoutine(RoutineBase):
    """A simple, text-only pomodoro-style routine.

    It does not wait for actual minutes; that is up to the caller. The idea is
    to structure a focus block as ten symbolic units. You can combine this with
    external timers if desired.
    """

    unit_label: str = "focus-unit"

    def __init__(self, unit_label: str = "focus-unit") -> None:
        RoutineBase.__init__(self, name="pomodoro")
        self.unit_label = unit_label

    def run(self) -> RoutineResult:
        notes: List[str] = []

        def record(rep: int) -> str:
            note = f"{self.unit_label}-{rep}"
            notes.append(note)
            return note

        step = Step(name=self.unit_label, action=record)
        ten = TenRun(step)
        ten.execute()
        return RoutineResult(name=self.name, total_reps=len(notes), notes=notes)

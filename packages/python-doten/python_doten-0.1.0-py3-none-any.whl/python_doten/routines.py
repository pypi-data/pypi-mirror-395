from __future__ import annotations

from abc import ABC, abstractmethod

from .core import Step, TenRun
from .models import RoutineResult


class RoutineBase(ABC):
    """Base class for higher-level routines that use `TenRun` internally."""

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def run(self) -> RoutineResult:
        raise NotImplementedError


class SimpleCountRoutine(RoutineBase):
    """A very small example routine.

    It just counts from 1 to 10 and records a short text note for each rep.
    """

    def __init__(self, label: str = "count") -> None:
        super().__init__(name=label)

    def run(self) -> RoutineResult:
        notes = []

        def record(rep: int) -> str:
            note = f"{self.name}-rep-{rep}"
            notes.append(note)
            return note

        step = Step(name=self.name, action=record)
        ten = TenRun(step)
        values = ten.execute()
        # values and notes are equivalent here, but we keep notes explicit
        return RoutineResult(name=self.name, total_reps=len(values), notes=notes)

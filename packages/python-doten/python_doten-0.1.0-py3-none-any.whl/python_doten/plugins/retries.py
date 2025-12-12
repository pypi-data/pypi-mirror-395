from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, List, Any

from ..core import Step, TenRun
from ..models import RoutineResult
from ..routines import RoutineBase


@dataclass
class RetryRoutine(RoutineBase):
    """A generic retry routine that runs a callable up to 10 times.

    The callable should raise an exception on failure. The routine stops after
    the first successful call and records the number of attempts.
    """

    func: Callable[[], Any]

    def __init__(self, func: Callable[[], Any]) -> None:
        RoutineBase.__init__(self, name="retries")
        self.func = func

    def run(self) -> RoutineResult:
        attempts: List[str] = []

        def attempt(rep: int) -> str:
            try:
                self.func()
                attempts.append(f"success-at-{rep}")
                # Stop the TenRun by raising a sentinel exception
                raise StopIteration
            except StopIteration:
                raise
            except Exception:
                attempts.append(f"failure-{rep}")
                return attempts[-1]

        step = Step(name="retry", action=attempt)
        ten = TenRun(step)

        try:
            ten.execute()
        except StopIteration:
            # expected when we intentionally stop on first success
            pass

        return RoutineResult(name=self.name, total_reps=len(attempts), notes=attempts)

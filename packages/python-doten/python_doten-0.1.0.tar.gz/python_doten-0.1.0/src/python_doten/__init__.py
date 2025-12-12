"""python-doten: do ten of something.

This package provides a tiny, dependency-free framework and CLI for running
ten-step routines ("ten runs"). It is intentionally small and stdlib-only.
"""

from .core import Step, TenRun
from .models import RoutineResult
from .routines import RoutineBase, SimpleCountRoutine

__all__ = [
    "Step",
    "TenRun",
    "RoutineResult",
    "RoutineBase",
    "SimpleCountRoutine",
]

__version__ = "0.1.0"

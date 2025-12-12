from __future__ import annotations

import argparse
import sys
from typing import Optional, List

from .core import Step, TenRun
from .models import RoutineResult


def _interactive_ten(label: str) -> RoutineResult:
    notes: List[str] = []

    print(f"== python-doten :: {label} ==")
    print("You will do up to 10 reps. Press Enter to confirm each rep, or type 'q' to stop.")
    print()

    def action(rep: int) -> str:
        prompt = f"[{rep}/10] Press Enter to mark rep, or type a short note (q to quit): "
        try:
            text = input(prompt)
        except EOFError:
            text = "EOF"
        if text.strip().lower() == "q":
            raise StopIteration
        note = text.strip() or f"{label}-rep-{rep}"
        notes.append(note)
        print(f"Recorded: {note}")
        return note

    step = Step(name=label, action=action)
    ten = TenRun(step)

    completed = 0
    try:
        ten.execute()
        completed = len(notes)
    except StopIteration:
        completed = len(notes)

    return RoutineResult(name=label, total_reps=completed, notes=notes)


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(
        prog="doten",
        description="Run ten-step rituals and routines (or fewer, if you stop early).",
    )
    parser.add_argument(
        "label",
        nargs="?",
        default="session",
        help="A label for this ten-run (e.g. pushups, deep-work, notes).",
    )

    args = parser.parse_args(argv)

    result = _interactive_ten(args.label)
    print()
    print(result.summary())
    return 0


def main_ten() -> int:
    """Alias for `main` used by the `doten-10` entry point."""
    return main()


def do_ten_now() -> int:
    """Entry point for `do-ten` command, always requires an explicit label via argv."""
    if len(sys.argv) < 2:
        print("Usage: do-ten <label>")
        return 1
    label = sys.argv[1]
    return main([label])


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

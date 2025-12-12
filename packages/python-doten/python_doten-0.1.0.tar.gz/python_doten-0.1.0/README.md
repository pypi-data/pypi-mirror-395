# python-doten

`python-doten` is a tiny framework for **doing things in sets of ten** — ten reps, ten retries, ten focused minutes, ten lines, ten whatever-you-decide.

The idea is simple:

> Most things feel less scary when you only have to do ten of them.

This package gives you a tiny, dependency‑free toolkit and CLI that helps you:

- Define **routines** that run in *ten-step cycles*.
- Track what you did in each rep.
- Build small rituals: workouts, pomodoros, code katas, journaling, etc.
- Script custom flows with nothing but the Python standard library.

No databases. No YAML oceans. No cloud. Just **you, a terminal, and ten reps**.

---

## ✨ Highlights

- 🔟 First-class support for **ten-step routines** (`TenRun`)
- 🧱 Simple core abstractions (`Step`, `Routine`) built only on stdlib
- 🧪 Minimal, straightforward tests as examples
- 🔌 Plugin mechanism using entry points, but the default plugins are all pure-stdlib
- 🧭 Pure Python, no runtime dependencies

---

## 🚀 Quickstart

Install from source (editable):

```bash
git clone https://pypi.org/project/python-doten/ python-doten-src
cd python-doten-src
pip install -e .
```

> Note: the final project URL is  
> <https://pypi.org/project/python-doten/>

Run the CLI:

```bash
doten
```

Or the explicit “do ten now” command:

```bash
do-ten "push-ups"
```

---

## 🏗 Core Concepts

### `Step`

A `Step` represents a single unit of work inside a ten-run:

```python
from python_doten.core import Step

def do_pushup(rep: int) -> str:
    print(f"Rep {rep}: push-up!")
    return "done"

step = Step(name="pushup", action=do_pushup)
```

### `TenRun`

`TenRun` executes up to ten steps in sequence, passing the current rep index to the underlying callable:

```python
from python_doten.core import Step, TenRun

def log_rep(rep: int) -> str:
    print(f"Rep #{rep}")
    return f"rep-{rep}"

run = TenRun(step=Step("logger", log_rep))
results = run.execute()
print(results)
```

### `Routine`

A `Routine` is a named, reusable higher-level thing that *uses* ten-run internally.

---

## 🧪 Minimal Example

```python
from python_doten.routines import SimpleCountRoutine

routine = SimpleCountRoutine(label="code-lines")
summary = routine.run()
print(summary)
```

---

## 🖥 CLI Usage

After installing:

```bash
doten
```

You’ll see an interactive prompt:

- Enter a label (`push-ups`, `deep-work`, `notes`, etc.)
- Confirm you want to run ten reps
- Press enter for each rep, optionally adding a short note

Non-interactive usage:

```bash
do-ten "deep-work"
```

This directly runs a ten-cycle with the given label.

---

## 🔌 Built-in Plugin Routines

The package ships with some opinionated sample routines, all pure stdlib:

- `PomodoroRoutine` – 10 cycles as “units”; you decide how long a rep is
- `WorkoutRoutine` – text-based structure for sets/reps
- `RetryRoutine` – generic retry loop with up to 10 attempts

These exist both as importable classes and as entry points, so in future you can build your own plugins and register them in `pyproject.toml`.

---

## 📁 Project Layout

```text
python-doten/
├── pyproject.toml
├── README.md
├── src/
│   └── python_doten/
│       ├── __init__.py
│       ├── cli.py
│       ├── core.py
│       ├── models.py
│       ├── routines.py
│       ├── plugins/
│       │   ├── __init__.py
│       │   ├── pomodoro.py
│       │   ├── workout.py
│       │   └── retries.py
│       └── data/
│           └── defaults.json
└── tests/
    ├── test_core.py
    └── test_routines.py
```

---

## 🧩 Extending

You can implement your own routine by subclassing `Routine` and composing a `TenRun`.

Example:

```python
from python_doten.core import Step, TenRun
from python_doten.models import RoutineResult
from python_doten.routines import RoutineBase

class JournalRoutine(RoutineBase):
    def __init__(self) -> None:
        super().__init__(name="journal")

    def run(self) -> RoutineResult:
        step = Step(
            name="journal-entry",
            action=lambda rep: input(f"[{rep}/10] Write a sentence: "),
        )
        ten = TenRun(step)
        entries = ten.execute()
        return RoutineResult(
            name=self.name,
            total_reps=len(entries),
            notes=entries,
        )
```

---

## 🧠 Philosophy

Why ten?

- 1 is too small, you can always delay it.
- 100 is too big, you never start.
- 10 is the psychological sweet spot.

`python-doten` doesn’t try to be a task manager or habit tracker. It’s more like a **ritual helper**: a little library you can wire into your own scripts, experiments, or daily routines.

---

## 🛠 Development

This project intentionally avoids external dependencies in its metadata.

- Tests use only the standard `unittest` module.
- CLI uses `argparse` and basic I/O.

Run tests:

```bash
python -m unittest
```

---

## 📝 License

MIT © 2025 Your Name

---

## 🌐 Links

- PyPI: <https://pypi.org/project/python-doten/>


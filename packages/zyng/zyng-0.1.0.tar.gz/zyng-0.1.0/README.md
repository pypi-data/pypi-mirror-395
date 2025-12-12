## Project status

Zyng is in an **early v0.1-alpha** stage.

- Core runtime (`ZyngContext` / `ZyngRuntime`) and AST (`Show` / `Let`) are implemented.
- A simple Markdown runner is available: `python -m zyng.runner <file.md>`.
- Basic tests are in place (`tests/test_runtime.py`, `tests/test_parse_line.py`).
- The syntax and semantics described here are **not stable yet**, but already good enough to experiment with.

See also:

- Core spec (draft): `docs/zyng_core_v0.1.md`
- Progress & roadmap: `PROGRESS.md`

## Quick Zyng example

This README itself can be executed by the Zyng runner.

```zyng
show "Now message" :::now
show "Yesterday message" :::yest
show "Tomorrow message" :::tomo
show "Exact time" :::at:"2025-12-03T21:00:00+09:00"

## Examples

You can find small runnable examples under the `examples/` directory.

- `examples/time_log.md`  
  Minimal example of `let` / `show` with time metadata (`now`, `yest`, `tomo`, `at:"..."`).
- `examples/variables.md`  
  Basic `{var}` interpolation and behavior for undefined variables.

Run them with:

```bash
python -m zyng.runner examples/time_log.md
python -m zyng.runner examples/variables.md
```

## For contributors (early notes)

This project is still in a very early stage.

- Install in editable mode:

  ```bash
  git clone https://github.com/YawKobayashi/zyng.git
  cd zyng
  pip install -e .
  ```

- Run tests:

  ```bash
  pytest
  ```

- Core runtime & AST live under: `zyng/core.py`
- Markdown runner lives under: `zyng/runner.py`
- Core language spec (draft): `docs/zyng_core_v0.1.md`

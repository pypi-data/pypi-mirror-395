# Repository Guidelines

## Project Structure & Module Organization
- Core code lives in `src/pyft4222`; `wrapper/` holds FTD2XX bindings, `spi/`, `i2c/`, and `gpio.py` expose protocol helpers, and `stream.py`/`handle.py` manage typed handles.
- `examples/gpio.py`, `examples/spi_master.py`, `examples/i2c_slave.py` are runnable usage references.
- Tests sit in `tests/raw` with pytest fixtures that open real FT4222 devices; keep new tests near related modules.

## Build, Test, and Development Commands
- Install deps with `uv sync --group dev` (creates `.venv` and pulls dev tools).
- Lint and type-check: `ruff check` and `uv tool run pyright` (strict mode).
- Run tests: `uv run pytest tests/raw` (requires connected FT4222 hardware and vendor drivers in the loader path).
- Build artifacts: `uv build` (hatchling backend; wheel includes platform libs defined as artifacts).
- Spot-check examples: `uv run python examples/spi_master.py` (or other example scripts) against real hardware.

## Coding Style & Naming Conventions
- Python 3.9+ with 4-space indent and type hints everywhere; prefer `Result` (`Ok`/`Err`) returns for fallible paths to keep API consistent.
- Ruff is configured for `E,F,B,SIM,RET,I` (line length unchecked); run formatters manually if needed, but avoid masking lint findings.
- Modules and functions use `snake_case`, classes `PascalCase`, constants `UPPER_SNAKE`; keep public API names stable once released.

## Testing Guidelines
- Pytest is the only test runner; name files `test_*.py` and use fixtures in `tests/fixtures.py` to open/close handles cleanly.
- Hardware-dependent assertions should be deterministic and avoid changing device state beyond the test scope; add skips/markers if a device capability is optional.
- Note in PRs when tests were run without hardware so reviewers know what was covered.

## Commit & Pull Request Guidelines
- Commit messages are short, imperative summaries (e.g., `Migrate to uv & ruff`, `Fix osx DLLs package error`); avoid mixing unrelated refactors and behavior tweaks.
- PRs include a brief change description, linked issue (if any), commands executed (lint/type/test/build), and hardware used for validation.
- Update `src/pyft4222/__about__.py` via the release process (e.g., bump2version) to avoid version drift.

## Environment & Configuration Tips
- Ensure the FTDI driver/`libft4222` DLL/so is discoverable by the loader; on Linux, add `/etc/udev/rules.d/99-ftdi.rules` to expose the USB device to non-root users (`idVendor=0403`, `idProduct=601c`).
- When adding new bindings, document any extra OS packages or device setup steps in `README.md` so users can reproduce your environment.

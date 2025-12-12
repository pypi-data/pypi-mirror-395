# Repository Guidelines

## Project Structure & Module Organization
- `src/opendota/`: async client, endpoint modules, and Pydantic models shipped with the wheel via Hatch.
- `tests/`: pytest suites (async and integration) mirroring the source layout; add new files as `tests/test_<feature>.py`.
- `pyproject.toml`: authoritative build, dependency, and tooling configuration; update instead of ad-hoc configs.

## Build, Test & Development Commands
- Bootstrap: `uv sync --dev` installs runtime plus dev extras.
- Lint & format: `uv run ruff format .` then `uv run ruff check .` (use `--fix` for autofixable issues).
- Type safety: `uv run mypy src/` before shipping interfaces.
- Tests: `uv run pytest` for the full suite; use `uv run pytest tests/test_matches.py::TestMatches::test_get_match` for a focused run.
- Build artifacts: `uv run python -m build` creates wheel/sdist before publishing via `uv run twine upload dist/*`.

## Coding Style & Naming Conventions
- Follow 4-space indentation, 120-character lines, and fully typed public interfaces.
- Keep async I/O inside `OpenDota` methods; avoid synchronous wrappers.
- Use snake_case for functions/variables, PascalCase for Pydantic models, and ALL_CAPS for constants.
- Prefer descriptive method names matching OpenDota endpoints (e.g., `get_public_matches`).

## Testing Guidelines
- Default to pytest with `pytest-asyncio` (`asyncio_mode = "auto"` already configured).
- Mirror source packages in `tests/`; group scenario fixtures under `/tests/conftest.py` when cross-module reuse is needed.
- Name async tests `test_<behavior>` inside `Test*` classes for pytest discovery.
- For coverage, run `uv run pytest --cov=python_opendota --cov-report=term-missing` and plug uncovered lines before PR.

## Commit & Pull Request Guidelines
- The `master` branch currently lacks history; adopt short, imperative commit titles (e.g., `feat: add hero stats models`) and include relevant context in the body.
- Ensure every commit builds and passes `uv run pytest` and `uv run ruff check .` locally.
- Pull requests should describe the API surface touched, note any breaking changes, and link related issues.
- Attach test evidence (command output summaries) or screenshots for documentation tweaks.

## Security & Configuration Tips
- Keep `.env` files local; document required variables in PRs and add safe defaults to `README.md` when possible.
- Rate-limited tests should mock external HTTP via `pytest-httpx`; real OpenDota calls belong in integration suites guarded by environment checks.

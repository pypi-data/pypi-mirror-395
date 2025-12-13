# Spotcrates — Engineering Guidelines

This document describes the conventions and practices used in this repository so contributors can work consistently.

Last updated: 2025-10-25 15:55 local time


## Coding conventions

- Language and versions
  - Python 3.10+ (CI matrix currently tests 3.10–3.14).
  - Prefer standard library features available in the lowest supported version.

- Style and linting
  - Follow PEP 8 with `flake8` enforcement. CI runs two passes:
    - Strict pass for syntax/undefined names: `E9,F63,F7,F82`.
    - Advisory pass with max line length 127 and complexity 10.
  - Plugin: `flake8-bugbear` is enabled for additional best‑practices checks.
  - Line length: 127 (as used in CI).
  - Imports: group as
    1) standard library, 2) third‑party, 3) local (`spotcrates.*`).
  - Naming
    - Modules: `snake_case.py`.
    - Functions/methods/variables: `snake_case`.
    - Classes/Enums/Exceptions: `CapWords` (e.g., `Playlists`, `FilterType`, `NotFoundException`).
    - Constants: `UPPER_SNAKE_CASE`.
  - Logging: use module‑level `logger = logging.getLogger(__name__)`; avoid printing except for CLI user output where appropriate.
  - Docstrings: prefer concise module/class/function docstrings where behavior is non‑obvious.

- Type hints
  - Use Python typing throughout. `mypy` is configured via `mypy.ini` with certain error codes disabled (`import`, `no-redef`).
  - Public function signatures should be annotated. Be pragmatic for internal helpers.

- Dependencies & packaging
  - Managed with Poetry (`pyproject.toml`).
  - Console entry point: `spotcrates = spotcrates.cli:main`.

- Error handling
  - Define specific exception types for domain errors (e.g., `PlaylistException`, `InvalidFilterException`).
  - Use clear messages; prefer raising over silently failing. Handle external API failures with logging and safe fallbacks where feasible.


## Code organization and package structure

- Top‑level layout
  - `spotcrates/` (package)
    - `__init__.py`: package metadata.
    - `cli.py`: CLI entry point and argument parsing; orchestrates operations.
    - `common.py`: shared utilities (config IO, Spotify auth helpers, batching/paging, value filters, constants, base lookup class).
    - `filters.py`: filter/sort types and lookup utilities for playlist descriptors.
    - `playlists.py`: core playlist operations (listing, filtering, daily mix handling, randomization, subscriptions, append/copy helpers) and config defaults.
  - `tests/` (pytest test suite)
    - `test_*.py`: unit tests per module/behavior (CLI parsing, filters, playlist listing/sorting, common utils).
    - `data/`: JSON fixtures representing Spotify API payloads for deterministic tests.
    - `utils.py`: helper functions for loading fixtures and building records.
  - Tooling/config
    - `pyproject.toml`: Poetry metadata, dependencies, coverage config (`fail_under = 80`).
    - `mypy.ini`: type checker configuration.
    - `.github/workflows/python-app.yml`: CI (lint, tests, coverage badge generation) across OS, Python, and Poetry versions.

- Architectural notes
  - The CLI layer (`cli.py`) maps user commands → calls into `Playlists` and other utilities. Keep business logic out of argument parsing where possible.
  - Reusable logic lives in `common.py`, `filters.py`, and `playlists.py` and should be written for testability (pure(ish) functions, small units, side‑effects isolated behind Spotify client calls).


## Testing approach (unit and integration)

- Framework & tools
  - `pytest` is used for the test suite, executed under coverage in CI.
  - Coverage configuration is in `pyproject.toml` with a current threshold of 80% (fail build below).

- Unit tests (current practice)
  - Location: `tests/test_*.py`.
  - Focus areas include:
    - CLI argument parsing and command lookup (`tests/test_cli.py`).
    - Filter lookup/behavior and list processing (e.g., `tests/test_filters.py`, `tests/test_filter_list.py`).
    - Common utilities like truncation, batching, and config handling (`tests/test_common.py`).
  - Data fixtures in `tests/data/*.json` emulate Spotify API responses; loaded via `tests/utils.py` to build typed records. This keeps unit tests deterministic and offline.
  - Avoid real network calls in unit tests; functions that use `spotipy.Spotify` should be tested by isolating/pure computations or by injecting fakes/mocks for the client where necessary.

- Integration tests (guidelines)
  - Goal: validate interactions that span CLI → `Playlists` → Spotify client boundaries and back.
  - Strategy:
    - Prefer mocked integration using a fake `spotipy.Spotify` or VCR‑style recorded responses. Keep networkless by default.
    - Gate any optional live/instrumented tests behind a marker and environment variable, e.g.:
      - Mark with `@pytest.mark.integration` and skip unless `LIVE_SPOTIFY_TESTS=1` is set and required credentials exist.
    - Use temporary playlists/user sandbox accounts when exercising write operations; clean up created artifacts in teardown.
  - File naming: `tests/test_integration_*.py` for integration scenarios.

- Running tests locally
  - With Poetry:
    - Lint: `poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics`
    - Lint (advisory): `poetry run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics`
    - Unit tests + coverage: `poetry run coverage run -m pytest && poetry run coverage report -m`
    - Just pytest: `poetry run pytest`
  - To run only integration tests (if/when added): `poetry run pytest -m integration`

- CI
  - GitHub Actions workflow runs linting, then tests with coverage across OS/Python/Poetry versions. Coverage is summarized and published as a dynamic badge.


## Contribution tips

- Keep PRs focused and include/adjust tests for new behaviors.
- Maintain consistent logging and error handling; prefer explicit exceptions for domain issues.
- If adding new modules, mirror existing patterns for structure, typing, and test layout.

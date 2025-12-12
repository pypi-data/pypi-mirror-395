# Project Context

## Purpose
`good-common` is the shared Python utility library for the GoodKiwi "good-*" ecosystem.
It centralises dependency-injection helpers, an async/sync pipeline framework, shared type definitions, and a large set of well-tested utilities used across services and libraries.
The goal is to reduce duplication, provide consistent behaviour and performance, and offer a stable, backward-compatible foundation for other GoodKiwi projects.

## Tech Stack
- **Language / runtime:** Python 3.12.8+ (tested on 3.12–3.14).
- **Packaging/build:** `pyproject.toml` with `setuptools`, `setuptools-scm`/`hatch-vcs` for VCS-based versioning, Cython extensions for hot paths.
- **Core libraries:** `fast-depends` (DI), `anyio` (async), `result` (Rust-style `Result`), `pydantic>=2` (models/types), `httpx` (HTTP client), `loguru` (logging), `orjson` (JSON), `ruamel-yaml`/`pyyaml` (YAML), `python-dateutil` and `dateparser` (dates), `uuid-utils`/`python-ulid` (IDs), `cytoolz` and `pyfarmhash` (performance/ hashing).
- **Domain helpers:** `courlan`, `tldextract`, `jsonpath-rust-bindings`, `python-slugify` and related URL/string utilities.
- **Tooling:** `pytest`/`pytest-asyncio`, `mypy`, `ruff`, `coverage`, managed via `uv`.

## Project Conventions

### Code Style
- Modern, typed Python: all new public APIs should be type-hinted; prefer explicit `typing` (including `Annotated`) and Pydantic models where appropriate.
- Linting with `ruff`, type-checking with `mypy` (see `tool.mypy` in `pyproject.toml`); keep changes passing both.
- Naming: modules and functions are `snake_case`, classes `PascalCase`, constants `UPPER_SNAKE_CASE`; public exports are curated via `__all__`.
- Prefer small, pure functions with clear inputs/outputs; avoid side effects except in clearly named orchestration/helpers.
- Use `loguru` for logging instead of `print`; do not log secrets or sensitive data.
- Follow existing patterns in `dependencies.py`, `pipeline/`, `types/`, and `utilities/` before introducing new abstractions; extend rather than duplicate.

### Architecture Patterns
- **Library layout:**
  - `dependencies.py` – thin wrappers around `fast-depends` (`BaseProvider`/`AsyncBaseProvider`) for DI integration; legacy patterns are being deprecated in favour of `Annotated[..., Provider(...)]`.
  - `pipeline/` – composable async/sync pipeline engine with `Pipeline`, `Attribute`, and `function_mapper` to wire steps via typed channels.
  - `types/` – shared type utilities (UUIDs, URLs/web validation, placeholders, etc.), some backed by Cython for performance.
  - `utilities/` – grab-bag of focused helpers (async orchestration, collections, data/encoding, regex, dates, strings, YAML, binary, logging helpers), with Cython-accelerated implementations where it matters.
  - `modeling/` – modeling utilities (e.g., `python-box-notify`) used for flexible data structures.
- **Design principles:** framework-agnostic, minimal but justified dependencies, preference for composition over inheritance, and stable, backward-compatible APIs (deprecate before removal and emit warnings, as in `dependencies.py`).
- **Specs & planning:** OpenSpec (`openspec/`) is used for planning non-trivial or breaking changes; new capabilities or architecture shifts should go through a change proposal before implementation.

### Testing Strategy
- Tests live under `tests/good_common/` and are written with `pytest` and `pytest-asyncio` (see `tool.pytest.ini_options` in `pyproject.toml`).
- Run tests via `uv run pytest`; use markers like `slow`, `benchmark`, and `integration` to control scope.
- New functionality must come with tests; behavioural changes should update existing tests rather than disabling them.
- Async behaviour, pipeline execution (including parallelism and error handling), and performance-sensitive paths have dedicated tests (e.g. import/performance tests).
- In addition to tests, run `uv run ruff check` and `uv run mypy` before merging significant changes.

### Git Workflow
- Default branch is `main`; do not commit directly to `main` for feature work—use short-lived feature/bugfix branches and open PRs.
- For new capabilities, breaking changes, or notable architectural work, create an OpenSpec change under `openspec/changes/` and get the proposal approved before implementing; simple bug fixes and non-functional tweaks can skip proposals per `openspec/AGENTS.md`.
- Keep commits small and focused with concise messages (e.g. "python upgrade", "ci-cd fix", "Refactor tests and improve performance").
- Ensure `pytest`, `ruff`, and `mypy` are clean before merging; avoid committing generated artefacts.

## Domain Context
- `good-common` is a foundational library used across multiple GoodKiwi "good-*" projects (services, CLIs, and libraries).
- It focuses on general-purpose but performance-conscious building blocks for data processing pipelines, async orchestration, and web/URL handling.
- Many downstream projects rely on stable behaviours here (e.g., URL normalization, ID/UUID handling, date parsing), so seemingly small changes can have broad impact.

## Important Constraints
- This is a shared, published library on PyPI; avoid breaking changes and follow a deprecate-then-remove strategy, surfacing `DeprecationWarning`s where appropriate.
- Must support and be tested on Python 3.12–3.14 (see classifiers and `requires-python` in `pyproject.toml`).
- Keep the dependency set lean and generally applicable; avoid adding heavy or highly project-specific dependencies without strong justification.
- Do not introduce direct dependencies on GoodKiwi app infrastructure (databases, queues, SaaS APIs); callers should integrate those concerns.
- Security: never hard-code credentials or secrets; avoid logging sensitive data; be cautious with network-facing utilities built on top of `httpx`.

## External Dependencies
- No direct external SaaS or infrastructure dependencies at the library level; it is designed to be usable in any Python project.
- Relies on third-party Python libraries for core behaviour, notably:
  - `fast-depends` (dependency injection integration), `anyio` (async compat), `result` (error handling), `pydantic` (typed models).
  - `loguru`, `orjson`, `ruamel-yaml`/`pyyaml`, `python-dateutil`, `dateparser`, `courlan`, `tldextract`, `python-slugify`, `jsonpath-rust-bindings`, `cytoolz`, `pyfarmhash`, `uuid-utils`, `python-ulid`, and related helpers.
- Callers are expected to manage actual external services (datastores, APIs, queues, etc.) and use `good-common` as an implementation detail rather than a service boundary.

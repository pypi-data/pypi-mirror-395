# Negative Slice Safety & Packaging Metadata Alignment

**Date**: 2025-11-17  
**Owner**: Droid  
**Related Files**:  
- `src/good_common/types/_url_parser_cy.pyx`  
- `pyproject.toml`  
- `setup_hybrid.py`

## Overview

Release builds surfaced two actionable issues:
1. Cython warns that `path = path[:-1]` runs under `wraparound=False`, so negative indexing translates into undefined pointer math.
2. Setuptools reports metadata defined outside `pyproject.toml` (`classifiers` and `install_requires`) being ignored/overwritten, violating the packaging spec and risking inconsistent releases.

## Requirements

1. Eliminate negative slicing in `_url_parser_cy.pyx` while preserving behavior and performance of `fast_clean_path`.
2. Ensure all packaging metadata originates from `pyproject.toml` (or is explicitly marked `dynamic`).
3. Remove duplicated `install_requires`/`classifiers` declarations in `setup_hybrid.py` so setuptools does not emit `_MissingDynamic` warnings.
4. Keep generated C files and build pipeline unchanged aside from the targeted fixes.
5. Maintain existing Python version constraints and dependency lists.

## Implementation Notes

- Replace `path[:-1]` with a positive-index slice (`path = path[:len(path)-1]` or equivalent) to satisfy `wraparound=False`. Guard for length > 1 as today.
- Review the rest of the Cython file for other negative indices inside `wraparound=False` context; confirm none remain.
- Move the current classifier list into `[project]` within `pyproject.toml`. No need to mark it `dynamic` once it lives there.
- Remove `install_requires` and `classifiers` arguments from `setup_hybrid.py`; setuptools will read dependencies/classifiers directly from `pyproject.toml` when building via PEP 517.
- Confirm `pyproject.toml` remains the single source of dependency truth; if other metadata duplicates exist, consolidate while keeping the minimal changes necessary.

## Todo List

1. Update `fast_clean_path` to avoid negative slicing under `wraparound=False`.
2. Add the classifier list to `[project]` in `pyproject.toml` and ensure it matches the previous values.
3. Remove duplicated `install_requires` and `classifiers` declarations from `setup_hybrid.py` (and any related metadata now redundant).
4. Run `uv run ruff check`, `uv run mypy`, and `uv run pytest` to verify the changes.

## Testing Strategy

- Unit tests: `uv run pytest` to cover `fast_clean_path` behavior regression risk.
- Static analysis: `uv run ruff check` for lint compliance.
- Type checking: `uv run mypy` to ensure type expectations remain intact.

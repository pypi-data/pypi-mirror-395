# jsonpath-rust-bindings Migration Guide

## Version Change: 0.7.0 → 1.0.2

The jsonpath-rust-bindings library has been upgraded from version 0.7.0 to 1.0.2, introducing several breaking changes. This document outlines the changes and provides a migration path.

## Breaking Changes

### 1. **Removed: `find_non_empty()` method**
- **Old API (0.7.0)**: `Finder.find_non_empty(query)`
- **New API (1.0.2)**: Method no longer exists
- **Impact**: The `find_non_empty()` wrapper function in `_collections.py` will fail
- **Migration**: Remove this function or implement filtering logic manually

### 2. **Regex operator syntax changed**
- **Old API (0.7.0)**: `~=` operator for regex matching (e.g., `$.book[?(@.author ~= '.*pattern')]`)
- **New API (1.0.2)**: Regex operator no longer supported with this syntax
- **Impact**: Filter expressions using regex patterns will fail with parsing errors
- **Migration**: Need to find alternative filtering approach or check if there's a new syntax

### 3. **Empty result behavior changed**
- **Old API (0.7.0)**: Non-existent paths returned `[JsonPathResult(data=, path="None", is_new_value=False)]`
- **New API (1.0.2)**: Non-existent paths return empty list `[]`
- **Impact**: Code that expects a single result with empty data will break
- **Migration**: Update logic to handle empty lists

### 4. **Compliance with RFC 9535**
- The library has been rewritten to be fully compliant with RFC 9535
- This may affect edge cases and specific query syntax

## Observed API Behavior (1.0.2)

### Available Methods
- `Finder.find(query)` - Still available and working

### Working Features
- Basic path queries: `$.field`, `$.nested.field`
- Array indexing: `$.array[0]`, `$.array[*]`
- Array slicing: `$.array[0:2]`, `$.array[2:]`
- Wildcards: `$.*`, `$..*`
- Recursive descent: `$..field`
- Basic filters: `$.array[?(@.field)]`, `$.array[?(@.price < 10)]`

### Not Working/Changed
- Regex filters with `~=` operator
- Negative array indices (still not supported)
- `find_non_empty()` method completely removed

## Migration Strategy

### Option 1: Pin to Old Version
If immediate migration is not feasible, pin the version in `pyproject.toml`:
```toml
jsonpath-rust-bindings==0.7.0
```

### Option 2: Update Code for 1.0.2

#### Fix `find_non_empty()` function
Current implementation in `_collections.py`:
```python
def find_non_empty(json: dict, query: str):
    return Finder(json).find_non_empty(query)
```

Proposed fix - implement filtering manually:
```python
def find_non_empty(json: dict, query: str):
    results = Finder(json).find(query)
    # Filter out None, empty strings, empty lists, etc.
    return [r for r in results if r.data not in (None, "", [], {})]
```

Or remove the function entirely if it's not being used.

#### Update Regex-based Filters
If regex filters are needed, investigate alternatives:
1. Check if there's a new syntax in 1.0.2
2. Implement post-filtering in Python
3. Use different JSONPath expressions

#### Update Empty Result Handling
Change code that expects non-empty results for non-existent paths:
```python
# Old expectation
result = find(data, "$.nonexistent")
assert len(result) == 1  # Used to return one result with empty data

# New behavior
result = find(data, "$.nonexistent")
assert len(result) == 0  # Now returns empty list
```

## Testing After Migration

Run the test suite to verify all functionality:
```bash
uv run pytest tests/good_common/utilities/test_jsonpath.py -v
```

## Recommendation

Given that:
1. `find_non_empty()` doesn't appear to be used elsewhere in the codebase
2. Regex filters might not be critical
3. The empty result behavior change is more logical

**Recommended approach**: Update the code to work with 1.0.2 by:
1. Removing or reimplementing `find_non_empty()`
2. Updating tests to match new behavior
3. Document any features that are no longer available
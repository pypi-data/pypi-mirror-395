# Good Common Library

Core utilities and common functionality used across the good-* ecosystem. This library provides foundational tools for dependency injection, pipeline processing, type definitions, and various utility functions.

## Package Overview

good-common is published on PyPI and serves as the foundation for other good-* packages. It contains battle-tested utilities extracted from various projects.

## Key Components

### Dependencies (`dependencies.py`)
- `BaseProvider`: A base class for creating fast_depends-compatible dependency providers
- Works with FastAPI and FastStream
- Supports customizable initialization through the `initializer` method

### Pipeline (`pipeline/`)
- Flexible pipeline creation and execution framework
- Supports both synchronous and asynchronous components
- Type-safe channel-based data passing between components
- Parallel execution with error handling via Result types
- Function mapping for parameter name adjustments

### Types (`types/`)
- **Base types**: Core type definitions and base classes
- **Field definitions**: Common field types and validators
- **UUID utilities**: UUID generation and handling
- **Web types**: URL validation, domain whitelisting
- **Placeholder types**: Placeholder and template handling

### Utilities (`utilities/`)
- **Async utilities**: Async helpers and nest_asyncio integration
- **Binary utilities**: Binary data handling
- **Collection utilities**: Enhanced collection operations
- **Data utilities**: Data transformation and manipulation
- **Date utilities**: Date/time handling with python-dateutil
- **Functional utilities**: Functional programming helpers
- **Iterator utilities**: Advanced iteration tools
- **Logging utilities**: Loguru-based logging setup
- **Orchestration**: Process and task orchestration
- **Regex utilities**: Common regex patterns and helpers
- **String utilities**: String manipulation and slugification
- **YAML utilities**: YAML processing with ruamel.yaml
- **IO utilities**: File and stream I/O helpers

### Modeling (`modeling/`)
- Type definitions and modeling utilities
- Integration with python-box for flexible data structures

## Dependencies

Key dependencies include:
- `fast-depends`: Dependency injection
- `loguru`: Logging
- `python-box-notify`: Dictionary-like objects
- `orjson`: Fast JSON processing
- `ruamel-yaml`: YAML with comment preservation
- `tqdm`: Progress bars
- `anyio`: Async compatibility layer
- `result`: Rust-like Result types for error handling

## Testing

Tests are located in `tests/good_common/` and cover all major components. Run tests with:

```bash
uv run pytest
```

## Common Patterns

### Using BaseProvider
```python
from good_common.dependencies import BaseProvider

class MyServiceProvider(BaseProvider[MyService], MyService):
    pass

# In FastAPI/FastStream
@inject
def endpoint(service: MyService = MyServiceProvider(config="value")):
    return service.do_something()
```

### Building Pipelines
```python
from good_common.pipeline import Pipeline, Attribute
from typing import Annotated

def step1(x: int) -> Annotated[int, Attribute("doubled")]:
    return x * 2

def step2(doubled: int) -> Annotated[str, Attribute("result")]:
    return f"Result: {doubled}"

pipeline = Pipeline(step1, step2)
result = await pipeline(x=5)  # result.result == "Result: 10"
```

### Using Utilities
```python
from good_common.utilities import *

# String utilities
from good_common.utilities import slugify_filename
safe_name = slugify_filename("My File (2024).txt")

# Date utilities  
from good_common.utilities import parse_date
dt = parse_date("2024-01-01")

# Collection utilities
from good_common.utilities import chunk_list
chunks = list(chunk_list([1,2,3,4,5], 2))  # [[1,2], [3,4], [5]]
```

## Development Notes

- This is a foundational library - be careful with breaking changes
- All utilities should be well-tested and documented
- Follow existing patterns for consistency
- Keep dependencies minimal and well-justified
- Ensure Python 3.12+ compatibility
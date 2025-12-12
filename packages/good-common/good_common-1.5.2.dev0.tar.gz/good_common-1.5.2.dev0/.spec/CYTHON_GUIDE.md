# Cython Optimization Guide for good-common

## Overview

The `good-common` library includes optional Cython optimizations that can provide 3-20x performance improvements for critical functions. These optimizations are completely optional - the library will work perfectly fine without them.

## How It Works

### For End Users

When you install `good-common` from PyPI, you'll get optimizations automatically if:

1. **Installing a wheel** (`pip install good-common`)
   - Pre-compiled wheels are available for:
     - macOS (x86_64, arm64, universal2)
     - Linux (x86_64, aarch64)
     - Windows (AMD64)
   - These include the compiled Cython extensions

2. **Installing from source** (`pip install good-common --no-binary :all:`)
   - If Cython is available: Compiles from `.pyx` sources
   - If only C compiler available: Compiles from included `.c` files
   - If compilation fails: Falls back to pure Python (still works!)

### Performance Impact

Benchmarked improvements on typical workloads:

| Function | Speedup | Use Case |
|----------|---------|----------|
| `filter_nulls` | 9.5x | Removing None values from nested structures |
| `deep_attribute_get` | 20.8x | Accessing nested dictionary attributes |
| `detect_string_type` | 10.7x | Identifying string types (URL, email, etc.) |
| `recursive_get` | 6.0x | Nested dictionary access |
| `index_object` | 3.4x | Converting nested dicts to flat representation |
| `sort_object_keys` | 3.8x | Recursively sorting dictionary keys |

### Checking Optimization Status

```python
from good_common.utilities._optimized import get_optimization_status, is_optimized

# Check what's optimized
print(get_optimization_status())
# Output: {'collections': True, 'functional': True, 'strings': True}

# Quick check if any optimizations are active
print(is_optimized())
# Output: True
```

## For Developers

### Building Locally

```bash
# Install development dependencies
uv sync

# Build Cython extensions
scripts/build_cython.sh

# Or manually:
uv run python setup.py build_ext --inplace
```

### Running Benchmarks

```bash
# Compare Python vs Cython performance
uv run python scripts/benchmark_cython.py
```

### Testing

```bash
# Run tests for Cython implementations
uv run pytest tests/good_common/utilities/test_cython_optimized.py -v
```

### Creating Distributions

```bash
# Generate C files from Cython sources (required before packaging)
uv run python scripts/generate_c_files.py

# Create source distribution (includes .pyx and .c files)
uv run python setup_hybrid.py sdist

# Create wheel for current platform
uv run python setup_hybrid.py bdist_wheel
```

## Package Structure

```
good-common/
├── src/good_common/utilities/
│   ├── _collections.py          # Pure Python implementation
│   ├── _collections_cy.pyx      # Cython source
│   ├── _collections_cy.c        # Generated C (included in sdist)
│   ├── _collections_cy.*.so     # Compiled extension (platform-specific)
│   ├── _functional.py           # Pure Python implementation
│   ├── _functional_cy.pyx       # Cython source
│   ├── _functional_cy.c         # Generated C
│   ├── _strings.py              # Pure Python implementation
│   ├── _strings_cy.pyx          # Cython source
│   ├── _strings_cy.c            # Generated C
│   └── _optimized.py            # Import wrapper with fallbacks
```

## Distribution Strategy

1. **Source Distribution (sdist)**
   - Includes: `.py`, `.pyx`, `.c` files
   - Users can build with or without Cython
   - Fallback to pure Python if build fails

2. **Wheels (bdist_wheel)**
   - Pre-compiled for specific platforms
   - No compilation needed by end users
   - Fastest installation

3. **GitHub Actions**
   - Automatically builds wheels for multiple platforms
   - Triggered on version tags (v*)

## Compatibility

- **Python**: 3.13+ required
- **Cython**: 3.0+ (optional)
- **Platforms**: Windows, macOS, Linux (x86_64, arm64)
- **Fallback**: Always available - pure Python works everywhere

## Troubleshooting

### "ImportError: No module named '_collections_cy'"
- This is normal! The library automatically falls back to pure Python
- Check optimization status with `get_optimization_status()`

### Build failures on installation
- The package will still install and work
- You'll get pure Python implementations (slower but functional)
- To get optimizations, ensure you have a C compiler

### Verifying optimizations are active
```python
import good_common.utilities._collections_cy  # Should not raise ImportError
```

## FAQ

**Q: Do end users need Cython installed?**
A: No! Wheels include compiled extensions. Source installs include C files.

**Q: What if compilation fails?**
A: The library falls back to pure Python automatically. Everything still works!

**Q: How much faster is it really?**
A: Core operations are 3-20x faster. Real-world impact depends on usage patterns.

**Q: Does this work on Apple Silicon (M1/M2)?**
A: Yes! We build universal2 and arm64 wheels for macOS.

**Q: Can I disable Cython optimizations?**
A: Yes, just delete the `.so`/`.pyd` files or set an environment variable to force pure Python.
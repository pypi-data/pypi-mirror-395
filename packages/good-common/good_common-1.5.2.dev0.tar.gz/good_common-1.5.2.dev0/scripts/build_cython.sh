#!/bin/bash
# Build script for Cython extensions

echo "Building Cython extensions for good-common..."
echo "============================================"

# Ensure we're in the right directory
cd "$(dirname "$0")"

# Install dependencies if needed
echo "Installing dependencies..."
uv sync

# Build Cython extensions
echo "Building Cython extensions..."
uv run python setup.py build_ext --inplace --force

# Check if build succeeded
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    
    # Check optimization status
    echo "Checking optimization status..."
    uv run python -c "
from good_common.utilities._optimized import get_optimization_status, is_optimized
status = get_optimization_status()
print('Cython modules available:')
for module, available in status.items():
    symbol = '✓' if available else '✗'
    print(f'  {module}: {symbol}')
print(f'\\nOptimization enabled: {is_optimized()}')
"
    
    echo ""
    echo "To run benchmarks: uv run python benchmark_cython.py"
    echo "To run tests: uv run pytest tests/good_common/utilities/test_cython_optimized.py"
else
    echo ""
    echo "❌ Build failed!"
    echo "Please check the error messages above."
    exit 1
fi
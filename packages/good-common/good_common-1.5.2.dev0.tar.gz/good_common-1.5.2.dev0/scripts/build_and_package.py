#!/usr/bin/env python
"""
Build and package good-common with Cython optimizations.
This creates both source distribution and platform wheels.
"""

import sys
import shutil
import subprocess
from pathlib import Path

def run_command(cmd, check=True):
    """Run a shell command and print output."""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=False, text=True)
    if check and result.returncode != 0:
        print(f"Error running command: {cmd}")
        sys.exit(1)
    return result

def clean_build_artifacts():
    """Clean previous build artifacts."""
    print("Cleaning previous builds...")
    dirs_to_remove = ['build', 'dist', '*.egg-info', 'src/*.egg-info']
    for pattern in dirs_to_remove:
        for path in Path('.').glob(pattern):
            if path.is_dir():
                shutil.rmtree(path)
                print(f"  Removed {path}")

def main():
    print("="*60)
    print("Building and Packaging good-common with Cython")
    print("="*60)
    
    # Step 1: Clean
    clean_build_artifacts()
    
    # Step 2: Generate C files from Cython sources
    print("\n1. Generating C files from Cython sources...")
    run_command("uv run python generate_c_files.py")
    
    # Step 3: Build extensions in-place for testing
    print("\n2. Building Cython extensions...")
    run_command("uv run python setup.py build_ext --inplace")
    
    # Step 4: Run tests to verify everything works
    print("\n3. Running tests...")
    result = run_command(
        "uv run pytest tests/good_common/utilities/test_cython_optimized.py -q",
        check=False
    )
    if result.returncode != 0:
        print("⚠️  Some tests failed, but continuing with packaging...")
    
    # Step 5: Create source distribution (includes .pyx and .c files)
    print("\n4. Creating source distribution...")
    run_command("uv run python setup_hybrid.py sdist")
    
    # Step 6: Create wheel for current platform
    print("\n5. Creating wheel for current platform...")
    run_command("uv run python setup_hybrid.py bdist_wheel")
    
    # Step 7: Display created packages
    print("\n" + "="*60)
    print("📦 Created packages:")
    print("="*60)
    
    dist_files = list(Path('dist').glob('*'))
    for file in dist_files:
        size = file.stat().st_size / 1024 / 1024  # MB
        print(f"  - {file.name} ({size:.2f} MB)")
    
    print("\n" + "="*60)
    print("✅ Build complete!")
    print("="*60)
    
    print("""
Next steps:

1. Test installation locally:
   pip install dist/good_common-*.whl

2. Upload to PyPI Test:
   twine upload --repository testpypi dist/*

3. Upload to PyPI:
   twine upload dist/*

Note: Users will get Cython optimizations if:
- Installing from wheel (pre-compiled)
- Installing from source with Cython + C compiler available
- Installing from source without Cython (uses included .c files)

Users will get pure Python fallback if:
- C compilation fails for any reason
- No compiler is available
""")

if __name__ == "__main__":
    main()
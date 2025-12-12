#!/usr/bin/env python
"""
Generate C files from Cython .pyx sources.
This is run before creating source distributions to ensure C files are included.
"""

import sys
from pathlib import Path

def generate_c_files():
    """Generate C files from Cython sources."""
    try:
        from Cython.Build import cythonize
    except ImportError:
        print("ERROR: Cython is required to generate C files")
        print("Install with: pip install cython")
        sys.exit(1)
    
    # Find all .pyx files
    pyx_files = list(Path("src").glob("**/*.pyx"))
    
    if not pyx_files:
        print("No .pyx files found")
        return
    
    print(f"Found {len(pyx_files)} Cython files:")
    for pyx_file in pyx_files:
        print(f"  - {pyx_file}")
    
    # Generate C files
    print("\nGenerating C files...")
    cythonize(
        [str(f) for f in pyx_files],
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
            'cdivision': True,
            'initializedcheck': False,
        },
        force=True,
        quiet=False,
    )
    
    # Check that C files were created
    c_files = list(Path("src").glob("**/*.c"))
    print(f"\nGenerated {len(c_files)} C files:")
    for c_file in c_files:
        size = c_file.stat().st_size
        print(f"  - {c_file} ({size:,} bytes)")
    
    print("\n✅ C files generated successfully!")
    print("These will be included in the source distribution.")

if __name__ == "__main__":
    generate_c_files()
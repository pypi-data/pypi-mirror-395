"""Setup script for building good-common with optional Cython extensions."""

import os
import sys
import warnings
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

# Try to import Cython
try:
    from Cython.Build import cythonize
    HAVE_CYTHON = True
except ImportError:
    HAVE_CYTHON = False
    cythonize = None

# Try to import numpy for include dirs
try:
    import numpy as np
    numpy_includes = [np.get_include()]
except ImportError:
    numpy_includes = []


class OptionalBuildExt(build_ext):
    """Build extension with graceful fallback if compilation fails."""
    
    def build_extension(self, ext):
        try:
            super().build_extension(ext)
        except Exception as e:
            warnings.warn(
                f"Failed to build extension {ext.name}: {e}\n"
                f"Falling back to pure Python implementation."
            )


def get_extensions():
    """Get list of extensions to build."""
    extensions = []
    
    # Define the Cython extensions
    ext_modules = [
        ("good_common.utilities._collections_cy", "src/good_common/utilities/_collections_cy"),
        ("good_common.utilities._functional_cy", "src/good_common/utilities/_functional_cy"),
        ("good_common.utilities._strings_cy", "src/good_common/utilities/_strings_cy"),
        ("good_common.types._url_parser_cy", "src/good_common/types/_url_parser_cy"),
        ("good_common.types._url_patterns_cy", "src/good_common/types/_url_patterns_cy"),
    ]
    
    for name, source_base in ext_modules:
        # Determine source file (.pyx or .c)
        pyx_file = f"{source_base}.pyx"
        c_file = f"{source_base}.c"
        
        if HAVE_CYTHON and os.path.exists(pyx_file):
            # Use .pyx source
            sources = [pyx_file]
        elif os.path.exists(c_file):
            # Use pre-generated .c source
            sources = [c_file]
        else:
            # Skip this extension
            continue
        
        # Create extension
        ext = Extension(
            name,
            sources,
            include_dirs=numpy_includes,
            language="c",
            extra_compile_args=["-O3"] if sys.platform != "win32" else [],
        )
        extensions.append(ext)
    
    return extensions


# Get extensions
extensions = get_extensions()

# Apply Cython if available and we have .pyx sources
if HAVE_CYTHON and extensions:
    # Check if any extension uses .pyx
    has_pyx = any(src.endswith('.pyx') for ext in extensions for src in ext.sources)
    if has_pyx:
        extensions = cythonize(
            extensions,
            compiler_directives={
                'language_level': "3",
                'boundscheck': False,
                'wraparound': False,
                'cdivision': True,
                'initializedcheck': False,
            }
        )

# Setup configuration
setup(
    ext_modules=extensions if extensions else [],
    cmdclass={'build_ext': OptionalBuildExt} if extensions else {},
    zip_safe=False,
)
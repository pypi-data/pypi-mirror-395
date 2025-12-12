"""
Hybrid setup script for good-common with Cython optimizations.
This handles building both source distributions and wheels.
"""

import importlib.util
import os
import sys
import warnings
from setuptools import setup, Extension, find_packages
from setuptools.command.build_ext import build_ext

# Check if we should use Cython or pre-generated C files
USE_CYTHON = os.environ.get('USE_CYTHON', 'auto')

def check_cython_available():
    """Check if Cython is available."""
    return importlib.util.find_spec("Cython.Build") is not None

# Determine whether to use Cython
if USE_CYTHON == 'auto':
    USE_CYTHON = check_cython_available()
elif USE_CYTHON in ('1', 'true', 'True'):
    USE_CYTHON = True
    if not check_cython_available():
        raise ImportError("Cython is required but not installed")
else:
    USE_CYTHON = False

print(f"Using Cython: {USE_CYTHON}")

# File extensions based on whether we're using Cython
ext = '.pyx' if USE_CYTHON else '.c'

# Define extensions
extensions = [
    Extension(
        "good_common.utilities._collections_cy",
        [f"src/good_common/utilities/_collections_cy{ext}"],
        extra_compile_args=["-O3", "-ffast-math"] if sys.platform != "win32" else ["/O2"],
    ),
    Extension(
        "good_common.utilities._functional_cy",
        [f"src/good_common/utilities/_functional_cy{ext}"],
        extra_compile_args=["-O3", "-ffast-math"] if sys.platform != "win32" else ["/O2"],
    ),
    Extension(
        "good_common.utilities._strings_cy",
        [f"src/good_common/utilities/_strings_cy{ext}"],
        extra_compile_args=["-O3"] if sys.platform != "win32" else ["/O2"],
    ),
]

# Custom build_ext that doesn't fail if compilation fails
class OptionalBuildExt(build_ext):
    """Build extensions, but make them optional."""
    
    def run(self):
        try:
            super().run()
        except Exception as e:
            warnings.warn(f"""
            WARNING: Failed to build Cython extensions: {e}
            The package will still work but without performance optimizations.
            """)
    
    def build_extension(self, ext):
        try:
            super().build_extension(ext)
        except Exception as e:
            warnings.warn(f"""
            WARNING: Failed to build extension {ext.name}: {e}
            The package will work but this optimization will not be available.
            """)


# If using Cython, compile .pyx -> .c
if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(
        extensions,
        compiler_directives={
            'language_level': "3",
            'boundscheck': False,
            'wraparound': False,
            'cdivision': True,
            'initializedcheck': False,
        },
        annotate=True,  # Generate HTML annotations
    )

# Get version from git tags using setuptools_scm
def get_version():
    try:
        from setuptools_scm import get_version
        return get_version()
    except ImportError:
        # Fallback for development
        return "0.3.5+dev"

# Setup configuration
setup(
    name="good-common",
    version=get_version(),
    description="Good Kiwi Common Library with Cython Optimizations",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Chris Goddard",
    author_email="chris@goodkiwi.llc",
    url="https://github.com/goodkiwi/good-common",
    packages=find_packages("src"),
    package_dir={"": "src"},
    ext_modules=extensions,
    cmdclass={'build_ext': OptionalBuildExt},
    zip_safe=False,
    python_requires=">=3.13",
    package_data={
        "good_common.utilities": [
            "*.pyx",  # Include Cython source
            "*.c",    # Include generated C files
            "*.pxd",  # Include Cython headers if any
        ],
    },
)
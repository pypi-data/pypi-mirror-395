"""
FFI builder module for pycint.

This module defines the FFI bindings for the libcint library.
It uses cffi to create Python bindings for the C library.
"""

import os
from pathlib import Path

from cffi import FFI

from pycint._cdef import CDEF

# Global variables for the FFI builder
_ffibuilder = None
_initialized = False


def get_ffibuilder():
    """Get or create the FFI builder instance."""
    global _ffibuilder
    if _ffibuilder is None:
        _ffibuilder = FFI()
        _ffibuilder.cdef(CDEF)
    return _ffibuilder


def configure_ffibuilder(lib_dir=None):
    """
    Configure the FFI builder with the correct library paths.

    This creates a new FFI builder each time to avoid the 'set_source() called multiple times' error.
    """
    global _ffibuilder, _initialized

    # Create a fresh FFI builder
    _ffibuilder = FFI()
    _ffibuilder.cdef(CDEF)

    # Default paths to use for building the FFI module
    library_dirs = []
    include_dirs = []

    # Only configure paths if they're needed
    if lib_dir:
        library_dirs = [lib_dir]
        # When lib_dir is provided, use relative paths
        include_dirs = [
            "libcint/src",
            "libcint/include",
        ]
    elif os.path.exists("setup.py"):  # Development environment
        # Get the project root directory
        root_dir = Path(__file__).resolve().parent.parent / "libcint"
        include_dirs = [str(root_dir / "src"), str(root_dir / "include")]

    # Configure the builder with correct paths
    _ffibuilder.set_source(
        "pycint._cint",
        None,  # No preprocessor code - we just link to the compiled library
        libraries=["cint"] if lib_dir else [],  # Link against libcint if available
        library_dirs=library_dirs,
        include_dirs=include_dirs,
    )

    _initialized = True


# For backward compatibility
ffibuilder = get_ffibuilder()


def compile_ffi(verbose=False):
    """Compile the FFI bindings."""
    if not _initialized:
        # Configure with default paths if not already configured
        configure_ffibuilder()

    try:
        ffibuilder.compile(verbose=verbose)
        return True
    except Exception as e:
        if verbose:
            print(f"FFI compilation failed: {e}")
        return False


if __name__ == "__main__":
    # If this module is run directly, try to compile with default settings
    compile_ffi(verbose=True)

"""
pycint - Python bindings for libcint.

This module provides Python bindings to the libcint library,
which is a library for quantum chemistry integrals.
"""

from pathlib import Path

from pycint._cint import ffi
from pycint.typing import Cint

DIR = Path(__file__).resolve().parent


def _find_library_path() -> str:
    """Find the path to the libcint library."""
    # Get the current package directory

    # Try to find the library in the package's lib directory first
    # This is the preferred location for installed packages
    package_lib_dir = DIR / "lib"
    lib_path = package_lib_dir / "libcint.so"
    if lib_path.exists():
        return str(lib_path)

    # If not found, try in the parent directory's lib folder
    # This is for development environments
    parent_lib_dir = DIR.parent / "lib"
    lib_path = parent_lib_dir / "libcint.so"
    if lib_path.exists():
        return str(lib_path)

    # default
    return "libcint.so"


# Find and load the library
lib_path = _find_library_path()

try:
    lib: Cint = ffi.dlopen(lib_path)
except OSError as e:
    # Provide a more informative error message
    raise ImportError(
        f"Failed to load libcint library from '{lib_path}'. "
        "Please ensure that pycint is properly installed with its compiled C library."
    ) from e

# Export the library object
__all__ = ["lib"]

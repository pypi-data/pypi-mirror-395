#!/usr/bin/env python
"""
Setup script for pycint.

This script builds and installs the pycint package, which includes
the libcint C library and Python bindings using cffi.
"""

import os
import subprocess
from pathlib import Path

import setuptools.command.install
from setuptools import Extension, find_packages, setup
from setuptools.command.build_ext import build_ext

# Get the directory of setup.py
DIR: Path = Path(__file__).resolve().parent

GIT_REPO = "https://github.com/sunqm/libcint.git"


def get_libcint(path: Path = Path("libcint"), commit_id: str = "master", force=False):
    """Clone and configure libcint repository."""
    # Clone the repository if needed
    if force and path.exists():
        subprocess.run(["rm", "-rf", str(path)], check=True)
        subprocess.run(["git", "clone", GIT_REPO, str(path)], check=True)
    elif not path.exists():
        subprocess.run(["git", "clone", GIT_REPO, str(path)], check=True)

    # Checkout the specific commit
    subprocess.run(["git", "checkout", commit_id], cwd=str(path), check=True)

    # Let CMake generate cint_config.h automatically instead of copying it manually


class CMakeExtension(Extension):
    """Extension that uses CMake to build."""

    def __init__(self, name, sourcedir=""):
        super().__init__(name, sources=[])
        self.sourcedir = os.path.abspath(sourcedir)


class CMakeBuild(build_ext):
    """Custom build_ext command to use CMake for building libcint."""

    def run(self):
        # Check if we're in a clean build environment (like when building a wheel)
        if not os.path.exists("libcint"):
            # Skip building in clean environments
            print("Skipping libcint build in clean environment")
            return

        try:
            subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError("CMake must be installed to build the extensions")

        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))
        libcint_dir = os.path.abspath(os.path.join(DIR, "libcint"))

        # Configure CMake args
        cmake_args = [
            f"-DCMAKE_LIBRARY_OUTPUT_DIRECTORY={extdir}",
            # f"-DPYTHON_EXECUTABLE={sys.executable}",
            f"-DCMAKE_INSTALL_PREFIX={extdir}",
            "-DBUILD_SHARED_LIBS=ON",
            "-DENABLE_EXAMPLE=OFF",
            "-DENABLE_TEST=OFF",
            "-DWITH_FORTRAN=OFF",
            "-DWITH_CINT2_INTERFACE=ON",
            "-DCMAKE_BUILD_TYPE=Release",
        ]

        # Set source directory to libcint
        ext.sourcedir = libcint_dir

        # Create build directory
        build_dir = os.path.join(self.build_temp, ext.name)
        if not os.path.exists(build_dir):
            os.makedirs(build_dir)

        print(f"Building libcint in {build_dir}")
        print(f"CMake args: {cmake_args}")

        # Configure with CMake
        subprocess.check_call(["cmake", ext.sourcedir] + cmake_args, cwd=build_dir)

        # Build the library
        subprocess.check_call(
            ["cmake", "--build", ".", "--target", "install"], cwd=build_dir
        )

        # Write a file with the library path information for later use
        with open(os.path.join(extdir, ".lib_path"), "w") as f:
            f.write(extdir)


def compile_ffi(force=False):
    """Compile the FFI bindings."""
    output_file = DIR / "pycint" / "_cint.py"
    lib_path_file = DIR / ".lib_path"

    if not output_file.exists() or force:
        print("Compiling FFI bindings...")
        try:
            lib_dir = None

            # Try to get the library path from the previous build
            if lib_path_file.exists():
                with open(lib_path_file, "r") as f:
                    lib_dir = f.read().strip()

            # Import and configure the FFI builder
            from pycint._cffi_builder import configure_ffibuilder, ffibuilder

            # Configure with library path if available
            if lib_dir:
                configure_ffibuilder(lib_dir)

            # Compile the FFI module
            ffibuilder.compile(verbose=True)
            return True
        except Exception as e:
            print(f"FFI compilation failed: {e}")
            return False
    return True


# First build the C extension
# Then compile FFI bindings
class CustomBuildExt(CMakeBuild):
    """Custom build command that builds both the C extension and FFI bindings."""

    def run(self):
        # First check if we're in a clean build environment
        if not os.path.exists("libcint"):
            # Skip building in clean environments
            print("Skipping build in clean environment")
            return

        # First build the C library
        super().run()

        # Then compile the FFI bindings
        compile_ffi()


class InstallCommand(setuptools.command.install.install):
    """Custom install command to ensure the library is properly installed."""

    def run(self):
        # First run the standard install
        super().run()

        # Then copy the compiled library to the package directory
        install_lib = self.install_lib
        if not install_lib:
            install_lib = os.path.join(
                self.install_libbase, self.distribution.metadata.name
            )

        # Create the lib directory in the package if it doesn't exist
        lib_dir = os.path.join(install_lib, "lib")
        if not os.path.exists(lib_dir):
            os.makedirs(lib_dir)

        # Copy the compiled library to the package lib directory
        for lib_name in ["libcint.so", "libcint.so.6", "libcint.so.6.1.3"]:
            src = DIR / lib_name
            if os.path.exists(src):
                dst = os.path.join(lib_dir, lib_name)
                self.copy_file(src, dst)


compile_ffi()


setup(
    name="pycint",
    packages=find_packages(),
    ext_modules=[CMakeExtension("libcint")],
    cmdclass={
        "build_ext": CustomBuildExt,
        "install": InstallCommand,
    },
    install_requires=["numpy>=2", "cffi>=2"],
    package_data={
        "": [
            "*.so",
            "*.so.*",
            "*.h",
            "libcint/include/*",
            "libcint/src/*",
            "libcint/CMakeLists.txt",
            "libcint/LICENSE",
        ]
    },
    include_package_data=True,
)

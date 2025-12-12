# https://python-poetry.org/docs/building-extension-modules/#cython-pyproject

from __future__ import annotations

import os
import shutil
import platform

from pathlib import Path

from Cython.Build import cythonize
from setuptools import Distribution
from setuptools import Extension
from setuptools.command.build_ext import build_ext

# did not work on arm64 architecture clang
# COMPILE_ARGS = ["-march=native", "-O3", "-msse", "-msse2", "-mfma", "-mfpmath=sse"]
COMPILE_ARGS = ["-O3"]
LINK_ARGS = []
INCLUDE_DIRS = []
LIBRARIES = ["m"]
if platform.system().lower() == "windows":
    # O3 doesn't work for Windows
    COMPILE_ARGS = ["/O2", "/arch:AVX2"]
    LIBRARIES = []  # mathematical functions not available on Windows
elif platform.system().lower() == "linux" and platform.machine().lower() == "x86_64":
    # further x86_64 specific optimization flags
    COMPILE_ARGS.extend(["-march=native", "-msse", "-msse2", "-mfma", "-mfpmath=sse"])


def build() -> None:
    # Conditional compilation
    if os.environ.get("USE_CYTHON", "1") == "1":
        extensions = [
            Extension(
                "*",
                ["tarandm_analytics_utils/**/*.py"],
                extra_compile_args=COMPILE_ARGS,
                extra_link_args=LINK_ARGS,
                include_dirs=INCLUDE_DIRS,
                libraries=LIBRARIES,
            )
        ]
        ext_modules = cythonize(
            extensions,
            include_path=INCLUDE_DIRS,
            compiler_directives={"binding": True, "language_level": 3},
        )
    else:
        ext_modules = []  # Skip Cython compilation

    distribution = Distribution({"name": "package", "ext_modules": ext_modules})

    cmd = build_ext(distribution)
    cmd.ensure_finalized()
    cmd.run()

    # Copy built extensions back to the project
    for output in cmd.get_outputs():
        output = Path(output)
        relative_extension = output.relative_to(cmd.build_lib)

        shutil.copyfile(output, relative_extension)
        mode = os.stat(relative_extension).st_mode
        mode |= (mode & 0o444) >> 2
        os.chmod(relative_extension, mode)


if __name__ == "__main__":
    build()

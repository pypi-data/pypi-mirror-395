"""
Common methods and definitions for project hooks.
"""

# built-in
from multiprocessing import cpu_count
from pathlib import Path
from sys import version_info

# internal
from experimental_lowqa.edit import is_local_bin, local_bin

PYTHON = f"python{version_info.major}.{version_info.minor}"
PREFIX = Path.home().joinpath(".local")
PREFIX_ARGS = f"--prefix={PREFIX}"
MAKE_NPROCS = f"-j{cpu_count()}"

VENV = Path.home().joinpath("venv")
VENV_BIN = VENV.joinpath("bin")

# Full paths to programs that should be used instead of allowing PATH to
# resolve them.
PROGS = {"pip": VENV_BIN.joinpath("pip")}


def link_local_bin(path: Path) -> None:
    """Link a local binary from some arbitrary location."""

    prog = path.name
    if not is_local_bin(prog):
        local_bin(prog).symlink_to(path.resolve())

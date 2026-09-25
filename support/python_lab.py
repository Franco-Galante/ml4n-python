"""Computation behind 01_python.py that the class does not need to step into.

edtrace traces the lecture module and nothing else, so everything here runs as
a single step: the code panel stays on the Python being taught, not on the
scaffolding that sets up a file or formats a disassembly.
"""

import dis
import platform
import sys
from pathlib import Path

# The lecture writes its example files here, at run time, under var/ (which is
# gitignored): the course ships no data files of its own, and the folder has to
# exist before the lecture opens a path inside it.
DATA_DIR = Path("var/data")
DATA_DIR.mkdir(parents=True, exist_ok=True)


def bytecode_of(source: str) -> str:
    """The bytecode instructions `source` is translated into, one per row."""
    code = compile(source, "example.py", "exec")
    return "\n".join(f"{instruction.opname:<14} {instruction.argrepr}".rstrip() for instruction in dis.get_instructions(code))


def interpreter_facts() -> dict:
    """What is executing the lecture right now.

    No paths on purpose: `sys.executable` would publish the lecturer's home
    directory in the trace, and the trace is course material.
    """
    return {
        "implementation": platform.python_implementation(),
        "version": platform.python_version(),
        "in_virtual_env": sys.prefix != sys.base_prefix,
        "bytecode_tag": sys.implementation.cache_tag,
    }


def describe(error: Exception) -> str:
    """An exception the way the interpreter reports it: `TypeError: ...`."""
    return f"{type(error).__name__}: {error}"


def read_text(path: str) -> str:
    """The whole content of a file, to show what a write produced."""
    return Path(path).read_text()


class Triangle:
    """The triangle of the private-attributes demo of 01_python.py.

    The class body is identical to the one the class has just stepped through,
    so the lecture shows it as a snippet and keeps the stepping for the access
    that fails.  Defined here rather than in the lecture file because only the
    lecture module is traced: an imported class costs one step, not eight.
    """

    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c
        self.__perimeter = a + b + c  # 2 leading underscores make the attribute private

    def get_perimeter(self):
        return self.__perimeter


def make_triangle(a: int, b: int, c: int) -> Triangle:
    """The Triangle above, built without the lecture stepping through __init__ again."""
    return Triangle(a, b, c)

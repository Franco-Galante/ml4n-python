"""Computation behind 02_numpy.py that the class does not need to step into.

edtrace traces the lecture module and nothing else, so everything here runs as
a single step: the code panel stays on the numpy being taught, not on the
timing harness that measures it.
"""

import math
import sys
import time
from pathlib import Path

import numpy as np

# The same helper as lecture 1: an exception printed the way the interpreter
# prints it, so a caught error can be shown on the variable panel.
from .python_lab import describe  # noqa: F401  (re-exported for the lecture)

# Generated at run time under var/ (gitignored), so the lecture ships no data
# files of its own and every run starts from the same content.
DATA_DIR = Path("var/data")


def compare_speed(n: int = 1_000_000) -> dict:
    """Time the same inner product as a Python loop and as one numpy call.

    Floats on both sides, like the memory measurement.  The two sums add the
    products in a different order, so they agree up to rounding, not bit by bit.
    Each side keeps its best of `repeats` runs, so one unlucky run (another
    process, a cold cache) does not decide the ratio shown in class.
    """
    values1, values2 = [float(i) for i in range(n)], [float(i) for i in range(n)]
    x, y = np.arange(n, dtype=np.float64), np.arange(n, dtype=np.float64)

    def best_of(compute, repeats: int = 3) -> tuple[float, float]:
        times = []
        for _ in range(repeats):
            start = time.perf_counter()
            result = compute()
            times.append(time.perf_counter() - start)
        return result, min(times)

    total_python, python_seconds = best_of(lambda: sum(a * b for a, b in zip(values1, values2)))
    total_numpy, numpy_seconds = best_of(lambda: float(np.dot(x, y)))

    return {
        "elements": f"{n:,}",
        "python_lists": f"{python_seconds * 1000:,.0f} ms",
        "numpy_arrays": f"{numpy_seconds * 1000:,.1f} ms",
        "numpy_is": f"{python_seconds / numpy_seconds:,.0f} times faster",
        "same_result": math.isclose(total_python, total_numpy, rel_tol=1e-9),
    }


def memory_footprint(n: int = 10_000) -> dict:
    """How many bytes the same numbers take as a list of floats and as an array."""
    values = [float(i) for i in range(n)]
    array = np.arange(n, dtype=np.float64)
    pointers = sys.getsizeof(values)
    objects = sum(sys.getsizeof(value) for value in values)
    return {
        "elements": f"{n:,}",
        "list_pointers": f"{pointers:,} bytes",
        "list_float_objects": f"{objects:,} bytes",
        "array_total": f"{array.nbytes:,} bytes",
        "bytes_per_element": f"{pointers / n + objects / n:.0f} vs {array.itemsize}",
    }


def data_path(name: str) -> str:
    """A writable path under var/data/ for the save and load demo."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return (DATA_DIR / name).as_posix()

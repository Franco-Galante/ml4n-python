"""Long-form content for 02_numpy.py: table specs, code snippets, speaker notes.

The viewer swaps only the first line of a call for its rendering, so anything
too long for one lecture line lives here and the lecture keeps a single call.
"""

# The presenter is the same as in lecture 1: one place to edit the portrait.
from .python_content import AUTHORS  # noqa: F401  (re-exported for the title slide)

# ------------------------------------------------------------- why numpy --
LIST_VS_ARRAY = {
    "headers": ["", "Python list", "NumPy array"],
    "widths": ["18%", "41%", "41%"],
    "rows": [
        ["**Memory**", "A table of references, each to an object with its own header: 8 + 24 = **32 bytes** per `float`", "One **contiguous** buffer of raw values: **8 bytes** per `float64`"],
        ["**Type checks**", "At **every** element: each object carries its own type", "**Once** for the entire array: one `dtype`"],
        ["**Access**", "Follow a reference to each object, wherever it is in memory", "Values side by side: the CPU reads them in large, cache-friendly blocks"],
        ["**Operations**", "Python loops: several bytecode instructions and a new object per element", "**Vectorized**: the loop runs in compiled code, with no Python object per element"],
    ],
}

IMPORT_NUMPY = [
    ("what everybody writes", "import numpy as np\n\nnp.array([1, 2, 3])", "python"),
]

# ------------------------------------------------------ numpy arrays --
DTYPES = {
    "headers": ["Family", "NumPy types", "Notes"],
    "widths": ["20%", "36%", "44%"],
    "rows": [
        ["**Integers**", "`int8`, `int16`, `int32`, `int64`", "`uint8` ... `uint64` for the unsigned ones. The number is the width **in bits**"],
        ["**Floats**", "`float16`, `float32`, `float64`", "`float64` is the default for decimal data, `float32` halves the memory"],
        ["**Booleans**", "`bool`", "One byte per element: this is what a mask is made of"],
    ],
}

CREATION = {
    "headers": ["Function", "What you get"],
    "widths": ["44%", "56%"],
    "rows": [
        ["`np.array(my_list, dtype=np.float16)`", "An array from a Python list; the `dtype` is inferred when you do not give one"],
        ["`np.zeros(shape)`, `np.ones(shape)`", "All zeros, or all ones, of the given shape"],
        ["`np.full(shape, value)`", "Every element equal to `value`"],
        ["`np.linspace(start, stop, num)`", "`num` samples from `start` to `stop`, **stop included**"],
        ["`np.arange(start, stop, step)`", "Like `range`, with a step: **stop excluded**"],
        ["`np.random.random(shape)`", "Uniform random numbers in [0, 1)"],
        ["`np.random.normal(mean, std, shape)`", "Random numbers from a normal distribution"],
    ],
}

# ------------------------------------------------------------ computation --
UFUNCS = {
    "headers": ["Kind", "Examples", "Element by element?", "What comes out"],
    "widths": ["18%", "34%", "24%", "24%"],
    "rows": [
        ["**Binary ufunc**", "`x + y`, `x - y`, `x * y`, `x / y`, `x % y`, `x // y`, `x ** y`", "**Yes**: pairs the cells in the same position", "Same shape as the inputs"],
        ["**Unary ufunc**", "`np.abs(x)`, `np.exp(x)`, `np.log(x)`, `np.sin(x)`, ...", "**Yes**: one cell at a time", "Same shape; `x` is **not modified**"],
        ["**Aggregation**", "`x.sum()`, `x.mean()`, `x.std()`, `x.min()`, `x.argmax()`", "**No**: combines many cells into one", "One value, or one axis less with `axis=`"],
        ["**Algebra**", "`np.dot(x, y)`, `x @ y`", "**No**: rows against columns", "The shape of the matrix product"],
    ],
}

SORTING = [
    ("a sorted copy", "y = np.sort(x)\n# x is not modified", "python"),
    ("sorted in place", "x.sort()\n# x itself is now sorted", "python"),
]

# ---------------------------------------------------------- accessing --
INDEXING = {
    "headers": ["Kind", "Syntax", "View or copy?"],
    "widths": ["26%", "38%", "36%"],
    "rows": [
        ["**Simple indexing**", "`x[1, 2]`", "A **single value**: one integer per axis"],
        ["**Slicing**", "`x[start:stop:step, start:stop:step]`, one slice per axis", "A **view**: writing into it writes into `x`"],
        ["**Masking**", "`x[x > 4]`", "A **copy**: 1-D when the mask has the same shape as `x`; a mask on a single axis keeps the other axes"],
        ["**Fancy indexing**", "`x[[1, 3]]`", "A **copy**"],
        ["**Combined**", "`x[1]` (= `x[1, :]`), `x[:, 1]`, `x[0, 1:]`, `x[[0, 2], :2]`", "A **view** if it mixes only simple indexing and slicing; a **copy** as soon as a mask or a list is involved"],
    ],
}

VIEW_VS_COPY = [
    ("a view: x changes too", 'view = x[:, 1:]\nview[:, :] = 0\n# x is now [[1,0,0],[4,0,0],[7,0,0]]', "python"),
    ("a copy: x is safe", 'x1 = x[:, 1:].copy()\nx1[:, :] = 0\n# x is unchanged', "python"),
]

MASK_NOTE = "The mask is itself an array of bool, the same shape as x: x > 4 does not return a single True/False, it compares every element."

# --------------------------------------------------- working with arrays --
SAVE_LOAD = [
    ("one array", 'x = np.arange(10)\nnp.save("tempfile", x)      # writes tempfile.npy\ny = np.load("tempfile.npy")', "python"),
    ("several arrays", 'np.savez("archive", x=arr1, y=arr2)\narchive = np.load("archive.npz")\narchive["x"]', "python"),
]

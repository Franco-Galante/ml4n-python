"""Long-form content for 01_python.py: table specs, captions, speaker notes.

The viewer swaps only the first line of a call for its rendering, so anything
too long for one lecture line lives here and the lecture keeps a single call.
"""

# ----------------------------------------------------------------- title --
AUTHORS = [
    {"name": "Franco Galante", "affiliation": "Politecnico di Torino", "image": "images/01_python/franco_galante.jpg"},
]

# ------------------------------------------------ executing Python programs --
RUN_SCRIPT = [
    ("~/Documents/MyScript/my_script.py", 'print("Hello")', "python"),
    ("terminal", "cd ~/Documents/MyScript\npython3 my_script.py"),
]

# Name tags for images/01_python/VS_code_1.png: x and y are percent of the
# image, place is where the tag sits relative to that point (see slides.py).
# `description` is revealed step by step by explain() in a card placed at
# `note`; in the handout the same text prints as the numbered legend.
VSCODE_LABELS = [
    {"x": 3.0, "y": 73.8, "text": "Activity bar", "number": 1, "place": "right-of", "description": "switch between Explorer, Search, Source Control, Run and Debug, Extensions.", "note": {"x": 17.0, "y": 73.8, "place": "right-of"}},
    {"x": 12.3, "y": 23.0, "text": "Explorer", "number": 2, "place": "center", "description": "the files of the project folder.", "note": {"x": 19.0, "y": 23.0, "place": "right-of"}},
    {"x": 53.0, "y": 21.8, "text": "Editor", "number": 3, "place": "center", "description": "one tab per open file.", "note": {"x": 53.0, "y": 25.0, "place": "below"}},
    {"x": 55.0, "y": 76.5, "text": "Integrated terminal", "number": 4, "place": "center", "description": "a normal PowerShell or bash, already inside the project folder (*View → Terminal*).", "note": {"x": 55.0, "y": 80.0, "place": "below"}},
    {"x": 95.9, "y": 97.2, "text": "Status bar: Python interpreter", "title": "Status bar", "number": 5, "place": "above-left", "description": "among other things, the Python interpreter in use.", "note": {"x": 95.9, "y": 89.5, "place": "above-left"}},
    {"x": 88.1, "y": 6.2, "text": "Run button", "number": 6, "place": "left-of", "description": "runs the open file with that interpreter, in the integrated terminal.", "note": {"x": 81.0, "y": 10.0, "place": "below"}},
    {"x": 2.9, "y": 30.25, "text": "Extensions", "place": "right-of"},
]

# Same conventions, for images/01_python/VS_code_2_python_extension.png.  All
# cards open in the empty terminal area; the number badge ties each to its tag.
_EXTENSION_NOTE = {"x": 24.0, "y": 80.0, "place": "right-of"}
EXTENSION_LABELS = [
    {"x": 3.0, "y": 30.25, "text": "Extensions view", "number": 1, "place": "right-of", "description": "many useful extensions live here, e.g. **Remote - SSH** (work on a remote machine as if it were local) or **Claude Code** (an AI coding assistant).", "note": _EXTENSION_NOTE},
    {"x": 21.8, "y": 10.5, "text": "Search", "number": 2, "place": "right-of", "description": "type *python* to find the Python extensions.", "note": _EXTENSION_NOTE},]

IDE_VS_NOTEBOOK = {
    "headers": ["", "IDE", "Jupyter notebook"],
    "widths": ["20%", "40%", "40%"],
    "rows": [
        ["**Best for**", "More **complex** projects, with many files", "**Simple** scripts and prototypes"],
        ["**Strengths**", "More powerful **debug** commands and code **editing** tools", "A great **visualization** tool: inspect the results step by step"],
        ["**Typical result**", "A project you run and debug inside the IDE", "A **report** with Python code, its output, and text for explanations"],
    ],
}

# ------------------------------------------------------ Python language --
JAVA_VS_PYTHON = [
    ("Java", "List<Integer> l = new LinkedList<>();\nfor (int i=0; i<4; i++) {\n    l.add(i);\n}"),
    ("Python", "l = []\nfor i in range(0,4):\n    l.append(i)", "python"),
]

# ------------------------------------------------------ basic data types --
DATA_TYPES = {
    "headers": ["", "Types", "Mutable?"],
    "widths": ["28%", "36%", "36%"],
    "rows": [
        ["**Basic building blocks**", "`int`, `float`, `bool`, `str`, `None`", "**No**: all of these objects are immutable"],
        ["**Containers**: sequence", "`tuple`", "**No**: an immutable list of objects"],
        ["**Containers**: collections", "`list`, `set`, `dict`", "**Yes**: mutable collections of objects"],
    ],}

# ---------------------------------------------------------- containers --
CONTAINERS = {
    "headers": ["", "tuple", "list", "set", "dict"],
    "widths": ["24%", "19%", "19%", "19%", "19%"],
    "rows": [
        ["Mutable", "No", "Yes", "Yes", "Yes"],
        ["Ordered", "Yes", "Yes", "No", "Yes, insertion order (Python 3.7+)"],
        ["Unique values", "No", "No", "Yes", "Yes (keys)"],
        ["Limitations on values", "No", "No", "Must be hashable", "Keys must be hashable"],
        ["Search cost (`in`)", "O(n)", "O(n)", "O(1)", "O(1)"],
    ],}

# ---------------------------------------------- controlling program flow --
# Read, not run: the class knows what break and continue do, and stepping
# through the turns of the loop would cost more than the point is worth.
BREAK_CONTINUE = """seen = []
for vehicle in ["car", "skip", "end", "van"]:
    if vehicle == "skip":
        continue          # jump to the next iteration
    elif vehicle == "end":
        break             # leave the loop altogether
    seen.append(vehicle)  # only "car" makes it into seen"""

# ------------------------------------------------------------ functions --
COMPREHENSION_SYNTAX = "res_list = [f(el) for el in iterable]"

DEFAULT_ARGS = """def func(a, b, c="defC", d="defD"):
    print(f"{a}, {b}, {c}, {d}")

func(1, 2)             # 1, 2, defC, defD  - the defaults for c and d
func(1, 2, "a")        # 1, 2, a, defD     - c by position, d by default
func(1, 2, d="b")      # 1, 2, defC, b     - d by keyword, c by default
func(b=2, a=1, d="b")  # 1, 2, defC, b     - keyword order does not matter

func(1, c="a")         # TypeError: func() missing 1 required positional argument: 'b'"""

# -------------------------------------------------------------- classes --
METHOD_TEMPLATE = "class MyClass:\n    def my_method(self, param1, param2):\n        ...\n        self.attr1 = param1\n        ..."

PRIVATE_TRIANGLE = """class Triangle:
    def __init__(self, a, b, c):
        self.a, self.b, self.c = a, b, c
        self.__perimeter = a + b + c  # 2 leading underscores make the attribute private

    def get_perimeter(self):
        return self.__perimeter"""

# ------------------------------------------ details: bytecode and execution --
# Used by 01_python_details.py, the companion file for in-depth material.
BYTECODE_JAVA_PYTHON = {
    "headers": ["", "Java", "Python"],
    "widths": ["20%", "40%", "40%"],
    "rows": [
        ["**When bytecode is produced**", "Explicitly, ahead of time: `javac` produces `.class` files, and you **distribute the bytecode**", "Implicitly, when you run or import a file: you **distribute the source**, and `.pyc` files are just a cache"],
        ["**What bytecode is**", "A stable, **standardized** format: it runs on any JVM, and other languages target it (Kotlin, Scala)", "An **internal detail** that changes between Python versions"],
        ["**Types**", "Known at compile time, so the bytecode is type-specific (`iadd` for ints, `dadd` for doubles)", "Generic (`BINARY_OP +`): type checks happen **at runtime**, on every operation"],
        ["**Execution**", "Interpreted at first, but hot code is **JIT-compiled** as standard: long-running programs mostly run generated machine code", "Mostly **interpreted**"],
    ],
    "caption": "**Result:** Java is typically much faster on CPU-heavy code, thanks to both static types and the JIT.",
}

# ------------------------------------------------------ files, exceptions --
OPEN_CLOSE = [
    ("open and close", 'f = open("my_file.txt", "r")\n...\nf.close()', "python"),
    ("with statement", 'with open("my_file.txt", "r") as f:\n    ...', "python"),
]

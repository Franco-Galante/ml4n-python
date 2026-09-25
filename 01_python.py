"""Machine Learning for Networking - Introduction to Python.

It covers last year's Python lecture (Introduction to Python). The slides are
now **interactive**: they run the code and show the values of variables on a 
panel. The code is executed in a **Python virtual environment** created by `uv`.

    uv run python tools/prepare_lecture.py 01_python
    npm run --prefix edtrace/frontend dev '--' --port 5173 --strictPort
    open http://localhost:5173/?trace=01_python

This lecture is based on "Introduction to Python" by Andrea Pasini, Flavio
Giobergia, Elena Baralis, and Gabriele Ciravegna.
"""

from edtrace import text
from support.python_content import AUTHORS, BREAK_CONTINUE, COMPREHENSION_SYNTAX, CONTAINERS, DATA_TYPES, DEFAULT_ARGS, EXTENSION_LABELS, IDE_VS_NOTEBOOK, JAVA_VS_PYTHON, METHOD_TEMPLATE, OPEN_CLOSE, PRIVATE_TRIANGLE, RUN_SCRIPT, VSCODE_LABELS
from support.python_lab import describe, interpreter_facts, make_triangle, read_text
from support.slides import CALLOUT, SUBLIST, SUBSUBLIST, annotated_figure, code_block, code_row, demo, explain, figure, people_row, section, table_all, table_head, table_row, theme


def main() -> None:
    title()
    executing_python_programs()
    development_scenarios()
    python_language()
    basic_data_types()
    tuples_and_lists()
    sets_and_dictionaries()
    copying_objects()
    controlling_program_flow()
    functions()
    lambdas_and_comprehensions()
    classes()
    files()
    closing()
    before_lab_1()


def title():
    theme()  # vertical rhythm for the whole page: renders an invisible <style>
    # ---------- Title ----------  @hide
    text("# Machine Learning for Networking")
    text("## Introduction to Python")
    people_row(AUTHORS, gap="22px", photo="170px", name_size="18px")  # @stepover

    section("The Python part of the course")
    text("1. **Python engine and language** - setup, data types, object oriented programming *(today)*")
    text("2. **Numpy library** - computation with multi-dimensional arrays")
    text("3. **Pandas library** - tabular data and data preprocessing")
    text("4. **Matplotlib library** - data visualization and graphics")

    section("Today")
    text("- **Executing Python programs**: Python programs, Python setup")
    text("- **Python language**: data types, controlling program flow, functions, lambda functions, list comprehensions, classes")
    text("- And to close: reading and writing **files**")
    text("- **Lab 1**: a first hands-on experience with Python")
    variable_panel = "Here!"  # any inspected variable opens the panel
    text("**How to read this lecture:** every code example now *runs*, the values of the variables are shown in a overlay panel. While I step through the code watch the variable panel!", style=CALLOUT)  # @inspect variable_panel


def executing_python_programs():
    text("# 1. Executing Python programs")
    section("Python is an interpreted language")  # @clear variable_panel
    text("- Code is **not compiled** to machine language.", style=SUBLIST)
    text("- However, the source code is compiled to an intermediate level, called **bytecode**.", style=SUBLIST)
    text("- For this reason, to run Python programs you need an **interpreter** that is able to execute the bytecode.", style=SUBLIST)
    text("The sequence of operations executed by the interpreter:")
    figure("images/01_python/interpreter_pipeline.svg")  # @stepover

    text("- **Caching**: the bytecode of each module you `import` is saved in `__pycache__/` and reused.", style=SUBLIST)
    text("- When you edit the file, Python notices and translates it again.", style=SUBSUBLIST)
    text("- **Main advantage of bytecode**: the translation to bytecode is automatic and the same on every machine, so you share the source code as is and it runs on any system with a Python interpreter.", style=SUBLIST)
    text("- Only the interpreter is built for each platform, not your program, as would happen in C or C++.", style=SUBSUBLIST)

    section("A common Python 3 setup on a Linux system")
    text("Typically in the `/usr/bin` folder:")
    text("- `python3`: run Python programs", style=SUBLIST)
    text("- `ipython3`: run programs line by line", style=SUBLIST)
    text("- `jupyter`: run a Jupyter notebook", style=SUBLIST)
    text("- `pip3`: install Python packages", style=SUBLIST)
    text("To find where your Python commands live, on **Linux and macOS** use `which <command>`:")
    figure("images/01_python/terminal_which.png", width="671px")  # same width as where.exe: terminal text at the body size @stepover
    text("On **Windows**, in PowerShell, use `where.exe <command>`. Type the `.exe`: in PowerShell a bare `where` is an alias of `Where-Object`, not the command lookup.")
    figure("images/01_python/terminal_where.png", width="671px")  # same width as which: terminal text at the body size @stepover
    text("- Several matches: the **first one on the `PATH`** is the one that runs when you type `python`.", style=SUBLIST)
    text("- `where.exe` is easy to use, but it only searches the current folder and the folders listed in `PATH`: an installation that is not on the `PATH` is not reported. To find **all** of them, search the disk (slow on a whole drive): `Get-ChildItem C:\\ -Recurse -Filter python.exe -ErrorAction SilentlyContinue`", style=SUBLIST)

    section("Executing a Python program")
    code_row(RUN_SCRIPT)  # @stepover
    text("Type in your terminal: move to the folder that contains the script, then hand the script to the interpreter.")

    section("Running Python line by line with IPython")
    text("Type `ipython3` (or `ipython`, depending on your installation) in your terminal:")
    figure("images/01_python/interactive_python.mp4", width="1044px", poster="images/01_python/interactive_python_poster.png")  # terminal text at the body size @stepover

    section("Installing libraries")
    text("- Python comes with many useful libraries: **Numpy, Pandas, Matplotlib, Scikit-learn, SciPy**, ...", style=SUBLIST)
    text("- To use any of them, you first have to install it with the `pip` command: `pip3 install <package>`, e.g. `pip3 install numpy`, `pip3 install pandas`. On **Windows** the command is usually just `pip`.", style=SUBLIST)
    figure("images/01_python/pip_install.png", width="767px")  # terminal text at the body size @stepover

    section("Virtual environments")
    text("- The `pip` command associates the libraries to your **default Python installation**.", style=SUBLIST)
    text("- A more powerful way of managing libraries is to use a Python **environment** (`virtualenv` or `conda`).", style=SUBLIST)
    text("- Useful when you have **many projects** that use different libraries and **configurations** (e.g. versions).", style=SUBSUBLIST)
    text("- Each project is associated to its own virtual environment.", style=SUBSUBLIST)
    text("This lecture is itself a Python program, running inside the virtual environment of the course repository:")
    facts = interpreter_facts()  # @inspect facts
    text("- `in_virtual_env` is `True`: the course uses `uv`, which creates the environment in `.venv/` (`uv sync`) and runs commands inside it.", style=SUBLIST)


def development_scenarios():
    text("# 2. Development scenarios")
    text("Typically two:")
    text("1. Develop your Python **project** with an **IDE**, for example Visual Studio Code or PyCharm.", style=SUBLIST)
    text("- **Debug** and **run** your code inside the IDE.", style=SUBSUBLIST)
    text("2. Develop and test a Python **script** with a **Jupyter notebook**.", style=SUBLIST)
    text("- Inspect the results **step by step**, and keep the history of the output of the script.", style=SUBSUBLIST)
    text("**Note:** notebooks **do not work well with git**, because they store outputs and metadata next to the code.", style=CALLOUT)

    section("Scenario 1: Visual Studio Code (IDE)")
    text("In VS Code a **project is a folder**: open the folder (*File → Open Folder*), not a single file.")
    annotated_figure("images/01_python/VS_code_1.png", VSCODE_LABELS)  # @stepover
    explain(VSCODE_LABELS, 1)  # @stepover
    explain(VSCODE_LABELS, 2)  # @stepover
    explain(VSCODE_LABELS, 3)  # @stepover
    explain(VSCODE_LABELS, 4)  # @stepover
    explain(VSCODE_LABELS, 5)  # @stepover
    explain(VSCODE_LABELS, 6)  # @stepover

    text("Out of the box VS Code is a text editor: Python support comes from an **extension**.")
    annotated_figure("images/01_python/VS_code_2_python_extension.png", EXTENSION_LABELS)  # @stepover
    explain(EXTENSION_LABELS, 1)  # @stepover
    explain(EXTENSION_LABELS, 2)  # @stepover

    section("Scenario 2: Jupyter notebook")
    text("- Jupyter needs the `notebook` package: install it with `pip install notebook`.", style=SUBLIST)
    text("- Then type `jupyter notebook` in your terminal: Jupyter opens in your browser.", style=SUBLIST)
    text("- Click **New**, then **Python 3**, to create a new, empty notebook.", style=SUBLIST)
    figure("images/01_python/notebook_setup.mp4", poster="images/01_python/notebook_setup_poster.png")  # @stepover
    text("A notebook is a sequence of **cells**:")
    text("- **Markdown cells**: comments, titles, and the organization of your work.", style=SUBLIST)
    text("- **Code cells**: the code to run.", style=SUBLIST)
    text("- **Output cells**: under each code cell, the result of running it.", style=SUBLIST)
    text("- Based on the **IPython** command.", style=SUBLIST)
    text("- Each code cell can be executed **separately** by pressing `CTRL + ENTER`.", style=SUBLIST)
    text("⚠️ **Stale imports**: the cells run in one Python process, the **kernel**, which loads each module only **once**. After editing your own module, running `import` again keeps the old version: **restart the kernel** (or turn on `%autoreload`).", style=CALLOUT)

    section("IDE vs Jupyter notebook")
    table_head(IDE_VS_NOTEBOOK)  # @stepover
    table_row(IDE_VS_NOTEBOOK, "**Best for")  # @stepover
    table_row(IDE_VS_NOTEBOOK, "**Strengths")  # @stepover
    table_row(IDE_VS_NOTEBOOK, "**Typical result")  # @stepover


def python_language():
    text("# 3. Python language")
    section("Clean and concise syntax")
    text("- No semi-colons to end instructions", style=SUBLIST)
    text("- No braces to define if clauses and for loops", style=SUBLIST)
    text("- No need to specify variable types", style=SUBLIST)
    code_row(JAVA_VS_PYTHON)  # @stepover

    section("Python is an object-oriented language")
    text("Every piece of data in the program is an **object**.")
    text("- Objects have **properties** and **functionalities**.", style=SUBLIST)
    text("- Even a simple **integer** number is a Python object, with a *type*, an *id* and a *value*.", style=SUBLIST)

    demo("Defining a variable")
    text("**No need** to specify its data type: **just assign** a value to a new variable name.")
    a = 3  # @inspect a
    a_type = type(a).__name__  # @inspect a_type
    a_id = id(a)  # @inspect a_id
    figure("images/01_python/variable_reference.svg")  # @stepover
    text("`type()` and `id()` read two properties of the object `a` refers to; the third is the value itself.")
    text("In Python, a **variable is a reference to an object**: when you assign an object to a variable, the variable becomes a reference to that object.")  # @clear a a_type a_id

    section("Variables are references")
    text("A single Python object can have **multiple references** (aliases):")
    code_block("x = 3\ny = x", language="python")  # @stepover
    figure("images/01_python/object_references.svg")  # @stepover

    demo("Verify this reasoning with id()")
    text("`id(my_variable)` returns the **identifier** of the object that the variable is referencing.")
    x = 5.6  # @inspect x
    y = x  # @inspect y
    id_x = id(x)  # @inspect id_x
    id_y = id(y)  # @inspect id_y
    text("Same identifier: `x` and `y` are two references to **one** object. Now, if you assign `y` to a new value...")
    y = 3  # @inspect y
    id_y = id(y)  # @inspect id_y
    text("...`id_y` changes and `id_x` does not: `x` still refers to the float `5.6`, while `y` refers to a **new** integer object.")
    figure("images/01_python/immutable_rebinding.svg")  # @stepover @clear x y id_x id_y
    text("What this shows is **rebinding**: `y = 3` does not touch the float object, it points `y` at a different one, and `x` is left alone. The **question** now is whether an object can be **changed** once it exists.", style=CALLOUT)

    section("Mutable and immutable objects")
    text("Starting again from two \"references\" pointing to one float, let's try to modify its value:")
    x = 5.6  # @inspect x
    y = x  # one object, two names @inspect y
    y = y + 1  # @inspect y
    text("`x` is still `5.6`: `y + 1` did **not** add 1 to the object the two names share, it built a **new** float and rebound `y` onto it. There is no operation that changes a float - none exists.")
    text("Now the very same script, with a **list**:")  # @clear x y
    l1 = [1, 2, 3]  # @inspect l1
    l2 = l1  # one object, two names @inspect l2
    l2.append(4)  # @inspect l2 l1
    text("This time `l1` changed as well, and the two names still point to **one** object:")
    same_object = l1 is l2  # @inspect same_object
    text("**Immutable** (`int`, `float`, `bool`, `str`, `tuple`, `None`): the object can never change, so every *modification* is really a new object. **Mutable** (`list`, `set`, `dict`): the object itself changes, and every reference to it sees the change.", style=CALLOUT)


def basic_data_types():
    text("# 4. Python data types")
    section("Basic building blocks and containers")
    table_head(DATA_TYPES)  # @stepover
    table_row(DATA_TYPES, "**Basic")  # @stepover
    table_row(DATA_TYPES, "**Containers**: seq")  # @stepover
    table_row(DATA_TYPES, "**Containers**: col")  # @stepover
    text("**Note:** Python is *dynamically typed*. Watch the type of `value` on the panel:", style=CALLOUT)
    value = 1  # @inspect value
    value = "hello"  # @inspect value
    text("The object has a type; the variable is just a reference, and it can refer to an object of any type.")

    demo("int, float")  # @clear value
    text("- **No theoretical size limit**: effectively limited by the available memory.", style=SUBLIST)
    text("- Available operations: `+`, `-`, `*`, `/`, `//` (integer division), `%` (remainder), `**` (exponentiation).", style=SUBLIST)
    x = 9  # @inspect x
    y = 5  # @inspect y
    r1 = x // y  # @inspect r1
    r2 = x % y  # @inspect r2
    r3 = x / y  # @inspect r3
    r4 = x ** 2  # @inspect r4
    text("Note that dividing 2 **integers** with `/` yields a **float**: look at the type of `r3`.")
    big = 2 ** 200  # @clear x y r1 r2 r3 r4
    digits = len(str(big))  # @inspect digits
    text("And no size limit: `2 ** 200` is an exact integer with that many digits, no overflow.")

    demo("bool")  # @clear digits
    text("Can assume the values `True` and `False`. Boolean operators: `and`, `or`, `not`.")
    is_sunny = True  # @inspect is_sunny
    is_rainy = not is_sunny  # @inspect is_rainy
    temperature1 = 30
    temperature2 = 35
    raising = temperature2 > temperature1  # @inspect raising
    text("A comparison is an expression like any other: its value is a `bool`.")

    demo("str")  # @clear is_sunny is_rainy raising
    text("Definition with **single or double quotes** is equivalent: pick the one that lets you write the other inside the string.")
    string1 = "Python's nice"  # with double quotes @inspect string1
    string2 = 'He said "yes"'  # with single quotes @inspect string2
    text("The quotes are only the delimiters: the panel shows the text itself, without them.")

    demo("Conversion between types")  # @clear string1 string2
    x = 9.8
    y = 4
    r1 = int(x)  # @inspect r1
    r2 = float(y)  # @inspect r2
    r3 = str(x)  # @inspect r3
    r4 = float("6.7")  # @inspect r4
    r5 = bool("True")  # @inspect r5
    r6 = bool(0)  # @inspect r6
    text("Only `0`, `\"\"`, `[]`, `{}`, `set()` and `()` convert to `False` through `bool()`. Which means:")
    r7 = bool("False")  # a non-empty string @inspect r7 @clear r1 r2 r3 r4
    text("`bool()` does not read the text: any non-empty string is `True`.")

    demo("Strings are immutable")  # @clear r5 r6 r7
    text("Changing a character raises an error. An error would stop this lecture, so we catch it with `try`/`except` and put the message on the panel:")
    str1 = "example"  # @inspect str1
    try:
        str1[0] = "E"  # will cause an error
    except TypeError as error:
        message = describe(error)  # @inspect message
    text("Use instead a **new** string, built from the old one:")
    str1 = "E" + str1[1:]  # @inspect str1 @clear message
    text("`str1` now refers to a new object: the original `\"example\"` was never modified.")

    demo("Sub-strings")  # @clear str1
    text("- `str[start:stop]`: the start index is **included**, the stop index is **excluded**, and indices start **from 0**.", style=SUBLIST)
    text("- We can optionally specify a step, `str[start:stop:step]`: see the list section.", style=SUBLIST)
    text("- Shortcuts: **omit start** to begin from the beginning, **omit stop** to go until the end of the string.", style=SUBLIST)
    s1 = "Hello"  # @inspect s1
    charact = s1[0]  # @inspect charact
    s2 = s1[0:3]  # @inspect s2
    s3 = s1[1:]  # @inspect s3
    s4 = s1[:3]  # @inspect s4
    s5 = s1[:]  # @inspect s5
    text("**Negative indices** count characters from the end: `-1` is the last character.")
    s1 = "MyFile.txt"  # @inspect s1 @clear charact s2 s3 s4 s5
    s2 = s1[:-1]  # @inspect s2
    s3 = s1[:-2]  # @inspect s3
    s4 = s1[-3:]  # @inspect s4
    text("`s1[-3:]` is the usual way to read a file extension.")

    demo("Strings: concatenation")  # @clear s1 s2 s3 s4
    text("Use the `+` operator:")
    string1 = "Value of "
    sensor_id = "sensor 1."
    message = string1 + sensor_id  # concatenation @inspect message
    val = 0.75
    message = "Value: " + str(val)  # float to str @inspect message
    text("The `str()` is not optional:")
    try:
        message = "Value: " + val  # without str()
    except TypeError as error:
        message = describe(error)  # @inspect message
    text("`+` joins a string only with another string.")

    section("Formatted string literals (f-strings)")  # @clear message
    text("Introduced in **Python 3.6**. Suppose you want to build the string *My float is 17.5 and my int is 5* out of two variables. Syntax: `f\"My float is {var1} and my int is {var2}\"`")
    figure("images/01_python/fstring_anatomy.svg")  # @stepover
    var1 = 17.5  # @inspect var1
    var2 = 5  # @inspect var2
    sentence = f"My float is {var1} and my int is {var2}"  # @inspect sentence
    text("No `str()` needed: every value in braces is converted for you.")

    demo("None")  # @clear var1 var2 sentence
    text("Specifies that a reference **does not contain data**.")
    my_var = None  # @inspect my_var
    if my_var is None:
        my_var = 10  # @inspect my_var
    text("Useful to represent **missing data** in a list or a table, and to initialize an empty variable that will be assigned later on (e.g. when computing a min/max).")


def tuples_and_lists():
    text("# 5. Tuples and lists")
    demo("Tuple")
    text("An **immutable** sequence of variables. Definition:")
    t1 = ("Turin", "Italy")  # city and state @inspect t1
    t2 = "Paris", "France"  # optional parentheses @inspect t2
    t3 = ("Rome", 2, 25.6)  # can contain different types @inspect t3
    t4 = ("London",)  # tuple with a single element @inspect t4
    t5 = ("London")  # without the comma @inspect t5
    text("The comma makes the tuple, not the parentheses: `t5` is just a string.")

    demo("Tuple unpacking")  # @clear t1 t2 t3 t4 t5
    text("**Assigning** a tuple to a set of variables:")
    city_record = ("Turin", "Italy", 12)  # a different name from the city_data below, so the panel lists it in the order it is built @inspect city_record
    city, state, temperature = city_record  # @inspect city state temperature
    text("**Swapping** elements is an interesting case of unpacking:")
    a = 1  # @inspect a @clear city_record city state temperature
    b = 2  # @inspect b
    a, b = b, a  # @inspect a b
    text("The right-hand side builds the tuple `(2, 1)` first, then it is unpacked into `a` and `b`: no temporary variable needed.")

    demo("Tuple: concatenation and access")  # @clear a b
    text("Tuples can be **concatenated**, and a **new** tuple is generated upon concatenation:")
    city = "Turin", "Italy"  # @inspect city
    temperatures = 6, 15  # @inspect temperatures
    city_data = city + temperatures  # @inspect city_data
    text("Accessing elements: `t[start:stop]`, with an optional step, exactly like strings.")
    t1 = ("a", "b", "c", "d")  # @inspect t1 @clear city temperatures city_data
    val1 = t1[0]  # @inspect val1
    t2 = t1[1:]  # @inspect t2
    t3 = t1[:-1]  # @inspect t3
    try:
        t1[0] = 2  # will cause an error: a tuple is immutable
    except TypeError as error:
        message = describe(error)  # @inspect message
    text("Slicing a tuple is allowed, since it builds a new tuple; assigning to an element is not.")

    section("List")  # @clear t1 val1 t2 t3 message
    text("A **mutable** sequence of heterogeneous elements. Each element is a **reference** to a Python object.")
    figure("images/01_python/list_references.svg")  # @stepover

    demo("List: definition")
    l1 = []  # empty list @inspect l1
    l2 = [1, "str", 5.6, None]  # can contain different types @inspect l2
    a, b, c, d = l2  # can be assigned to variables @inspect a b c d
    text("Unpacking works on any sequence, not only on tuples.")

    demo("List: adding elements and concatenating lists")  # @clear l1 l2 a b c d
    l1 = [2, 4, 6]  # @inspect l1
    l2 = [10, 12]  # @inspect l2
    l1.append(8)  # append an element to l1 @inspect l1
    l3 = l1 + l2  # concatenate 2 lists @inspect l3
    text("`append` modifies `l1` in place; `+` leaves both lists alone and builds a third one.")

    demo("List: accessing elements")  # @clear l1 l2 l3
    text("Same syntax as tuples, but this time **assignment is allowed**:")
    l1 = [0, 2, 4, 6]  # @inspect l1
    val1 = l1[0]  # @inspect val1
    a, b = l1[1:-1]  # @inspect a b
    l1[0] = "a"  # @inspect l1
    text("We can also specify a **step**: `[start:stop:step]`.")
    l1 = [0, 1, 2, 3, 4]  # @inspect l1 @clear val1 a b
    l2 = l1[::2]  # step = 2 skips 1 element @inspect l2
    l3 = l1[::-1]  # step = -1 reads the list in reverse order @inspect l3
    l4 = l1[::-2]  # step = -2 reverse order, skip 1 element @inspect l4
    text("The same steps work on strings and tuples: `\"Hello\"[::-1]` is `\"olleH\"`.")

    demo("The in operator")  # @clear l1 l2 l3 l4
    text("**Check** whether an element belongs to a list:")
    l1 = [0, 1, 2]  # @inspect l1
    myval = 2
    found = myval in l1  # True, since 2 is in l1 @inspect found
    text("**Iterate** over the list elements. Where the slide prints each element, we collect it in `output`: `print()` only reaches the terminal, not this screen.")
    output = []  # @clear found
    for el in l1:  # @inspect el
        output.append(el)  # instead of print(el) @inspect output
    text("Same loop, same order as the list.")

    demo("List: sum, min, max, sort")  # @clear el output
    l1 = [0, 1, 2, 3, 4]  # @inspect l1
    min_val = min(l1)  # @inspect min_val
    max_val = max(l1)  # @inspect max_val
    sum_val = sum(l1)  # @inspect sum_val
    l1 = [3, 2, 5, 7]  # @inspect l1
    l2 = sorted(l1)  # @inspect l2
    text("`sorted()` returns a **new** sorted list: `l1` is unchanged.")
    l1.sort()  # sorts l1 itself, and returns nothing @inspect l1
    text("`list.sort()` does the opposite: it sorts the list **in place**. Same order, but now it is `l1` that changed.")


def sets_and_dictionaries():
    text("# 6. Sets and dictionaries")
    demo("Set")
    text("An **unordered** collection of **unique** elements. Definition:")
    s0 = set()  # empty set @inspect s0
    s1 = {1, 2, 3}  # @inspect s1
    s2 = {3, 3, "b", "b"}  # duplicates are dropped @inspect s2
    s3 = set([3, 3, 1, 2])  # from a list @inspect s3
    text("Watch out: `{}` is **not** an empty set - it is an empty dictionary. Use `set()`.")
    text("Add and remove elements:")  # @clear s0 s2 s3
    s1.add("4")  # @inspect s1
    s1.remove(3)  # @inspect s1
    text("`\"4\"` is a string, not the number `4`: a set can hold elements of different types.")

    demo("The in operator on sets")  # @clear s1
    s1 = set([0, 1, 2, 3, 4])  # @inspect s1
    myval = 2
    found = myval in s1  # True, since 2 is in s1 @inspect found
    text("**Note:** sets are **unordered**: the order of iteration is not well-defined. Two sets with the same elements are equal, whatever order you write them in:", style=CALLOUT)
    same_set = {1, 2, 3} == {3, 2, 1}  # @inspect same_set @clear s1 found
    output = []
    for el in {3, 2, 1}:  # @inspect el
        output.append(el)  # instead of print(el) @inspect output
    text("Written as `{3, 2, 1}`, iterated in another order: it depends on how Python stores the elements, not on how you wrote them. Never rely on it.")

    demo("Set example: removing list duplicates")  # @clear same_set el output
    input_list = [1, 5, 5, 4, 2, 8, 3, 3]  # @inspect input_list
    out_list = list(set(input_list))  # @inspect out_list
    text("**Note:** the order of the original elements is not preserved.")

    demo("Dictionary")  # @clear input_list out_list
    text("A collection of **key-value** pairs that allows fast **access** of elements **by key**. Keys are **unique**.")
    d1 = {"Name": "John", "Age": 25}  # @inspect d1
    d0 = {}  # empty dictionary @inspect d0
    text("**Keys** must be **hashable** types: e.g. `int`, `float`, `str`, `bool`, `tuple`. **Values** can be any Python object.")
    d1 = {("a", "b"): 120, ("c", "d", "e"): 1000}  # itemsets and their support @inspect d1 @clear d0
    try:
        d2 = {["a", "b"]: 120}  # a list as a key
    except TypeError as error:
        message = describe(error)  # @inspect message
    text("Lists and dictionaries are **not hashable**: they are mutable, so their hash could change. The same applies to the elements of sets!")

    demo("Dictionary: access by key")  # @clear d1 message
    images = {10: "plane.png", 25: "flower.png"}  # @inspect images
    img10 = images[10]  # @inspect img10
    try:
        img0 = images[0]  # get an error if the key does not exist
    except KeyError as error:
        message = describe(error)  # @inspect message
    img0 = images.get(0)  # .get() returns None if the key does not exist @inspect img0
    img0 = images.get(0, "notfound.png")  # optionally, a default value @inspect img0
    text("Reading **keys** and **values**:")
    occurrences = {"Car": 33, "Truck": 55}  # @inspect occurrences @clear images img10 message img0
    keys = list(occurrences.keys())  # @inspect keys
    values = list(occurrences.values())  # @inspect values
    text("**Note:** `keys()` and `values()` return **views** on the original data, not copies. A view sees later changes:")
    key_view = occurrences.keys()  # @clear keys values
    occurrences["Van"] = 12  # @inspect occurrences
    keys_now = list(key_view)  # the same view, read again @inspect keys_now

    demo("Dictionary: adding, updating, deleting")  # @clear occurrences keys_now
    occur = {"Car": 33, "Truck": 55}  # @inspect occur
    occur["Car"] = 56  # update an existing value @inspect occur
    occur["Road"] = 3  # add a new key @inspect occur
    del occur["Truck"]  # delete a key @inspect occur
    text("Check whether a **key** exists with `in`:")
    has_car = "Car" in occur  # @inspect has_car
    has_truck = "Truck" in occur  # @inspect has_truck
    text("`in` on a dictionary looks at the **keys**, not at the values.")

    demo("Dictionary: iterating keys and values")  # @clear occur has_car has_truck
    text("E.g. get the cumulative price of the items in a market basket:")
    basket = {"Cola": 0.99, "Apples": 1.5, "Salt": 0.4}  # @inspect basket
    price = 0
    output = []
    for k, v in basket.items():  # @inspect k v
        price += v  # @inspect price
        output.append(f"{k}: {price}")  # instead of print @inspect output
    text('- Previous Python versions had no order guarantee; since **Python 3.7** dictionaries officially preserve **insertion order** (see more at <a href="https://docs.python.org/3/whatsnew/3.7.html" target="_blank">What\'s New In Python 3.7</a>).', style=SUBLIST)

    section("tuple vs list vs set vs dict")  # @clear basket k v price output
    table_all(CONTAINERS)  # the whole comparison at a glance @stepover


def copying_objects():
    text("# 7. Shallow vs deep copy")
    section("Two ways of copying")
    text("- **Shallow**: copies the parent object, and shares the references to its children.", style=SUBLIST)
    text("- **Deep**: recursively copies all the children of the parent object.", style=SUBLIST)
    figure("images/01_python/shallow_vs_deep_copy.svg")  # @stepover

    demo("Shallow copy")
    temperatures = {"Turin": [10, 12, 10], "Milan": [15, 16, 16]}  # @inspect temperatures
    temp2 = temperatures.copy()  # @inspect temp2
    temp2["Turin"].append(13)  # edit a child node @inspect temperatures temp2
    temp2["Rome"] = [10, 11, 10]  # edit the parent node @inspect temperatures temp2
    text("- **Changes in the child** structure (the list): `temperatures` sees the `13` too.", style=SUBLIST)
    text("- **No changes in the parent** structure (the dict): the key `'Rome'` was not added to `temperatures`.", style=SUBLIST)

    demo("Deep copy")  # @clear temperatures temp2
    import copy

    temperatures = {"Turin": [10, 12, 10], "Milan": [15, 16, 16]}  # @inspect temperatures
    temp2 = copy.deepcopy(temperatures)  # @inspect temp2
    temp2["Turin"].append(13)  # edit a child node @inspect temperatures temp2
    temp2["Rome"] = [10, 11, 10]  # edit the parent node @inspect temperatures temp2
    text("**No changes at all** to `temperatures`: every list was copied.", style=CALLOUT)


def controlling_program_flow():
    text("# 8. Controlling program flow")

    demo("if / elif / else")
    text("Conditions are expressed with `>`, `<`, `>=`, `<=`, `==`, `!=`, and can include the boolean operators `and`, `not`, `or`.")
    sensor_on = True  # @inspect sensor_on
    temperature = 15.5  # @inspect temperature
    if sensor_on and temperature == 10:
        message = "Temperature is 10"  # @inspect message
    elif sensor_on and 10 < temperature < 20:
        message = "Temperature is between 10 and 20"  # @inspect message
    else:
        message = "Temperature is out of range, or the sensor is off"  # @inspect message
    text("Only the branch that is taken runs: change `temperature` and a different line lights up.")
    text("- **No parentheses** around the condition and **no braces** around the body: a colon opens the block, the **indentation** delimits it.", style=SUBLIST)  # @clear sensor_on temperature message
    text("- Comparisons can be **chained**, as in maths: `10 < temperature < 20`.", style=SUBLIST)

    demo("Indentation is not a matter of style")
    text("It is the only thing that tells Python which lines belong to the `if`, so getting it wrong is an error at **compile time**:")
    try:
        compile('if sensor_on:\nprint("Temperature is 10")', "my_script.py", "exec")  # missing indentation
    except IndentationError as error:
        message = describe(error)  # @inspect message
    text("Four spaces per level, and never mix tabs and spaces in the same file.")

    demo("for")  # @clear message
    text("To iterate a fixed number of times, use `range(start, stop)` - as for slices, `stop` is **excluded**:")
    for i in range(5, 8):  # three turns: 5, 6, 7 @inspect i
        txt = f"The value of i is {i}"  # @inspect txt
    text("`i` is handed to you at every turn: no counter to declare, and none to increment.")
    text("To iterate over a collection, Python gives you its **elements**, not their indices. `enumerate` gives you both:")  # @clear i txt
    my_list = ["a", "b", "c"]  # @inspect my_list
    for i, element in enumerate(my_list):  # @inspect i element
        txt = f"my_list[{i}] is {element}"  # @inspect txt
    text("And `zip` walks **two collections at a time**:")
    l1 = ["a", "b", "c"]  # @inspect l1 @clear my_list i element txt
    l2 = ["A", "B", "C"]  # @inspect l2
    for el1, el2 in zip(l1, l2):  # @inspect el1 el2
        txt = f"el1: {el1}, el2: {el2}"  # @inspect txt
    text("`enumerate` and `zip` both hand out **tuples**, unpacked straight into the loop variables.")

    demo("while")  # @clear l1 l2 el1 el2 txt
    text("Iterate **while** the specified condition is `True`:")
    counter = 0  # @inspect counter
    while counter < 5:
        counter += 2  # increment counter by 2 @inspect counter
    text("The condition is checked **before** every turn: after the third one `counter` is 6, and the loop does not start again.")

    section("break / continue")  # @clear counter
    text("They alter the flow of a `for` or a `while` loop: `continue` jumps to the next iteration, `break` leaves the loop altogether.")
    code_block(BREAK_CONTINUE, language="python")  # @stepover
    text("Three turns only: `skip` is skipped, `end` stops the loop, and `van` is never even read.")
    text("⚠️ Careful when the same loop reads the **lines of a file**: every line keeps its newline, so the value to compare is `'skip\\n'` and not `'skip'`, and nothing is ever skipped. `line.strip()` is the fix - we come back to it in section 12.", style=CALLOUT)


def functions():
    text("# 9. Functions")
    demo("Defining and invoking a function")
    text("Functions are **essential** to organize code and avoid repetitions.")
    import math

    def euclidean_distance(x, y):  # function name and parameters
        dist = 0  # @inspect dist
        for x_el, y_el in zip(x, y):  # @inspect x_el y_el
            dist += (x_el - y_el) ** 2  # @inspect dist
        return math.sqrt(dist)  # return value (alternatively, dist**0.5)

    result1 = f"{euclidean_distance([1, 2, 3], [2, 4, 5]):.2f}"  # invocation @inspect result1

    demo("Variable scope: local")  # @clear result1 result2
    text("Scope rules specify the **visibility** of variables.")

    def my_func(x, y):
        w = 5  # defined inside the function: local scope @inspect w
        return x + y + w

    result = my_func(2, 4)  # @inspect result
    try:
        value = w  # outside the function
    except NameError as error:
        message = describe(error)  # @inspect message
    text("The `w` of the function is **not accessible from outside**: it disappeared when the function returned.")

    demo("Variable scope: global")  # @clear result message
    text("Variables defined **outside** the function can be read inside it. (Here \"outside\" is the lecture function around it; in a notebook cell it is the global scope - the rules are the same.)")

    def my_func(x, y):
        return x + y + z  # z can be read inside the function

    z = 5  # define z in the global scope
    result = my_func(2, 4)  # @inspect result
    text("**Global scope vs local scope**: what if the function assigns `z` itself?")

    def my_func(x, y):  # @clear result
        z = 2  # define z in the local scope @inspect z
        return x + y + z  # use z from the local scope

    z = 5  # define z in the global scope
    result = my_func(2, 4)  # @inspect result
    text(f"`result` is 8, and the global `z` is still **{z}**: the assignment inside the function created a *local* `z`, it did not modify the global one.")

    demo("Functions can return tuples")  # @clear result

    def add_sub(x, y):
        return x + y, x - y

    summ, diff = add_sub(5, 3)  # @inspect summ diff
    sentence = f"Sum is {summ}, difference is {diff}."  # @inspect sentence

    section("Parameters with default value")  # @clear summ diff sentence
    code_block(DEFAULT_ARGS, language="python")  # @stepover
    text("Parameters with a default can be omitted; the others cannot.")


def lambdas_and_comprehensions():
    text("# 10. Lambda functions and comprehensions")
    demo("Lambda functions")
    text("Functions that can be defined **inline** and **without a name**:")
    squared = lambda x: x**2  # input parameter(s): return value
    result = squared(5)  # @inspect result
    text("**Sort / min / max by key**: the lambda tells the function *what to compare*.")
    records = [{"name": "v1", "val": 5}, {"name": "v2", "val": 1}, {"name": "v3", "val": 6}]  # @inspect records @clear result
    min_val = min(records, key=lambda r: r["val"])  # the dict with the smallest val @inspect min_val
    sorted_records = sorted(records, key=lambda r: r["val"])  # ordered by the values of the val key @inspect sorted_records
    text("Without `key`, Python would have to compare two dicts, which it refuses to do.")

    section("List comprehensions")  # @clear records min_val sorted_records
    text("Allow creating **lists** from other **iterables** (e.g. a list or a tuple). Useful for implementing the **map pattern**. Syntax:")
    code_block(COMPREHENSION_SYNTAX, language="python")  # @stepover
    text("- `for el in iterable`: iterate all the elements", style=SUBLIST)
    text("- `f(el)`: transform `el` into another value", style=SUBLIST)

    demo("Map, then filter + map")
    text("Example: convert the dictionary keys to uppercase (map pattern).")
    dct = {"a": 10, "b": 20, "c": 30}  # @inspect dct
    my_list = [s.upper() for s in dct.keys()]  # @inspect my_list
    text("Comprehensions also allow specifying **conditions** on elements. Example: square the positive numbers of a list (filter + map patterns).")
    my_list1 = [-1, 4, -2, 6, 3]  # @inspect my_list1 @clear dct my_list
    my_list2 = [el**2 for el in my_list1 if el > 0]  # @inspect my_list2
    text("The `if` filters first, then `el**2` maps what is left.")

    demo("Other comprehensions")  # @clear my_list1 my_list2
    text("**Dictionary comprehensions**: similarly to lists, allow building dictionaries.")
    keys = ["a", "b", "c"]
    values = [-1, 4, -2]
    my_dict = {k: v for k, v in zip(keys, values)}  # @inspect my_dict
    text("**Set comprehensions**: same syntax with braces and a single expression.")
    squares = {v**2 for v in [4, 3, 2, -2, 1]}  # @inspect squares
    text("`2` and `-2` square to the same `4`, which the set keeps only once.")

    text("List comprehensions and lambda functions can shorten your code, but... **pay attention to readability!** And **comments are welcome!**", style=CALLOUT)  # @clear my_dict squares


def classes():
    text("# 11. Classes")
    section("Classes and objects")
    text("A **class** is a model that specifies a collection of:")
    text("- **attributes** (= variables)", style=SUBLIST)
    text("- **methods** (that interact with attributes)", style=SUBLIST)
    text("- a **constructor** (a special method called to initialize an object)", style=SUBLIST)
    text("An **object** is an **instance** of a specific class. Example:")
    text("- class: `Triangle` (all the triangles have 3 edges)", style=SUBLIST)
    text("- object: a specific instance of `Triangle`", style=SUBLIST)

    demo("A simple class")

    class Triangle:  # class name
        num_edges = 3  # attribute definition

    triangle1 = Triangle()  # class instantiation
    edges = triangle1.num_edges  # access to the attribute @inspect edges
    text("In this example, all the object instances of `Triangle` have the same value for `num_edges`: 3.")

    demo("Constructor and initialization")  # @clear edges

    class Triangle:
        num_edges = 3

        def __init__(self, a, b, c):  # self is always the first parameter, then the constructor parameters
            self.a = a  # initialize the attributes @inspect self.a
            self.b = b  # @inspect self.b
            self.c = c  # @inspect self.c

    triangle1 = Triangle(2, 4, 3)  # invoke the constructor and instantiate a new Triangle @inspect triangle1.a triangle1.b triangle1.c
    triangle2 = Triangle(2, 5, 2)  # @inspect triangle2.a triangle2.b triangle2.c
    text("`self` is a reference to the **current object**: the same `__init__` filled in two different triangles.")

    section("Methods")  # @clear triangle1.a triangle1.b triangle1.c triangle2.a triangle2.b triangle2.c
    text("- Equivalent to Python functions, but defined **inside a class**.", style=SUBLIST)
    text("- The first argument is always `self` (a reference to the current object), which allows accessing the object attributes.", style=SUBLIST)
    code_block(METHOD_TEMPLATE, title="example", language="python")  # @stepover

    demo("Example with methods")

    class Triangle:
        def __init__(self, a, b, c):
            self.a, self.b, self.c = a, b, c

        def get_perimeter(self):  # method
            return self.a + self.b + self.c  # use self to refer to the attributes

    triangle1 = Triangle(2, 4, 3)  # the constructor again, this time without stepping into it @stepover
    perimeter = triangle1.get_perimeter()  # method invocation: self is passed automatically @inspect perimeter
    text("We wrote `triangle1.get_perimeter()`, and Python called `get_perimeter(triangle1)`.")

    demo("Private attributes")  # @clear perimeter
    text("Methods or attributes that are available **only inside the object** and **not accessible from outside**: necessary for elements that are useful to the object but must not be seen or modified from outside.")

    code_block(PRIVATE_TRIANGLE, language="python")  # the same class as above, with one private attribute @stepover
    triangle1 = make_triangle(2, 4, 3)  # the class above, built without stepping through it again
    perimeter = triangle1.get_perimeter()  # the public method reads the private attribute @inspect perimeter
    try:
        perimeter = triangle1.__perimeter  # cannot access private attributes
    except AttributeError as error:
        message = describe(error)  # @inspect message
    text("Under the hood Python **renames** the attribute to `_Triangle__perimeter`: private by convention, protected against accidents, not locked.")


def files():
    text("# 12. Files")
    section("File handling")
    text("Use `open(filename, mode)` to read or write a file. Watch out for the mode: `\"r\"` reading, `\"w\"` writing, `\"a\"` append.")
    code_row(OPEN_CLOSE)  # @stepover
    text("- We always need to remember `f.close()`. Unless... we use the **with** statement!", style=SUBLIST)
    text("- It avoids remembering to close the file, and even in case of errors it guarantees a correct closure.", style=SUBSUBLIST)

    demo("The long way: open, use, close")
    path = "var/data/my_file.txt"  # @inspect path
    f = open(path, "w")  # "w" creates the file, or empties it if it exists
    f.write("car\nskip\ntruck\nend\nvan\n")  # five lines, each ending with a newline
    f.close()  # nothing is guaranteed to be on disk until this runs
    closed = f.closed  # every file object knows whether it is closed @inspect closed
    text("`closed` is an **attribute** of the file object, not a method: it is `False` while the file is open and `True` once it has been closed.")

    demo("The short way: the with statement")  # @clear closed
    with open(path, "r") as f:
        first_line = f.readline()  # @inspect first_line
    closed = f.closed  # closed automatically when the with block ends @inspect closed
    text("One line less, and no way to forget the `close()` - even if an error interrupts the block.")

    demo("How to read")  # @clear first_line closed
    with open(path, "r") as f:
        lines = f.readlines()  # readlines() reads all the lines at once @inspect lines
    output = []
    with open(path, "r") as f:
        for line in f:  # same as reading one line at a time @inspect line
            output.append(line.strip())  # @inspect output
    text("What if the file is **too big** to fit in memory? **Chunk it!** `read(n)` reads `n` characters at a time:")
    chunks = []  # @clear lines line output
    with open(path, "r") as f:
        chunk = f.read(5)  # @inspect chunk
        while chunk:
            chunks.append(chunk)  # @inspect chunks
            chunk = f.read(5)  # @inspect chunk
    text("An empty string means the end of the file, which stops the `while`. The newlines count as characters too.")

    demo("How to write")  # @clear chunk chunks
    scratch = "var/data/scratch.txt"
    with open(scratch, "w") as f:
        f.write("Two weeks of measurements\n")
    with open(scratch, "w") as f:  # opening with w cancels all the existing content
        f.write("Ops I deleted everything!")
    content = read_text(scratch)  # @inspect content
    text("Example: make a **copy** of a file.")
    copy_path = "var/data/my_file_copy.txt"  # @clear content
    with open(path, "r") as f1:
        with open(copy_path, "w") as f2:
            for line in f1:
                f2.write(line)
    copied = read_text(copy_path)  # @inspect copied
    text("**Iterating over the file object** is what reads the file **line by line**: `for line in f1` hands out one line per turn, and never loads the whole file into memory.", style=CALLOUT)
    text("`write` does not add newlines: the copy has them because every `line` still carries its own.")


def closing():
    text("# Wrapping up")
    text("1) **Variables are references** to objects. Basic types are immutable: a new value is a new object.", style=SUBLIST)
    text("2) **tuple, list, set, dict**: pick the container by mutability, order, uniqueness and search cost.", style=SUBLIST)
    text("3) **Copies are shallow** by default: `copy.deepcopy` when the children must not be shared.", style=SUBLIST)
    text("4) **Scope**: a function reads global variables, but assigning creates a local one.", style=SUBLIST)
    text("5) **Comprehensions and lambdas** shorten code; readability decides how much.", style=SUBLIST)



def before_lab_1():
    text("# 13. Lab 1")
    text("*A first hands-on session: use what we saw today, and get a first taste of a (statistical) machine learning approach.*")

    section("Where to run it")
    text("- **Google Colab**: a notebook in the browser, nothing to install, Python and the usual libraries already there.", style=SUBLIST)
    text("- Or the **course Jupyter cluster**: the same idea, on our machines (the link is on the course page).", style=SUBLIST)
    text("- Either way, **no setup today**: open the notebook there and work in the browser.", style=SUBLIST)
    text("- ⚠️ A Colab session is thrown away when it ends: **download your notebook** before you close it.", style=SUBLIST)

    section("What you will do")
    text("1. **Warm-up**: short exercises on exactly what we saw - strings, lists and tuples, dictionaries, functions and lambdas.", style=SUBLIST)
    text("2. **Iris**: load a dataset of 150 flowers - 4 measurements and one species each - as a list of lists, with the `csv` module.", style=SUBLIST)
    text("3. **Statistics by hand**: mean and standard deviation of each measurement, first over the whole dataset, then per species.", style=SUBLIST)
    text("4. **A first classifier**: find which measurement separates the three species best, turn it into a couple of rules, and measure the **accuracy** of those rules.", style=SUBLIST)
    text("No numpy, no pandas, no scikit-learn: plain Python is already enough to classify something - and to feel where it starts to hurt, which is exactly what the next lectures fix.", style=CALLOUT)

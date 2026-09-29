"""Machine Learning for Networking - NumPy: Numerical Python.

It covers last year's NumPy lecture. The slides are now **interactive**: they
run the code and draw every array on the variable panel, which is where the
matrices of the original slides came from.

    uv run python tools/prepare_lecture.py 02_numpy
    npm run --prefix edtrace/frontend dev '--' --port 5173 --strictPort
    open http://localhost:5173/?trace=02_numpy

This lecture is based on "Numpy: Numerical Python" by Andrea Pasini, Flavio
Giobergia, Elena Baralis, and Gabriele Ciravegna.
"""

import numpy as np

from edtrace import note, text
from support.numpy_content import AUTHORS, CREATION, DTYPES, IMPORT_NUMPY, INDEXING, LIST_VS_ARRAY, MASK_NOTE, SAVE_LOAD, SORTING, UFUNCS, VIEW_VS_COPY
from support.numpy_lab import compare_speed, data_path, describe, memory_footprint
from support.slides import CALLOUT, EXERCISE, SUBLIST, SUBSUBLIST, code_row, demo, figure, people_row, section, table_head, table_row, theme


def main() -> None:
    title()
    numpy_and_efficiency()
    numpy_arrays()
    computation()
    broadcasting()
    accessing_arrays()
    working_with_arrays()
    closing()


def title():
    theme()  # vertical rhythm for the whole page: renders an invisible <style>
    # ---------- Title ----------  @hide
    text("# Machine Learning for Networking")
    text("## NumPy: Numerical Python")
    people_row(AUTHORS, gap="22px", photo="170px", name_size="18px")  # @stepover

    section("Today")
    text("1. **NumPy and computation efficiency**")
    text("2. **NumPy arrays**: creation, data types, axes and shape")
    text("3. **Computation with NumPy arrays**: universal functions, aggregations, sorting, algebra")
    text("4. **Broadcasting**: operations between arrays with different shape")
    text("5. **Accessing NumPy arrays**: indexing, slicing, masking, fancy indexing")
    text("6. **Working with arrays**: concatenating, splitting, reshaping, saving")
    variable_panel = "Here!"  # any inspected variable opens the panel
    text("**How to read this lecture:** every code example *runs*, the values of the variables are shown in an overlay panel. While I step through the code watch the variable panel!", style=CALLOUT)  # @inspect variable_panel
    text("✍️ **Exercises, in class:** three notebooks in `exercises/02_numpy/`. We stop and do them as we go - **2.1** after the arrays, **2.2** after the operations and broadcasting, **2.3** after indexing and manipulation.", style=EXERCISE)


def numpy_and_efficiency():
    text("# 1. NumPy and computation efficiency")
    text("NumPy is not part of Python itself: install it inside your virtual environment with `pip install numpy` (on Google Colab it is already installed).")

    section("Loading NumPy")
    text("- `import library_name` loads a library, and `as` defines the name you use to refer to it in your code.", style=SUBLIST)
    code_row(IMPORT_NUMPY)  # @stepover
    text("This is the way everybody calls NumPy: `np`. It is just a convention, but try to respect it, it helps readability.", style=SUBLIST)
    version = np.__version__  # the NumPy that is running this lecture @inspect version

    section("From lists to arrays")  # @clear version
    text("The main object of NumPy is the **array**. As in the snippet above, one way to create it is from a Python list:")
    arr = np.array([0.67, 0.45, 0.33])  # @inspect arr
    dtype = str(arr.dtype)  # @inspect dtype
    shape = arr.shape  # @inspect shape
    text("- **Fixed type**: all its elements have the same type, the `dtype`.", style=SUBLIST)
    text("- `float64` is a 64-bit floating point number: each element occupies **8 bytes**.", style=SUBSUBLIST)
    text("- **Multidimensional**: it represents vectors, matrices and n-dimensional arrays; the `shape` gives the size along each dimension.", style=SUBLIST)
    text("- **Flexible indexing**: besides the usual slices, you can select elements with conditions or with lists of positions (section 5).", style=SUBLIST)

    section("Why NumPy")  # @clear arr dtype shape
    text("The inner product of two vectors of one million numbers, stored as two **Python lists** (and computed with a Python loop) and as two **NumPy arrays** (and computed with one NumPy call), measured when running the lecture:")
    speed = compare_speed(1_000_000)  # @inspect speed
    text("And the memory taken by 10 000 numbers, stored as a list of floats and as an array:")
    memory = memory_footprint(10_000)  # @inspect memory
    text("Same result, **much faster**, and about **four times less memory**. We will see in a moment where the difference comes from.", style=CALLOUT)
    text("- This is why NumPy is the foundation of the data science libraries: **scikit-learn**, **SciPy** and **pandas** are built on it.", style=SUBLIST)

    section("Where the difference comes from")  # @clear speed memory
    text("A list stores **references**: that is what lets it hold anything, but every element pays for it - each element is a reference to a full Python object, and each object carries its own header:")
    text("- **The list object**: a fixed header, plus the address of the array of slots.", style=SUBLIST)
    text("- **The slots**: one 8-byte reference per element.", style=SUBLIST)
    text("- **One object per element**: a `float` takes 24 bytes - 16 of header (reference count, type), 8 for the value.", style=SUBLIST)
    figure("images/02_numpy/python_list_memory.svg", width="864px")  # drawn at 1.2x its natural size, so its lettering matches the body text @stepover
    text("A NumPy array is **fixed-type** (no **per-element** overhead) and sits at **contiguous memory addresses**:")
    figure("images/02_numpy/numpy_array_memory.svg", width="828px")  # @stepover
    text("Side by side, this is where both the memory and the speed difference come from:")
    table_head(LIST_VS_ARRAY)  # @stepover
    table_row(LIST_VS_ARRAY, "**Memory")  # @stepover
    table_row(LIST_VS_ARRAY, "**Type checks")  # @stepover
    table_row(LIST_VS_ARRAY, "**Access")  # @stepover
    table_row(LIST_VS_ARRAY, "**Operations")  # @stepover
    text("**Note:** *one object per element* is the typical case, since values computed or read from a file are all distinct objects. But a list can hold the **same** object many times: `[0.0] * 10_000` has 10 000 slots referring to **one** float (the same aliasing as `l2 = l1` in lecture 1, and safe because floats are immutable), so it takes about 8 bytes per element. A NumPy array takes 8 bytes per element whatever the values.", style=CALLOUT)


def numpy_arrays():
    text("# 2. NumPy arrays")
    section("From nested lists to multidimensional arrays")
    text("Arrays can have an **arbitrary number of dimensions**. In section 1 we built a vector from a list; **nested** lists give arrays with more dimensions:")
    arr1 = np.array([1, 2, 3])  # a vector @inspect arr1
    arr2 = np.array([[1, 2, 3],  # a 2D matrix @inspect arr2
                     [4, 5, 6]])
    arr3 = np.array([[[1, 2, 3], [4, 5, 6]],  # a 3D array @inspect arr3
                     [[7, 8, 9], [10, 11, 12]],
                     [[13, 14, 15], [16, 17, 18]]])

    section("Axes and shape")
    text("- The **axes** of an array define its dimensions: a 1-D vector has 1 axis, a 2D matrix has 2 axes, an ND array has N axes.", style=SUBLIST)
    text("- The **shape** is a tuple that specifies the number of elements along each axis.", style=SUBLIST)
    figure("images/02_numpy/axes_and_shape.svg", width="888px")  # @stepover
    text("- Each new dimension is added **on the left** of the shape: it becomes axis 0, and the existing axes shift one position to the right.")
    text("- Axes can also be numbered with **negative** values, counting from the end. **Axis -1 is always along the rows** (within each row, across the columns), whatever the number of dimensions:")
    figure("images/02_numpy/negative_axes.svg", width="888px")  # @stepover

    demo("Shapes, on the panel")
    vector_shape = arr1.shape  # the arrays created above @inspect arr1 vector_shape
    matrix_shape = arr2.shape  # (height, width) @inspect arr2 matrix_shape
    cube_shape = arr3.shape  # (depth, height, width) @inspect arr3 cube_shape
    text("A one-element tuple is written `(3,)`: the comma is what makes it a tuple, as we saw in lecture 1.")  # @clear arr1 vector_shape arr2 matrix_shape arr3 cube_shape

    section("Data types")
    text("NumPy defines **its own** data types, and all the elements of an array share **a single** one (the `dtype`, as we saw in section 1).")
    table_head(DTYPES)  # @stepover
    table_row(DTYPES, "**Integers")  # @stepover
    table_row(DTYPES, "**Floats")  # @stepover
    table_row(DTYPES, "**Booleans")  # @stepover

    demo("dtype")
    arr = np.array([0.0, 1.0, 2.0])  # @inspect arr
    dtype = arr.dtype  # @inspect dtype
    whole = np.array([0, 1, 2]).dtype  # no decimal point: integers @inspect whole
    mixed = np.array([1, 2.5]).dtype  # an int and a float: everything becomes float64 @inspect mixed
    small = np.array([0.0, 1.0, 2.0], dtype=np.float16).dtype  # asked for explicitly @inspect small
    text("The dtype is **inferred** from the values unless you ask for one; with mixed values, NumPy picks a type that can hold them all (**upcasting**). `float16` takes 2 bytes per element instead of 8, at the price of precision.")  # @clear arr dtype whole mixed small

    section("1-D vector* vs column vector")
    text("\\* A 1-D vector is often called a *row vector*, and it behaves like one; strictly speaking, though, a row vector is 2D, with shape `(1, 3)`.")
    figure("images/02_numpy/row_vs_column.svg", width="744px")  # @stepover
    b =np.array([0.1, 0.2, 0.3])  # a 1-D vector: one axis, it behaves like a row @inspect b
    b_shape = b.shape  # @inspect b_shape
    a = np.array([[0.1], [0.2], [0.3]])  # a column vector @inspect a
    a_shape = a.shape  # @inspect a_shape
    text("**A column vector is a 2D matrix** with one column. Keep an eye on this: it is where the broadcasting surprises come from.", style=CALLOUT)  # @clear b b_shape a a_shape

    section("Creating arrays from scratch")
    table_head(CREATION)  # @stepover
    table_row(CREATION, "`np.array(")  # @stepover
    table_row(CREATION, "`np.zeros(")  # @stepover
    table_row(CREATION, "`np.full(")  # @stepover
    table_row(CREATION, "`np.linspace(")  # @stepover
    table_row(CREATION, "`np.arange(")  # @stepover
    table_row(CREATION, "`np.random.random(")  # @stepover
    table_row(CREATION, "`np.random.normal(")  # @stepover

    demo("Creation, running")
    ones = np.ones((2, 3))  # @inspect ones
    filled = np.full((2, 1), 1.1)  # @inspect filled
    line = np.linspace(0, 1, 11)  # 11 samples, stop included @inspect line
    steps = np.arange(1, 7, 2)  # stop excluded @inspect steps
    text("`linspace` fixes **how many** samples you want, `arange` fixes **the step** between them.")  # @clear ones filled line steps
    np.random.seed(2)  # so that the lecture always shows the same numbers
    uniform = np.random.random((2, 3))  # uniformly distributed in [0, 1) @inspect uniform
    normal = np.random.normal(0, 1, (2, 3))  # mean 0, standard deviation 1 @inspect normal
    text("Without the `seed`, these two would be different at every run.")  # @clear uniform normal

    demo("Main attributes of an array")
    x = np.array([[2, 3, 4], [5, 6, 7]])  # @inspect x
    ndim = x.ndim  # number of dimensions @inspect ndim
    shape = x.shape  # tuple with the array shape @inspect shape
    size = x.size  # product of the shape values @inspect size
    as_functions = (np.ndim(x), np.shape(x), np.size(x))  # the same three, as functions @inspect as_functions
    text("`size` is how many numbers are in there, `shape` is how they are arranged.")  # @clear x ndim shape size as_functions
    text("✍️ **Your turn - `2.1_numpy_arrays.ipynb`, exercises 1, 2 and 3.** Build arrays from lists and read their `dtype`; count the rows and the columns of a 3D array; then create arrays from scratch with `ones`, `zeros`, `full`, `random` and `linspace`.", style=EXERCISE)


def computation():
    text("# 3. Computation with NumPy arrays")
    section("Operations on arrays")
    text("Four kinds of operations, all on entire arrays and without a Python loop:", style={"display": "block", "marginBottom": "20px"})
    table_head(UFUNCS)  # @stepover
    table_row(UFUNCS, "**Binary")  # @stepover
    table_row(UFUNCS, "**Unary")  # @stepover
    table_row(UFUNCS, "**Aggregation")  # @stepover
    table_row(UFUNCS, "**Algebra")  # @stepover
    text("Binary operations work on arrays of the **same shape** - the next section lifts that restriction:", style={"display": "block", "marginTop": "30px"})  # the gap a figure leaves after itself
    figure("images/02_numpy/elementwise.svg", width="624px")  # @stepover

    demo("Binary operations")
    x = np.array([[1, 1], [2, 2]])  # @inspect x
    y = np.array([[3, 4], [6, 5]])  # @inspect y
    product = x * y  # @inspect product
    total = x + y  # @inspect total
    powers = x**2  # @inspect powers
    text("`*` is **not** the matrix product: it multiplies the cells that sit in the same position.")  # @clear y product total powers

    demo("Unary operations")
    exponential = np.exp(x)  # @inspect exponential
    logarithms = np.log2(np.array([1.0, 2.0, 4.0, 8.0]))  # @inspect logarithms
    text("**Note:** the original array `x` is unchanged - a ufunc always returns a **new** array.")  # @clear exponential logarithms x

    section("Aggregate functions")
    text("- They return a **single value** from an array: `np.min(x)`, `np.max(x)`, `np.mean(x)`, `np.std(x)`, `np.sum(x)`, `np.argmin(x)`, `np.argmax(x)`.", style=SUBLIST)
    text("- Or equivalently, as methods of the array: `x.min()`, `x.max()`, `x.mean()`, `x.std()`, `x.sum()`, `x.argmin()`, `x.argmax()`.", style=SUBLIST)

    demo("Aggregating the entire array")
    x = np.array([[1, 1], [2, 2]])  # @inspect x
    total = x.sum()  # @inspect total
    average = x.mean()  # @inspect average
    spread = x.std()  # divides by n (population std); x.std(ddof=1) divides by n - 1 @inspect spread
    position = x.argmax()  # the position, not the value @inspect position
    figure("images/02_numpy/argmax_flat.svg", width="504px")  # @stepover
    text("`argmax` returns **where** the maximum is; with no axis, the position in the array read row by row.")  # @clear x total average spread position

    section("Aggregating along an axis")
    text("`axis=` says which dimension the operation runs along, and **that dimension is removed** from the output.")
    figure("images/02_numpy/aggregate_axis.svg", width="672px")  # @stepover

    demo("One value per row, one per column")
    x = np.array([[1, 7], [2, 4]])  # @inspect x
    row_sums = x.sum(axis=-1)  # one sum per row (for a matrix, the same as axis=1) @inspect row_sums
    column_argmax = x.argmax(axis=0)  # one index per column @inspect column_argmax
    shapes = (x.shape, row_sums.shape)  # (2, 2) in, (2,) out @inspect shapes
    text("Rule of thumb: `axis=-1` always moves **along** a row, whatever the number of dimensions, so it collapses each row into one number.")  # @clear x row_sums column_argmax shapes
    text("The same rule holds in three dimensions, one axis at a time:", style={"display": "block", "marginTop": "30px"})
    figure("images/02_numpy/aggregate_3d_last.svg", width="936px")  # @stepover
    figure("images/02_numpy/aggregate_3d_middle.svg", width="936px")  # @stepover

    section("Sorting")
    code_row(SORTING)  # @stepover
    text("- `np.sort(x)` creates a **sorted copy**, `x` is not modified. `x.sort()` sorts `x` **in place**.", style=SUBLIST)
    text("- The array is sorted along the **last axis (-1)** by default, and `axis=` changes that.", style=SUBLIST)

    demo("sort")
    x = np.array([[2, 1, 3], [7, 9, 8]])  # @inspect x
    by_row = np.sort(x)  # along axis -1 @inspect by_row
    still_x = x  # untouched @inspect still_x
    other = np.array([[2, 7, 3], [7, 2, 1]])  # @inspect other
    by_column = np.sort(other, axis=0)  # along axis 0 @inspect by_column
    text("Each row (or each column) is sorted on its own: sorting a matrix does not order the whole thing.")  # @clear still_x other by_column

    demo("argsort")
    text("`np.argsort(x)` returns the **positions** that would sort the array, again along axis -1:")
    figure("images/02_numpy/argsort.svg", width="552px")  # @stepover
    order = np.argsort(x)  # @inspect order
    text("The indices are what you need to sort **something else** by these values - a very common pattern.")  # @clear x by_row order

    section("Algebraic operations")
    text("`np.dot(x, y)` covers the inner product of two 1-D arrays, a matrix times a vector, and a matrix times a matrix:")
    figure("images/02_numpy/dot_products.svg", width="672px")  # @stepover

    x = np.array([1, 2, 3])  # @inspect x
    y = np.array([0, 2, 1])  # @inspect y
    inner = np.dot(x, y)  # 1*0 + 2*2 + 3*1 @inspect inner
    m = np.array([[1, 1], [2, 2]])  # @inspect m
    matrix_vector = np.dot(m, np.array([2, 3]))  # @inspect matrix_vector
    matrix_matrix = np.dot(m, np.array([[2, 2], [1, 1]]))  # @inspect matrix_matrix
    with_operator = m @ np.array([[2, 2], [1, 1]])  # same result, written with the operator @inspect with_operator
    text("Since **Python 3.5** the `@` operator is the matrix product, and it reads much better inside a long formula.")  # @clear x y inner m matrix_vector matrix_matrix with_operator
    text("✍️ **Your turn - `2.2_numpy_operations.ipynb`, exercises 1, 2 and 3.** Apply the sigmoid to an entire array with one ufunc; aggregate along the right axis; and find the three highest values and the **positions** of the two lowest ones.", style=EXERCISE)


def broadcasting():
    text("# 4. Broadcasting")
    section("Operations between arrays with different shape")
    text("A pattern that lets a smaller array take part in an operation with a bigger one, **without copying** anything in memory:")
    figure("images/02_numpy/broadcasting_cases.svg", width="564px")  # @stepover

    section("The rules of broadcasting")
    text("1. The shape of the array with **fewer dimensions** is padded with **leading ones** (shapes are compared **from the right**).", style=SUBLIST)
    text("2. If the shape along a dimension is **1** for one array and **greater than 1** for the other, the first is **stretched** to match the second.", style=SUBLIST)
    text("3. If a dimension has **different sizes, both greater than 1**, broadcasting **cannot be performed**.", style=SUBLIST)

    section("Example: compute x + y")
    text("`x` is a 1-D vector of shape (3,), `y` a column of shape (3, 1):")
    figure("images/02_numpy/broadcast_start.svg", width="408px")  # @stepover
    text("**Rule 1**: `x` has fewer dimensions, so its shape is padded with a leading one: (3,) becomes (1, 3).")
    figure("images/02_numpy/broadcast_rule1.svg", width="408px")  # @stepover
    text("**Rule 2**: every axis of size 1 is stretched, `x` downwards and `y` sideways, until both are (3, 3).")
    figure("images/02_numpy/broadcast_rule2.svg", width="360px")  # @stepover
    text("Now the shapes are equal, and the sum is element by element (Rule 3 never triggers here):")
    figure("images/02_numpy/broadcast_result.svg", width="228px")  # @stepover

    demo("A row plus a column")
    x = np.array([1, 2, 3])  # @inspect x
    shifted = x + 10  # the simplest case: a scalar is broadcast to every cell @inspect shifted
    y = np.array([[11], [12], [13]])  # @inspect y
    shapes = (x.shape, y.shape)  # (3,) and (3, 1) @inspect shapes
    z = x + y  # @inspect z
    z_shape = z.shape  # @inspect z_shape
    text("Rule 1 pads `x` to (1, 3), rule 2 stretches `x` downwards and `y` sideways: every pair meets, and the result is (3, 3).")  # @clear x shifted y shapes z z_shape

    demo("When broadcasting fails")
    x = np.array([[1, 2], [3, 4], [5, 6]])  # shape (3, 2) @inspect x
    y = np.array([11, 12, 13])  # shape (3,), padded to (1, 3) @inspect y
    try:
        z = x + y  # will cause an error
    except ValueError as error:
        message = describe(error)  # @inspect message
    figure("images/02_numpy/broadcast_fails.svg", width="432px")  # @stepover
    text("Rule 3: 2 and 3 are both greater than 1 and they differ. Compare the shapes **from the right**, and remember that a column vector is (3, 1) while a 1-D vector is (3,).", style=CALLOUT)  # @clear x y message
    text("✍️ **Your turn - `2.2_numpy_operations.ipynb`, exercises 4 and 5.** Multiply a (2, 3) array by a 2-element one: work out *from the shapes* why it fails, and what `x2` has to become for it to work; then **center** the columns of a data matrix (subtract from each column its mean) without a loop.", style=EXERCISE)


def accessing_arrays():
    text("# 5. Accessing NumPy arrays")
    demo("Simple indexing: one element")
    x = np.array([[2, 3, 4], [5, 6, 7]])  # @inspect x
    el = x[1, 2]  # read @inspect el
    x[1, 2] = 1  # write @inspect x
    last = x[0, -1]  # last element of the first row @inspect last
    second_last = x[0, -2]  # second from the end @inspect second_last
    text("One integer per axis, separated by commas, gives one element. Negative indices count from the end, as for lists and strings.")  # @clear x el last second_last

    section("Slicing: access ranges of elements")
    text("- `x[start:stop:step, start:stop:step]`, one slice per axis: from `start` (**included**) to `stop` (**excluded**), with a fixed step.", style=SUBLIST)
    text("- Omit `start` to begin at the beginning, `stop` to go until the end, `step` if you do not want to skip elements.", style=SUBLIST)
    figure("images/02_numpy/slicing_grid.svg", width="576px")  # @stepover

    demo("Two slices, one per axis")
    x = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])  # @inspect x
    all_rows_last_columns = x[:, 1:]  # or x[0:3, 1:3] @inspect all_rows_last_columns
    two_rows_every_other = x[:2, ::2]  # or x[0:2, 0:3:2] @inspect two_rows_every_other
    text("The first slice applies to the rows, the second to the columns.")  # @clear all_rows_last_columns two_rows_every_other

    demo("A slice is a view, not a copy")
    code_row(VIEW_VS_COPY)  # @stepover
    view = x[:, 1:]  # @inspect view
    view[:, :] = 0  # write into the view @inspect view x
    text("`x` changed, although it is not on the left-hand side of the assignment: a view is a window on the same data.")  # @clear view
    x = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])  # start again @inspect x
    safe = x[:, 1:].copy()  # a copy this time @inspect safe
    safe[:, :] = 0  # @inspect safe x
    text("With `.copy()` the original is out of reach. Writing straight through the slice, `x[:, 1:] = 0`, is the other way to change `x` on purpose.")  # @clear x safe

    demo("Fewer indices than axes: rows and columns")
    x = np.array([[2, 3, 4], [5, 6, 7]])  # @inspect x
    row = x[1]  # shorthand for x[1, :]: the missing index is a full slice @inspect row
    same_row = x[1, :]  # the same thing, written out @inspect same_row
    column = x[:, 1]  # for a column, the slice must be written explicitly @inspect column
    text("Missing indices are always filled **on the right** with `:`, so `x[1]` is a row and a column needs `x[:, 1]`. In both, the integer removes its axis, and the result is a **view**. The same rule comes back with masks and lists of indices.")  # @clear x row same_row column

    section("Masking: select with a boolean array")
    text("- `x[mask]`, where `mask` is a **boolean array with the same shape** as `x`, keeps the elements where the mask is `True`.", style=SUBLIST)
    text("- Masks are built by comparing: `x > 4`, and any of `>`, `>=`, `<`, `<=`, `==`, `!=`.", style=SUBLIST)
    text("- With a mask of the same shape as `x`, the result is a **one-dimensional** array, and a **copy** of the selected elements. (A mask on the first axis only selects whole rows instead, by the same rule as `x[1]`: `x[[True, False, True]]` is `x[[True, False, True], :]`.)", style=SUBLIST)

    demo("Masking, running")
    x = np.array([1.2, 4.1, 1.5, 4.5])  # @inspect x
    mask = x > 4  # a bool array, not a single True @inspect mask
    selected = x[mask]  # @inspect selected
    x2 = np.array([[1.2, 4.1], [1.5, 4.5]])  # @inspect x2
    mask2 = x2 > 1.3  # three elements out of four @inspect mask2
    selected2 = x2[mask2]  # @inspect selected2
    text("Even though `x2` is (2, 2), the result is 1-D: in general the selected elements do not form a rectangle (here, three cells out of four), so NumPy cannot keep the shape.")  # @clear x mask selected x2 mask2 selected2

    demo("Combining masks")
    text("Boolean operations between masks of the same shape use the **bitwise** operators `&` (and), `|` (or), `^` (xor), `~` (negation) - not the `and`/`or` keywords.")
    x = np.array([0.5, 1.0, 3.0, 5.0, 7.0])  # @inspect x
    between = ~((x < 1) | (x > 5))  # elements between 1 and 5, included @inspect between
    same = (x >= 1) & (x <= 5)  # the same mask, written the other way @inspect same
    values = x[between]  # @inspect values
    text("Mind the parentheses: `&` and `|` bind **tighter** than the comparisons.")  # @clear x between same values

    demo("Writing through a mask, and the copy")
    x = np.array([1.2, 4.1, 1.5, 4.5])  # @inspect x
    x[x > 4] = 0  # assignment is allowed @inspect x
    x = np.array([1.2, 4.1, 1.5, 4.5])  # start again @inspect x
    masked = x[x > 4]  # masked is a copy of those elements @inspect masked
    masked[:] = 0  # @inspect masked x
    text("`x[x > 4] = 0` writes into `x`; `masked = x[x > 4]` hands you a copy, so writing into it leaves `x` alone.")  # @clear x masked

    section("Fancy indexing: select by index")
    text("Give the **indices** of the elements you want, as a list - one list per axis.")
    text("- With a **single list**, only the first axis is indexed and the others are taken whole, by the same rule as `x[1]`: `x[[1, 2]]` is `x[[1, 2], :]`, the whole rows 1 and 2.", style=SUBLIST)
    figure("images/02_numpy/fancy_rows.svg", width="348px")  # @stepover
    text("- With **two lists**, they are read **in pairs**: the first index of one list goes with the first index of the other, and so on. `x[[1, 2], [0, 2]]` picks the two cells (1, 0) and (2, 2), not a 2×2 block:", style=SUBLIST)
    figure("images/02_numpy/fancy_pairs.svg", width="432px")  # @stepover

    demo("Fancy indexing, running")
    x = np.array([7.0, 9.0, 6.0, 5.0])  # @inspect x
    picked = x[[1, 3]]  # @inspect picked
    x2 = np.array([[0.0, 1.0, 2.0], [3.0, 4.0, 5.0], [6.0, 7.0, 8.0]])  # @inspect x2
    rows = x2[[1, 2]]  # whole rows: the same as x2[[1, 2], :] @inspect rows
    coordinates = x2[[1, 2], [0, 2]]  # the pairs (1, 0) and (2, 2) @inspect coordinates
    text("Two lists mean one index per axis, read **in pairs**: the result is a 1-D array of the selected elements.")  # @clear x picked x2 rows coordinates

    demo("Fancy indexing gives a copy too")
    x = np.array([1.2, 4.1, 1.5, 4.5])  # @inspect x
    x[[1, 3]] = 0  # assignment is allowed @inspect x
    x = np.array([1.2, 4.1, 1.5, 4.5])  # start again @inspect x
    selection = x[[1, 3]]  # a copy @inspect selection
    selection[:] = 0  # @inspect selection x
    text("Same story as masking: writing **through** the index works, writing **into the result** does not reach `x`.")  # @clear x selection

    section("Combined indexing")
    text("You can mix all of them on the same array. The number of dimensions stays the **same as the input** with masking or fancy indexing + slicing, and is **reduced by one for each axis indexed with a single integer**, as we saw with `x[1]`. Four combinations, on the same 3×3 matrix:")
    x = np.array([[0.0, 1.0, 2.0], [3.0, 4.0, 5.0], [6.0, 7.0, 8.0]])  # @inspect x
    text("- **Masking + slicing**: the rows where the mask is `True`, and the columns from 1 on. Two axes kept:", style=SUBLIST)
    figure("images/02_numpy/combined_mask_slice.svg", width="240px")  # @stepover
    mask_slice = x[[True, False, True], 1:]  # @inspect mask_slice
    text("- **Fancy + slicing**: rows 0 and 2, and the first two columns. Two axes kept:", style=SUBLIST)
    figure("images/02_numpy/combined_fancy_slice.svg", width="240px")  # @stepover
    fancy_slice = x[[0, 2], :2]  # @inspect fancy_slice
    text("- **Simple + slicing**: row 0 only, columns from 1 on. The integer removes the row axis:", style=SUBLIST)
    figure("images/02_numpy/combined_simple_slice.svg", width="240px")  # @stepover
    simple_slice = x[0, 1:]  # @inspect simple_slice
    text("- **Simple + masking**: column 0 only, in the rows where the mask is `True`. The integer removes the column axis:", style=SUBLIST)
    figure("images/02_numpy/combined_simple_mask.svg", width="240px")  # @stepover
    simple_mask = x[[True, False, True], 0]  # @inspect simple_mask
    shapes = (mask_slice.shape, fancy_slice.shape, simple_slice.shape, simple_mask.shape)  # @inspect shapes
    text("The first two keep two axes, the last two are 1-D: each integer written as a plain index costs one dimension.")  # @clear x mask_slice fancy_slice simple_slice simple_mask shapes

    demo("Pairs, not blocks")
    text("A 3×3 matrix of letters: we want the block of rows 1, 2 and columns 0, 2, i.e. `'d'`, `'f'`, `'g'`, `'i'`.")
    figure("images/02_numpy/fancy_block_target.svg", width="276px")  # @stepover
    letters = np.array([["a", "b", "c"], ["d", "e", "f"], ["g", "h", "i"]])  # @inspect letters
    pairs = letters[[1, 2], [0, 2]]  # two lists, read in pairs: only (1, 0) and (2, 2) @inspect pairs
    block = letters[[1, 2], :][:, [0, 2]]  # fancy + slicing picks the rows, then slicing + fancy picks their columns @inspect block
    text("Two lists in the same brackets pick **pairs** of coordinates. To get a **block**, combine each list with a slice, in two steps: first the rows (`[[1, 2], :]`), then the columns of those rows (`[:, [0, 2]]`).")  # @clear letters pairs block

    section("Summary: five ways in")
    table_head(INDEXING)  # @stepover
    table_row(INDEXING, "**Simple")  # @stepover
    table_row(INDEXING, "**Slicing")  # @stepover
    table_row(INDEXING, "**Masking")  # @stepover
    table_row(INDEXING, "**Fancy")  # @stepover
    table_row(INDEXING, "**Combined")  # @stepover
    text("**Slicing provides views** on the array: reading and writing a view reads and writes the original data. **Masking and fancy indexing provide copies.**", style=CALLOUT)
    text("✍️ **Your turn - `2.3_numpy_array_manipulation.ipynb`, exercises 1 and 2.** Read a column and the elements above a threshold on two rows; then **write** into a column through a mask, and find out what happens when you try the same on two columns at once.", style=EXERCISE)


def working_with_arrays():
    text("# 6. Working with arrays")
    section("Concatenation along an existing axis")
    text("The result has the **same number of dimensions** as the inputs: the size along the axis of concatenation can vary, the others must be equal.")
    figure("images/02_numpy/concatenate.svg", width="696px")  # @stepover

    demo("concatenate, hstack, vstack")
    x = np.array([[1, 2, 3], [4, 5, 6]])  # @inspect x
    y = np.array([[11, 12, 13], [14, 15, 16]])  # @inspect y
    stacked = np.concatenate((x, y))  # default axis 0 @inspect stacked
    side_by_side = np.concatenate((x, y), axis=1)  # @inspect side_by_side
    horizontal = np.hstack((x, y))  # along the rows, the same as axis=1 @inspect horizontal
    vertical = np.vstack((x, y))  # along the columns, the same as axis=0 @inspect vertical
    text("`hstack` and `vstack` are `concatenate` with the axis written into the name.")  # @clear x y stacked side_by_side horizontal vertical

    demo("vstack can also create a new axis")
    x = np.array([1, 2, 3])  # 1-D @inspect x
    y = np.array([11, 12, 13])  # 1-D @inspect y
    rows = np.vstack((x, y))  # two 1-D vectors become a 2x3 matrix @inspect rows
    try:
        np.concatenate((x, y), axis=1)  # will cause an error: there is no axis 1
    except ValueError as error:
        message = describe(error)  # @inspect message
    text("`vstack` stacks equal-length 1-D vectors along a **new** axis, which `np.concatenate` cannot do: it only works with axes that already exist.")  # @clear x y rows message

    section("Splitting arrays")
    text("- `np.split(arr, N, axis=0)` outputs a **list** of arrays.", style=SUBLIST)
    text("- If `N` is an **integer**, it divides `arr` into N equal parts along the axis - if that is possible.", style=SUBLIST)
    text("- If `N` is a **list**, it gives the positions where the array is cut.", style=SUBLIST)
    figure("images/02_numpy/split.svg", width="648px")  # @stepover

    demo("split, hsplit, vsplit")
    x = np.array([7, 7, 9, 9, 8, 8])  # @inspect x
    parts = np.split(x, [2, 4])  # cut before element 2 and before element 4 @inspect parts
    equal = np.split(x, 3)  # the same three parts, asked for differently @inspect equal
    grid = np.array([[1, 2, 3, 11, 12, 13], [4, 5, 6, 14, 15, 16]])  # @inspect grid
    left_right = np.hsplit(grid, [3])  # cut along axis 1 @inspect left_right
    tall = np.vstack((np.array([[1, 2, 3], [4, 5, 6]]), np.array([[11, 12, 13], [14, 15, 16]])))  # @inspect tall
    top_bottom = np.vsplit(tall, 2)  # two equal parts along axis 0 @inspect top_bottom
    text("The output is a plain Python **list** of arrays, which is why the panel shows them side by side.")  # @clear x parts equal grid left_right tall top_bottom

    section("Reshaping arrays")
    figure("images/02_numpy/reshape.svg", width="792px")  # @stepover

    demo("reshape")
    x = np.arange(6)  # @inspect x
    y = x.reshape((2, 3))  # filled row by row @inspect y
    column = np.array([1, 2, 3]).reshape(-1, 1)  # a column vector @inspect column
    text("At most **one** dimension can be `-1` (unknown): NumPy works it out from the size of the source and from the other dimensions.")
    try:
        x.reshape((4, 2))  # will cause an error: 6 elements do not fill 8 places
    except ValueError as error:
        message = describe(error)  # @inspect message
    text("Here the reshape does not move the data: it only changes how the same buffer is read back. (On an array that is not contiguous, e.g. a slice with a step, NumPy may have to make a copy.)")  # @clear x y column message

    section("Saving and loading arrays")
    code_row(SAVE_LOAD)  # @stepover
    text("- `np.save(filename, array)` writes one array, `np.load(filename)` reads it back; without the `.npy` extension, it is added for you.", style=SUBLIST)
    text("- `np.savez` writes **several** arrays into one archive (`.npz`); with keyword arguments, the archive behaves like a dictionary of arrays.", style=SUBLIST)

    demo("Saving and loading, running")
    path = data_path("tempfile.npy")  # somewhere under var/data @inspect path
    x = np.arange(10)  # @inspect x
    np.save(path, x)
    loaded = np.load(path)  # @inspect loaded
    archive_path = data_path("archive.npz")  # @inspect archive_path
    np.savez(archive_path, x=x, y=np.arange(3))  # two arrays, each with a name
    archive = np.load(archive_path)
    names = archive.files  # the names inside the archive @inspect names
    first = archive["x"]  # read one of them back @inspect first
    text("`.npy` keeps the dtype and the shape, so what you load is exactly what you saved - unlike a CSV.")  # @clear path x loaded archive_path names first
    text("✍️ **Your turn - `2.3_numpy_array_manipulation.ipynb`, exercises 3 and 4.** Concatenate a (2, 2) and a (3, 2) array vertically, try the same horizontally, and reshape until the dimensions that are *not* being concatenated match; then **split** the result back into the two blocks it was made of.", style=EXERCISE)


def closing():
    text("# Wrapping up")
    text("1) An array is **one contiguous buffer with one dtype**: that is where both the memory saving and the speed come from.", style=SUBLIST)
    text("2) **Axes and shape** are the vocabulary: an aggregation consumes the axis you give it, simple indexing consumes the axis you index.", style=SUBLIST)
    text("3) **Broadcasting**: pad the shorter shape with leading ones, stretch the axes of size 1, and fail when two sizes above 1 differ.", style=SUBLIST)
    text("4) **Slicing gives views**, masking and fancy indexing give **copies**: it decides whether your assignment reaches the original array.", style=SUBLIST)
    text("5) **concatenate, split, reshape** rearrange arrays without ever touching the numbers themselves.", style=SUBLIST)

"""Machine Learning for Networking - pandas and Matplotlib.

It covers last year's pandas and Matplotlib lectures. The slides are now
**interactive**: they run the code, draw every Series and DataFrame on the
variable panel, and every figure on the page is drawn by the code next to it.

    uv run python tools/prepare_lecture.py 03_pandas_and_matplotlib
    npm run --prefix edtrace/frontend dev '--' --port 5173 --strictPort
    open http://localhost:5173/?trace=03_pandas_and_matplotlib

This lecture is based on "Pandas" and "Matplotlib" by Andrea Pasini, Flavio
Giobergia, Elena Baralis, and Gabriele Ciravegna.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from edtrace import text
from support.pandas_matplotlib_content import ALIGNMENT, AUTHORS, PANDAS_2_VS_3, COMBINING, DF_ACCESS, GROUPBY, IMPORT_MATPLOTLIB, IMPORT_PANDAS, INTERFACES, IO_FORMATS, IRIS_SAMPLE, LAB1_VS_PANDAS, LINE_STYLE, LOC_ILOC, MISSING, MYCSV, MYCSV_MISSING, PLOT_TYPES, READ_CSV, READ_CSV_MISSING
from support.pandas_matplotlib_lab import anatomy_figure, data_path, describe, read_file, show, write_file
from support.slides import CALLOUT, EXERCISE, SUBLIST, SUBLIST_SPACED, SUBSUBLIST, code_row, compact_panel, demo, figure, people_row, section, table_all, table_head, table_row, theme


def main() -> None:
    title()
    introduction_to_pandas()
    series()
    dataframes()
    computation()
    combining()
    grouping()
    input_output()
    missing_values()
    introduction_to_matplotlib()
    figures_and_axes()
    plot_types()
    closing()


def title():
    theme()  # vertical rhythm for the whole page: renders an invisible <style>
    # ---------- Title ----------  @hide
    text("# Machine Learning for Networking")
    text("## pandas and Matplotlib")
    people_row(AUTHORS, gap="22px", photo="170px", name_size="18px")  # @stepover

    section("Today")
    text("1. **pandas**: Series and DataFrames, computation, combining and grouping tables, reading and writing files, missing values")
    text("2. **Matplotlib**: figures and axes, and the five most common plots - line, scatter, bar, histogram, box plot")
    variable_panel = "Here!"  # any inspected variable opens the panel
    text("**How to read this lecture:** every code example *runs*, the values of the variables are shown in an overlay panel. While I step through the code watch the variable panel! Series and DataFrames are drawn there as tables, with the index in **bold**.", style=CALLOUT)  # @inspect variable_panel
    text("✍️ **Exercises, in class:** the notebooks in `exercises/03_pandas/` and `exercises/04_matplotlib/`. We stop and do them as we go - **3.1** after Series and DataFrames, **3.2** after reading files, **4.1** after figures and axes, **4.2** after the plot types. **3.3** is extra practice, for home.", style=EXERCISE)


def introduction_to_pandas():
    text("# 1. Introduction to pandas")
    text("pandas is not part of Python either: install it inside your virtual environment with `pip install pandas` (on Google Colab it is already installed).")

    section("What pandas gives you")
    text("- Two data structures, **built on NumPy arrays**:", style=SUBLIST)
    text("- **Series**: a column.", style=SUBSUBLIST)
    text("- **DataFrame**: a table.", style=SUBSUBLIST)
    text("- The data analysis tools that go with them: managing **tables and series**, **statistics** on data, **missing data**, reading and writing **files**.", style=SUBLIST)
    code_row(IMPORT_PANDAS)  # @stepover
    text("`pd` is the convention, like `np` for NumPy.", style=SUBLIST)
    version = pd.__version__  # the pandas that is running this lecture @inspect version

    section("Why pandas")  # @clear version
    text("- In Lab 1 you computed the mean of each measurement **per species**, with loops and dictionaries.", style=SUBLIST) 
    text("- Here are nine flowers of the same Iris dataset, in a CSV file with a header:", style=SUBLIST)
    compact_panel("14px")  # wide tables: a smaller panel until the end of this section @stepover
    path = write_file("iris_sample.csv", IRIS_SAMPLE)  # @inspect path
    iris = pd.read_csv(path)  # one call: header, columns, types @inspect iris
    means = iris.groupby("species").mean()  # every column, every species @inspect means
    code_row(LAB1_VS_PANDAS, space_before="56px")  # @stepover @clear path iris means
    text("Two lines, and the **names** travel with the numbers: rows are labelled by species, columns by measurement. We will see each piece of this during the lecture.", style=CALLOUT)


def series():
    text("# 2. Series")
    section("A column with an index")
    text("- A **Series** is a one-dimensional sequence of **homogeneous** elements (the *values*), like a 1-D NumPy array.", style=SUBLIST)
    text("- Each element is associated with a label of an explicit **index**: integers, or strings such as dates or names.", style=SUBLIST)
    text("- The index is the whole set of names; each name in it is a **label**. We say \"by label\" (`.loc`) vs \"by position\" (`.iloc`), because \"by index\" could mean either.", style=SUBSUBLIST)
    figure("images/03_pandas_and_matplotlib/series_anatomy.svg", width="278px")  # drawn at 1.2x its natural size @stepover

    demo("Creating a Series")
    text("A Series can be created in several ways:")
    text("- **From a list**.", style=SUBLIST_SPACED)
    s1 = pd.Series([2.0, 3.1, 4.5])  # the index is 0, 1, 2 @inspect s1
    text("- **From a list, specifying the index** (the labels) explicitly, with `index=`: here a string label for each element.", style=SUBLIST_SPACED)
    text("- Without `index=`, as above, the labels are progressive numbers, `0, 1, 2, ...`, like the positions of a list.", style=SUBSUBLIST)
    s2 = pd.Series([2.0, 3.1, 4.5], index=["mon", "tue", "wed"])  # strings as index @inspect s2
    text("- **From a dictionary**: the **keys** define the index, and the values are the values of the Series, in the same order.", style=SUBLIST_SPACED)
    s3 = pd.Series({"c": 2.0, "b": 3.1, "a": 4.5})  # the keys become the index @inspect s3

    demo("Values and index")  # @clear s1 s3
    values = s2.values  # a NumPy array @inspect values
    index = s2.index  # an Index object, shown here as its labels @inspect index
    kinds = (type(values).__name__, type(index).__name__)  # @inspect kinds
    text("A Series is a NumPy array with a **label** for every element. The `Index` is an object defined by pandas; it keeps the labels, and makes lookups by label fast.")

    demo("Accessing elements: loc and iloc")  # @clear s2 values index kinds
    s1 = pd.Series([2.0, 3.1, 4.5], index=["a", "b", "c"])  # @inspect s1
    text("Two ways to point at the same element, by its name or by its position, always with square brackets:")
    text("- **By label**, the name in the index you specified (the *explicit* index): `s.loc[label]`.", style=SUBLIST_SPACED)
    first_by_label = s1.loc["a"]  # by label @inspect first_by_label
    text("- **By position**, as for lists and NumPy arrays (the *implicit* index): `s.iloc[position]`.", style=SUBLIST_SPACED)
    first_by_position = s1.iloc[0]  # by position: the same element @inspect first_by_position
    text("- Both allow **editing** values, and the edit changes the original Series:", style=SUBLIST_SPACED)
    s1.loc["b"] = 10  # by label @inspect s1
    s1.iloc[2] = 20  # by position @inspect s1

    demo("Slicing")  # @clear first_by_label first_by_position
    text("As for lists, strings and NumPy arrays, you can take a **slice** of a Series, but here in two different ways: by label with `.loc`, by position with `.iloc`.")
    s1 = pd.Series([10, 20, 30, 40])  # the default index: 0, 1, 2, 3 @inspect s1
    by_label = s1.loc[1:3]  # labels 1 to 3: stop element INCLUDED @inspect by_label
    by_position = s1.iloc[1:3]  # positions 1 to 3: stop element excluded @inspect by_position
    text("⚠️ Same slice `[1:3]`, different results: a slice of **labels** includes its stop, a slice of **positions** excludes it (as everywhere in Python).", style=CALLOUT)
    text("- **Second trap**: with an integer index, a number can be a label or a position. Here labels and positions do not match:", style=SUBLIST_SPACED)  # @clear s1 by_label by_position
    numbers = pd.Series([10, 20, 30, 40], index=[3, 2, 1, 0])  # an integer index, not in order @inspect numbers
    by_label = numbers.loc[0]  # the element LABELLED 0: the last one @inspect by_label
    by_position = numbers.iloc[0]  # the element in POSITION 0: the first one @inspect by_position
    text("- **Third trap**: a slice of labels follows the **order of the index**, not the alphabet. The same slice on two Series with the same labels, in a different order:", style=SUBLIST_SPACED)  # @clear numbers by_label by_position
    ordered = pd.Series([10, 20, 30, 40], index=["a", "b", "c", "d"])  # @inspect ordered
    shuffled = pd.Series([10, 20, 30, 40], index=["b", "a", "d", "c"])  # @inspect shuffled
    from_ordered = ordered.loc["b":"c"]  # from b to c: two elements @inspect from_ordered
    from_shuffled = shuffled.loc["b":"c"]  # from b (first) to c (last): all four @inspect from_shuffled
    text("`'b':'c'` means *from where `b` is to where `c` is*: in `shuffled` that is the whole Series, `a` and `d` included.")
    text("Always say which one you mean: `.loc` or `.iloc`, never a bare `s[...]`, whose meaning depends on what you put inside (more in a moment).", style=CALLOUT)

    demo("Masking and fancy indexing")  # @clear ordered shuffled from_ordered from_shuffled
    s1 = pd.Series([2.0, 3.1, 4.5], index=["a", "b", "c"])  # @inspect s1
    text("The same tools as NumPy, through `.loc` and `.iloc`, and the result keeps the **labels** of what it selected:")
    text("- **Masking**: a comparison builds a boolean Series with the same index, and `&`, `|`, `~` combine masks, as in NumPy.", style=SUBLIST_SPACED)
    mask = (s1 > 2) & (s1 < 10)  # @inspect mask
    masked = s1.loc[mask]  # @inspect masked
    text("- `.iloc` refuses this mask, because its index is made of text labels, which cannot be read as positions: masks go with `.loc`, or pass `.iloc` a plain boolean array, `s1.iloc[mask.to_numpy()]`.", style=SUBSUBLIST)
    try:
        s1.iloc[mask]  # a boolean Series, read by position
    except ValueError as error:
        message = describe(error)  # @inspect message
    text("- Since pandas 3.0, `.iloc` does take a boolean Series whose index is made of **integers** (e.g. the default `0, 1, 2, ...`), matched by label. pandas 2.x refuses any boolean Series (`NotImplementedError`): `.to_numpy()` works in both.", style=SUBSUBLIST)  # @clear message
    numbers = pd.Series([2.0, 3.1, 4.5])  # the default index: 0, 1, 2 @inspect numbers
    big_numbers = numbers.iloc[numbers > 2]  # pandas 3 only @inspect big_numbers
    text("- **Fancy indexing**: a list of labels with `.loc`, a list of positions with `.iloc`.", style=SUBLIST_SPACED)  # @clear numbers big_numbers
    picked = s1.loc[["a", "c"]]  # a list of labels @inspect picked
    picked_too = s1.iloc[[0, 2]]  # a list of positions @inspect picked_too
    text("Plain brackets, `s1[s1 > 2]`, work too, but their meaning depends on what you put inside: on a Series, a single number is a **label** while a slice of numbers is a **position**; on a DataFrame, a name selects a **column** while a mask or a slice selects **rows**. `.loc` and `.iloc` always mean one thing: use them.")

    section("Summary: loc vs iloc")  # @clear s1 mask masked picked picked_too
    table_head(LOC_ILOC)  # @stepover
    table_row(LOC_ILOC, "**Selects")  # @stepover
    table_row(LOC_ILOC, "**Single")  # @stepover
    table_row(LOC_ILOC, "**Slice")  # @stepover
    table_row(LOC_ILOC, "**Mask")  # @stepover
    table_row(LOC_ILOC, "**Fancy")  # @stepover
    text("✍️ **Your turn - `3.1_pandas_series_and_dataframes.ipynb`, exercise 1.** Build a Series of fruits, then read the first three elements, the values of two fruits by name, and the names of the fruits above a threshold.", style=EXERCISE)


def dataframes():
    text("# 3. DataFrames")
    section("A table of Series")
    text("A **DataFrame** is a two-dimensional table where:")
    text("- the **columns** are Series objects (each with its own type),", style=SUBLIST)
    text("- and all the columns share the **same index**.", style=SUBLIST)
    figure("images/03_pandas_and_matplotlib/dataframe_of_series.svg", width="958px")  # drawn at 1.2x its natural size @stepover

    demo("Creating a DataFrame")
    text("A DataFrame can be created in several ways:")
    text("- **From a dictionary of Series**: the keys name the columns, and the index the Series share becomes the index of the table.", style=SUBLIST_SPACED)
    price = pd.Series([1.0, 1.4, 5.0], index=["Water", "Beer", "Wine"])  # @inspect price
    quantity = pd.Series([5, 10, 8], index=["Water", "Beer", "Wine"])  # @inspect quantity
    liters = pd.Series([1.5, 0.3, 1.0], index=["Water", "Beer", "Wine"])  # @inspect liters
    df = pd.DataFrame({"Price": price, "Quantity": quantity, "Liters": liters})  # @inspect df
    dtypes = df.dtypes  # each column keeps its own type: Quantity holds integers @inspect dtypes
    text("- **From a dictionary of lists**: one list per column, all of the same length.", style=SUBLIST_SPACED)  # @clear price quantity liters df dtypes
    from_dict = pd.DataFrame({"c1": [0, 1, 2], "c2": [0, 2, 4]})  # @inspect from_dict
    text("- Without `index=`, the index is again `0, 1, 2, ...`, as for a Series.", style=SUBSUBLIST)
    text("- **From a list of dictionaries**: one dictionary per **row**; a key missing from a row becomes `NaN`.", style=SUBLIST_SPACED)
    from_records = pd.DataFrame([{"c1": i, "c2": 2 * i} for i in range(3)])  # @inspect from_records
    text("- **From a 2D NumPy array**: `columns=` names the columns, `index=` labels the rows.", style=SUBLIST_SPACED)
    arr = np.arange(6).reshape((3, 2))  # @inspect arr
    from_array = pd.DataFrame(arr, columns=["c1", "c2"], index=["a", "b", "c"])  # @inspect from_array

    demo("Columns, index, values")  # @clear from_dict from_records arr from_array
    df = pd.DataFrame({"Price": [1.0, 1.4, 5.0], "Quantity": [5, 10, 8], "Liters": [1.5, 0.3, 1.0]}, index=["a", "b", "c"])  # @inspect df
    text("Three attributes give back the pieces of the table:")
    text("- `df.columns`: the column names, as an `Index`.", style=SUBLIST_SPACED)
    columns = df.columns  # @inspect columns
    text("- `df.index`: the row labels, as an `Index`.", style=SUBLIST_SPACED)
    index = df.index  # @inspect index
    text("- `df.to_numpy()` (or `df.values`): the data, as a 2D NumPy array.", style=SUBLIST_SPACED)
    values = df.to_numpy()  # @inspect values
    text("One array means **one** dtype, one that can hold every column. Here all the columns are numbers, so the integers of `Quantity` became floats (upcasting, as in lecture 2). With a column of strings the dtype would be `object`: nothing is converted, and every value stays a separate Python object, as in a list.")

    demo("Accessing columns and rows")  # @clear columns index values
    text("On a DataFrame, plain brackets and `.loc`/`.iloc` do different jobs:")
    text("- **A column**: plain brackets with its name. The result is a Series, indexed like the DataFrame.", style=SUBLIST_SPACED)
    quantities = df["Quantity"]  # @inspect quantities
    text("- **Some columns**: a list of names. The result is a DataFrame.", style=SUBLIST_SPACED)
    two_columns = df[["Price", "Liters"]]  # @inspect two_columns
    text("- **A row**: `.loc` with its label, `.iloc` with its position. The result is a Series too, whose index is made of the **column names**.", style=SUBLIST_SPACED)  # @clear quantities two_columns
    row_a = df.loc["a"]  # @inspect row_a
    row_0 = df.iloc[0]  # the same row, by position @inspect row_0
    text("- The values of a row share one dtype: in this all-number table, `Quantity` is now `5.0`.", style=SUBSUBLIST)
    text("- `.loc` looks for **row** labels: the name of a column is not one of them.", style=SUBLIST_SPACED)
    try:
        df.loc["Quantity"]  # a column name, used as a row label
    except KeyError as error:
        message = describe(error)  # @inspect message
    text("So: a name (or a list of names) in plain brackets selects **columns**, `.loc`/`.iloc` select **rows**.")

    demo("Slicing, masking, fancy indexing")  # @clear row_a row_0 message
    text("As in NumPy, `.loc` and `.iloc` take one selector per axis, **rows first, then columns**, and each selector can be a label, a slice, a mask or a list:")
    text("- **Two slices** of labels: both stops included, as for a Series.", style=SUBLIST_SPACED)
    block = df.loc["b":"c", "Quantity":"Liters"]  # @inspect block
    text("- **Two lists**: here they select a **block**, every row with every column, not pairs of coordinates as in NumPy.", style=SUBLIST_SPACED)  # @clear block
    corners = df.loc[["a", "c"], ["Price", "Liters"]]  # rows a and c, columns Price and Liters @inspect corners
    text("- **A mask to choose the rows**: a condition on the columns is `True` or `False` for each row, and keeps the rows where it is `True`. Here: `Quantity` below 10 **and** `Liters` above 1.", style=SUBLIST_SPACED)  # @clear corners
    mask = (df["Quantity"] < 10) & (df["Liters"] > 1)  # one True/False per row @inspect mask
    text("- Then choose the columns as usual, with a slice or a list:", style=SUBSUBLIST)
    selected = df.loc[mask, "Quantity":]  # masking + slicing @inspect selected
    two_columns = df.loc[mask, ["Price", "Liters"]]  # masking + fancy @inspect two_columns
    figure("images/03_pandas_and_matplotlib/dataframe_masking.svg", width="1061px")  # @stepover
    text("- A mask in **plain brackets** selects rows too: `df[mask]` is a common shorthand for `df.loc[mask]`, and you will see it everywhere.", style=SUBSUBLIST)  # @clear selected two_columns
    same_rows = df[mask]  # the same rows as df.loc[mask] @inspect same_rows

    section("Summary: accessing a DataFrame")  # @clear mask same_rows
    table_head(DF_ACCESS)  # @stepover
    table_row(DF_ACCESS, "`df['Quantity']`")  # @stepover
    table_row(DF_ACCESS, "`df[['Price'")  # @stepover
    table_row(DF_ACCESS, "`df[mask]`")  # @stepover
    table_row(DF_ACCESS, "`df.loc['a']`")  # @stepover
    table_row(DF_ACCESS, "`df.loc[rows")  # @stepover
    table_row(DF_ACCESS, "`df.iloc[rows")  # @stepover

    demo("Adding, renaming and dropping columns")
    df = pd.DataFrame({"Price": [1.0, 1.4, 5.0], "Quantity": [5, 10, 8], "Liters": [1.5, 0.3, 1.0]}, index=["a", "b", "c"])  # start again @inspect df
    text("- **Adding** a column: assign to a new name. It modifies `df` **in place**, and the values can be a Series (aligned on the index), a list (of the right length), or computed from other columns.", style=SUBLIST_SPACED)
    df["Available"] = pd.Series([True, False, True], index=["a", "b", "c"])  # @inspect df
    df["Total"] = df["Price"] * df["Quantity"]  # @inspect df
    text("- Assigning to an existing name **replaces** that column:", style=SUBSUBLIST)
    df["Available"] = [False, False, True]  # @inspect df
    text("- **Renaming**: a dictionary maps the old names to the new ones.", style=SUBLIST_SPACED)
    renamed = df.rename(columns={"Quantity": "nItems", "Liters": "[L]"})  # @inspect renamed
    text("- **Dropping**: a list of names.", style=SUBLIST_SPACED)
    dropped = df.drop(columns=["Quantity", "Liters"])  # @inspect dropped
    text("Unlike adding, `rename` and `drop` **return a new DataFrame** and leave `df` as it was: assign the result (`df = df.drop(...)`). Many pandas methods work this way - check the documentation.")

    demo("Assigning: copies and views")  # @clear df renamed dropped
    df = pd.DataFrame({"Price": [1.0, 1.4, 5.0], "Quantity": [5, 10, 8], "Liters": [1.5, 0.3, 1.0]}, index=["a", "b", "c"])  # start again @inspect df
    text("⚠️ This section describes **pandas 3.0**, where this behaviour changed: check your version with `pd.__version__`. On pandas 2.x (e.g. on Colab), turn on the same behaviour with `pd.options.mode.copy_on_write = True`.", style=CALLOUT)
    text("In NumPy it depends on how you select: a slice is a **view** of the array, a mask or a list gives a **copy** (lecture 2). Since pandas 3.0 the rule is the same for every selection, and there are two ways to write:")
    text("- **Select and assign in one statement**, `df.loc[...] = ...`: this always writes into `df`.", style=SUBLIST_SPACED)
    df.loc[["a", "c"], ["Price", "Liters"]] = 0  # @inspect df
    text("- **Take a piece out, then write into it**: whatever you selected - one column, a list of columns, a slice of rows, a mask - the piece **behaves as a copy**. It changes, `df` does not:", style=SUBLIST_SPACED)
    prices = df["Price"]  # one column @inspect prices
    prices.loc["b"] = 99  # @inspect prices df
    two_columns = df[["Price", "Liters"]]  # a list of columns: the same @inspect two_columns @clear prices
    two_columns.loc["b", "Liters"] = 99  # @inspect two_columns df
    first_rows = df.loc["a":"b"]  # a slice of rows: the same, unlike NumPy @inspect first_rows @clear two_columns
    first_rows.loc["a", "Quantity"] = 0  # @inspect first_rows df
    text("- Under the hood this is **copy-on-write**: selecting a column, a list of columns or a slice of rows does not copy the data (the piece still shares memory with `df`, so selecting is cheap), but the first write into either of them gives that one its own copy; a mask copies at once. Either way, the write never reaches the other.", style=SUBSUBLIST)
    text("**Rule:** a piece you take out of a DataFrame is a separate object; to change `df`, write through `df.loc[...] = ...` in a single statement. Before pandas 3.0 the answer depended on the selection (a single column was often a view, a list of columns a copy), and pandas warned with a `SettingWithCopyWarning`: you will still see it in older code and tutorials.", style=CALLOUT)
    text("✍️ **Your turn - `3.1_pandas_series_and_dataframes.ipynb`, exercise 2.** Build a DataFrame from a NumPy-style table, add a computed column `area`, select the rows with an odd index, and the height and weight of the samples with area above 20.", style=EXERCISE)  # @clear df first_rows
    text("**pandas 2.x vs pandas 3.0**: the main differences, for reference, for when you meet older code, tutorials or installations:", style={"display": "block", "marginTop": "40px"})
    table_all(PANDAS_2_VS_3)  # the whole table in one step: a reference, not discussed row by row @stepover


def computation():
    text("# 4. Computation with pandas")
    section("Three kinds of operations")
    text("- **Unary operations**, applied to each element; the result is still a Series or a DataFrame:", style=SUBLIST)
    text("- arithmetic with a number, e.g. `s / 4 + 1`;", style=SUBSUBLIST)
    text("- any NumPy ufunc, e.g. `np.exp`, `np.abs`, ...", style=SUBSUBLIST)
    text("- **Operations between** Series and DataFrames (`+`, `-`, `*`, `/`): element by element, **after aligning** the indices and the columns.", style=SUBLIST)
    text("- **Aggregations** (`mean`, `std`, `min`, `max`, `sum`, ...).", style=SUBLIST)

    demo("Unary operations")
    s = pd.Series([-1.0, 2.0, -3.0], index=["a", "b", "c"])  # @inspect s
    shifted = s / 4 + 1  # @inspect shifted
    absolute = np.abs(s)  # a NumPy ufunc on a Series @inspect absolute
    text("The index is carried along: the result is labelled like the input.")

    demo("Operations between Series: alignment")  # @clear s shifted absolute
    s1 = pd.Series([3, 1, 10], index=["b", "a", "c"])  # @inspect s1
    s2 = pd.Series([1, 3, 30], index=["a", "b", "d"])  # @inspect s2
    total = s1 + s2  # @inspect total
    figure("images/03_pandas_and_matplotlib/series_alignment.svg", width="667px")  # @stepover
    text("- pandas pairs the elements by **label**, not by position: `a` with `a`, `b` with `b`, whatever their order.", style=SUBLIST_SPACED)
    text("- A label found in only one of the two (`c`, `d`) gets `NaN` (*Not a Number*); since the two indices differ, the result index is their **union**, sorted.", style=SUBLIST)
    text("- `NaN` is a float: that is why `total` holds floats, although both inputs are integers.", style=SUBLIST)

    demo("Operations between DataFrames")  # @clear s1 s2 total
    text("The same alignment, on **both axes**:")
    text("- **On the index**: same columns, different row labels.", style=SUBLIST_SPACED)
    df1 = pd.DataFrame({"Total": [3, 1, 10], "Quantity": [4, 2, 20]}, index=["b", "a", "c"])  # @inspect df1
    df2 = pd.DataFrame({"Total": [1, 3, 30], "Quantity": [2, 4, 40]}, index=["a", "b", "d"])  # @inspect df2
    by_index = df1 + df2  # @inspect by_index
    text("- **On the columns**: `df3` has a column (`Price`) that `df1` lacks, and lacks one (`Quantity`) that `df1` has.", style=SUBLIST_SPACED)  # @clear df2 by_index
    df3 = pd.DataFrame({"Total": [1, 3, 5], "Price": [4, 2, 1]}, index=["a", "b", "c"])  # @inspect df3
    by_columns = df1 + df3  # @inspect by_columns
    figure("images/03_pandas_and_matplotlib/dataframe_alignment.svg", width="912px")  # @stepover
    text("A cell gets a value only where its row label **and** its column label exist on both sides. Where the two sides have different labels, the result takes their union, sorted: the rows `a, b, c, d` of `by_index`, the columns `Price, Quantity, Total` of `by_columns`. Identical labels keep their order: the columns of `by_index` are still `Total, Quantity`.")

    demo("DataFrame and Series: broadcasting")  # @clear df1 df3 by_columns
    df1 = pd.DataFrame({"Total": [1, 3, 5], "Quantity": [2, 4, 6]}, index=["a", "b", "c"])  # @inspect df1
    s1 = pd.Series({"Total": 1, "Quantity": 2})  # its index matches the COLUMNS of df1 @inspect s1
    res = df1 + s1  # added to every row @inspect res
    figure("images/03_pandas_and_matplotlib/dataframe_broadcasting.svg", width="816px")  # @stepover
    text("The Series is added to **each row**, as a NumPy 1-D vector would be (broadcasting), matching the **index** of the Series with the **columns** of the DataFrame.")

    section("Summary: alignment")  # @clear df1 s1 res
    table_all(ALIGNMENT)  # @stepover

    demo("Aggregations")
    df = pd.DataFrame({"Total": [1, 3, 5], "Quantity": [2, 4, 6]}, index=["a", "b", "c"])  # @inspect df
    text("- On a **Series**, e.g. a column, they return a single value.", style=SUBLIST_SPACED)
    total_mean = df["Total"].mean()  # @inspect total_mean
    text("- On a **DataFrame** they work column by column (over the rows, like `axis=0` in NumPy), and return a Series with one value per column.", style=SUBLIST_SPACED)
    mean_series = df.mean()  # @inspect mean_series
    std_series = df.std()  # @inspect std_series
    text("- Example, **z-score normalization**: subtract from each column its mean, and divide by its standard deviation. Broadcasting matches the column names for us.", style=SUBLIST_SPACED)  # @clear total_mean
    df_norm = (df - mean_series) / std_series  # @inspect df_norm
    text("Every column now has mean 0 and standard deviation 1: a very common **preprocessing** step before training a model, written without a loop and without ever naming a column.")
    text("⚠️ `df.std()` divides by `n - 1` (the sample standard deviation), while NumPy's `x.std()` divides by `n`: on small tables the two differ. `df.std(ddof=0)` gives NumPy's result.", style=CALLOUT)


def combining():
    text("# 5. Combining Series and DataFrames")
    text("Two functions put Series and DataFrames together: `pd.concat` **stacks** them, `pd.merge` **joins** them on common values.")

    demo("Concatenating Series")
    s1 = pd.Series(["a", "b"], index=[1, 2])  # @inspect s1
    s2 = pd.Series(["c", "d"], index=[1, 2])  # @inspect s2
    stacked = pd.concat((s1, s2))  # one after the other @inspect stacked
    text("- The index is kept as it is, **duplicates included**: nothing in pandas prevents duplicate labels, so label `1` now points at two elements.", style=SUBLIST_SPACED)
    ones = stacked.loc[1]  # a repeated label: a Series with every match @inspect ones
    text("- So `.loc[label]` returns a **single value** (a scalar) if the label is unique, and a **Series** with all the matches if the label is repeated:", style=SUBSUBLIST)
    single = s1.loc[1]  # a unique label: a scalar @inspect single
    text("- `ignore_index=True` throws the old index away and numbers the elements again.", style=SUBLIST_SPACED)  # @clear ones single
    renumbered = pd.concat((s1, s2), ignore_index=True)  # @inspect renumbered

    demo("Concatenating DataFrames")  # @clear s1 s2 stacked renumbered
    df1 = pd.DataFrame({"Total": [1, 3], "Quantity": [2, 4]}, index=["a", "b"])  # @inspect df1
    df2 = pd.DataFrame({"Total": [5, 7], "Quantity": [6, 8], "Liters": [1.0, 2.0]}, index=["c", "d"])  # one more column @inspect df2
    vertical = pd.concat((df1, df2))  # vertically, by default @inspect vertical
    text("The columns are aligned **by name**, and the column missing in `df1` is filled with `NaN`.")

    demo("Merge: joining on common values")  # @clear df1 df2 vertical
    text("`pd.merge(df1, df2)` combines two DataFrames the way a database **join** does: it pairs the rows that have **equal values** in some columns, whatever their position.")
    df1 = pd.DataFrame({"k1": [0, 1], "c2": ["a", "b"]}, index=["i1", "i2"])  # @inspect df1
    df2 = pd.DataFrame({"k1": [1, 0], "c3": ["b1", "a1"]}, index=["i1", "i2"])  # @inspect df2
    text("- **On the columns with the same name**, by default (here `k1`; `on='k1'` says it explicitly).", style=SUBLIST_SPACED)
    on_columns = pd.merge(df1, df2)  # @inspect on_columns
    text("- The rows are paired by `k1`, not by position, and the result gets a new index `0, 1, ...`.", style=SUBSUBLIST)
    text("- **On the indices**, with `left_index=True, right_index=True`.", style=SUBLIST_SPACED)
    on_index = pd.merge(df1, df2, left_index=True, right_index=True)  # @inspect on_index
    text("- `k1` is now an ordinary column on both sides, so it is kept twice, as `k1_x` and `k1_y`.", style=SUBSUBLIST)
    text("- **Many-to-one**: each value of `k1` appears twice on the left and once on the right, so each right row is repeated.", style=SUBLIST_SPACED)  # @clear on_columns on_index
    df1 = pd.DataFrame({"k1": [0, 1, 0, 1], "c2": ["a", "b", "c", "d"]}, index=["i1", "i2", "i3", "i4"])  # four rows now @inspect df1
    many_to_one = pd.merge(df1, df2)  # @inspect many_to_one
    figure("images/03_pandas_and_matplotlib/many_to_one_merge.svg", width="806px")  # @stepover
    text("- `validate=` checks the kind of merge you expect (`'1:1'`, `'1:m'`, `'m:1'`, `'m:m'`), and raises an error if the data do not match it:", style=SUBLIST_SPACED)
    try:
        pd.merge(df1, df2, validate="1:1")  # but k1 repeats on the left
    except pd.errors.MergeError as error:
        message = describe(error)  # @inspect message

    section("Summary: combining")  # @clear df1 df2 many_to_one message
    table_all(COMBINING)  # @stepover


def grouping():
    text("# 6. Grouping data")
    text("pandas provides the equivalent of the SQL **group by** statement, `df.groupby(...)`:")
    text("- **split** the rows into groups by the value of a key column;", style=SUBLIST_SPACED)
    text("- then **iterate** over the groups,", style=SUBLIST)
    text("- **aggregate** each of them (one row per group),", style=SUBLIST)
    text("- or **filter** them (keep or drop whole groups).", style=SUBLIST)
    figure("images/03_pandas_and_matplotlib/groupby_overview.svg", width="984px")  # @stepover

    demo("Applying group by")
    df = pd.DataFrame({"k": ["a", "b", "a", "b"], "c1": [2, 10, 3, 15], "c2": [4, 20, 5, 30]})  # @inspect df
    grouped_df = df.groupby("k")  # two groups: 'a' and 'b' @inspect grouped_df
    text("The result is a `DataFrameGroupBy` object, not a table: nothing is computed until you ask for it. The panel shows the groups it will produce, each with its rows.")

    demo("Iterating over the groups")
    keys = []
    for key, group_df in grouped_df:  # each group is a subset of the original DataFrame @inspect key group_df
        keys.append(key)  # @inspect keys
    text("Each iteration hands out a key and its group, a DataFrame that keeps the original index of its rows (0 and 2 for `a`).")

    demo("Aggregating by group")  # @clear key group_df keys
    text("Whatever you aggregate, the result has **one row per group**, and the key becomes its **index**: on the panel, the key's name `k` sits on a row of its own, above the labels `a` and `b`.")
    text("- **One column**: select it, then aggregate. The result is a Series.", style=SUBLIST_SPACED)
    c1_means = grouped_df["c1"].mean()  # @inspect c1_means
    text("- **Every column**, one aggregation. The result is a DataFrame:", style=SUBLIST_SPACED)  # @clear c1_means
    means = grouped_df.mean()  # @inspect means
    text("This is exactly what we did on the Iris dataset at the beginning of the lecture (section 1): `iris.groupby(\"species\").mean()`, the mean of every measurement per species.", style=CALLOUT)
    text("- `reset_index()` turns the key back into an ordinary column, and the index into `0, 1, ...`:", style=SUBSUBLIST)
    means_flat = means.reset_index()  # @inspect means_flat
    text("- **Every column, several aggregations** with `agg`: one column for every (column, aggregation) pair, 2 × 2 = 4 here, so the column names have **two levels**:", style=SUBLIST_SPACED)  # @clear means means_flat
    extremes = grouped_df.agg(["max", "min"])  # @inspect extremes
    text("- Best practice: **name** each result yourself (*named aggregation*, `new_name=(column, aggregation)`), then `reset_index()`. The same four results, in a flat table with one level of names:", style=SUBSUBLIST)
    named = grouped_df.agg(c1_max=("c1", "max"), c1_min=("c1", "min"), c2_max=("c2", "max"), c2_min=("c2", "min")).reset_index()  # @inspect named

    demo("Filtering groups")  # @clear extremes named
    text("`filter` keeps or drops **whole groups**, with a function that receives each group as a DataFrame and returns `True` or `False`:")
    kept = grouped_df.filter(lambda x: x["c1"].mean() > 5)  # keep the groups whose c1 has a mean above 5 @inspect kept
    text("Group `a` has mean 2.5 and is dropped, group `b` (12.5) is kept. The result is made of the original **rows**, not of one row per group.")

    section("Summary: group by")  # @clear kept
    table_all(GROUPBY)  # @stepover


def input_output():
    text("# 7. DataFrames and I/O")
    demo("Reading a CSV file")
    text("`pd.read_csv(path, sep=',')`:")
    text("- reads the **column names** from the first line of the file, after skipping the first `skiprows` lines;", style=SUBLIST)
    text("- **infers** the type of each column.", style=SUBLIST)
    text("A file with a title line on top:")
    code_row(READ_CSV)  # @stepover
    path = write_file("mycsv.csv", MYCSV)  # @inspect path
    df = pd.read_csv(path, sep=",", skiprows=1)  # skip the title line @inspect df
    dtypes = df.dtypes  # @inspect dtypes

    demo("Missing values in a CSV")  # @clear path df dtypes
    text("A file with some missing values, marked in different ways:")
    code_row(READ_CSV_MISSING)  # @stepover
    path = write_file("mycsv_missing.csv", MYCSV_MISSING)  # @inspect path
    text("- Empty fields and the text `NaN` become `NaN` on their own, but any other marker is read as text: `c2` becomes a column of **strings**.", style=SUBLIST_SPACED)
    raw = pd.read_csv(path, sep=",")  # @inspect raw
    raw_dtypes = raw.dtypes  # @inspect raw_dtypes
    text("- pandas 3 stores text in its own `str` dtype; older versions show `object`.", style=SUBSUBLIST)
    text("- List the other markers with `na_values`, and `c2` is a column of numbers.", style=SUBLIST_SPACED)  # @clear raw raw_dtypes
    df = pd.read_csv(path, sep=",", na_values=["no info", "x"])  # @inspect df
    dtypes = df.dtypes  # @inspect dtypes

    demo("Writing a CSV file")  # @clear path dtypes
    saved = data_path("savedcsv.csv")
    text("- `df.to_csv(path)` writes the index too, as a nameless first column. Missing values become empty fields.", style=SUBLIST_SPACED)
    df.to_csv(saved, sep=",")
    with_index = read_file(saved)  # @inspect with_index
    text("- `index=False` leaves it out: what you want when the index is just `0, 1, 2, ...`.", style=SUBLIST_SPACED)
    df.to_csv(saved, sep=",", index=False)
    without_index = read_file(saved)  # @inspect without_index

    demo("JSON")  # @clear with_index without_index
    json_path = data_path("myjson.json")
    text("- `df.to_json(path)` writes one object per column, with an `index: value` pair for each row.", style=SUBLIST_SPACED)
    df.to_json(json_path)
    as_json = read_file(json_path)  # @inspect as_json
    text("- `pd.read_json(path)` reads it back into the same table.", style=SUBLIST_SPACED)
    back = pd.read_json(json_path)  # @inspect back

    section("Many other formats")  # @clear df as_json back
    table_all(IO_FORMATS)  # @stepover
    text("✍️ **Your turn - `3.2_pandas_grouping.ipynb`.** Read the whole Iris dataset **straight from its URL** with `pd.read_csv` (it has no header: name the columns yourself), compute the mean and the standard deviation of each feature per class with `groupby`, and (⭐) predict the class of each flower from the closest class mean - without iterating over the rows.", style=EXERCISE)


def missing_values():
    text("# 8. Missing values")
    text("Missing data are the rule in real datasets: a sensor that did not answer, a field left empty, a merge or an alignment with no match. pandas marks them with `NaN`, and accepts Python's `None` as well:")
    s1 = pd.Series([4, None, 5, np.nan])  # @inspect s1
    text("Both became `NaN`, and the Series is `float64`: `NaN` is a floating point value, so the numbers stay in a fast NumPy array. (`None` is a Python object: `np.array([4, None, 5])` has dtype `object`.)")

    demo("Detecting, dropping, filling")
    text("- `isna()` (and its opposite `notna()`): a boolean mask, `True` where a value is missing.", style=SUBLIST_SPACED)
    missing = s1.isna()  # @inspect missing
    text("- `dropna()`: drops the missing elements.", style=SUBLIST_SPACED)
    dropped = s1.dropna()  # @inspect dropped
    text("- `fillna(value)`: replaces every missing value with `value`.", style=SUBLIST_SPACED)
    zeros = s1.fillna(0)  # @inspect zeros
    text("- `ffill()` (`bfill()`): replaces every missing value with the previous (next) valid one.", style=SUBLIST_SPACED)
    forward = s1.ffill()  # @inspect forward
    text("None of them modifies `s1`: each returns a new Series. Which one to use depends on the data: dropping loses information, filling invents it.")

    demo("Missing values in a DataFrame")  # @clear s1 missing dropped zeros forward
    df = pd.DataFrame({"Total": [1, 3, 5], "Quantity": [2, np.nan, 6]}, index=["a", "b", "c"])  # @inspect df
    text("- `dropna()` drops the **rows** with at least one missing value, `axis='columns'` the columns instead (`how='all'`: only the fully empty ones).", style=SUBLIST_SPACED)
    rows_dropped = df.dropna()  # @inspect rows_dropped
    columns_dropped = df.dropna(axis="columns")  # @inspect columns_dropped
    text("- Aggregations **skip** `NaN` by default: the mean of `Quantity` is the mean of the two values that exist.", style=SUBLIST_SPACED)  # @clear rows_dropped columns_dropped
    quantity_mean = df["Quantity"].mean()  # @inspect quantity_mean

    section("Summary: missing values")  # @clear df quantity_mean
    table_head(MISSING)  # @stepover
    table_row(MISSING, "`isna()`")  # @stepover
    table_row(MISSING, "`dropna()`")  # @stepover
    table_row(MISSING, "`fillna(")  # @stepover
    table_row(MISSING, "`ffill()`")  # @stepover


def introduction_to_matplotlib():
    text("# 9. Introduction to Matplotlib")
    text("Matplotlib is **the** plotting library of Python: pandas draws with it, and so does **Seaborn**, a higher-level library for statistical charts that you will meet later in the course. The library is large, and visualization is not the focus of this course: here we see the core. Install it with `pip install matplotlib` (on Google Colab it is already installed).")
    code_row(IMPORT_MATPLOTLIB)  # @stepover

    section("Two interfaces")
    text("Matplotlib can be used in two ways:")
    text("- **Stateful** (MATLAB style): you call functions of the `pyplot` module (`plt.plot`, `plt.xlabel`, ...), and they all work on the **current** Figure and Axes, which pyplot remembers for you.", style=SUBLIST)
    text("- **Stateless** (object oriented): you call the methods of a **specific** Figure or Axes object (`ax.plot`, `ax.set_xlabel`, ...): with several plots at once, it is always clear which one you are changing.", style=SUBLIST)

    demo("Stateful: plot y = x²")
    x = np.linspace(-10, 10, 100)  # 100 points between -10 and 10
    y = x**2
    plt.figure(figsize=(5, 3))  # a new figure, 5 x 3 inches: it becomes the current one
    plt.plot(x, y)  # draws on the current figure
    show(plt.gcf(), "parabola")  # instead of plt.show() @stepover
    text("`plt.show()` displays the current figure (in a notebook, a figure at the end of a cell is shown anyway). In this lecture, `show(...)` saves the figure and puts it on the page instead.")


def figures_and_axes():
    text("# 10. Stateless: Figures and Axes")
    text("A **Figure** is the whole image; the **Axes** are the plots inside it, each with its own x axis and y axis. One Figure can hold several Axes:")
    show(anatomy_figure(), "anatomy")  # @stepover

    demo("A new figure, a line plot")
    text("- `plt.subplots(figsize=(width, height))` returns a new Figure **and** its Axes; the size is in inches, and with no other arguments there is a single Axes.", style=SUBLIST_SPACED)
    fig, ax = plt.subplots(figsize=(5, 3))
    text("- `ax.plot(x, y)` takes two lists (or NumPy arrays) of coordinates and joins the points with segments; each new call adds a line, in a new colour.", style=SUBLIST_SPACED)
    ax.plot([0, 1, 2], [2, 4, 6])
    ax.plot([0, 1, 2], [3, 6, 9])
    text("- The `ax.set_...` methods set the attributes, and `ax.grid()` draws the grid.", style=SUBLIST_SPACED)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_xticks([0, 1, 2])
    ax.grid()
    show(fig, "two_lines")  # instead of plt.show() @stepover

    section("Figure and axis attributes")
    text("Both interfaces can set the attributes of figures and axes - the size of the figure, the axis labels, limits and ticks, the grid - with slightly different names (`plt.ylabel` becomes `ax.set_ylabel`):")
    code_row(INTERFACES)  # @stepover
    text("✍️ **Your turn - `4.1_matplotlib_figures_and_axes.ipynb`, exercises 1 and 2.** Plot `sin(x)` with a title and axis names, first with the stateful interface, then with the stateless one: the two figures must come out identical.", style=EXERCISE)

    demo("Many subplots")
    text("The first two parameters of `plt.subplots` are the **rows** and the **columns** of a grid of Axes, and `ax` is then a NumPy array of Axes objects:")
    text("- **One row** of n Axes: `ax` has shape `(n,)`, and `ax[1]` is the second plot.", style=SUBLIST_SPACED)
    fig, ax = plt.subplots(1, 2, figsize=(5, 2.5))
    one_row = ax.shape  # @inspect one_row
    ax[0].plot([0, 1, 2], [2, 4, 6])
    ax[1].plot([0, 1, 2], [3, 6, 9])
    fig.tight_layout()  # fit the subplots in the figure, without overlaps or blank borders
    show(fig, "subplots_row")  # @stepover
    text("- **A grid** of m rows and n columns: `ax` has shape `(m, n)`, and `ax[1, 1]` is the bottom-right plot.", style=SUBLIST_SPACED)  # @clear one_row
    fig, ax = plt.subplots(2, 2, figsize=(5, 4))
    grid = ax.shape  # @inspect grid
    ax[0, 0].plot([0, 1, 2], [2, 4, 6])  # top left
    ax[1, 1].plot([0, 1, 2], [3, 6, 9])  # bottom right
    fig.tight_layout()
    show(fig, "subplots_grid")  # @stepover
    text("Call `tight_layout()` at the end, otherwise the labels of neighbouring subplots can overlap.")


def plot_types():
    text("# 11. Plot types")
    text("The five most common plots: line, scatter, bar, histogram and box plot. All of them are methods of the Axes.")

    demo("Line plot")
    text("A sequence of points joined by segments, all with the **same** style (colour, line, marker, ...), set by keyword arguments:")
    x = np.linspace(0, 5, 20)
    y = np.exp(x)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.plot(x, y, c="blue", linestyle="", marker="*", label="curve 1")  # markers only, no line
    ax.plot(x, 2 * y, c="green", linestyle="--", label="curve 2")  # a dashed line
    ax.legend(loc="upper left")  # the labels, in a legend
    show(fig, "line_plot")  # @stepover
    table_all(LINE_STYLE)  # @stepover

    demo("Scatter plot")
    text("A cloud of points where, unlike a line plot, each point has **its own** colour and size:")
    np.random.seed(0)  # so that the lecture always shows the same points
    x = np.random.rand(50)
    y = np.random.rand(50)
    colors = x + y  # one number per point: the colour as a function of x and y
    area = 100 * (x + y)  # one number per point: the size
    fig, ax = plt.subplots(figsize=(5, 3))
    points = ax.scatter(x, y, c=colors, s=area, cmap="viridis")
    fig.colorbar(points, ax=ax)  # which colour stands for which number
    show(fig, "scatter_plot")  # @stepover
    text("- `c` gives one number per point, in the same order as `x` and `y`: their range, min to max, is stretched over a **colormap** (`cmap`).", style=SUBLIST_SPACED)
    text('- Other colormaps: `"spring"`, `"coolwarm"`, `"plasma"`, ... see the <a href="https://matplotlib.org/stable/users/explain/colors/colormaps.html" target="_blank">Matplotlib colormaps</a>.', style=SUBSUBLIST)
    text("- `s` gives the size of each marker, as an area (in points squared).", style=SUBLIST)

    demo("Bar chart")
    text("One bar per number, at the given x positions; here two series of bars, **grouped** by sensor:")
    height_min = [10, 2, 8]
    height_max = [8, 6, 5]
    labels = ["Sensor 1", "Sensor 2", "Sensor 3"]
    x = np.arange(3)  # the position of each group of bars @inspect x
    width = 0.4
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(x - width / 2, height_min, width=width, label="min")  # shifted to the left
    ax.bar(x + width / 2, height_max, width=width, label="max")  # shifted to the right
    ax.set_xticks(x, labels)  # positions and names of the x ticks
    ax.legend()
    show(fig, "bar_chart")  # @stepover
    text("- To **group** bars, shift each series by half a bar width, and write the category names on the ticks.", style=SUBLIST_SPACED)
    text("- A single series can name its bars directly: `ax.bar(x, height, tick_label=labels)`.", style=SUBLIST)

    demo("Histogram")  # @clear x
    text("The **frequency distribution** of one variable: how many values fall in each interval (*bin*):")
    np.random.seed(0)
    heights = np.random.normal(170, 10, 500)  # 500 people: mean 170 cm, standard deviation 10 cm
    bins = np.arange(140, 200, 2.5)  # the edges of the intervals @inspect bins
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.hist(heights, bins=bins)
    ax.text(142, 40, f"μ = {np.mean(heights):.2f}\nσ = {np.std(heights):.2f}", fontsize=10)  # text at data coordinates (142, 40)
    ax.set_xlabel("Height (cm)")
    ax.set_ylabel("Number of people")
    ax.set_title("Height distribution")
    show(fig, "histogram")  # @stepover
    text("- `bins=` an integer n splits the range into n equal bins (10 by default); `bins=` an array gives the **edges** of the bins.", style=SUBLIST_SPACED)
    text("- `ax.text(x, y, string)` writes on the plot, at the coordinates of the data. Between dollar signs Matplotlib also renders LaTeX-like math: `r'$\\mu$'` is μ.", style=SUBLIST)

    demo("Box plot")  # @clear bins
    text("Another way to show a distribution, handy to **compare** several of them side by side:")
    np.random.seed(0)
    short = np.random.normal(170, 10, 500)
    tall = np.random.normal(190, 10, 500)
    fig, ax = plt.subplots(figsize=(5, 3))
    ax.boxplot([short, tall])  # one box per distribution
    ax.set_xticks([1, 2], ["Short", "Tall"])  # the boxes sit at x = 1, 2, ...
    ax.set_ylabel("Height (cm)")
    show(fig, "box_plot")  # @stepover
    text("- The **box** extends from the first quartile (Q1) to the third quartile (Q3), and the **middle line** is the median.", style=SUBLIST_SPACED)
    text("- The **whiskers** extend from the box to the farthest data point lying within 1.5 × the inter-quartile range (IQR = Q3 - Q1) from the box.", style=SUBLIST)
    text("- The **fliers** are the points past the end of the whiskers: candidate outliers.", style=SUBLIST)

    demo("pandas draws with Matplotlib")
    compact_panel("14px")  # a wide table: a smaller panel until the end of this section @stepover
    text("Series and DataFrames have a `.plot` accessor that builds the Matplotlib plot for you, with the index on the x axis and the column names in the legend. The per-species means of section 1, as a bar chart:")
    iris = pd.read_csv(data_path("iris_sample.csv"))  # the file written in section 1
    means = iris.groupby("species").mean()  # @inspect means
    fig, ax = plt.subplots(figsize=(6, 3))
    means.plot.bar(ax=ax, rot=0)  # one group of bars per row, one bar per column
    ax.set_ylabel("cm")
    show(fig, "pandas_bar")  # @stepover
    text("Pass the Axes with `ax=`, and the rest of the figure is yours to set as usual.")

    demo("Writing images to file")  # @clear means
    text("`fig.savefig(path)` writes the figure to a file; the extension picks the format: `.png`, `.jpg`, `.svg`, `.pdf`, `.eps`.")
    fig, ax = plt.subplots(figsize=(3, 2))
    ax.plot([0, 1, 2], [2, 4, 6])
    path = data_path("test.png")  # @inspect path
    fig.savefig(path)
    plt.close(fig)  # a saved figure is still open: close it, or a notebook shows it too
    text("That is exactly what `show(...)` has been doing all along in this lecture, with `.svg`.")

    section("Summary: plot types")  # @clear path
    table_all(PLOT_TYPES)  # @stepover
    text("✍️ **Your turn - `4.2_matplotlib_advanced_plots.ipynb`, exercises 1, 2 and 3.** A scatter plot of two clouds of points with a legend; two bar charts side by side; and two overlapping histograms, with a legend, a text box with their mean and variance, axis limits, a title and a grid.", style=EXERCISE)


def closing():
    text("# Wrapping up")
    text("1) A **Series** is a NumPy array with a label on every element; a **DataFrame** is a table of Series that share one index.", style=SUBLIST)
    text("2) **`.loc` works with labels** (slice stop included), **`.iloc` with positions** (stop excluded): say which one you mean.", style=SUBLIST)
    text("3) Operations **align on labels**, not on positions: what does not match becomes `NaN`.", style=SUBLIST)
    text("4) **concat** stacks, **merge** joins on values, **groupby** splits, aggregates and filters.", style=SUBLIST)
    text("5) Since pandas 3.0, what you take out of a DataFrame behaves as a **copy**: write through `df.loc[...] = ...`.", style=SUBLIST)
    text("6) Matplotlib: a **Figure** holds one or more **Axes**; prefer the object-oriented `fig, ax = plt.subplots()` over the stateful `plt.*` calls.", style=SUBLIST)

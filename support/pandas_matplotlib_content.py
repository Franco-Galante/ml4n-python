"""Long-form content for 03_pandas_and_matplotlib.py: table specs, code snippets, example files.

The viewer swaps only the first line of a call for its rendering, so anything
too long for one lecture line lives here and the lecture keeps a single call.
"""

# The presenter is the same as in lecture 1: one place to edit the portrait.
from .python_content import AUTHORS  # noqa: F401  (re-exported for the title slide)

# ----------------------------------------------------------------- pandas --
IMPORT_PANDAS = [
    ("what everybody writes", "import numpy as np\nimport pandas as pd\n\npd.Series([2.0, 3.1, 4.5])", "python"),
]

# Nine flowers of Lab 1's Iris dataset, three per species, with a header row.
IRIS_SAMPLE = """sepal_length,sepal_width,petal_length,petal_width,species
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
4.7,3.2,1.3,0.2,setosa
7.0,3.2,4.7,1.4,versicolor
6.4,3.2,4.5,1.5,versicolor
6.9,3.1,4.9,1.5,versicolor
6.3,3.3,6.0,2.5,virginica
5.8,2.7,5.1,1.9,virginica
7.1,3.0,5.9,2.1,virginica
"""

LAB1_VS_PANDAS = [
    ("Lab 1: plain Python", "import csv\n\nrows = []\nwith open(path) as f:\n    reader = csv.reader(f)\n    next(reader)  # skip the header\n    for record in reader:\n        rows.append(record)  # every field is a string\n\nsums, counts = {}, {}\nfor row in rows:\n    species = row[4]\n    sums[species] = sums.get(species, 0) + float(row[0])  # str -> float\n    counts[species] = counts.get(species, 0) + 1\nmeans = {s: sums[s] / counts[s] for s in sums}\n\n# ...and again for every other column", "python"),
    ("pandas", "iris = pd.read_csv(path)\nmeans = iris.groupby(\"species\").mean()\n\n# every column, every species", "python"),
]

LOC_ILOC = {
    "headers": ["", "`s.loc[...]`", "`s.iloc[...]`"],
    "widths": ["22%", "39%", "39%"],
    "rows": [
        ["**Selects by**", "**Label**: the names in the index you gave (`'mon'`, `'a'`, ...)", "**Position**: `0, 1, 2, ...`, as in a list or an array"],
        ["**Single element**", "`s.loc['b']`", "`s.iloc[1]`"],
        ["**Slice**", "`s.loc['b':'c']`: stop **included**", "`s.iloc[1:3]`: stop **excluded**, as in Python"],
        ["**Mask**", "`s.loc[s > 2]`", "`s.iloc[(s > 2).to_numpy()]`: a plain boolean array (pandas 3 also takes a boolean Series with an integer index)"],
        ["**Fancy**", "`s.loc[['a', 'c']]`", "`s.iloc[[0, 2]]`"],
    ],
}

DF_ACCESS = {
    "headers": ["You write", "You get", "Notes"],
    "widths": ["34%", "22%", "44%"],
    "rows": [
        ["`df['Quantity']`", "A column (**Series**)", "A **name** in plain brackets selects a column: `df['a']` looks for a column named `'a'`"],
        ["`df[['Price', 'Liters']]`", "Some columns (**DataFrame**)", "A list of names"],
        ["`df[mask]`", "Some rows (**DataFrame**)", "A **mask** in plain brackets selects rows: shorthand for `df.loc[mask]`"],
        ["`df.loc['a']`, `df.iloc[0]`", "A row (**Series**)", "The column names become its index"],
        ["`df.loc[rows, columns]`", "Anything", "One selector per axis, as in NumPy: labels, slices (stop **included**), masks, lists"],
        ["`df.iloc[rows, columns]`", "Anything", "The same, with **positions** (stop excluded)"],
    ],
}

PANDAS_2_VS_3 = {
    "headers": ["Area", "pandas 2.x", "pandas 3.0", "Example"],
    "widths": ["17%", "25%", "25%", "33%"],
    "rows": [
        ["**String columns**", "Inferred as `object`", "Inferred as the dedicated `str` dtype", "`pd.Series(['a', 'b']).dtype`: `object` vs `str`"],
        ["**Copy or view**", "A selection could be a view or a copy, hard to predict", "**Copy-on-Write** always on: every selection behaves as a copy", "`p = df['Price']; p.loc['b'] = 99` changes `df` in 2.x, not in 3.0"],
        ["**Chained assignment**", "Sometimes worked, often with a `SettingWithCopyWarning`", "Never modifies the original (`ChainedAssignmentError` warning)", "`df['Price']['b'] = 99`: write `df.loc['b', 'Price'] = 99` instead"],
        ["**Float into an int column**", "The column silently becomes `float64`", "`TypeError`: create the column as float", "`df.loc[0, 'n'] = 1.5` on an `int64` column"],
        ["**Integer key, text index**", "`s[0]` falls back to the first **position** (with a warning)", "`s[0]` is always a **label**: `KeyError`", "Write `s.iloc[0]`"],
        ["**Boolean Series in `.iloc`**", "Never: `NotImplementedError` (or `ValueError` with a text index)", "Accepted if its index is made of integers, matched by label", "`s.iloc[s > 2]` on the default index `0, 1, 2, ...`; `s.iloc[(s > 2).to_numpy()]` works in both"],
        ["**Datetime resolution**", "Always nanoseconds", "Inferred from the data (seconds ... nanoseconds)", "`pd.to_datetime(['2026-10-01']).dtype`: `datetime64[ns]` vs `datetime64[us]`"],
        ["**Categorical `groupby`**", "`observed=False`: every category, even the empty ones", "`observed=True`: only the categories present in the data", "Categories `a`, `b`, data only `a`: groups `a, b` vs `a`"],
        ["**Removed functions**", "Deprecated, still working", "Removed", "`fillna(method='ffill')` → `ffill()`, `applymap` → `map`, `freq='H'` → `'h'`"],
        ["**Compatibility**", "Python ≥ 3.9", "Python ≥ 3.11, NumPy ≥ 1.26", "`pd.__version__` tells you which one you have"],
    ],
}

ALIGNMENT = {
    "headers": ["Operands", "Aligned on", "What does not match"],
    "widths": ["30%", "35%", "35%"],
    "rows": [
        ["**Series** and **Series**", "The **index**", "`NaN` in the result"],
        ["**DataFrame** and **DataFrame**", "The **index** and the **columns**", "`NaN` in the result"],
        ["**DataFrame** and **Series**", "The **columns** of the DataFrame with the **index** of the Series; the Series is repeated on every row (broadcasting)", "`NaN` in the result"],
    ],
}

COMBINING = {
    "headers": ["Function", "What it does", "Watch out"],
    "widths": ["26%", "38%", "36%"],
    "rows": [
        ["`pd.concat((a, b))`", "**Stacks** Series or DataFrames, vertically by default", "Keeps the index as it is, duplicates included (`ignore_index=True` renumbers)"],
        ["`pd.merge(df1, df2)`", "**Joins** two DataFrames on the values of some columns, like a database join", "One-to-one, many-to-one or many-to-many: `validate='1:1'` checks it"],
        ["`df1.append(df2)`", "**Removed** in pandas 2.0: older tutorials still use it", "Write `pd.concat((df1, df2))` instead"],
    ],
}

GROUPBY = {
    "headers": ["Operation", "Code", "What comes out"],
    "widths": ["22%", "44%", "34%"],
    "rows": [
        ["**Iterate**", "`for key, group in df.groupby('k'):`", "One (key, DataFrame) pair per group"],
        ["**One column**", "`df.groupby('k')['c1'].mean()`", "A Series, one value per group, indexed by the key"],
        ["**Every column**", "`df.groupby('k').mean()`", "A DataFrame, **one row per group**, indexed by the key"],
        ["**Key back as a column**", "`df.groupby('k').mean().reset_index()`", "The key is an ordinary column, the index is `0, 1, ...`"],
        ["**Several aggregations**", "`df.groupby('k').agg(['max', 'min'])`", "One column per (column, aggregation) pair: **two levels** of names"],
        ["**Named aggregation**", "`df.groupby('k').agg(c1_max=('c1', 'max')).reset_index()`", "**Best practice**: one level of names, only the results you ask for"],
        ["**Filter**", "`df.groupby('k').filter(lambda g: g['c1'].mean() > 5)`", "The **rows** of the groups that pass the test"],
    ],
}

# ---------------------------------------------------------------------- I/O --
MYCSV = """MyTitle
c1,c2,c3
0,1,2
3,4,5
6,7,8
"""

MYCSV_MISSING = """c1,c2,c3
0,no info,
3,4,5
6,x,NaN
"""

READ_CSV = [
    ("mycsv.csv", MYCSV),
]

READ_CSV_MISSING = [
    ("mycsv_missing.csv", MYCSV_MISSING),
]

IO_FORMATS = {
    "headers": ["Format", "Read", "Write"],
    "widths": ["22%", "39%", "39%"],
    "rows": [
        ["**CSV**", "`pd.read_csv(path, sep=',')`", "`df.to_csv(path, index=False)`"],
        ["**JSON**", "`pd.read_json(path)`", "`df.to_json(path)`"],
        ["**Excel**", "`pd.read_excel(path)`", "`df.to_excel(path)`"],
        ["**Parquet**", "`pd.read_parquet(path)`", "`df.to_parquet(path)`: compressed and typed, for large tables"],
    ],
    "caption": 'And many more (HTML, HDF5, SQL, ...): see the <a href="https://pandas.pydata.org/docs/user_guide/io.html" target="_blank">pandas I/O guide</a>.',
}

MISSING = {
    "headers": ["Method", "What it does"],
    "widths": ["34%", "66%"],
    "rows": [
        ["`isna()`, `notna()`", "A boolean mask of the same shape: `True` where a value is missing (or present)"],
        ["`dropna()`", "Drops the elements (Series) or the **rows** (DataFrame) with at least one missing value; `axis='columns'` drops columns, `how='all'` only fully empty ones"],
        ["`fillna(value)`", "Replaces every missing value with `value`"],
        ["`ffill()`, `bfill()`", "Replaces every missing value with the previous (next) valid one"],
    ],
}

# ------------------------------------------------------------- Matplotlib --
IMPORT_MATPLOTLIB = [
    ("what everybody writes", "import matplotlib.pyplot as plt", "python"),
]

INTERFACES = [
    ("stateful (pyplot)", "plt.figure(figsize=(10, 5))\nplt.plot(x, y)\nplt.ylabel('Y')\nplt.xlim([0, 10])\nplt.xticks([0, 1, 2, 5, 10])\nplt.grid()\nplt.show()", "python"),
    ("stateless (object oriented)", "fig, ax = plt.subplots(figsize=(10, 5))\nax.plot(x, y)\nax.set_ylabel('Y')\nax.set_xlim([0, 10])\nax.set_xticks([0, 1, 2, 5, 10])\nax.grid()\nplt.show()", "python"),
]

LINE_STYLE = {
    "headers": ["Parameter", "Controls", "Examples"],
    "widths": ["20%", "32%", "48%"],
    "rows": [
        ["`linestyle`", "The line between the points", "`'-'` (solid), `'--'` (dashed), `':'` (dotted), `''` (none)"],
        ["`marker`", "The symbol on each point", "`'o'`, `'*'`, `'+'`, `'^'`"],
        ["`c` (or `color`)", "Line and markers", "`'red'`, `'grey'`; `'#0F0F6B'` (RGB); `(0.5, 1, 0.8, 0.8)` (RGBA)"],
        ["`label`", "The name in the legend", "`'curve 1'`, then `ax.legend()`"],
    ],
}

PLOT_TYPES = {
    "headers": ["Plot", "Method", "Use it to show"],
    "widths": ["20%", "30%", "50%"],
    "rows": [
        ["**Line plot**", "`ax.plot(x, y)`", "A sequence of points joined by segments, all with the same style: a function, a time series"],
        ["**Scatter plot**", "`ax.scatter(x, y)`", "A cloud of points, each with its own colour and size: the relation between two features"],
        ["**Bar chart**", "`ax.bar(x, height)`", "One number per category"],
        ["**Histogram**", "`ax.hist(x, bins)`", "The **distribution** of one variable: how many values fall in each interval"],
        ["**Box plot**", "`ax.boxplot([x1, x2])`", "Several distributions side by side, summarised by their quartiles"],
    ],
}

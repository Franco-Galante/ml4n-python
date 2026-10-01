"""Computation behind 03_pandas_and_matplotlib.py that the class does not need to step into.

edtrace traces the lecture module and nothing else, so everything here runs as
a single step: the code panel stays on the pandas and the Matplotlib being
taught, not on the scaffolding that draws them.

Two things the viewer cannot do on its own, and that this module adds:

- **pandas objects on the panel.**  edtrace serialises a value it does not know
  with `str()`, so a DataFrame would reach the panel as one long escaped string.
  It does honour an `asdict()` method, though: the classes below get one that
  hands back a grid of strings (a NumPy array, which the viewer draws as a
  table), with the column names on top and the index on the left - the way a
  notebook shows a DataFrame.  Importing this module is enough to install it.
- **Matplotlib figures in the lecture.**  The viewer has no Matplotlib support,
  so `show(fig, name)` saves the figure as an SVG under var/ and puts it on the
  page with `figure()`, where `plt.show()` would open a window.
"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # no window: the figures are written to files

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from pandas.core.groupby import DataFrameGroupBy, SeriesGroupBy  # noqa: E402
from pandas.io.formats.format import format_array  # noqa: E402

from .python_lab import describe as _describe  # noqa: E402
from .slides import _media_size, figure  # noqa: E402


def describe(error: Exception) -> str:
    """The same helper as lectures 1 and 2 (an exception printed the way the
    interpreter prints it), cut to its first line: some pandas errors append a
    listing of the offending rows, which the panel cannot show."""
    return _describe(error).split("\n")[0]

# Generated at run time under var/ (gitignored), so the lecture ships no data
# files of its own and every run starts from the same content.
DATA_DIR = Path("var/data")
PLOT_DIR = Path("var/plots/03_pandas_and_matplotlib")


# ------------------------------------------------------ pandas on the panel --
def _cells(column: pd.Series) -> list[str]:
    """One column formatted the way pandas prints it (NaN, aligned decimals), then trimmed."""
    try:
        return [cell.strip() for cell in format_array(column._values, None)]
    except Exception:  # an exotic dtype: plain str() is good enough
        return [str(value) for value in column]


def _labels(index: pd.Index) -> list[list[str]]:
    """The labels of an index, one list per level (a MultiIndex has several)."""
    if isinstance(index, pd.MultiIndex):
        return [[str(label[level]) for label in index] for level in range(index.nlevels)]
    return [[str(label) for label in index]]


def _frame_grid(df: pd.DataFrame) -> np.ndarray:
    """A DataFrame as a grid of strings: column names on top, index on the left.

    The top-left cell is always empty: THEME_CSS in slides.py keys off it to
    set the header row and the index column in bold, so a DataFrame reads
    differently from a plain NumPy matrix.
    """
    index_levels = _labels(df.index)
    width = len(index_levels)
    rows = [[""] * width + level for level in _labels(df.columns)]
    if any(name is not None for name in df.index.names):  # pandas prints the index name on a row of its own
        rows.append([str(name) if name is not None else "" for name in df.index.names] + [""] * df.shape[1])
    columns = [_cells(df.iloc[:, j]) for j in range(df.shape[1])]
    for i in range(df.shape[0]):
        rows.append([level[i] for level in index_levels] + [column[i] for column in columns])
    return np.array(rows, dtype=object)


def _series_grid(series: pd.Series) -> np.ndarray:
    """A Series the way pandas prints it: index on the left, values on the right,
    and `Name: ..., dtype: ...` underneath.

    The first row is left entirely empty: THEME_CSS in slides.py hides it, and
    uses it to tell a Series from a DataFrame, whose header row has names.
    Without it, the name would sit on top like a column header, and a row
    taken with df.loc['a'] would look like a table with a column called 'a'.
    """
    index_levels = _labels(series.index)
    width = len(index_levels)
    rows = [[""] * (width + 1)]
    if any(name is not None for name in series.index.names):
        rows.append([str(name) if name is not None else "" for name in series.index.names] + [""])
    values = _cells(series)
    for i in range(len(series)):
        rows.append([level[i] for level in index_levels] + [values[i]])
    name = "" if series.name is None else f"Name: {series.name}"
    rows.append([name] + [""] * (width - 1) + [f"dtype: {series.dtype}"])
    return np.array(rows, dtype=object)


def _index_labels(index: pd.Index) -> list:
    """An Index (df.columns, df.index) as the list of its labels."""
    return [label.item() if hasattr(label, "item") else label for label in index]


def _groups(grouped) -> dict:
    """A GroupBy object as {key: the rows of that group}: what iterating over it hands out."""
    return {str(key): group for key, group in grouped}


# edtrace's to_serializable_value() calls value.asdict() when it exists.
pd.DataFrame.asdict = _frame_grid
pd.Series.asdict = _series_grid
pd.Index.asdict = _index_labels
DataFrameGroupBy.asdict = _groups
SeriesGroupBy.asdict = _groups


# ------------------------------------------------------------------ files --
def data_path(name: str) -> str:
    """A writable path under var/data/ for the files the lecture reads and writes."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    return (DATA_DIR / name).as_posix()


def write_file(name: str, content: str) -> str:
    """Write a small example file under var/data/ and return its path."""
    path = data_path(name)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    return path


def read_file(path: str) -> str:
    """The content of a text file, to show on the panel what pandas wrote."""
    with open(path, encoding="utf-8") as f:
        return f.read()


# --------------------------------------------------------------- figures --
def show(fig, name: str, width: str | None = None) -> None:
    """Put a Matplotlib figure on the page: what plt.show() does in a notebook.

    The figure is saved as an SVG cropped to its content (`bbox_inches="tight"`,
    or the axis labels of a small figure fall off its edge), and drawn at 1.2x
    its natural size, like every other figure of the course, so its lettering
    (10 pt by default) comes out at about the body-text size.  It is then
    closed, so the next stateful plt.* call starts from a fresh figure.
    """
    PLOT_DIR.mkdir(parents=True, exist_ok=True)
    path = (PLOT_DIR / f"{name}.svg").as_posix()
    fig.savefig(path, format="svg", bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)
    if width is None:
        points = _media_size(path)[0]  # the SVG's own width, in points
        width = f"{points * 96 / 72 * 1.2:.0f}px"
    figure(path, width=width)


def anatomy_figure():
    """One Figure with two Axes, each part labelled with its own name."""
    fig, axes = plt.subplots(1, 2, figsize=(7, 3))
    fig.patch.set_facecolor("#eaf2fb")
    fig.suptitle("Figure", fontweight="bold")
    for ax, name in zip(axes, ["Axes 0", "Axes 1"]):
        ax.set_title(name)
        ax.set_xlabel("x axis")
        ax.set_ylabel("y axis")
    axes[0].plot([0, 1, 2], [2, 4, 6])
    axes[1].plot([0, 1, 2], [3, 6, 9], color="tab:orange")
    fig.tight_layout()
    return fig

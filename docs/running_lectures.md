# Running the lectures on your own computer

Each lecture of this course is a **Python program**. The online viewer linked in the [README](../README.md) shows a run that we recorded; this guide is for when you want to **execute the lectures yourself** - to change the code and see what happens, or to work offline.

You do not need any of this to follow the course: the online viewer and the PDF handouts cover everything.

How it works, in one paragraph: a tool called [edtrace](https://github.com/percyliang/edtrace) runs a lecture file (`01_python.py`, ...) and records every step - which line ran, what it displayed, and the value of the variables marked for inspection - into a *trace* (`var/traces/01_python.json`). A small web app, the **viewer**, then replays that trace in your browser. So there are two parts to install: the Python side, which executes the lectures, and the viewer, which is a JavaScript app run by Node.js.

## Step 0 - Install the prerequisites (skip what you already have)

Check what you already have:

```bash
git --version
uv --version
node --version
npm --version
```

You need **Git**, **uv** (a fast Python package and environment manager) and **Node.js (LTS)**. You do not need to install Python: `uv` downloads the right version by itself.

### macOS

- Git: running `git --version` may prompt macOS to install the Command Line Tools. You can also install Git from <https://git-scm.com/download/mac>.
- uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- Node.js LTS: <https://nodejs.org/en/download>

Restart the terminal after installing tools if a command is not immediately found.

### Linux

- Git: install it with your distribution package manager, for example:

```bash
# Ubuntu / Debian
sudo apt update && sudo apt install git
```

- uv:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

- Node.js LTS: <https://nodejs.org/en/download>

### Windows

Use **PowerShell**.

- Git: <https://git-scm.com/download/win>
- uv:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

- Node.js LTS: <https://nodejs.org/en/download>

Close and reopen PowerShell after installation if needed.

## Step 1 - Download the course once

```bash
git clone --recurse-submodules https://github.com/Franco-Galante/ml4n-students.git
cd ml4n-students
```

`--recurse-submodules` also downloads the viewer, which lives in the `edtrace/` folder as a separate repository (a git *submodule*). If you cloned without it, `edtrace/` is empty; fix it with:

```bash
git submodule update --init --recursive
```

**Run every command in this guide from the course folder**, not from a subdirectory. The tools use paths relative to it.

## Step 2 - Install the course dependencies once

```bash
uv sync
npm ci --prefix edtrace/frontend
```

- `uv sync` creates a virtual environment in `.venv/` with the Python packages listed in `pyproject.toml`, at the exact versions of `uv.lock`. **edtrace depends on PyTorch, so expect a download of a few gigabytes and several minutes the first time.** Later runs are fast.
- `npm ci` installs the viewer's JavaScript packages into `edtrace/frontend/node_modules/`.

You normally do this only once, or again when the course dependencies are updated.

## Step 3 - Execute a lecture

```bash
uv run python tools/prepare_lecture.py 01_python
```

This runs `01_python.py` and writes a fresh trace to `var/traces/01_python.json`. Traces are not stored in the repository, so run this at least once per lecture before you can view it. When there are several lectures, you can prepare them in one command by listing their names:

```bash
uv run python tools/prepare_lecture.py 01_python 02_numpy
```

`uv run` executes the command inside the course environment of Step 2, so you never have to activate it by hand.

## Step 4 - Explore your execution in the browser

Start the viewer:

```bash
npm run --prefix edtrace/frontend dev -- --port 5173 --strictPort
```

Then open <http://localhost:5173/?trace=01_python>.

Leave the server running: to switch lecture, just change the `trace` parameter in the URL. Stop it with `Ctrl+C` in the terminal.

Controls (the letter shortcuts are uppercase, so press them with Shift):

| Key | Action |
| --- | --- |
| `→` / `l` | step forward |
| `←` / `h` | step backward |
| `Shift + →` / `j` | step over forward (do not enter a function call) |
| `Shift + ←` / `k` | step over backward |
| `u` | step out of the current function |
| `Shift + A` | toggle gradual reveal (on by default) |
| `Shift + R` | toggle rendered / raw-code view |
| `Shift + E` | show / hide the variable panel |
| `Shift + N` | show / hide notes |
| `g` | load a different trace |

You can also click a line number to jump directly to that point of the execution.

## Step 5 - Modify a lecture

This is the point of running the lectures yourself. Open `01_python.py` in your editor, change an example, then run Step 3 again and reload the browser page: the viewer now shows *your* execution.

A few things to know:

- **Everything starts from `main()`.** The lecture file calls one function per section from `main()`; code written at the top level of the file runs but does not appear in the viewer.
- **To watch a variable**, append `# @inspect variable_name` to the line that changes it. `# @clear variable_name` removes it from the panel.
- **Only some calls reach the screen**: `text(...)`, `image(...)`, `plot(...)` and the helpers from `support/`. A `print()` goes to your terminal, not to the viewer.
- **Only the lecture file is stepped through.** The `support/` folder holds code the lectures import - the page layout (`slides.py`), long texts and tables (`*_content.py`), and helper computations (`*_lab.py`) - and the viewer runs each call into it as a single step.
- Errors stop the lecture: `prepare_lecture.py` then prints a Python traceback that points at the line to fix.

To go back to the original version of a file, `git checkout -- 01_python.py`.

## Running the notebooks locally

The exercises and labs are Jupyter notebooks meant for Google Colab or the course Jupyter cluster (see the README). To run them on your computer instead, start Jupyter from the course folder with the libraries they use:

```bash
uv run --with jupyter --with pandas --with matplotlib jupyter notebook
```

`--with` adds the packages for this command only, without changing `pyproject.toml`, so `git pull` keeps working.

## Updating the course later

New lectures and exercises are added during the course (solutions are on the course portal). To get them:

```bash
git pull
git submodule update --init --recursive
uv sync
npm ci --prefix edtrace/frontend
```

Then re-run `prepare_lecture.py` for the lectures you want to view, since traces are generated locally and are not updated by `git pull`.

If you edited a lecture, `git pull` may refuse to overwrite your changes. Either keep a copy of your version under another name, or discard your changes with `git checkout -- <file>` before pulling. Work you want to keep is safest in a file of your own.

## Troubleshooting

**`uv`, `node`, or `npm` not found, right after installing it.** Close the terminal and open a new one so it picks up the updated `PATH`.

**`Error loading trace` in the browser.** You have not executed that lecture yet, or the name in the URL does not match the lecture file. Run `uv run python tools/prepare_lecture.py <lecture_name>` and check the spelling.

**The page stays blank.** Reload it: the viewer sometimes fails to start on the first load. If it is still blank, the viewer is not running, or it failed to start because port 5173 is already used by something else. Look at the terminal output; if the port is busy, start it without a fixed port and use the address it prints:

```bash
npm run --prefix edtrace/frontend dev
```

**`No such file or directory: tools/prepare_lecture.py`.** You are not in the course folder. `cd` into it and retry.

**`edtrace/frontend` is empty, or `npm ci` complains there is no `package-lock.json`.** The submodule was not downloaded. Run `git submodule update --init --recursive`.

**Images are missing from the lecture.** Re-run `prepare_lecture.py` for that lecture; it republishes the image files together with the trace.

**`git status` says the `edtrace` folder is modified.** Expected: generated files are written inside it. You can ignore it, and you should not commit it.

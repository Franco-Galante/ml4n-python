"""Execute one or more lectures and publish their assets to the viewer."""

from pathlib import Path
import os
import shutil
import subprocess
import sys

PUBLIC = Path("edtrace/frontend/public")
ASSET_DIRS = ("var", "images")


def publish(name: str) -> None:
    """Make ./<name> reachable from the viewer's static root.

    A symlink is used where the platform allows it, so new traces appear
    without re-copying. Otherwise the directory is copied on every run.
    """
    source = Path(name)
    if not source.exists():
        return

    target = PUBLIC / name
    if target.is_symlink():
        return
    # edtrace commits public/var and public/images as symlinks; where git cannot
    # create symlinks (Windows by default) it checks them out as small text files.
    if target.is_file():
        target.unlink()

    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        relative = os.path.relpath(source.resolve(), target.parent.resolve())
        os.symlink(relative, target, target_is_directory=True)
    except (OSError, NotImplementedError):
        shutil.copytree(source, target, dirs_exist_ok=True)


def main() -> None:
    lectures = sys.argv[1:]
    if not lectures:
        raise SystemExit(
            "Usage: python tools/prepare_lecture.py lecture_01 [lecture_02 ...]"
        )

    if not PUBLIC.parent.is_dir():
        raise SystemExit(
            "Run this from the course root (the directory containing edtrace/)."
        )

    # Execute with the current Python environment (normally launched via `uv run`).
    # UTF-8 mode: edtrace reads the lecture source back with a bare open(), which
    # on Windows uses the ANSI codepage and fails on any emoji in the lecture.
    subprocess.run(
        [sys.executable, "-m", "edtrace.execute", "-m", *lectures],
        check=True,
        env={**os.environ, "PYTHONUTF8": "1"},
    )

    for name in ASSET_DIRS:
        publish(name)

    for lecture in lectures:
        print(f"Trace ready: var/traces/{lecture}.json")


if __name__ == "__main__":
    main()

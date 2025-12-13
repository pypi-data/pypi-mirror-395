"""Tools for the command line interface"""

import collections
import difflib
import filecmp
import importlib
import pathlib
import tempfile

import click
import rich.progress
import typer
from pydantic import ValidationError
from rich.syntax import Syntax

from oocli import data


def format_validation_error(exception: ValidationError):
    """Format a Pydantic Validation Error into a readable form"""
    organized_errors = collections.defaultdict(list)
    for error in exception.errors():
        organized_errors[error["loc"]].append(error["msg"])

    formatted_error = [f"{exception.error_count()} {exception.title} validation errors"]
    for location, errors in organized_errors.items():
        formatted_error.append(f"  {'.'.join(map(str, location))}:")
        for error in errors:
            formatted_error.append(f"    {error}")

    return "\n".join(formatted_error)


def one_line(run: data.Run):
    """Return run information formatted in one line of text"""
    line = f"[sha]{run.short_sha}[/sha]"
    if run.tags:
        line = line + f" [sha]([bold]{', '.join(run.tags)}[/bold])[/sha]"
    if run.ended is None:
        line = line + "[green]"
    elif run.exit_status != 0:
        line = line + "[red]"

    title, *_ = run.message.splitlines()
    return line + f" {title}"


def print_version_and_exit(enable: bool):
    if enable:
        print(f"o-o {importlib.metadata.version('o-o')}")
        raise typer.Exit()


def print_diffs(
    left: pathlib.Path,
    right: pathlib.Path,
    /,
    print_fn=print,
):
    """Print diffs between given directories"""

    def _unified_diff(left, right, /):
        udiff = difflib.unified_diff(
            "" if left is None else left.read_text().splitlines(keepends=True),
            "" if right is None else right.read_text().splitlines(keepends=True),
            "/dev/null" if left is None else str(left),
            "/dev/null" if right is None else str(right),
        )
        return "".join(udiff)

    with tempfile.TemporaryDirectory() as empty_dir:
        empty_dir = pathlib.Path(empty_dir)

        def _diffs(left, right, /):
            diffs = filecmp.dircmp(left, right)
            for diff in diffs.diff_files:
                yield _unified_diff(left / diff, right / diff)

            for diff in diffs.left_only:
                if (left / diff).is_dir():
                    yield from _diffs(left / diff, empty_dir)
                else:
                    yield _unified_diff(left / diff, None)

            for diff in diffs.right_only:
                if (right / diff).is_dir():
                    yield from _diffs(empty_dir, right / diff)
                else:
                    yield _unified_diff(None, right / diff)

            for subdir in diffs.common_dirs:
                yield from _diffs(left / subdir, right / subdir)

        for diff in _diffs(left, right):
            print_fn(Syntax("".join(diff), lexer="diff"))


def prompt_for_message(*, default=None):
    """Prompt the user to write a message"""
    message = click.edit(
        f"{default or ''}\n"
        "# Please enter a message that describes this operation. Lines starting\n"
        "# with '#' will be ignored.\n"
    )
    if message is not None:
        message = "\n".join(
            line for line in message.splitlines() if not line.startswith("#")
        )
    return message


class TaskDisplay:
    """Progress spinner"""

    def __init__(self, console=None, disable=False):
        self._progress = rich.progress.Progress(
            rich.progress.SpinnerColumn(),
            rich.progress.TextColumn("[dim yellow]{task.description}"),
            transient=True,
            console=console,
            disable=disable,
        )
        self._task = None

    def __enter__(self):
        self._progress.__enter__()
        return self

    def __exit__(self, *args):
        self._progress.__exit__(*args)

    def set_current(self, description):
        if self._task is not None:
            self._progress.update(self._task, visible=False)
        self._task = self._progress.add_task(description, total=None)

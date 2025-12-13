import subprocess

from collections import deque
from logging import getLogger
from pathlib import Path
from re import sub
from typing import Iterable, Self
from unicodedata import normalize
from uuid import UUID

from phystool.config import config

logger = getLogger(__name__)


def should_compile(tex_file: Path) -> bool:
    dest_file = tex_file.with_suffix(".pdf")
    return (
        not dest_file.is_file() or dest_file.stat().st_mtime < tex_file.stat().st_mtime
    )


def terminal_yes_no(prompt: str) -> bool:
    """
    Ask for a confirmation in the terminal.

    :param prompt: text displayed before the '[y/n]:' question
    """
    while True:
        answer = input(prompt + " [y/n]: ").lower()
        if answer in ["yes", "y"]:
            return True
        elif answer in ["no", "n"]:
            return False


def silent_keyboard_interrupt(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyboardInterrupt:
            print()  # to force a new line
            pass

    return inner


def greptex(query: str, path: Path, silent: bool) -> set[UUID]:
    """Find query in tex files stored in the single directory `path`.

    Format query to match a newline followed by spaces and returns a set of
    uuids of tex files containing query.

    :param query: string that should be matched
    :param path: directory where the search occurs
    :param silent: if True, logs a warning when no match was found
    :returns: a set of uuids corresponding to tex files that contains the query
    """
    if not query:
        return set()
    query = (
        query.replace("\\", "\\\\")
        .replace("$", "\\$")
        .replace("{", "\\{")
        .replace("}", "\\}")
    )
    command = [
        "rg",
        "--type",
        "tex",
        "--color",
        "never",
        "--multiline",
        "--smart-case",
        "--files-with-matches",
        "--max-depth",
        "1",
        r"\s+".join([tmp.strip() for tmp in query.split()]),
        str(path),
    ]

    try:
        match = subprocess.run(command, capture_output=True, text=True)
        return set(UUID(Path(m).stem) for m in match.stdout.split("\n") if m)
    except subprocess.CalledProcessError as e:
        if e.returncode == 1:
            if not silent:
                logger.warning(f"'{query}' not found in any texfile in {path}")
        else:
            logger.error(e)
        return set()


def as_valid_filename(value: str) -> str:
    """
    Taken from slugify at https://github.com/django/django/blob/stable/5.2.x/
    Convert to ASCII. Convert spaces or repeated dashes to single dashes. Remove
    characters that aren't alphanumerics, underscores, or hyphens. Convert to lowercase.
    Strip leading and trailing whitespace, dashes, and underscores.
    """
    value = normalize("NFKD", value).encode("ascii", "ignore").decode("ascii").lower()
    value = sub(r"[-\s]+", "-", value)
    value = sub(r"[^\w\s-]", "", value)
    return value.strip("-_")


class ContextIterator[T]:
    """
    Wrapper around an iterable that allows peeking ahead to get next elements
    without consuming the iterator.
    """

    def __init__(self, iterable: Iterable[T], before: int, after: int):
        self._iterable = iter(iterable)
        self._cache_next: deque[T] = deque()
        self._cache_prev: deque[T] = deque()
        self._before = abs(before)
        self._after = abs(after)
        self._first_call = True
        self._current: T

    def __next__(self) -> T:
        if self._first_call:
            self._first_call = False
        else:
            self._cache_prev.append(self._current)
            if len(self._cache_prev) > self._before:
                self._cache_prev.popleft()

        if self._cache_next:
            self._current = self._cache_next.popleft()
        else:
            self._current = next(self._iterable)

        return self._current

    def __iter__(self) -> Self:
        return self

    def get(self) -> list[T]:
        try:
            while len(self._cache_next) < self._after:
                self._cache_next.append(next(self._iterable))
        except StopIteration:
            pass

        return list(self._cache_prev) + [self._current] + list(self._cache_next)


def progress_bar(max_step: int, step: int, length: int, msg: str) -> None:
    """Display a progress bar in the terminal

    :param max_step: process' maximum number of steps
    :param step: current process' step
    :param length: number of characters of the progress bar
    :param msg: message displayed after the progress bar
    """
    if max_step:
        m = int(step * length / max_step)
        print(
            f"\r[{'='*m}{' '*(length-m)}]{100*step/max_step:7.2f}% {msg}",
            flush=True,
            end="",
        )
    else:
        print(f"\r[{'?'*length}]{' '*8} {msg}", flush=True, end="")


def texfile_to_symlink(tex_file: Path) -> Path:
    fname = tex_file.resolve().with_suffix(".tex")
    link = config.AUX_DIR
    for p in fname.parent.parts[3:]:
        link /= p
    link /= fname.name

    if link.exists():
        return link

    if not link.parent.exists():
        link.parent.mkdir(parents=True, exist_ok=True)

    link.symlink_to(fname)
    return link

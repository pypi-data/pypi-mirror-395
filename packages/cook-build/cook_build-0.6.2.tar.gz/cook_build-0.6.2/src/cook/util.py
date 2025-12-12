from __future__ import annotations
import contextlib
from datetime import datetime, timedelta
import hashlib
import inspect
import os
from pathlib import Path
import threading
from time import time
from typing import TYPE_CHECKING, Generator


if TYPE_CHECKING:
    from .task import Task


PathOrStr = Path | str


def evaluate_digest(path: PathOrStr, size=2**16, hasher: str = "sha1") -> bytes:
    hasher_instance = hashlib.new(hasher)
    path = Path(path)
    with path.open("rb") as fp:
        while chunk := fp.read(size):
            hasher_instance.update(chunk)
    return hasher_instance.digest()


def evaluate_hexdigest(path: PathOrStr, size=2**16, hasher: str = "sha1") -> str:
    return evaluate_digest(path, size, hasher).hex()


class Timer:
    def __init__(self):
        self.start = None

    def __enter__(self) -> Timer:
        self.start = time()
        return self

    def __exit__(self, *_) -> None:
        self.end = time()

    @property
    def duration(self):
        assert self.start is not None, "Timer has not started yet."
        assert self.end is not None, "Timer has not finished yet."
        return self.end - self.start


class CookError(Exception):
    pass


class FailedTaskError(Exception):
    def __init__(self, *args: object, task: "Task") -> None:
        super().__init__(*args)
        self.task = task


@contextlib.contextmanager
def working_directory(path: PathOrStr) -> Generator[Path]:
    path = Path(path)
    original = Path.cwd()
    try:
        os.chdir(path)
        yield path
    finally:
        os.chdir(original)


def get_location() -> tuple[Path, int]:
    """
    Get the first location in the call stack which is not part of the Cook package.

    Returns:
        Location as a tuple :code:`(filename, lineno)`.
    """
    frame = inspect.currentframe()
    assert frame is not None, "Could not fetch current frame."
    while frame.f_globals.get("__name__", "<unknown>").startswith("cook"):
        frame = frame.f_back
        assert frame is not None, "Could not fetch parent frame."
    return Path(frame.f_code.co_filename).resolve(), frame.f_lineno


class StopEvent(threading.Event):
    """
    Event used for stopping execution with a polling interval.
    """

    def __init__(self, interval: float = 1) -> None:
        super().__init__()
        self.interval = interval


def format_timedelta(delta: timedelta) -> str:
    """
    Format a time difference.
    """
    if delta.total_seconds() < 1:
        return str(delta)
    return str(delta).rsplit(".", 2)[0]


def format_datetime(dt: datetime) -> str:
    """
    Format a date-time.
    """
    return str(dt).rsplit(".", 2)[0]

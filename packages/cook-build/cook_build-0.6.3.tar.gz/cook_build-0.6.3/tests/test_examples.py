from cook.__main__ import __main__
from cook.util import working_directory
from pathlib import Path
import pytest


@pytest.mark.parametrize(
    "name, task",
    [
        ("hellomake", "say-hello"),
    ],
)
def test_example(name: str, task: str) -> None:
    with working_directory(f"examples/{name}"):
        # Remove the database file before testing for consistent execution.
        db = Path(".cook")
        if db.is_file():
            db.unlink()
        __main__(["exec", task])

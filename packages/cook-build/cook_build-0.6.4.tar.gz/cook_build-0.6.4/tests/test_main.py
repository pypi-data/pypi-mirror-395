import colorama
from cook.__main__ import __main__, Formatter
import logging
from pathlib import Path
import pytest
import shutil
import sys


RECIPES = Path(__file__).parent / "recipes"


def strip_colors(text: str) -> str:
    for ansi_codes in [colorama.Fore, colorama.Back]:
        for code in vars(ansi_codes).values():
            text = text.replace(code, "")
    return text


def test_blah_recipe_run(tmp_wd: Path) -> None:
    __main__(["--recipe", str(RECIPES / "blah.py"), "exec", "run"])


@pytest.mark.parametrize(
    "patterns, expected",
    [
        (["*"], ["create_source", "compile", "link", "run"]),
        (["c*"], ["create_source", "compile"]),
        (["--re", r"^\w{3}\w?$"], ["link", "run"]),
        (["run"], ["run"]),
    ],
)
def test_blah_recipe_ls(
    patterns: str, expected: list[str], capsys: pytest.CaptureFixture
) -> None:
    __main__(["--recipe", str(RECIPES / "blah.py"), "ls", *patterns])
    out, _ = capsys.readouterr()
    for task in expected:
        assert f"<task `{task}` @ " in strip_colors(out)


def test_blah_recipe_info(tmp_wd: Path, capsys: pytest.CaptureFixture) -> None:
    __main__(["--recipe", str(RECIPES / "blah.py"), "info", "link"])
    stdout, _ = capsys.readouterr()
    assert "status: stale" in strip_colors(stdout)

    __main__(["--recipe", str(RECIPES / "blah.py"), "exec", "link"])
    __main__(["--recipe", str(RECIPES / "blah.py"), "info", "link"])
    stdout, _ = capsys.readouterr()
    assert "status: current" in strip_colors(stdout)

    __main__(["--recipe", str(RECIPES / "blah.py"), "info", "run"])
    stdout, _ = capsys.readouterr()
    assert "targets: -" in strip_colors(stdout)

    # Check filtering based on stale/current status.
    __main__(["--recipe", str(RECIPES / "blah.py"), "info", "--stale"])
    stdout, _ = capsys.readouterr()
    assert "status: current" not in strip_colors(stdout)

    __main__(["--recipe", str(RECIPES / "blah.py"), "info", "--current"])
    stdout, _ = capsys.readouterr()
    assert "status: stale" not in strip_colors(stdout)

    __main__(["--recipe", str(RECIPES / "blah.py"), "info"])
    stdout, _ = capsys.readouterr()
    stdout = strip_colors(stdout)
    assert "status: stale" in stdout and "status: current" in stdout

    # Check only one can be given.
    with pytest.raises(ValueError, match="may be given at the same time"):
        __main__(["--recipe", str(RECIPES / "blah.py"), "info", "--current", "--stale"])


def test_blah_recipe_reset(tmp_wd: Path) -> None:
    __main__(["--recipe", str(RECIPES / "blah.py"), "reset", "link"])


def test_simple_dag_run(tmp_wd: Path) -> None:
    __main__(["--recipe", str(RECIPES / "simple_dag.py"), "exec", "3-1"])


@pytest.mark.parametrize(
    "patterns",
    [
        ["foo"],
        ["foo", "bar"],
        ["foo", "bar", "baz"],
        ["*hidden*"],
    ],
)
def test_simple_dag_no_matching_tasks(
    caplog: pytest.LogCaptureFixture, patterns: list[str]
) -> None:
    with pytest.raises(SystemExit), caplog.at_level("WARNING"):
        __main__(["--recipe", str(RECIPES / "simple_dag.py"), "ls", *patterns])
    assert "found no tasks matching" in caplog.text


def test_module_import(tmp_wd: Path) -> None:
    recipe = tmp_wd / "my_recipe.py"
    shutil.copy(RECIPES / "simple_dag.py", recipe)
    __main__(["-m", "my_recipe", "ls"])


def test_bad_recipe(caplog: pytest.LogCaptureFixture) -> None:
    with pytest.raises(SystemExit), caplog.at_level("ERROR"):
        __main__(["--recipe", str(RECIPES / "bad.py"), "exec", "false"])
    assert "failed to execute" in caplog.text


def test_custom_formatter() -> None:
    try:
        raise ValueError("terrible error")
    except ValueError:
        exc_info = sys.exc_info()
    formatter = Formatter()
    record = logging.LogRecord(
        "a", logging.ERROR, "b", 2, "foo", None, exc_info=exc_info
    )
    formatted = formatter.format(record)
    assert isinstance(formatted, str)
    assert "terrible error" in formatted


def test_terrible_recipe(caplog: pytest.LogCaptureFixture) -> None:
    with pytest.raises(SystemExit), caplog.at_level("CRITICAL"):
        __main__(["--recipe", str(RECIPES / "terrible.not-py"), "ls"])
    assert "failed to load recipe" in caplog.text


def test_dry_run_shows_tasks(tmp_wd: Path, caplog: pytest.LogCaptureFixture) -> None:
    """Dry-run should show what would execute without running tasks."""
    with caplog.at_level(logging.INFO):
        __main__(["--recipe", str(RECIPES / "blah.py"), "exec", "--dry-run", "run"])

    # Should show "would execute" messages
    assert "would execute <task `create_source`" in caplog.text
    assert "would execute <task `compile`" in caplog.text
    assert "would execute <task `link`" in caplog.text
    assert "would execute <task `run`" in caplog.text

    # Should show actions
    assert "action:" in caplog.text

    # Should NOT show "executing" or "completed" messages
    assert "executing <task" not in caplog.text
    assert "completed <task" not in caplog.text


def test_dry_run_does_not_create_files(tmp_wd: Path) -> None:
    """Dry-run should not create target files."""
    __main__(["--recipe", str(RECIPES / "blah.py"), "exec", "--dry-run", "link"])

    # Files should NOT be created
    assert not (tmp_wd / "blah.c").exists()
    assert not (tmp_wd / "blah.o").exists()
    assert not (tmp_wd / "blah").exists()


def test_dry_run_does_not_update_database(tmp_wd: Path) -> None:
    """Dry-run should not update the database."""
    # First, run normally to create database entry
    __main__(["--recipe", str(RECIPES / "blah.py"), "exec", "link"])

    # Check the database was updated
    __main__(["--recipe", str(RECIPES / "blah.py"), "info", "link"])

    # Reset the task
    __main__(["--recipe", str(RECIPES / "blah.py"), "reset", "link"])

    # Now dry-run should not update last_completed
    __main__(["--recipe", str(RECIPES / "blah.py"), "exec", "--dry-run", "link"])

    # Task should still be stale (database not updated)
    __main__(["--recipe", str(RECIPES / "blah.py"), "info", "--stale", "link"])


def test_dry_run_with_no_stale_tasks(
    tmp_wd: Path, caplog: pytest.LogCaptureFixture
) -> None:
    """Dry-run with no stale tasks should be silent."""
    # First, run normally
    __main__(["--recipe", str(RECIPES / "blah.py"), "exec", "link"])

    # Now dry-run with nothing stale
    caplog.clear()
    with caplog.at_level(logging.INFO):
        __main__(["--recipe", str(RECIPES / "blah.py"), "exec", "--dry-run", "link"])

    # Should be silent (no "would execute" messages)
    assert "would execute" not in caplog.text

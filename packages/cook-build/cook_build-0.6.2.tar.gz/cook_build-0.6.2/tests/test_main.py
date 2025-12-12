from cook.__main__ import __main__, Formatter
import logging
from pathlib import Path
import pytest
import shutil
import sys


RECIPES = Path(__file__).parent / "recipes"


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
        assert f"<task `{task}` @ " in pytest.shared.strip_colors(out)


def test_blah_recipe_info(tmp_wd: Path, capsys: pytest.CaptureFixture) -> None:
    __main__(["--recipe", str(RECIPES / "blah.py"), "info", "link"])
    stdout, _ = capsys.readouterr()
    assert "status: stale" in pytest.shared.strip_colors(stdout)

    __main__(["--recipe", str(RECIPES / "blah.py"), "exec", "link"])
    __main__(["--recipe", str(RECIPES / "blah.py"), "info", "link"])
    stdout, _ = capsys.readouterr()
    assert "status: current" in pytest.shared.strip_colors(stdout)

    __main__(["--recipe", str(RECIPES / "blah.py"), "info", "run"])
    stdout, _ = capsys.readouterr()
    assert "targets: -" in pytest.shared.strip_colors(stdout)

    # Check filtering based on stale/current status.
    __main__(["--recipe", str(RECIPES / "blah.py"), "info", "--stale"])
    stdout, _ = capsys.readouterr()
    assert "status: current" not in pytest.shared.strip_colors(stdout)

    __main__(["--recipe", str(RECIPES / "blah.py"), "info", "--current"])
    stdout, _ = capsys.readouterr()
    assert "status: stale" not in pytest.shared.strip_colors(stdout)

    __main__(["--recipe", str(RECIPES / "blah.py"), "info"])
    stdout, _ = capsys.readouterr()
    stdout = pytest.shared.strip_colors(stdout)
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

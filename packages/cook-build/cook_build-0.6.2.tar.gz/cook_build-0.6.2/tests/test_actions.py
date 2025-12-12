from cook.actions import CompositeAction, FunctionAction, ModuleAction, SubprocessAction
from cook.util import StopEvent, Timer
from pathlib import Path
import pytest
from subprocess import SubprocessError
import sys
import threading
import time
from unittest import mock


def test_shell_action(tmp_wd: Path) -> None:
    action = SubprocessAction("echo hello > world.txt", shell=True)
    action.execute(None)
    assert (tmp_wd / "world.txt").read_text().strip() == "hello"


def test_shell_action_timeout() -> None:
    stop = StopEvent(0.01)

    def target():
        time.sleep(1)
        stop.set()

    thread = threading.Thread(target=target)
    thread.start()

    action = SubprocessAction(["sleep", "2"])
    with Timer() as timer, pytest.raises(SubprocessError, match="SIGTERM"):
        action.execute(None, stop)

    assert 1 < timer.duration < 2
    assert not thread.is_alive()


def test_subprocess_action(tmp_wd: Path) -> None:
    action = SubprocessAction(["touch", "foo"])
    action.execute(None)
    assert (tmp_wd / "foo").is_file()


def test_bad_subprocess_action() -> None:
    action = SubprocessAction("false")
    with pytest.raises(SubprocessError):
        action.execute(None)


def test_subprocess_action_repr() -> None:
    assert repr(SubprocessAction("false")) == "SubprocessAction('false')"
    assert repr(SubprocessAction(["wait", "3"])) == "SubprocessAction('wait 3')"


def test_function_action() -> None:
    args = []

    action = FunctionAction(args.append)
    action.execute(42)

    assert args == [42]


def test_composite_action() -> None:
    args = []

    action = CompositeAction(FunctionAction(args.append), FunctionAction(args.append))
    action.execute("hello")
    assert args == ["hello", "hello"]


def test_module_action() -> None:
    action = ModuleAction([pytest, "-h"])
    action.execute(None)

    with pytest.raises(ValueError, match="shell execution"):
        ModuleAction([pytest], shell=True)

    with pytest.raises(ValueError, match="not be empty"):
        ModuleAction([])

    with pytest.raises(TypeError, match="must be a module"):
        ModuleAction([None])


def test_module_action_debug() -> None:
    with mock.patch("subprocess.Popen") as Popen:
        Popen().wait = mock.MagicMock(return_value=0)
        ModuleAction([pytest], debug=True).execute(None)
    Popen.assert_called_with([sys.executable, "-m", "pdb", "-m", "pytest"])

    with mock.patch("subprocess.Popen") as Popen:
        Popen().wait = mock.MagicMock(return_value=0)
        ModuleAction([pytest], debug=False).execute(None)
    Popen.assert_called_with([sys.executable, "-m", "pytest"])


def test_composite_digest() -> None:
    actions = [
        SubprocessAction("hello"),
        SubprocessAction(["foo", "bar"]),
    ]
    assert CompositeAction(*actions).hexdigest

    actions.append(FunctionAction(print))
    assert CompositeAction(*actions).hexdigest is None

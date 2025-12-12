from cook import Controller, Manager, Task
from cook.actions import Action, CompositeAction, FunctionAction, SubprocessAction
from cook.contexts import normalize_action, normalize_dependencies
from cook.controller import QUERIES
from cook.util import FailedTaskError, StopEvent, Timer
from datetime import datetime
from pathlib import Path
import pytest
import shutil
from sqlite3 import Connection
import threading
import time
from unittest.mock import patch


def touch(task: Task) -> None:
    for target in task.targets:
        target.write_text(target.name)


def test_controller_empty_task(m: Manager, conn: Connection) -> None:
    task = m.create_task("foo")
    c = Controller(m.resolve_dependencies(), conn)
    assert c.is_stale(task)
    assert c.resolve_stale_tasks() == {task}


def test_controller_missing_target(m: Manager, conn: Connection) -> None:
    task = m.create_task("foo", targets=["bar"])
    c = Controller(m.resolve_dependencies(), conn)
    assert c.is_stale(task)
    assert c.resolve_stale_tasks() == {task}


def test_controller_simple_file_deps(
    m: Manager, conn: Connection, tmp_wd: Path
) -> None:
    for path in ["input.txt", "output.txt"]:
        Path(path).write_text(path)
    with normalize_dependencies():
        task = m.create_task("foo", dependencies=["input.txt"], targets=["output.txt"])
    c = Controller(m.resolve_dependencies(), conn)

    # No entry in the database.
    assert c.is_stale(task)
    assert c.resolve_stale_tasks() == {task}

    # Up to date entry in the database.
    params = {
        "name": "foo",
        "digest": "80d4129af3d5366c3fcd26c498e143d9a199f7c4",
        "last_completed": None,
    }
    conn.execute(QUERIES["upsert_task_completed"], params)
    c = Controller(m.resolve_dependencies(), conn)
    assert not c.is_stale(task)

    # Wrong digest in the database.
    params = {"name": "foo", "digest": "-", "last_completed": None}
    conn.execute(QUERIES["upsert_task_completed"], params)
    c = Controller(m.resolve_dependencies(), conn)
    assert c.is_stale(task)


def test_controller_missing_input(m: Manager, conn: Connection) -> None:
    with normalize_dependencies():
        m.create_task("input", targets=["input.txt"], action=FunctionAction(touch))
        output = m.create_task(
            "output",
            targets=["output.txt"],
            action=FunctionAction(touch),
            dependencies=["input.txt"],
        )

    # Create the output.
    Path("output.txt").write_text("output.txt")
    params = {
        "name": "output",
        "digest": "80d4129af3d5366c3fcd26c498e143d9a199f7c4",
        "last_completed": None,
    }
    conn.execute(QUERIES["upsert_task_completed"], params)
    c = Controller(m.resolve_dependencies(), conn)
    assert c.is_stale(output) is True


def test_controller(m: Manager, conn: Connection) -> None:
    for filename in ["input1.txt", "input2.txt", "intermediate.txt", "output1.txt"]:
        Path(filename).write_text(filename)

    with normalize_dependencies():
        intermediate = m.create_task(
            "intermediate",
            dependencies=["input1.txt", "input2.txt"],
            targets=["intermediate.txt"],
            action=FunctionAction(touch),
        )
        output1 = m.create_task(
            "output1",
            dependencies=["intermediate.txt"],
            targets=["output1.txt"],
            action=FunctionAction(touch),
        )
        output2 = m.create_task(
            "output2",
            targets=["output2.txt"],
            action=FunctionAction(touch),
            dependencies=["intermediate.txt", "input2.txt", "output1.txt"],
        )
        special = m.create_task("special", dependencies=["intermediate.txt"])

    # We should get back all tasks at the beginning.
    c = Controller(m.resolve_dependencies(), conn)
    assert c.resolve_stale_tasks() == {intermediate, output1, output2, special}

    # Make sure we don't get any tasks that are upstream from what we request.
    c = Controller(m.resolve_dependencies(), conn)
    assert c.resolve_stale_tasks([output1]) == {intermediate, output1}

    # Execute tasks and check that they are no longer stale.
    c = Controller(m.resolve_dependencies(), conn)
    c.execute(output1)
    assert not c.resolve_stale_tasks([output1])

    # But the other ones are still stale.
    c = Controller(m.resolve_dependencies(), conn)
    assert c.resolve_stale_tasks() == {output2, special}

    # Execute the second output. The special task without outputs never disappears.
    c = Controller(m.resolve_dependencies(), conn)
    c.execute(output2)
    assert c.resolve_stale_tasks() == {special}


def test_target_not_created(m: Manager, conn: Connection) -> None:
    task = m.create_task("nothing", targets=["missing"])
    c = Controller(m.resolve_dependencies(), conn)
    with pytest.raises(FailedTaskError, match="did not create"):
        c.execute(task)


def test_failing_task(m: Manager, conn: Connection) -> None:
    def raise_exception(_) -> None:
        raise RuntimeError

    task = m.create_task("nothing", action=FunctionAction(raise_exception))
    c = Controller(m.resolve_dependencies(), conn)
    with pytest.raises(FailedTaskError):
        c.execute(task)
    (last_failed,) = conn.execute(
        "SELECT last_failed FROM tasks WHERE name = 'nothing'"
    ).fetchone()
    assert (datetime.now() - last_failed).total_seconds() < 1


def test_concurrency(m: Manager, conn: Connection) -> None:
    delay = 0.2
    num_tasks = 4

    tasks = [
        m.create_task(
            str(i),
            action=SubprocessAction(f"sleep {delay} && touch {i}.txt", shell=True),
            targets=[f"{i}.txt"],
        )
        for i in range(num_tasks)
    ]
    task = m.create_task("result", dependencies=[task.targets[0] for task in tasks])

    c = Controller(m.resolve_dependencies(), conn)
    with Timer() as timer:
        c.execute(task)
    assert timer.duration > num_tasks * delay

    c = Controller(m.resolve_dependencies(), conn)
    with Timer() as timer:
        c.execute(task, num_concurrent=num_tasks)
    assert timer.duration < 2 * delay


def test_digest_cache(m: Manager, conn: Connection, tmp_wd: Path) -> None:
    c = Controller(m.resolve_dependencies(), conn)
    shutil.copy(__file__, tmp_wd / "foo")
    with patch("cook.util.evaluate_digest", return_value=b"aaaa") as evaluate_digest:
        c._evaluate_path_hexdigest("foo")
        c._evaluate_path_hexdigest("foo")
    evaluate_digest.assert_called_once()


def test_skip_if_no_stale_tasks(m: Manager, conn: Connection, tmp_wd: Path) -> None:
    c = Controller(m, conn)
    c.execute([])


def test_tasks_are_executed(m: Manager, conn: Connection, tmp_wd: Path) -> None:
    with normalize_dependencies():
        m.create_task("base", targets=["base.txt"], action=FunctionAction(touch))
        task1 = m.create_task(
            "task1",
            targets=["task1.txt"],
            action=FunctionAction(touch),
            dependencies=["base.txt"],
        )
        task2 = m.create_task(
            "task2",
            targets=["task2.txt"],
            action=FunctionAction(touch),
            dependencies=["base.txt"],
        )
    # Execute the first task.
    c = Controller(m.resolve_dependencies(), conn)
    c.execute(task1)

    # Verify the second is still stale.
    c = Controller(m.resolve_dependencies(), conn)
    assert c.is_stale(task2)

    with open("task2.txt", "w"):
        pass

    c = Controller(m.resolve_dependencies(), conn)
    assert c.is_stale(task2)


def test_is_stale_called_once(m: Manager, conn: Connection) -> None:
    with normalize_dependencies():
        m.create_task("base", targets=["base.txt"], action=FunctionAction(touch))
        m.create_task(
            "task1",
            targets=["task1.txt"],
            action=FunctionAction(touch),
            dependencies=["base.txt"],
        )
        m.create_task(
            "task2",
            targets=["task2.txt"],
            action=FunctionAction(touch),
            dependencies=["base.txt"],
        )

    with patch(
        "cook.controller.Controller._is_self_stale", return_value=False
    ) as _is_self_stale:
        c = Controller(m.resolve_dependencies(), conn)
        [c.is_stale(list(c.dependencies)) for _ in range(7)]

    assert _is_self_stale.call_count == 3


def test_stop_long_running_subprocess(m: Manager, conn: Connection) -> None:
    task = m.create_task("sleep", action=SubprocessAction(["sleep", "60"]))
    c = Controller(m.resolve_dependencies(), conn)

    # Set the stop interval in one second.
    stop = StopEvent(0.01)

    def _target():
        time.sleep(1)
        stop.set()

    thread = threading.Thread(target=_target)
    thread.start()

    with (
        patch("cook.util.StopEvent", return_value=stop),
        Timer() as timer,
        pytest.raises(FailedTaskError, match="SIGTERM: 15"),
    ):
        c.execute(task)

    assert 1 < timer.duration and timer.duration < 2
    assert not thread.is_alive()


def test_set_stop_between_tasks(m: Manager, conn: Connection) -> None:
    calls = []

    def _action(task):
        calls.append(task)
        time.sleep(0.5)

    task1 = m.create_task("sleep1", action=FunctionAction(_action))
    task2 = m.create_task("sleep2", action=FunctionAction(_action))
    c = Controller(m.resolve_dependencies(), conn)

    # Set the stop interval shortly after dispatching the tasks.
    stop = StopEvent(10)

    def _target():
        time.sleep(0.3)
        stop.set()

    thread = threading.Thread(target=_target)
    thread.start()

    with patch("cook.util.StopEvent", return_value=stop), Timer() as timer:
        c.execute([task1, task2])

    assert 0.5 < timer.duration and timer.duration < 1
    assert not thread.is_alive()
    assert len(calls) == 1


def test_no_start_after_failure(m: Manager, conn: Connection) -> None:
    calls = []

    def _action(task):
        calls.append(task)
        raise ValueError

    task1 = m.create_task("sleep1", action=FunctionAction(_action))
    task2 = m.create_task("sleep2", action=FunctionAction(_action))
    c = Controller(m.resolve_dependencies(), conn)

    with pytest.raises(FailedTaskError):
        c.execute([task1, task2])

    assert len(calls) == 1


def test_digest_race(m: Manager, conn: Connection) -> None:
    with normalize_dependencies(), normalize_action():
        task1 = m.create_task("task1", action="echo foo > bar.txt", targets=["bar.txt"])
        task2 = m.create_task(
            "task2",
            action="sleep 1 && echo hello > world.txt",
            targets=["world.txt"],
            dependencies=["bar.txt"],
        )

    # Execute and ...
    c = Controller(m.resolve_dependencies(), conn)
    assert c.is_stale(task2)
    c.execute(task2)

    # ... ensure the task is no longer stale.
    c = Controller(m.resolve_dependencies(), conn)
    assert not c.is_stale(task2)

    # Modify the file and check the task is stale.
    c = Controller(m.resolve_dependencies(), conn)
    task1.targets[0].write_text("buzz")
    assert c.is_stale(task2)

    # Execute again but modify the dependency during execution.
    c = Controller(m.resolve_dependencies(), conn)

    def _target():
        time.sleep(0.5)
        task1.targets[0].write_text("fizz")

    thread = threading.Thread(target=_target)

    thread.start()
    c.execute(task2)
    assert not thread.is_alive()

    c = Controller(m.resolve_dependencies(), conn)
    assert c.is_stale(task2)


@pytest.mark.parametrize(
    "action1, action2",
    [
        (
            SubprocessAction("echo hello > b.txt", shell=True),
            SubprocessAction("echo fizz > b.txt", shell=True),
        ),
        (
            CompositeAction(
                SubprocessAction("echo a > b.txt", shell=True), SubprocessAction("true")
            ),
            CompositeAction(
                SubprocessAction("echo a > b.txt", shell=True),
                SubprocessAction("false"),
            ),
        ),
    ],
)
def test_action_digest(
    m: Manager, conn: Connection, action1: Action, action2: Action
) -> None:
    with normalize_dependencies():
        task = m.create_task("task", action=action1, targets=["b.txt"])

    # Execute and check stale status.
    Controller(m.resolve_dependencies(), conn).execute(task)
    assert not Controller(m.resolve_dependencies(), conn).is_stale(task)

    # Modify the task and check stale status.
    task.action = action2
    assert Controller(m.resolve_dependencies(), conn).is_stale(task)


def test_last_started_completed(m: Manager, conn: Connection) -> None:
    with normalize_action():
        task = m.create_task("task", action="sleep 1")
    Controller(m.resolve_dependencies(), conn).execute(task)
    ((last_started, last_completed),) = conn.execute(
        "SELECT last_started, last_completed FROM tasks"
    ).fetchall()
    delta = last_completed - last_started
    assert delta.total_seconds() > 1


# TODO: add tests to verify what happens when tasks are cancelled, e.g., by `KeyboardInterrupt`.

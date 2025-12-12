from cook import Manager
from cook.contexts import create_group, normalize_dependencies
from cook.util import CookError
import logging
from pathlib import Path
import pytest


def test_resolve_dependencies(m: Manager) -> None:
    Path("input1.txt").write_text("input1.txt")
    Path("input2.txt").write_text("input2.txt")

    with normalize_dependencies():
        intermediate = m.create_task(
            "intermediate",
            dependencies=["input1.txt", "input2.txt"],
            targets=["intermediate.txt"],
        )
        with create_group("outputs") as outputs:
            output1 = m.create_task(
                "output1", dependencies=["intermediate.txt"], targets=["output1.txt"]
            )
            output2 = m.create_task(
                "output2",
                targets=["output2.txt"],
                dependencies=["intermediate.txt", "input2.txt", "output1.txt"],
            )
        special = m.create_task("special", dependencies=["intermediate.txt"])
        dependent = m.create_task("dependent", task_dependencies=[output1])
    dependencies = m.resolve_dependencies()

    expected = {
        output1: {intermediate},
        output2: {intermediate, output1},
        special: {intermediate},
        dependent: {output1},
        outputs.task: {output1, output2},
    }
    for task, deps in expected.items():
        assert set(dependencies.successors(task)) == deps


def test_missing_file(m: Manager) -> None:
    with normalize_dependencies():
        m.create_task("has_missing_file_dependency", dependencies=["missing-file.txt"])
    with pytest.raises(FileNotFoundError, match="does not exist nor is"):
        m.resolve_dependencies()


def test_conflicting_targets(m: Manager) -> None:
    m.create_task("foo", targets=["bar"])
    m.create_task("baz", targets=["bar"])
    with pytest.raises(ValueError, match="both have target"):
        m.resolve_dependencies()


def test_symlink_targets(
    m: Manager, caplog: pytest.LogCaptureFixture, tmp_wd: Path
) -> None:
    file2 = Path("file2")
    file1 = Path("file1")
    m.create_task("task1", targets=[file1])
    m.create_task("task2", targets=[file2])
    file2.symlink_to("file3")

    with caplog.at_level(logging.WARNING):
        m.resolve_dependencies()
    assert "is a symlink" in caplog.messages[0]

    file2.unlink()
    file2.symlink_to(file1)
    with pytest.raises(ValueError, match="both have target"):
        m.resolve_dependencies()


def test_same_name(m: Manager) -> None:
    m.create_task("foo")
    with pytest.raises(ValueError, match="task with name 'foo' already exists"):
        m.create_task("foo")


def test_get_manager_instance() -> None:
    with pytest.raises(ValueError, match="no manager"):
        Manager.get_instance()
    with Manager() as m:
        assert Manager.get_instance() is m
    with pytest.raises(RuntimeError, match="unexpected manager"), Manager():
        Manager._INSTANCE = "asdf"
    with pytest.raises(ValueError, match="already active"), Manager(), Manager():
        pass


def test_dependency_graph(m: Manager) -> None:
    with normalize_dependencies():
        bar = m.create_task("bar", targets=["a"])
        foo = m.create_task("foo", dependencies=["a"])
    dependencies = m.resolve_dependencies()
    assert set(dependencies.successors(foo)) == {bar}
    assert set(dependencies.predecessors(bar)) == {foo}


def test_dependency_graph_cycle(m: Manager) -> None:
    with normalize_dependencies():
        m.create_task("bar", targets=["bar"], dependencies=["foo"])
        m.create_task("foo", targets=["foo"], dependencies=["bar"])
    with pytest.raises(CookError, match="contains a cycle"):
        m.resolve_dependencies()

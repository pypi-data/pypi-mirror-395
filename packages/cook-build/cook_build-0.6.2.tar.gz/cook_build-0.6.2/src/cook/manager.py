from __future__ import annotations
import logging
import networkx as nx
from pathlib import Path
from typing import TYPE_CHECKING
from . import task as task_
from . import util


if TYPE_CHECKING:
    from .actions import Action
    from .contexts import Context
    from .task import Task


LOGGER = logging.getLogger(__name__)


class Manager:
    """
    Task manager that captures the relationship between tasks, targets, and dependencies.
    """

    _INSTANCE: Manager | None = None

    def __init__(self, contexts: list["Context"] | None = None) -> None:
        self.contexts: list["Context"] = contexts or []
        self.tasks: dict[str, "Task"] = {}

    def __enter__(self) -> Manager:
        if Manager._INSTANCE:
            raise ValueError("another manager is already active")
        Manager._INSTANCE = self
        return self

    def __exit__(self, *_) -> None:
        if Manager._INSTANCE is not self:
            raise RuntimeError("exiting failed: unexpected manager")
        Manager._INSTANCE = None

    @staticmethod
    def get_instance() -> Manager:
        """
        Get the currently activate task manager.
        """
        if not Manager._INSTANCE:
            raise ValueError("no manager is active")
        return Manager._INSTANCE

    def create_task(self, name: str, **kwargs):
        """
        Create a task. See :func:`.create_task` for details.
        """
        try:
            if name in self.tasks:
                raise ValueError(f"task with name '{name}' already exists")
            task = task_.Task(name, **kwargs)
            for context in reversed(self.contexts):
                task = context.apply(task)
                if task is None:
                    raise ValueError(f"{context} did not return a task")
            self.tasks[name] = task
            return task
        except:  # noqa: 722
            filename, lineno = util.get_location()
            LOGGER.exception(
                "failed to create task with name '%s' at %s:%d", name, filename, lineno
            )
            raise

    def resolve_dependencies(self) -> nx.DiGraph:
        """
        Resolve dependencies between tasks.

        Returns:
            Directed graph of dependencies. Edges point *from* a task *to* others it depends on.
        """
        # Run over all the targets and dependencies to explore connections between tasks.
        task_by_target: dict[Path, "Task"] = {}
        tasks_by_file_dependency: dict[Path, set["Task"]] = {}
        dependencies: dict["Task", set["Task"]] = {}
        for task in self.tasks.values():
            if task.task_dependencies:
                dependencies[task] = set(task.task_dependencies)
            for path in task.targets:
                if path.is_symlink():
                    LOGGER.warning(
                        "target %s of %s is a symlink which may lead to unexpected "
                        "behavior",
                        path,
                        task,
                    )
                path = path.resolve()
                if other := task_by_target.get(path):
                    raise ValueError(
                        f"tasks {task} and {other} both have target {path}"
                    )
                task_by_target[path] = task
            for path in task.dependencies:
                path = Path(path).resolve()
                tasks_by_file_dependency.setdefault(path, set()).add(task)

        # Build a directed graph of dependencies based on files produced and consumed by tasks.
        for file_dependency, dependent_tasks in tasks_by_file_dependency.items():
            # This is the task that's going to generate the file we're after.
            if task := task_by_target.get(file_dependency):
                # For each of the dependent tasks, add the target task as a dependency.
                for dependent_task in dependent_tasks:
                    dependencies.setdefault(dependent_task, set()).add(task)
            elif not file_dependency.is_file():
                raise FileNotFoundError(
                    f"file {file_dependency} required by tasks {dependent_tasks} does not exist "
                    "nor is there a task to create it"
                )

        graph = nx.DiGraph()
        graph.add_nodes_from(self.tasks.values())
        graph.add_edges_from(
            (task, dep) for task, deps in dependencies.items() for dep in deps
        )

        try:
            cycle = nx.find_cycle(graph)
            raise util.CookError(f"dependency graph contains a cycle: {cycle}")
        except nx.NetworkXNoCycle:
            pass

        return graph


def create_task(
    name: str,
    *,
    action: "Action | str | None" = None,
    targets: list["Path"] | None = None,
    dependencies: list["Path"] | None = None,
    task_dependencies: list["Task"] | None = None,
    location: tuple[str, int] | None = None,
) -> "Task":
    """
    Create a new task.

    Args:
        name: Name of the new task.
        action: Action to execute or a string for shell commands.
        targets: Paths for files to be generated.
        dependencies: Paths to files on which this task depends.
        task_dependencies: Tasks which the new task explicitly depends on.
        location: Location at which the task was created as a tuple :code:`(filename, lineno)`
            (defaults to :func:`~.util.get_location`).

    Returns:
        New task.
    """
    return Manager.get_instance().create_task(
        name,
        action=action,
        targets=targets,
        dependencies=dependencies,
        location=location,
        task_dependencies=task_dependencies,
    )

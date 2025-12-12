r"""
Contexts
--------

:class:`.Context`\ s can modify the creation of :class:`~.task.Task`\ s and are activated using the
:code:`with` keyword. Builtin contexts handle the majority of Cook's task creation logic, such as
:class:`.normalize_dependencies` and :class:`.create_group`. The innermost context is applied first.

Custom contexts can be implemented by inheriting from :class:`.Context` and implementing the
:meth:`~.Context.apply` method which receives a :class:`~.task.Task` and must return a
:class:`~.task.Task`. For example, the following context converts all task names to uppercase.

.. doctest::

    >>> from cook import create_task
    >>> from cook.contexts import Context

    >>> class UpperCaseContext(Context):
    ...     def apply(self, task):
    ...         task.name = task.name.upper()
    ...         return task

    >>> # Using the contexts yields uppercase task names.
    >>> with UpperCaseContext():
    ...    create_task("foo")
    <task `FOO` @ ...>

    >>> # create_task behaves as usual after the context is exited.
    >>> create_task("bar")
    <task `bar` @ ...>
"""

from __future__ import annotations
from pathlib import Path
from types import ModuleType
from typing import Callable, TYPE_CHECKING
from . import actions
from . import manager as manager_
from . import task as task_
from . import util


if TYPE_CHECKING:
    from .manager import Manager
    from .task import Task


class Context:
    """
    Context that is applied to tasks when they are created.

    Args:
        manager: Manager to which the context is added.
    """

    def __init__(self, manager: "Manager | None" = None) -> None:
        self.manager = manager or manager_.Manager.get_instance()

    def __enter__(self) -> Context:
        self.manager.contexts.append(self)
        return self

    def __exit__(self, ex_type, ex_value, ex_traceback) -> None:
        if not self.manager.contexts:
            raise RuntimeError("exiting failed: no active contexts")
        if self.manager.contexts[-1] is not self:
            raise RuntimeError("exiting failed: unexpected context")
        self.manager.contexts.pop()

    def apply(self, task: "Task") -> "Task":
        """
        Apply the context to a task.

        Args:
            task: Task to modify.

        Returns:
            Modified task.
        """
        raise NotImplementedError


class FunctionContext(Context):
    """
    Context wrapping a function to modify or replace a task.

    Args:
        func: Function to call which must accept a :class:`~.task.Task` as its first argument and
            return a :class:`~.task.Task`.
        *args: Additional positional arguments.
        **kwargs: Keyword arguments.

    .. note::

        :code:`manager` is a reserved keyword for the constructor of all contexts and cannot be used
        as a keyword argument for the wrapped function.

    Example:

        .. doctest::

            >>> from cook import create_task
            >>> from cook.contexts import FunctionContext
            >>> from cook.task import Task

            >>> def repeat(task: Task, n: int) -> Task:
            ...     task.name = task.name * n
            ...     return task

            >>> with FunctionContext(repeat, 3):
            ...     create_task("baz")
            <task `bazbazbaz` @ ...>
    """

    def __init__(
        self,
        func: Callable[["Task"], Task],
        *args,
        manager: "Manager | None" = None,
        **kwargs,
    ) -> None:
        super().__init__(manager)
        self.func = func
        self.args = args or ()
        self.kwargs = kwargs or {}

    def apply(self, task: "Task") -> "Task":
        return self.func(task, *self.args, **self.kwargs)


class create_target_directories(Context):
    """
    Create parent directories for all targets before the task is executed.

    .. note::

        This context is active by default.
    """

    def apply(self, task: "Task") -> Task:
        for target in task.targets:
            name = f"_create_target_directories:{target.parent}"
            # No need to create a task if the parent already exists.
            if target.parent.is_dir():
                continue
            # Create a task if necessary.
            create = self.manager.tasks.get(name)
            if create is None:
                create = self.manager.create_task(
                    name,
                    action=actions.FunctionAction(
                        lambda _: target.parent.mkdir(parents=True, exist_ok=True)
                    ),
                )
            task.task_dependencies.append(create)
        return task


class normalize_action(Context):
    """
    Normalize actions of tasks.

    - If the action is a callable, it will be wrapped in a :class:`~.actions.FunctionAction`.
    - If the action is a string, it will be executed using a :class:`~.actions.SubprocessAction`
      with :code:`shell = True`.
    - If the action is a list of actions, a :class:`~.actions.CompositeAction` will be created.
    - If the action is a list and the first element is a module, a :class:`~.actions.ModuleAction`
      will be created. A subsequent elements ared passed to the module as strings on the command
      line.
    - If the action is any other list, it will be executed using a
      :class:`.actions.SubprocessAction` after converting elements to strings.

    .. note::

        This context is active by default.
    """

    def apply(self, task: "Task") -> "Task":
        if isinstance(task.action, Callable):
            task.action = actions.FunctionAction(task.action)
        elif isinstance(task.action, str):
            task.action = actions.SubprocessAction(task.action, shell=True)
        elif isinstance(task.action, list):
            if not task.action:
                raise ValueError("action must not be an empty list")
            if all(isinstance(x, actions.Action) for x in task.action):
                task.action = actions.CompositeAction(*task.action)
            elif isinstance(task.action[0], ModuleType):
                task.action = actions.ModuleAction(task.action)
            else:
                task.action = actions.SubprocessAction(list(map(str, task.action)))
        return task


class normalize_dependencies(Context):
    """
    Normalize dependencies of tasks.

    - If a dependency is a string, it will be converted to a :class:`~pathlib.Path`.
    - If a dependency is a :class:`~.task.Task` or :class:`.create_group`, it will be removed and
      added to the :code:`task_dependencies` of the task.
    - If a task dependency is a string, the corresponding task will be looked up by name.
    - If a task dependency is a group, it will be replaced by the corresponding meta task.

    .. note::

        This context is active by default.
    """

    def apply(self, task: "Task") -> "Task":
        # Move task and group dependencies to the task_dependencies if they appear in regular
        # dependencies.
        dependencies = []
        task_dependencies = task.task_dependencies
        for dependency in task.dependencies:
            if isinstance(dependency, (task_.Task, create_group)):
                task_dependencies.append(dependency)  # pyright: ignore[reportArgumentType]
            else:
                dependencies.append(dependency)
        task.dependencies = [Path(x) for x in dependencies]  # pyright: ignore[reportAttributeAccessIssue]

        # Unpack group dependencies and look up tasks by name.
        task_dependencies = []
        for other in task.task_dependencies:
            if isinstance(other, create_group):
                other = other.task
            elif isinstance(other, str):
                other = self.manager.tasks[other]
            task_dependencies.append(other)
        task.task_dependencies = task_dependencies

        return task


class create_group(Context):
    """
    Context for grouping tasks. A task with the same name will be created.

    Args:
        name: Name of the group.
        manager: Manager to which the context is added.
        location: Location at which the group was created as a tuple :code:`(filename, lineno)`
            (defaults to :func:`~.util.get_location`).

    Example:

        .. doctest::

            >>> from cook import create_task
            >>> from cook.contexts import create_group

            >>> with create_group("my_group") as my_group:
            ...     create_task("task1")
            ...     create_task("task2")
            <task `task1` @ ...>
            <task `task2` @ ...>

            >>> my_group
            <group `my_group` @ ... with 2 tasks>
    """

    def __init__(
        self,
        name: str,
        manager: "Manager | None" = None,
        location: tuple[str, int] | None = None,
    ) -> None:
        super().__init__(manager)
        self.name = name
        self.task: task_.Task | None = None
        self.location = location or util.get_location()

    def apply(self, task: "Task") -> "Task":
        # Skip if we're creating the task for the group itself to avoid infinite recursion.
        if task.name == self.name:
            return task
        if self.task is None:
            self.task = self.manager.create_task(self.name)
        self.task.task_dependencies.append(task)
        return task

    def __exit__(self, ex_type, ex_value, ex_traceback) -> None:
        super().__exit__(ex_type, ex_value, ex_traceback)
        # Raise an error if the group was successfully created but no tasks were added.
        has_dependents = self.task and self.task.task_dependencies
        if not has_dependents and not ex_value:
            raise RuntimeError(f"group `{self.name}` has no tasks")

    def __repr__(self) -> str:
        filename, lineno = self.location
        num_tasks = len(self.task.task_dependencies) if self.task else 0
        desc = "task" if num_tasks == 1 else "tasks"
        return f"<group `{self.name}` @ {filename}:{lineno} with {num_tasks} {desc}>"

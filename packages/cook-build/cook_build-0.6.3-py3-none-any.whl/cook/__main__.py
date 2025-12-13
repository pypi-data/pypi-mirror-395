import argparse
import colorama
from contextlib import closing
from datetime import datetime
import fnmatch
import importlib.util
import logging
import os
from pathlib import Path
import re
import sqlite3
import sys
import textwrap
from typing import Iterable

from .contexts import (
    create_target_directories,
    normalize_action,
    normalize_dependencies,
)
from .controller import Controller, QUERIES
from .manager import Manager
from .task import Task
from .util import FailedTaskError, format_datetime, format_timedelta


LOGGER = logging.getLogger("cook")


class NoMatchingTaskError(ValueError):
    def __init__(
        self, patterns: Iterable[re.Pattern | str], hidden_tasks_available: bool
    ) -> None:
        self.hidden_tasks_available = hidden_tasks_available
        formatted_patterns = [f"`{pattern}`" for pattern in patterns]
        if len(formatted_patterns) == 1:
            message = f"found no tasks matching pattern {formatted_patterns[0]}"
        else:
            *formatted_patterns, last = formatted_patterns
            message = (
                "found no tasks matching patterns "
                + ", ".join(formatted_patterns)
                + (", or " if len(formatted_patterns) > 1 else " or ")
                + last
            )
        if hidden_tasks_available:
            message = message + "; use --all or -a to include hidden tasks"
        super().__init__(message)


class Args:
    tasks: Iterable[re.Pattern | str]
    re: bool
    all: bool


class Command:
    """
    Abstract base class for commands.
    """

    NAME: str | None = None
    ALLOW_EMPTY_PATTERN: bool = False

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--re",
            "-r",
            action="store_true",
            help="use regular expressions for pattern matching instead of glob",
        )
        parser.add_argument(
            "--all",
            "-a",
            action="store_true",
            help="include tasks starting with `_` prefix",
        )
        parser.add_argument(
            "tasks",
            nargs="*" if self.ALLOW_EMPTY_PATTERN else "+",
            help="task or tasks to execute as regular expressions or glob patterns",
        )

    def execute(self, controller: Controller, args: argparse.Namespace) -> None:
        raise NotImplementedError

    def discover_tasks(self, controller: Controller, args: Args) -> list[Task]:
        task: Task
        tasks: list[Task] = []

        # Get tasks based on the pattern matching.
        if not args.tasks:
            tasks = list(controller.dependencies)
        else:
            for task in controller.dependencies:
                if args.re:
                    match = any(re.match(pattern, task.name) for pattern in args.tasks)
                else:
                    match = any(
                        fnmatch.fnmatch(task.name, pattern)  # pyright: ignore[reportArgumentType]
                        for pattern in args.tasks
                    )
                if match:
                    tasks.append(task)

        # Store whether any of the candidates are hidden by default.
        has_hidden_task = any(task.name.startswith("_") for task in tasks)

        # Filter out hidden tasks if desired unless the name is an exact match to a specified
        # pattern.
        if not args.all:
            tasks = [
                task
                for task in tasks
                if not task.name.startswith("_") or task.name in args.tasks
            ]

        if not tasks:
            raise NoMatchingTaskError(args.tasks, not args.all and has_hidden_task)
        return tasks


class ExecArgs(Args):
    jobs: int


class ExecCommand(Command):
    """
    Execute one or more tasks.
    """

    NAME = "exec"

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--jobs", "-j", help="number of concurrent jobs", type=int, default=1
        )
        super().configure_parser(parser)

    def execute(self, controller: Controller, args: ExecArgs) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        tasks = self.discover_tasks(controller, args)
        controller.execute(tasks, num_concurrent=args.jobs)


class LsArgs(Args):
    stale: bool
    current: bool


class LsCommand(Command):
    """
    List tasks.
    """

    NAME = "ls"
    ALLOW_EMPTY_PATTERN = True

    def configure_parser(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument(
            "--stale", "-s", action="store_true", help="only show stale tasks"
        )
        parser.add_argument(
            "--current", "-c", action="store_true", help="only show current tasks"
        )
        super().configure_parser(parser)

    def execute(self, controller: Controller, args: LsArgs) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        tasks = self.discover_tasks(controller, args)
        tasks = [
            task.format(colorama.Fore.YELLOW if is_stale else colorama.Fore.GREEN)
            for is_stale, task in zip(controller.is_stale(tasks), tasks)
        ]
        print("\n".join(tasks))

    def discover_tasks(self, controller: Controller, args: LsArgs) -> list[Task]:  # pyright: ignore[reportIncompatibleMethodOverride]
        if args.current and args.stale:
            raise ValueError(
                "only one of `--stale` and `--current` may be given at the same time"
            )
        tasks = super().discover_tasks(controller, args)
        if args.stale:
            return [
                task for stale, task in zip(controller.is_stale(tasks), tasks) if stale
            ]
        elif args.current:
            return [
                task
                for stale, task in zip(controller.is_stale(tasks), tasks)
                if not stale
            ]
        return tasks


class InfoCommand(LsCommand):
    """
    Display information about one or more tasks.
    """

    NAME = "info"

    def execute(self, controller: Controller, args: LsArgs) -> None:
        tasks = self.discover_tasks(controller, args)
        stales = controller.is_stale(tasks)

        stale_string = f"{colorama.Fore.YELLOW}stale{colorama.Fore.RESET}"
        current_string = f"{colorama.Fore.GREEN}current{colorama.Fore.RESET}"
        indent = "    "

        task: Task
        for stale, task in zip(stales, tasks):
            # Show the status.
            parts = [
                f"status: {stale_string if stale else current_string}",
            ]
            # Show when the task last completed and failed.
            last = controller.connection.execute(
                "SELECT last_started, last_completed, last_failed FROM tasks WHERE name = :name",
                {"name": task.name},
            ).fetchone() or (None, None, None)
            for key, value in zip(["started", "completed", "failed"], last):
                if value is None:
                    parts.append(f"last {key}: -")
                    continue
                parts.append(
                    f"last {key}: {format_timedelta(datetime.now() - value)} ago "
                    f"({format_datetime(value)})"
                )
            # Show dependencies and targets.
            task_dependencies = list(
                sorted(controller.dependencies.successors(task), key=lambda t: t.name)
            )
            task_dependencies = [
                dep.format(colorama.Fore.YELLOW if is_stale else colorama.Fore.GREEN)
                for is_stale, dep in zip(
                    controller.is_stale(task_dependencies), task_dependencies
                )
            ]
            items = [
                ("dependencies", task.dependencies),
                ("targets", task.targets),
                ("task_dependencies", task_dependencies),
            ]
            for key, value in items:
                value = "\n".join(map(str, value))
                if value:
                    parts.append(f"{key}:\n{textwrap.indent(value, indent)}")
                else:
                    parts.append(f"{key}: -")
            parts.append(f"action: {task.action if task.action else '-'}")

            parts = textwrap.indent("\n".join(parts), indent)
            print(f"{task}\n{parts}")


class ResetArgs(Args):
    pass


class ResetCommand(Command):
    """
    Reset the status of one or more tasks.
    """

    NAME = "reset"

    def execute(self, controller: Controller, args: ResetArgs) -> None:  # pyright: ignore[reportIncompatibleMethodOverride]
        tasks = self.discover_tasks(controller, args)
        controller.reset(*tasks)


class Formatter(logging.Formatter):
    COLOR_BY_LEVEL = {
        "DEBUG": colorama.Fore.MAGENTA,
        "INFO": colorama.Fore.BLUE,
        "WARNING": colorama.Fore.YELLOW,
        "ERROR": colorama.Fore.RED,
        "CRITICAL": colorama.Fore.WHITE + colorama.Back.RED,
    }
    RESET = colorama.Fore.RESET + colorama.Back.RESET

    def format(self, record: logging.LogRecord) -> str:
        color = self.COLOR_BY_LEVEL[record.levelname]
        formatted = f"{color}{record.levelname}{self.RESET}: {record.getMessage()}"
        if record.exc_info:
            formatted = f"{formatted}\n{self.formatException(record.exc_info)}"
        return formatted


def __main__(cli_args: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser("cook")
    parser.add_argument(
        "--recipe",
        help="file containing declarative recipe for tasks",
        default="recipe.py",
        type=Path,
    )
    parser.add_argument(
        "--module", "-m", help="module containing declarative recipe for tasks"
    )
    parser.add_argument(
        "--db", help="database for keeping track of assets", default=".cook"
    )
    parser.add_argument(
        "--log-level",
        help="log level",
        default="info",
        choices={"error", "warning", "info", "debug"},
    )
    subparsers = parser.add_subparsers()
    subparsers.required = True

    for command_cls in [ExecCommand, LsCommand, InfoCommand, ResetCommand]:
        subparser = subparsers.add_parser(command_cls.NAME, help=command_cls.__doc__)
        command = command_cls()
        command.configure_parser(subparser)
        subparser.set_defaults(command=command)

    args = parser.parse_args(cli_args)

    handler = logging.StreamHandler()
    handler.setFormatter(Formatter())
    logging.basicConfig(level=args.log_level.upper(), handlers=[handler])

    with Manager() as manager:
        try:
            manager.contexts.extend(
                [
                    create_target_directories(),
                    normalize_action(),
                    normalize_dependencies(),
                ]
            )
            if args.module:
                # Temporarily add the current working directory to the path.
                try:
                    sys.path.append(os.getcwd())
                    importlib.import_module(args.module)
                finally:
                    sys.path.pop()
            elif args.recipe.is_file():
                # Parse the recipe.
                spec = importlib.util.spec_from_file_location("recipe", args.recipe)
                assert spec, f"Could not load spec for '{args.recipe}'."
                recipe = importlib.util.module_from_spec(spec)
                assert spec.loader, f"Could not load recipe '{args.recipe}'."
                spec.loader.exec_module(recipe)
            else:  # pragma: no cover
                raise ValueError(
                    "recipe file or module must be specified; default recipe.py not "
                    "found"
                )
        except:  # noqa: E722
            LOGGER.fatal("failed to load recipe", exc_info=sys.exc_info())
            sys.exit(1)

    with closing(
        sqlite3.connect(args.db, detect_types=sqlite3.PARSE_DECLTYPES)
    ) as connection:
        _setup_schema(connection)
        controller = Controller(manager.resolve_dependencies(), connection)
        command: Command = args.command
        try:
            command.execute(controller, args)
        except KeyboardInterrupt:  # pragma: no cover
            LOGGER.warning("interrupted by user")
        except NoMatchingTaskError as ex:
            LOGGER.warning(ex)
            sys.exit(1)
        except FailedTaskError:
            sys.exit(1)


def _setup_schema(connection: sqlite3.Connection) -> None:
    connection.executescript(QUERIES["schema"])
    # Attempt to add the column which may not be present for cook versions <0.6.
    try:
        connection.execute("ALTER TABLE tasks ADD COLUMN last_started TIMESTAMP")
    except sqlite3.OperationalError as ex:
        if "duplicate column name" not in ex.args[0]:
            raise  # pragma: no cover


if __name__ == "__main__":
    __main__()

from __future__ import annotations
import colorama
from pathlib import Path
from typing import TYPE_CHECKING
from . import util


if TYPE_CHECKING:
    from .util import PathOrStr
    from .actions import Action


class Task:
    """
    Task to be executed.
    """

    def __init__(
        self,
        name: str,
        *,
        dependencies: list["PathOrStr"] | None = None,
        targets: list["PathOrStr"] | None = None,
        action: Action | None = None,
        task_dependencies: list[Task] | None = None,
        location: tuple[str, int] | None = None,
    ) -> None:
        self.name = name
        self.dependencies = dependencies or []
        self.targets = [Path(path) for path in (targets or [])]
        self.action = action
        self.task_dependencies = task_dependencies or []
        self.location = location or util.get_location()

    def execute(self, stop: util.StopEvent | None = None) -> None:
        if self.action:
            self.action.execute(self, stop)

    def __hash__(self) -> int:
        return hash(self.name)

    def format(self, color: str | None = None) -> str:
        name = self.name
        if color:
            name = f"{color}{name}{colorama.Fore.RESET}"
        filename, lineno = self.location
        return f"<task `{name}` @ {filename}:{lineno}>"

    def __repr__(self) -> str:
        return self.format()

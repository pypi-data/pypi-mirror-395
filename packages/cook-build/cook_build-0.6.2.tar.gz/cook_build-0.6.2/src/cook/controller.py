from dataclasses import dataclass
from datetime import datetime
import hashlib
import logging
import networkx as nx
from pathlib import Path
from queue import Empty, Queue
from sqlite3 import Connection
import sys
import threading
from types import TracebackType
from typing import (
    cast,
    Iterable,
    Literal,
    Sequence,
    TYPE_CHECKING,
    overload,
)
from . import util

if TYPE_CHECKING:
    from .task import Task


LOGGER = logging.getLogger(__name__)
QUERIES = {
    "schema": """
    -- Information about the status of tasks.
    CREATE TABLE IF NOT EXISTS "tasks" (
        "name" TEXT PRIMARY KEY,
        "digest" TEXT NOT NULL,
        "last_completed" TIMESTAMP,
        "last_failed" TIMESTAMP,
        "last_started" TIMESTAMP
    );

    -- Information about files so we can cache digests.
    CREATE TABLE IF NOT EXISTS "files" (
        "name" TEXT PRIMARY KEY,
        "digest" TEXT NOT NULL,
        "last_digested" TIMESTAMP NOT NULL
    );
    """,
    "select_task": """
        SELECT "digest"
        FROM "files"
        WHERE "name" = :name
    """,
    "upsert_task_completed": """
        INSERT INTO "tasks" ("name", "digest", "last_completed")
        VALUES (:name, :digest, :last_completed)
        ON CONFLICT ("name") DO UPDATE SET "digest" = :digest, last_completed = :last_completed
    """,
    "upsert_task_failed": """
        INSERT INTO "tasks" ("name", "digest", "last_failed")
        VALUES (:name, '__failed__', :last_failed)
        ON CONFLICT ("name") DO UPDATE SET "digest" = '__failed__', last_failed = :last_failed
    """,
    "upsert_task_started": """
        INSERT INTO "tasks" ("name", "digest", "last_started")
        VALUES (:name, '__pending__', :last_started)
        ON CONFLICT ("name") DO UPDATE SET "digest" = '__pending__', last_started = :last_started
    """,
    "upsert_file": """
        INSERT INTO "files" ("name", "digest", "last_digested")
        VALUES (:name, :digest, :last_digested)
        ON CONFLICT ("name") DO UPDATE SET "digest" = :digest, last_digested = :last_digested
    """,
    "select_file": """
        SELECT "digest", "last_digested"
        FROM "files"
        WHERE "name" = :name AND last_digested > :last_modified
    """,
}


@dataclass
class Event:
    kind: Literal["start", "complete", "fail"]
    task: "Task"
    timestamp: datetime
    exc_info: (
        tuple[type[BaseException], BaseException, TracebackType]
        | tuple[None, None, None]
    )
    digest: str | None


class Controller:
    """
    Controller to manage dependencies and execute tasks.
    """

    def __init__(self, dependencies: nx.DiGraph, connection: Connection) -> None:
        self.dependencies = dependencies
        self.connection = connection
        self._digest_cache: dict[Path, tuple[float, bytes]] = {}

    def resolve_stale_tasks(self, tasks: list["Task"] | None = None) -> set["Task"]:
        self.is_stale(tasks or list(self.dependencies))
        return {
            node for node, data in self.dependencies.nodes(True) if data.get("is_stale")
        }

    def _evaluate_task_hexdigest(self, task: "Task") -> str | None:
        """
        Evaluate the digest of a task by combining the digest of all its dependencies.
        """
        dependencies = []
        for dependency in task.dependencies:
            dependency = Path(dependency).resolve()
            if not dependency.is_file():
                LOGGER.debug("dependency %s of %s is missing", dependency, task)
                return None
            dependencies.append(dependency)

        hasher = hashlib.sha1()
        for dependency in sorted(dependencies):
            hasher.update(bytearray.fromhex(self._evaluate_path_hexdigest(dependency)))

        # Add the hash of the action.
        if task.action and (hexdigest := task.action.hexdigest):
            hasher.update(bytearray.fromhex(hexdigest))
        return hasher.hexdigest()

    def _evaluate_path_hexdigest(self, path: Path | str) -> str:
        """
        Get the digest of a file.
        """
        # Try to return the cached digest.
        path = Path(path)
        stat = path.stat()
        name = str(path.resolve())
        params = {"name": name, "last_modified": datetime.fromtimestamp(stat.st_mtime)}
        digest = self.connection.execute(QUERIES["select_file"], params).fetchone()
        if digest:
            return digest[0]

        # Evaluate a new digest and cache it.
        digest = util.evaluate_hexdigest(path)
        params = {
            "name": name,
            "last_digested": datetime.now(),
            "digest": digest,
        }
        self.connection.execute(QUERIES["upsert_file"], params)
        self.connection.commit()
        return digest

    @overload
    def is_stale(self, task: Sequence["Task"]) -> list[bool]: ...

    @overload
    def is_stale(self, task: "Task") -> bool: ...

    def is_stale(self, task: "Task | Sequence[Task]") -> bool | list[bool]:
        """
        Determine if one or more tasks are stale.

        Args:
            task: Task or tasks to check.

        Returns:
            If the task or tasks are stale.
        """
        if isinstance(task, Sequence):
            return [self.is_stale(x) for x in task]

        is_stale = self.dependencies.nodes[task].get("is_stale")
        if is_stale is not None:
            return is_stale
        is_stale = self._is_self_stale(task)
        successors = list(self.dependencies.successors(task))
        if successors:
            is_stale |= any(self.is_stale(successors))
        self.dependencies.nodes[task]["is_stale"] = is_stale
        return is_stale

    def _is_self_stale(self, task: "Task") -> bool:
        """
        Determine whether a task is *itself* stale irrespective of other tasks it may depend on.

        Args:
            task: Task to check.

        Returns:
            If the task is stale, ignoring dependencies.
        """
        # If there are no targets or the targets are missing, the task is stale.
        if not task.targets:
            LOGGER.debug("%s is stale because it has no targets", task)
            return True
        for target in task.targets:
            if not target.is_file():
                LOGGER.debug(
                    "%s is stale because its target `%s` is missing", task, target
                )
                return True

        # If there is no digest in the database, the task is stale.
        cached_digest = self.connection.execute(
            "SELECT digest FROM tasks WHERE name = :name", {"name": task.name}
        ).fetchone()
        if cached_digest is None:
            LOGGER.debug("%s is stale because it does not have a hash entry", task)
            return True

        # If one of the dependencies is missing, the task is stale.
        current_digest = self._evaluate_task_hexdigest(task)
        if current_digest is None:
            LOGGER.debug("%s is stale because one of its dependencies is missing", task)

        # If the digest has changed, the task is stale.
        (cached_digest,) = cached_digest
        if current_digest != cached_digest:
            LOGGER.debug(
                "%s is stale because one of its dependencies has changed (cached digest: "
                "%s, current digest: %s)",
                task,
                cached_digest,
                current_digest,
            )
            return True

        LOGGER.debug("%s is up to date", task)
        return False

    def execute(
        self, tasks: "Task | list[Task]", num_concurrent: int = 1, interval: float = 1
    ) -> None:
        """
        Execute one or more tasks.

        Args:
            tasks: Tasks to execute.
            num_concurrent: Number of concurrent threads to run.
        """
        if not isinstance(tasks, Sequence):
            tasks = [tasks]
        if not any(self.is_stale(tasks)):
            return

        # Start the worker threads.
        threads: list[threading.Thread] = []
        input_queue = Queue()
        output_queue = Queue[Event]()
        stop = util.StopEvent(interval)
        for i in range(num_concurrent):
            thread = threading.Thread(
                target=self._target,
                name=f"cook-thread-{i}",
                args=(stop, input_queue, output_queue),
                daemon=True,
            )
            thread.start()
            threads.append(thread)

        # Get the subgraph of stale nodes.
        stale_nodes = [
            node
            for node, data in self.dependencies.nodes.data()
            if data.get("is_stale")
        ]
        dependencies = cast(nx.DiGraph, self.dependencies.subgraph(stale_nodes).copy())

        # Initialize the input queue with leaf nodes.
        for node, out_degree in cast(Iterable, dependencies.out_degree()):
            if out_degree == 0:
                input_queue.put((node, self._evaluate_task_hexdigest(node)))

        try:
            while dependencies.number_of_nodes():
                # Try to get the next item in the queue, continuing if there's nothing available.
                try:
                    event = output_queue.get(timeout=interval)
                except Empty:  # pragma: no cover
                    continue

                assert event is not None, "output queue returned `None`; this is a bug"

                # Unpack the results.
                if event.kind == "fail":
                    # Update the status in the database.
                    params = {
                        "name": event.task.name,
                        "last_failed": event.timestamp,
                    }
                    self.connection.execute(QUERIES["upsert_task_failed"], params)
                    self.connection.commit()
                    ex = event.exc_info[1]
                    raise util.FailedTaskError(ex, task=event.task) from ex
                elif event.kind == "complete":
                    # Update the status in the database.
                    params = {
                        "name": event.task.name,
                        "digest": event.digest,
                        "last_completed": event.timestamp,
                    }
                    self.connection.execute(QUERIES["upsert_task_completed"], params)
                    self.connection.commit()
                elif event.kind == "start":
                    params = {
                        "name": event.task.name,
                        "last_started": event.timestamp,
                    }
                    self.connection.execute(QUERIES["upsert_task_started"], params)
                    self.connection.commit()
                    continue
                else:
                    raise ValueError(event)  # pragma: no cover

                # Check if the stop event is set and abort if so.
                if stop.is_set():
                    break

                # Add tasks that are now leaf nodes to the tree.
                predecessors = list(dependencies.predecessors(event.task))
                dependencies.remove_node(event.task)
                self.dependencies.add_node(event.task, is_stale=False)
                for node, out_degree in cast(
                    Iterable, dependencies.out_degree(predecessors)
                ):
                    if out_degree == 0:
                        input_queue.put((node, self._evaluate_task_hexdigest(node)))
        finally:
            # Set the stop event and add "None" to the queue so the workers stop waiting.
            LOGGER.debug(
                "set stop event for threads: %s", [thread.name for thread in threads]
            )
            stop.set()
            for thread in threads:
                input_queue.put((None, None))

            # Shut down the worker threads.
            for thread in threads:
                thread.join(3 * stop.interval)
                if thread.is_alive():  # pragma: no cover
                    raise RuntimeError(f"thread {thread} failed to join")

    def _target(
        self, stop: util.StopEvent, input_queue: Queue, output_queue: Queue
    ) -> None:
        LOGGER.debug(f"started thread `{threading.current_thread().name}`")
        while not stop.is_set():
            try:
                task: "Task"
                digest: str
                task, digest = input_queue.get(timeout=stop.interval)
            except Empty:  # pragma: no cover
                # It's unlikely there's nothing on the queue, but let's handle it anyway.
                continue
            # Check the stop event before executing the task; it may have been set while we were
            # waiting for the next task in the queue.
            if stop.is_set():
                break

            assert task is not None, "input queue returned `None`; this is a bug"

            start = datetime.now()
            try:
                # Execute the task.
                LOGGER.log(
                    logging.DEBUG if task.name.startswith("_") else logging.INFO,
                    "executing %s ...",
                    task,
                )
                output_queue.put(
                    Event(
                        kind="start",
                        task=task,
                        digest=None,
                        timestamp=start,
                        exc_info=(None, None, None),
                    )
                )
                task.execute(stop)

                # Check that all targets were created.
                for target in task.targets:
                    if not target.is_file():
                        raise FileNotFoundError(
                            f"task {task} did not create target {target}"
                        )
                    LOGGER.debug("%s created `%s`", task, target)

                # Add the result to the output queue and report success.
                output_queue.put(
                    Event(
                        kind="complete",
                        task=task,
                        digest=digest,
                        timestamp=datetime.now(),
                        exc_info=(None, None, None),
                    )
                )
                delta = util.format_timedelta(datetime.now() - start)
                LOGGER.log(
                    logging.DEBUG if task.name.startswith("_") else logging.INFO,
                    "completed %s in %s",
                    task,
                    delta,
                )
            except:  # noqa: E722
                exc_info = sys.exc_info()
                delta = util.format_timedelta(datetime.now() - start)
                LOGGER.exception(
                    "failed to execute %s after %s", task, delta, exc_info=exc_info
                )
                stop.set()
                output_queue.put(
                    Event(
                        kind="fail",
                        task=task,
                        digest=digest,
                        timestamp=datetime.now(),
                        exc_info=sys.exc_info(),
                    )
                )

        # Put anything on the queue in case the parent is waiting.
        LOGGER.debug(f"exiting thread `{threading.current_thread().name}`")
        output_queue.put(None)

    def reset(self, *tasks: "Task") -> None:
        # TODO: add tests for resetting.
        params = [{"name": task.name} for task in tasks]
        cursor = self.connection.executemany(
            "UPDATE tasks SET digest = '__reset__' WHERE name = :name", params
        )
        self.connection.commit()
        n_reset = cursor.rowcount
        LOGGER.info("reset %d %s", n_reset, "task" if n_reset == 1 else "tasks")

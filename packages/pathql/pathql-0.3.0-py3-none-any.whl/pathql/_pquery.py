"""tpath.pquery — path querying helpers for TPath objects.

This module provides a lightweight, SQL-like fluent query builder for
filesystem traversal and filtering of :class:`~tpath._core.TPath` objects.

Primary public API:
    - :class:`PQuery` - fluent builder with methods such as ``from_``,
        ``where``, ``distinct``, ``take``, ``order_by``, ``paginate``, ``files``,
        ``select``, and ``map_parallel``.
    - :func:`pquery` - convenience constructor returning a :class:`PQuery`.
    - :class:`MapResult` - dataclass returned by :meth:`PQuery.map_parallel`.

The :meth:`PQuery.map_parallel` method runs a single producer (crawler)
thread and one or more consumer worker threads and yields :class:`MapResult`
records for each processed file. For details and behavior (exception
policies, shutdown semantics, and example usage) see that method's docstring.

Example:

        from tpath.pquery import pquery

        # Stream file names in parallel (4 workers)
        for res in pquery(from_="src").where(lambda p: p.suffix == ".py").map_parallel(lambda p: p.name, workers=4):
                if res.success:
                        print(res.data)

"""

from __future__ import annotations

import logging
import os
import queue
import threading
import time
from collections.abc import Callable, Iterable, Iterator, Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeAlias, cast

from tpath import TPath

from ._stats import PQueryStats

# Type aliases for better readability and IDE support
PathLike: TypeAlias = str | Path | TPath
PathSequence: TypeAlias = Sequence[PathLike]
# PathInput represents what from_() accepts: single paths or sequences of paths
PathInput: TypeAlias = PathLike | PathSequence


def distinct_paths(paths: Iterable[TPath]) -> Iterator[TPath]:
    seen: set[TPath] = set()
    for path in paths:
        if path not in seen:
            seen.add(path)
            yield path


@dataclass
class MapResult:
    """Result record returned by PQuery.map_parallel for each processed file.

    Attributes:
        path: The TPath that was processed
        execution_time: Seconds spent executing the mapping function
        success: True when func completed without raising
        exception: The exception instance if the call failed, otherwise None
        data: The value returned by func when success is True, otherwise None
    """

    path: TPath
    execution_time: float
    success: bool
    exception: Exception | None = None
    data: Any | None = None


class PQuery:
    """
    A path query builder that provides a fluent API for file filtering.

    Similar to pathql but using lambda expressions for flexible filtering.
    """

    # Class-level logger (can be set globally)
    _logger: logging.Logger | None = None
    # Class-level log frequency
    _log_every_n: int = 1000

    def __init__(
        self,
        *,
        from_: PathLike | None = None,
        recursive: bool | None = None,
        where: Callable[[TPath], bool] | None = None,
        logger: logging.Logger | None = None,
        log_every_n: int | None = None,
    ):
        """
        Initialize a path query with optional parameters.

        Args:
            from_: Starting directory path (defaults to current directory '.' when query runs)
            recursive: Whether to search subdirectories recursively (defaults to True when query runs)
            where: Initial filter condition (defaults to files only when query runs: lambda p: p.is_file())

        Examples:
            PQuery()                                    # Uses defaults when executed
            PQuery(from_="/logs")                       # /logs dir, other defaults when executed
            PQuery(recursive=False)                     # Current dir, non-recursive, files only
            PQuery(where=lambda p: p.suffix == ".py")  # Current dir, recursive, Python files
            PQuery(from_="/src", recursive=False, where=lambda p: p.size.mb > 1)  # /src, non-recursive, large files
        """
        # Instance variables
        self.start_paths: list[TPath] = []
        self.is_recursive: bool = True
        self._query_func: list[Callable[[TPath], bool]] = []
        self._distinct: bool = False
        self._stats: PQueryStats = PQueryStats()
        # Instance-level logger and log frequency
        self._logger: logging.Logger | None = logger
        self._log_every_n: int = (
            log_every_n if log_every_n is not None else type(self)._log_every_n
        )
        # Store init parameters for later use
        self._init_from = from_
        self._init_recursive = recursive
        self._init_where = where

    def from_(self, *, paths: PathInput) -> PQuery:
        """
        Set or add starting directory paths.

        This builder method configures the starting paths for the query.

        Args:
            paths: One or more starting directory paths, or sequences of paths.
                   Each argument can be a single path (str, Path, TPath) or a
                   sequence of paths (list, tuple, etc.)

        Returns:
            PQuery: This PQuery instance for method chaining

        Examples:
            PQuery().from_(paths="/logs").where(lambda p: p.size.gb < 1)
            PQuery().from_(paths=["/logs", "/var/log", "/opt/app/logs"]).where(lambda p: p.suffix == ".log")
            PQuery().from_(paths=path_list).where(lambda p: p.suffix == ".txt")  # list of paths
            PQuery().from_(paths=["/logs", path_list, "/var/log"]).files()  # mixed individual and list
        """
        if not paths:
            raise ValueError("At least one path must be provided")

        # Flatten any sequences in the arguments with proper type handling
        flattened_paths: list[PathLike] = []
        for path_input in paths if isinstance(paths, list | tuple) else [paths]:
            if isinstance(path_input, str | Path | TPath):
                # Single path
                flattened_paths.append(path_input)
            elif hasattr(path_input, "__iter__") and not isinstance(
                path_input, str | bytes
            ):
                # Sequence of paths (list, tuple, etc.) - but not string/bytes
                flattened_paths.extend(path_input)  # type: ignore[arg-type]
            else:
                # Fallback: treat as single path
                flattened_paths.append(path_input)  # type: ignore[arg-type]

        if not flattened_paths:
            raise ValueError("At least one path must be provided")

        # Apply defaults if start_paths is empty
        if not self.start_paths:
            default_path = self._init_from or "."
            self.start_paths = [TPath(default_path)]

        # If this is the first call and we still have the default '.', replace it
        if len(self.start_paths) == 1 and str(self.start_paths[0]) == ".":
            self.start_paths = [
                path if isinstance(path, TPath) else TPath(path)
                for path in flattened_paths
            ]
        else:
            self.start_paths.extend(
                path if isinstance(path, TPath) else TPath(path)
                for path in flattened_paths
            )
        return self

    def take(
        self,
        limit: int,
        key: Callable[[TPath], Any] | None = None,
        reverse: bool = True,
        continue_on_exc: bool = True,
    ) -> list[TPath]:
        """
        Take the top limit files, optionally ordered by a key function.

        This terminal method executes the configured query and returns up to limit
        files, optionally sorted by a key function. The fluent chain ends here.

        This method is optimized for getting the "best" limit files without sorting all results.
        Uses heapq.nlargest/nsmallest for O(n log k) performance when key is provided.

        Args:
            limit: Number of files to return
            key: Optional function to extract comparison key from TPath
                Can return a single value or tuple for multi-column sorting
            reverse: If True (default), return largest/newest items
                    If False, return smallest/oldest items
            continue_on_exc: If True, continue processing on exceptions. If False, raise.

        Returns:
            list[TPath]: Up to limit files matching the criteria

        Examples:
            # Get 10 largest files (most common case)
            # largest = query.take(10, key=lambda p: p.size.bytes)

            # Get 5 oldest files
            # oldest = query.take(5, key=lambda p: p.mtime.timestamp, reverse=False)

            # Multi-column sort: largest files, then most recent
            # best = query.take(10, key=lambda p: (p.size.bytes, p.mtime.timestamp))

            # Just any 10 files (no ordering)
            # any_files = query.take(10)
        """
        import heapq  # noqa: F401 # Lazy import for performance optimization

        def safe_iter():
            for path in self._distinct_iter_files():
                try:
                    yield path
                except Exception:
                    if not continue_on_exc:
                        raise

        if key is None:
            result: list[TPath] = []
            for i, path in enumerate(safe_iter()):
                if i >= limit:
                    break
                result.append(path)
            return result
        if reverse:
            return heapq.nlargest(limit, safe_iter(), key=key)
        else:
            return heapq.nsmallest(limit, safe_iter(), key=key)

    def distinct(self) -> PQuery:
        """
        Enable deduplication of results at the generator level.

        This builder method sets up state for deduplication during file iteration.
        The actual duplicate removal occurs when files are yielded from the iterator.

        Returns:
            PQuery: This PQuery instance for method chaining

        Example:
            query = pquery(from_="./src").where(lambda p: p.suffix == ".py").distinct().take(10)

        Performance Notes:
            - Uses O(k) memory where k = number of unique files processed
            - Deduplication happens lazily during iteration, not upfront
        """
        self._distinct = True
        return self

    def _distinct_iter_files(self, continue_on_exc: bool = True) -> Iterator[TPath]:
        """Internal method that wraps _iter_files with deduplication if distinct is enabled."""
        base_iter = self._iter_files(continue_on_exc=continue_on_exc)
        if self._distinct:
            return distinct_paths(base_iter)
        return base_iter

    def recursive(self, recursive: bool = True) -> PQuery:
        """
        Enable recursive traversal of directories.

        This builder method configures the query to traverse subdirectories
        when searching for files, rather than only searching the immediate directory.

        Args:
            recursive: Whether to search subdirectories recursively

        Returns:
            PQuery: This PQuery instance for method chaining

        Example:
            query = pquery(from_="./src").recursive().where(lambda p: p.suffix == ".py")
        """

        # Override both the working state and the init parameter
        self.is_recursive = recursive
        self._init_recursive = (
            recursive  # Ensure this takes precedence over constructor default
        )
        return self

    def where(
        self, condition: Callable[[TPath], bool] | Iterable[Callable[[TPath], bool]]
    ) -> PQuery:
        """
        Add a query condition using a lambda expression.

        This builder method adds filtering conditions to the query.
        Multiple where() calls are combined with AND logic.

        Args:
            condition: Lambda function that takes a TPath and returns bool, or a sequence
                   of such functions (list, tuple, etc.)

        Returns:
            PQuery: This PQuery instance for method chaining

        Examples:
            # Multiple separate where() calls
            pquery(from_="/logs").where(lambda p: p.size.gb < 1).where(lambda p: p.age.days < 7)

            # Conditional sequencing of where clauses
            q = pquery(from_="/logs")
            q = q.where(lambda p: p.size > 100)
            if check_age:
                q = q.where(lambda p: p.age.year > 1)

            # Single where() call with list of conditions
            pquery(from_="/logs").where([lambda p: p.suffix == ".txt", lambda p: p.size.mb > 10])

            # Mixed approach
            pquery(from_="/logs").where(lambda p: p.age.days < 7).where([lambda p: p.suffix == ".txt", lambda p: p.size.mb > 10])

        Note:
            Multiple where() calls are combined with AND logic. All conditions must be true
            for a file to match.
        """
        import inspect

        def is_query_func(f: object) -> bool:
            # Accept only Callable[[TPath], bool] (runtime check: one positional arg)
            if not callable(f):
                return False
            sig = inspect.signature(f)
            params = list(sig.parameters.values())
            # Accept only functions with one positional argument
            return len(params) == 1 and (
                params[0].kind
                in (
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    inspect.Parameter.POSITIONAL_ONLY,
                )
            )

        if isinstance(condition, Iterable) and not isinstance(condition, str | bytes):
            for func in condition:
                if not callable(func):  # type: ignore[arg-type]
                    raise TypeError(
                        f"All items in condition sequence must be callable with one positional arg, got {type(func)}"
                    )  # type: ignore[arg-type]
                if not is_query_func(func):  # type: ignore[arg-type]
                    raise TypeError(
                        f"All items in condition sequence must be callable with one positional arg, got {type(func)}"
                    )  # type: ignore[arg-type]
                self._query_func.append(cast(Callable[[TPath], bool], func))
        elif is_query_func(condition):
            self._query_func.append(cast(Callable[[TPath], bool], condition))
        else:
            raise TypeError(
                f"where() expects a callable or iterable of callables, got {type(condition)}"
            )
        return self

    def _matches_query(self, path: TPath) -> bool:
        """Check if a path matches all query conditions (AND logic)."""
        if not self._query_func:
            return True
        return all(func(path) for func in self._query_func)

    def _iter_files(self, continue_on_exc: bool = True) -> Iterator[TPath]:
        """Internal method to iterate over all matching files using os.scandir, with live stats tracking."""

        # Convert TPath objects to string paths for stats
        self._stats.set_paths([str(p) for p in self.start_paths])
        # start_time is set by the dataclass

        logger = getattr(type(self), "_logger", None)
        if logger:
            logger.info(
                f"PQuery started: paths={self._stats.paths}, recursive={self.is_recursive}"
            )

        if not self.start_paths:
            default_path = self._init_from or "."
            self.start_paths = [TPath(default_path)]

        self.is_recursive = (
            self._init_recursive if self._init_recursive is not None else True
        )

        if not self._query_func:
            if self._init_where is not None:
                self._query_func = [self._init_where]
            else:
                self._query_func = [lambda p: p.is_file()]

        # Stack-based traversal: process files first, push dirs onto stack
        for start_path in self.start_paths:
            if not start_path.exists():
                continue

            # If start_path is a file, yield it directly
            if not start_path.is_dir():
                try:
                    matched = self._matches_query(start_path)
                    if matched:
                        self._stats.add_matched_file(str(start_path))
                        yield start_path
                    else:
                        self._stats.add_unmatched_file(str(start_path))

                    # Log progress after processing the file
                    if logger and self._stats.files_scanned % 1000 == 0:
                        logger.info(f"Progress: {self._stats.log_msg()}")
                except (OSError, PermissionError) as exc:
                    self._stats.add_error(f"{start_path}: {exc!r}")
                    logger = getattr(type(self), "_logger", None)
                    if logger:
                        logger.warning(f"Exception on {start_path}: {exc!r}")
                    if not continue_on_exc:
                        raise
                continue

            # Stack for directories to process
            stack = [Path(str(start_path))]
            while stack:
                current_dir = stack.pop()
                try:
                    with os.scandir(current_dir) as dir_entries:
                        dirs: list[Path] = []
                        for entry in dir_entries:
                            try:
                                if entry.is_file(follow_symlinks=False):
                                    tpath = TPath(entry.path, dir_entry=entry)
                                    if self._matches_query(tpath):
                                        self._stats.add_matched_file(entry.path)
                                        yield tpath
                                    else:
                                        self._stats.add_unmatched_file(entry.path)

                                # Check logging after processing each entry (file or dir)
                                if logger and self._stats.files_scanned % 1000 == 0:
                                    logger.info(f"Progress: {self._stats.log_msg()}")

                                # Add directories to stack if recursive
                                if self.is_recursive and entry.is_dir(
                                    follow_symlinks=False
                                ):
                                    dirs.append(Path(entry.path))
                            except (OSError, PermissionError) as exc:
                                self._stats.add_error(f"{entry.path}: {exc!r}")
                                if logger:
                                    logger.warning(
                                        f"Exception on {entry.path}: {exc!r}"
                                    )
                                if not continue_on_exc:
                                    raise
                                continue
                        # Push directories onto stack after yielding files
                        stack.extend(dirs)
                except (OSError, PermissionError) as exc:
                    self._stats.add_error(f"{current_dir}: {exc!r}")
                    if logger:
                        logger.warning(f"Exception on {current_dir}: {exc!r}")
                    if not continue_on_exc:
                        raise
                    continue
        # Final log at completion
        if logger:
            logger.info(f"PQuery completed: {self._stats.log_msg()}")

    def files(self, continue_on_exc: bool = True) -> Iterator[TPath]:
        """
        Execute the query and return matching files as an iterator.

        This terminal method executes the configured query and returns an iterator
        over the matching files. The fluent chain ends here.

        Args:
            continue_on_exc: If True, continue processing on exceptions. If False, raise.

        Returns:
            Iterator[TPath]: Iterator of matching file paths

        Examples:
            # Stream processing (memory efficient)
            for file in pquery(from_="/logs").where(lambda p: p.age.hours < 24).files():
                process_file(file)

            # Materialize when needed
            all_files = list(pquery(from_=paths).distinct().files())
        """

        def gen():
            for path in self._distinct_iter_files(continue_on_exc=continue_on_exc):
                try:
                    yield path
                except Exception as exc:
                    logger = self._logger or type(self)._logger
                    if logger:
                        logger.error(
                            f"PQuery.files caught exception: {exc!r}, continue_on_exc={continue_on_exc}"
                        )
                    if not continue_on_exc:
                        raise

        return gen()

    def select(
        self, field: Callable[[TPath], Any], continue_on_exc: bool = True
    ) -> Iterator[Any]:
        """
        Convert a stream of TPath objects into a stream of user-mapped values.

        This terminal method executes the query and yields the result of applying
        the provided mapping function to each matching TPath. The fluent chain ends after select().

        Args:
            field: Function that takes a TPath and returns the value when field(tpath) is called.

        Returns:
            Iterator[Any]: Iterator of mapped values from matching files.

        Examples:
            # Stream file sizes
            for size in pquery(from_="/logs").where(lambda p: p.age.hours < 24).select(lambda p: p.size.bytes):
                process_size(size)

            # Collect file names
            file_names = list(pquery(from_="/logs").where(lambda p: p.suffix == ".log").select(lambda p: p.name))
        """

        def gen():
            for path in self._distinct_iter_files():
                try:
                    yield field(path)
                except Exception:
                    if not continue_on_exc:
                        raise

        return gen()

    def first(self, continue_on_exc: bool = True) -> TPath | None:
        """
        Return the first matching file or None if no matches.

        This terminal method executes the configured query and returns the first
        matching file, or None if no files match. The fluent chain ends here.

        Args:
            continue_on_exc: If True, continue processing on exceptions. If False, raise.

        Returns:
            TPath | None: First matching file or None

        Example:
            latest_error = pquery(from_="./logs").where(lambda p: "error" in p.name).first()
        """
        it = self.files(continue_on_exc=continue_on_exc)
        try:
            return next(it)
        except StopIteration:
            return None

    def exists(self) -> bool:
        """
        Check if any files match the query.

        This terminal method executes the configured query and returns True if
        at least one file matches, False otherwise. The fluent chain ends here.

        Returns:
            bool: True if at least one matching file exists

        Example:
            has_large_files = pquery(from_="./data").where(lambda p: p.size.gb > 1).exists()
        """
        try:
            next(self._distinct_iter_files())
            return True
        except StopIteration:
            return False

    def count(self, continue_on_exc: bool = True) -> int:
        """
        Count the number of matching files.

        This terminal method executes the configured query and returns the total
        count of matching files. The fluent chain ends here.

        Args:
            continue_on_exc: If True, continue processing on exceptions. If False, raise.

        Returns:
            int: Number of matching files

        Example:
            num_python_files = pquery(from_="./src").where(lambda p: p.suffix == ".py").count()
        """
        return sum(1 for _ in self.files(continue_on_exc=continue_on_exc))

    def order_by(
        self,
        key: Callable[[TPath], Any] | None = None,
        ascending: bool = True,
        continue_on_exc: bool = True,
    ) -> list[TPath]:
        """
        Sort all matching files by a key function.

        This terminal method executes the configured query, collects all matching
        files, and returns them sorted. The fluent chain ends here.

        This method performs a full sort of all results. Use take() if you only need
        the top/bottom n files for better performance.

        Args:
            key: Function to extract comparison key from TPath
                Can return a single value or tuple for multi-column sorting
            ascending: If True (default), sort in ascending order
                      If False, sort in descending order
            continue_on_exc: If True, continue processing on exceptions. If False, raise.

        Returns:
            list[TPath]: All matching files sorted by the key

        Examples:
            # Sort by file size (smallest to largest)
            by_size = query.order_by(key=lambda p: p.size.bytes)

            # Sort by file size (largest to smallest)
            by_size_desc = query.order_by(key=lambda p: p.size.bytes, ascending=False)

            # Sort by modification time (newest to oldest)
            by_time = query.order_by(key=lambda p: p.mtime.timestamp, ascending=False)

            # Multi-column sort: by directory, then by name
            by_path = query.order_by(key=lambda p: (p.parent.name, p.name))

            # Sort by name (alphabetical)
            by_name = query.order_by(key=lambda p: p.name)
        """

        def safe_iter():
            for path in self._distinct_iter_files():
                try:
                    yield path
                except Exception:
                    if not continue_on_exc:
                        raise

        files = list(safe_iter())
        if key is None:
            return sorted(files, reverse=not ascending)
        return sorted(files, key=key, reverse=not ascending)

    def paginate(
        self, page_size: int = 10, continue_on_exc: bool = True
    ) -> Iterator[list[TPath]]:
        """
        Return an iterator that yields pages of files.

        This terminal method executes the configured query and returns an iterator
        that yields pages of matching files. The fluent chain ends here.

        This is the most efficient way to process large result sets in chunks,
        as it maintains a single iterator and processes each file exactly once.

        Args:
            page_size: Number of files per page (default: 10)
            continue_on_exc: If True, continue processing on exceptions. If False, raise.

        Yields:
            list[TPath]: Pages of files, each containing up to page_size items

        Examples:
            # Process files in batches for memory efficiency
            for page in query.paginate(100):
                process_batch(page)
                print(f"Processed {len(page)} files")

            # Web API pagination
            pages = list(query.paginate(20))
            page_1 = pages[0] if pages else []

            # Manual pagination with progress
            for page_num, page in enumerate(query.paginate(50)):
                print(f"Page {page_num + 1}: {len(page)} files")
                if not page:  # Empty page means we're done
                    break
        """
        import itertools  # noqa: F401 # Lazy import - only needed for pagination

        iterator = self.files(continue_on_exc=continue_on_exc)
        while True:
            page = list(itertools.islice(iterator, page_size))
            if not page:
                break
            yield page

    def map_parallel(
        self,
        func: Callable[[TPath], Any],
        *,
        workers: int = 1,
        exception_policy: str = "continue",
        timeout: float | None = None,
    ) -> Iterator[MapResult]:
        """
        Map `func` across matching files using a producer (crawler) + consumer workers.

        This terminal method streams MapResult objects as files are processed. The
        query traversal (producer) runs in a background thread and pushes TPath
        objects onto a bounded queue; `workers` consumer threads run the user
        provided `func` on each TPath and push MapResult objects onto a result
        queue which is consumed by the returned iterator.

        Defaults are simple: one crawler (producer) + one worker. Increase
        `workers` to parallelize IO/CPU-bound mapping as appropriate. Note that
        for CPU-bound heavy functions you may prefer a multiprocessing approach
        (not implemented here) due to the GIL.

        Args:
            func: Callable accepting a single TPath and returning any value
            workers: Number of consumer worker threads (default: 1)
            exception_policy: How to react when func raises on an item.
                - 'continue' (default): emit MapResult with success=False and continue
                - 'collect': same as 'continue' (keeps exceptions for caller to inspect)
                - 'exit': emit MapResult for the failure then try to stop all processing
            timeout: Optional timeout (seconds) applied to internal queue.get when
                waiting for results; None means block until results are available.

        Yields:
            MapResult objects in roughly the order they complete.
        """

        # local imports removed; threading and time are module-level imports

        if workers < 1:
            raise ValueError("workers must be >= 1")

        if exception_policy not in ("continue", "collect", "exit"):
            raise ValueError(
                "exception_policy must be one of 'continue', 'collect', 'exit'"
            )

        work_q: queue.Queue[object] = queue.Queue(maxsize=max(32, workers * 4))
        result_q: queue.Queue[object] = queue.Queue()
        sentinel = object()
        stop_event = threading.Event()

        def producer():
            """Producer thread.

            Crawls files using self._distinct_iter_files() and enqueues TPath objects
            onto the work_q. Respects `stop_event` so an 'exit' can stop the run.
            Uses a bounded put with timeout so the producer remains responsive and
            places sentinel objects when finished to signal worker shutdown.
            """
            try:
                for path in self._distinct_iter_files():
                    # If an 'exit' was requested, stop producing
                    if stop_event.is_set():
                        break
                    # Avoid blocking forever so we can respond to stop_event
                    while True:
                        try:
                            work_q.put(path, timeout=0.5)
                            break
                        except queue.Full:
                            if stop_event.is_set():
                                return
                            continue
            finally:
                # Signal workers we are done
                for _ in range(workers):
                    # If workers are blocked on get, this will allow them to exit
                    try:
                        work_q.put(sentinel)
                    except Exception:
                        pass

        def worker():
            """Worker thread.

            Consumes items from `work_q`, runs the user-provided `func` on each
            TPath, and places MapResult objects onto `result_q`. On exception the
            result contains success=False and the exception. If
            `exception_policy=='exit'` the worker sets `stop_event` to notify
            others and attempts to stop processing.
            When the worker exits it pushes a sentinel into `result_q` to
            indicate completion.
            """
            while not stop_event.is_set():
                try:
                    item: object = work_q.get()
                except Exception:
                    break
                if item is sentinel:
                    # Put sentinel back for other workers and exit
                    try:
                        work_q.put(sentinel)
                    except Exception:
                        pass
                    break
                start = time.perf_counter()
                try:
                    tp = cast(TPath, item)
                    data = func(tp)
                    elapsed = time.perf_counter() - start
                    result_q.put(
                        MapResult(
                            path=tp,
                            execution_time=elapsed,
                            success=True,
                            exception=None,
                            data=data,
                        )
                    )
                except Exception as exc:  # noqa: BLE001 - we want to capture any exception
                    elapsed = time.perf_counter() - start
                    result_q.put(
                        MapResult(
                            path=cast(TPath, item),
                            execution_time=elapsed,
                            success=False,
                            exception=exc,
                            data=None,
                        )
                    )
                    if exception_policy == "exit":
                        # Signal other threads to stop and stop producing
                        stop_event.set()
                        break
                finally:
                    try:
                        work_q.task_done()
                    except Exception:
                        pass
            # Worker exiting — signal completion to the result iterator
            result_q.put(sentinel)

        # Start threads
        prod_thread = threading.Thread(
            target=producer, name="pquery-producer", daemon=True
        )
        worker_threads = [
            threading.Thread(target=worker, name=f"pquery-worker-{i}", daemon=True)
            for i in range(workers)
        ]
        prod_thread.start()
        for t in worker_threads:
            t.start()

        # Result iterator: yield MapResult objects until all workers have signalled completion
        finished_workers = 0
        try:
            while True:
                try:
                    obj: object = (
                        result_q.get(timeout=timeout)
                        if timeout is not None
                        else result_q.get()
                    )
                except queue.Empty:
                    # Timeout waiting for results
                    if stop_event.is_set():
                        break
                    continue
                if obj is sentinel:
                    finished_workers += 1
                    if finished_workers >= workers:
                        break
                    else:
                        continue
                # obj is a MapResult
                res = cast(MapResult, obj)
                yield res
        finally:
            # Ensure threads are asked to stop and joined
            stop_event.set()
            try:
                prod_thread.join(timeout=1.0)
            except Exception:
                pass
            for t in worker_threads:
                try:
                    t.join(timeout=1.0)
                except Exception:
                    pass

    def __iter__(self) -> Iterator[TPath]:
        """
        Allow iteration over the query results.

        This terminal method executes the configured query and returns an iterator
        over the matching files. The fluent chain ends here.

        Returns:
            Iterator[TPath]: Iterator of matching file paths
        """
        return self._distinct_iter_files()


def pquery(
    from_: PathInput | None = None,
    recursive: bool = True,
) -> PQuery:
    """
    Create a new path query.

    Args:
        from_: Starting directory path(s). Can be:
            - Single path (string, Path, or TPath)
            - List of paths (strings, Paths, or TPaths)
            - None: defaults to current directory
        recursive: Whether to search subdirectories recursively
            - True: uses rglob("*") for recursive search
            - False: uses glob("*") for current directory only

    Returns:
        PQuery: A query builder object

    Examples:
        # Default to current directory
        py_files = pquery().where(lambda p: p.suffix == ".py").files()

        # Single path
        py_files = pquery(from_="./src").where(lambda p: p.suffix == ".py").files()

        # Multiple starting paths
        all_configs = pquery(from_=["/etc", "/opt/config"]).where(lambda p: p.suffix == ".conf").files()

        # Using the fluent API
        query = PQuery().from_(paths="/logs").from_(paths="/var/log").recursive(True).where(lambda p: p.size.gb > 1)
    """
    query = PQuery().recursive(recursive)

    if from_ is not None:
        # Use the from_() method which handles all the type complexity
        query.from_(paths=from_)

    return query


__all__ = ["pquery", "PQuery", "PathLike", "PathSequence", "PathInput"]

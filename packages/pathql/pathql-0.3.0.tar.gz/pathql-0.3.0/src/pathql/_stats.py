"""
PQueryStats: Statistics tracking for PQuery queries.
Handles file counts, errors, timings, and path management.
All timings are floats; elapsed_time is always set (0.0 if no events).
set_paths accepts Path objects or strings.
"""

import logging
import time
from dataclasses import dataclass, field


@dataclass
class PQueryStats:
    """
    Tracks statistics for a PQuery run.

    - elapsed_time is always a float (never None); 0.0 means no events processed yet.
    - start_time is set at object creation.
    """

    files_scanned: int = 0
    files_matched: int = 0
    errors: int = 0
    error_details: list[str] = field(default_factory=list)
    start_time: float = field(default_factory=time.time)
    end_time: float | None = None
    elapsed_time: float = 0.0
    paths: list[str] | None = None
    logger: logging.Logger | None = None
    log_every_n: int = 1000

    def set_paths(self, paths: list[str] | list[object]) -> None:
        """
        Set the paths, accepting Path objects or strings.
        Each entry is stringified and stored.
        """
        self.paths = [str(p) for p in paths]

    def add_matched_file(self, path: str) -> None:
        """
        Register a matched file.

        Args:
            path (str): The path of the matched file.
        """
        self.files_scanned += 1
        self.files_matched += 1
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time
        if (
            self.logger
            and self.log_every_n > 0
            and self.files_matched % self.log_every_n == 0
        ):
            self.logger.info(f"matched file: {path}")

    def add_unmatched_file(self, path: str) -> None:
        """
        Register an unmatched file.

        Args:
            path (str): The path of the unmatched file.
        """
        self.files_scanned += 1
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time

    def add_error(self, error: str) -> None:
        """
        Register an error.

        Args:
            error (str): The error message or detail.
        """
        self.errors += 1
        self.error_details.append(error)
        self.end_time = time.time()
        self.elapsed_time = self.end_time - self.start_time

    @property
    def current_elapsed(self) -> float:
        """
        Return the current elapsed time (live), even if the query is still running.
        If the query is complete, returns the final elapsed time.
        Always returns a float (never None); 0.0 means no events processed yet.
        """
        if self.end_time is not None:
            return self.elapsed_time
        return time.time() - self.start_time

    def log_msg(self) -> str:
        """
        Return a compact log-friendly summary string.

        Returns:
            str: Summary of scanned, matched, errors, and elapsed time.
        """
        return (
            f"scanned={self.files_scanned}, matched={self.files_matched}, "
            f"errors={self.errors}, elapsed={self.current_elapsed:.3f}s"
        )

    def __str__(self) -> str:
        """
        Return a detailed string representation of the stats object.

        Returns:
            str: Full summary of stats and paths.
        """
        return (
            f"PQueryStats(files_scanned={self.files_scanned}, files_matched={self.files_matched}, "
            f"errors={self.errors}, elapsed_time={self.current_elapsed:.3f}s, paths={self.paths})"
        )

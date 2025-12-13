"""
Test suite for PQueryStats.
Covers initialization, path handling, file/error counting, timing, and logging.
"""

import time
from pathlib import Path

import pytest

from src.pathql._stats import PQueryStats


def test_initial_state() -> None:
    """Test initial state of PQueryStats object."""
    # Arrange
    stats = PQueryStats()
    # Assert
    assert stats.files_scanned == 0
    assert stats.files_matched == 0
    assert stats.errors == 0
    assert stats.error_details == []
    assert stats.start_time > 0
    assert stats.end_time is None
    assert stats.elapsed_time == 0.0
    assert stats.paths is None or stats.paths == []


def test_set_paths_handles_str_and_path() -> None:
    """Test set_paths handles both str and Path objects."""
    # Arrange
    stats = PQueryStats()
    import os

    paths = ["/foo", Path("/bar"), Path("baz.txt")]
    # Act
    stats.set_paths(paths)
    # Assert
    expected = [os.path.normpath(p) for p in ["/foo", "/bar", "baz.txt"]]
    actual = [os.path.normpath(p) for p in (stats.paths or [])]
    assert actual == expected


@pytest.mark.parametrize(
    "N, M",
    [
        (0, 0),
        (0, 3),
        (5, 0),
        (5, 3),
        (1, 1),
        (10, 10),
        (20, 5),
    ],
)
def test_add_matched_and_unmatched_files_counts_and_timing(N: int, M: int) -> None:
    """Test adding N matched and M unmatched files updates counts and timings correctly for edge cases and typical values."""
    # Arrange
    stats = PQueryStats()
    matched_files = [f"/pass_{i}.txt" for i in range(N)]
    unmatched_files = [f"/fail_{i}.txt" for i in range(M)]
    # Act
    start = stats.start_time
    for f in matched_files:
        stats.add_matched_file(f)
    for f in unmatched_files:
        stats.add_unmatched_file(f)
    end = stats.end_time
    # Assert
    expected_scanned = N + M
    expected_matched = N
    assert stats.files_scanned == expected_scanned, (
        f"actual_scanned={stats.files_scanned}, expected_scanned={expected_scanned}"
    )
    assert stats.files_matched == expected_matched, (
        f"actual_matched={stats.files_matched}, expected_matched={expected_matched}"
    )
    if expected_scanned > 0:
        assert stats.elapsed_time is not None and stats.elapsed_time >= 0
        assert end is not None and start is not None and end >= start
    else:
        assert stats.elapsed_time == 0.0
        assert end is None


def test_add_error_increments_and_details() -> None:
    """Test add_error increments error count and appends details."""
    # Arrange
    stats = PQueryStats()
    error_msg = "error message"
    # Act
    stats.add_error(error_msg)
    # Assert
    assert stats.errors == 1
    assert error_msg in stats.error_details
    assert stats.elapsed_time is not None and stats.elapsed_time >= 0


def test_log_msg_and_str_output() -> None:
    """Test log_msg and __str__ output correct summary info."""
    # Arrange
    stats = PQueryStats()
    stats.add_matched_file("/foo")
    stats.add_unmatched_file("/bar")
    stats.add_error("error message")
    # Act
    log = stats.log_msg()
    s = str(stats)
    # Assert
    assert "scanned=2" in log
    assert "matched=1" in log
    assert "errors=1" in log
    assert "scanned=2" in s
    assert "matched=1" in s
    assert "errors=1" in s


def test_current_elapsed_live_and_final() -> None:
    """Test current_elapsed property live and after completion."""
    # Arrange
    stats = PQueryStats()
    time.sleep(0.01)
    # Act
    live_elapsed = stats.current_elapsed
    stats.add_matched_file("/foo")
    final_elapsed = stats.current_elapsed
    # Assert
    assert live_elapsed > 0
    assert final_elapsed >= 0

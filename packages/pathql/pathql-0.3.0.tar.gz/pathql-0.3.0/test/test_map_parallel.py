"""Tests for PQuery.map_parallel.

This file is a clean, CODESTYLE-compliant test harness for the threaded mapping facility.
"""

from __future__ import annotations

import pathlib
import time

import pytest

from src.pathql._pquery import pquery


def _make_files(tmp_path: pathlib.Path, count: int) -> list[str]:
    paths: list[str] = []
    for i in range(count):
        p = tmp_path / f"file_{i}.txt"
        p.write_text(f"{i}\n")
        paths.append(str(p))
    return paths


@pytest.mark.parametrize("policy", ["continue", "collect"])
def test_exception_policy_continue_collect(tmp_path: pathlib.Path, policy: str) -> None:
    """When one file raises, policy records failure and continues."""
    _make_files(tmp_path, 6)

    def work(p: pathlib.Path) -> str:
        if p.name.endswith("file_2.txt"):
            raise ValueError("boom")
        return p.name

    results = list(
        pquery(from_=str(tmp_path)).map_parallel(
            work, workers=2, exception_policy=policy
        )
    )

    failures = [r for r in results if not r.success]
    successes = [r for r in results if r.success]

    assert len(failures) == 1, "expected exactly one failure"
    assert isinstance(failures[0].exception, ValueError), "expected ValueError"
    assert len(successes) == 5, "expected 5 successes"


def test_basic(tmp_path: pathlib.Path) -> None:
    """All files are processed and MapResult fields are present."""
    _make_files(tmp_path, 4)

    results = list(
        pquery(from_=str(tmp_path)).map_parallel(lambda p: p.name, workers=1)
    )

    assert len(results) == 4, "expected 4 results"
    names = {r.data for r in results}
    assert names == {f"file_{i}.txt" for i in range(4)}, "unexpected result names"


def test_single_worker_series_timing(tmp_path: pathlib.Path) -> None:
    """With one worker, sleeps run in series and take longer."""
    _make_files(tmp_path, 4)

    def work(p: pathlib.Path) -> str:
        time.sleep(0.18)
        return p.name

    start = time.perf_counter()
    results = list(pquery(from_=str(tmp_path)).map_parallel(work, workers=1))
    series_time = time.perf_counter() - start

    assert len(results) == 4, "expected 4 results"
    assert series_time >= 4 * 0.15, "expected series timing"


def test_multi_worker_speedup(tmp_path: pathlib.Path) -> None:
    """Confirm multi-worker execution is faster than serial."""
    _make_files(tmp_path, 4)

    def work(p: pathlib.Path) -> str:
        time.sleep(0.18)
        return p.name

    start = time.perf_counter()
    list(pquery(from_=str(tmp_path)).map_parallel(work, workers=1))
    series_time = time.perf_counter() - start

    start = time.perf_counter()
    list(pquery(from_=str(tmp_path)).map_parallel(work, workers=4))
    parallel_time = time.perf_counter() - start

    assert parallel_time > 0, "parallel_time should be positive"
    assert series_time / parallel_time >= 1.5, "expected measurable speedup"


def test_exception_policy_exit(tmp_path: pathlib.Path) -> None:
    """Using 'exit' should stop soon after a failure; some successes expected."""
    _make_files(tmp_path, 12)

    def work(p: pathlib.Path) -> str:
        if p.name.endswith("file_5.txt"):
            raise RuntimeError("stopnow")
        time.sleep(0.02)
        return p.name

    results = list(
        pquery(from_=str(tmp_path)).map_parallel(
            work, workers=3, exception_policy="exit"
        )
    )

    failures = [r for r in results if not r.success]
    successes = [r for r in results if r.success]

    assert len(failures) >= 1, "expected at least one failure"
    assert any(isinstance(r.exception, RuntimeError) for r in failures), (
        "expected RuntimeError in failures"
    )
    assert len(successes) >= 1, "expected some successes before exit"
    assert len(results) < 12, "expected fewer than total files due to exit"


@pytest.mark.parametrize("workers", [1, 2])
def test_map_parallel_basic_parametrized(tmp_path: pathlib.Path, workers: int) -> None:
    """Verify that all files are processed and MapResult fields are present."""
    # Arrange
    _make_files(tmp_path, 4)

    # Act
    results = list(
        pquery(from_=str(tmp_path)).map_parallel(lambda p: p.name, workers=workers)
    )

    # Assert
    assert len(results) == 4, "expected 4 results"
    names = {r.data for r in results}
    assert names == {f"file_{i}.txt" for i in range(4)}, "unexpected result names"
    for r in results:
        assert hasattr(r.path, "name"), "result.path missing .name"
        assert isinstance(r.execution_time, float), "execution_time must be float"
        assert r.execution_time >= 0, "execution_time must be non-negative"
        assert r.success is True, "expected success True"
        assert r.exception is None, "expected no exception"


def test_map_parallel_single_worker_series_timing_and_results(
    tmp_path: pathlib.Path,
) -> None:
    """Using one worker, mapping with sleep should execute in series."""
    # Arrange
    _make_files(tmp_path, 4)

    def work(p: pathlib.Path) -> str:
        time.sleep(0.18)
        return p.name

    # Act
    start = time.perf_counter()
    results = list(pquery(from_=str(tmp_path)).map_parallel(work, workers=1))
    series_time = time.perf_counter() - start

    # Assert
    assert len(results) == 4, "expected 4 results"
    assert series_time >= 4 * 0.15, "expected series timing"
    for r in results:
        assert r.success is True, "expected success True"
        assert r.exception is None, "expected no exception"
        assert r.data.endswith(".txt"), "expected data to be filename"
        assert r.execution_time >= 0, "execution_time must be non-negative"


def test_map_parallel_multi_worker_speedup_and_results(tmp_path: pathlib.Path) -> None:
    """Confirm multi-worker execution is significantly faster than serial."""
    # Arrange
    _make_files(tmp_path, 4)

    def work(p: pathlib.Path) -> str:
        time.sleep(0.18)
        return p.name

    # Act - series run (1 worker)
    start = time.perf_counter()
    series_results = list(pquery(from_=str(tmp_path)).map_parallel(work, workers=1))
    series_time = time.perf_counter() - start

    # Act - parallel run (4 workers)
    start = time.perf_counter()
    parallel_results = list(pquery(from_=str(tmp_path)).map_parallel(work, workers=4))
    parallel_time = time.perf_counter() - start

    # Assert - Verify results correctness
    assert len(series_results) == 4, "expected 4 series results"
    assert len(parallel_results) == 4, "expected 4 parallel results"
    for r in series_results + parallel_results:
        assert r.success is True, "expected success True"
        assert r.exception is None, "expected no exception"
        assert r.data.endswith(".txt"), "expected data to be filename"

    # Expect significant speedup: series_time should be at least ~3x parallel_time
    assert parallel_time > 0, "parallel_time should be positive"
    assert series_time / parallel_time >= 3.0, "expected >=3x speedup"


@pytest.mark.parametrize("policy", ["continue", "collect"])
def test_map_parallel_exception_policy_continue_collect(
    tmp_path: pathlib.Path, policy: str
) -> None:
    """When mapping raises for one file, continue/collect should record failure and proceed."""
    # Arrange
    _make_files(tmp_path, 6)

    def work(p: pathlib.Path) -> str:
        if p.name.endswith("file_2.txt"):
            raise ValueError("boom")
        return p.name

    # Act
    results = list(
        pquery(from_=str(tmp_path)).map_parallel(
            work, workers=2, exception_policy=policy
        )
    )

    # Assert
    failures = [r for r in results if not r.success]
    successes = [r for r in results if r.success]

    assert len(failures) == 1, "expected exactly one failure"
    assert isinstance(failures[0].exception, ValueError), "expected ValueError"
    assert len(successes) == 5, "expected 5 successes"


def test_map_parallel_exception_policy_exit(tmp_path: pathlib.Path) -> None:
    """Using 'exit' causes processing to stop soon after a failure; some successes should exist."""
    # Arrange
    _make_files(tmp_path, 12)

    def work(p: pathlib.Path) -> str:
        if p.name.endswith("file_5.txt"):
            raise RuntimeError("stopnow")
        # small sleep to allow overlap and increase chance the exit cuts work short
        time.sleep(0.02)
        return p.name

    # Act
    results = list(
        pquery(from_=str(tmp_path)).map_parallel(
            work, workers=3, exception_policy="exit"
        )
    )

    # Assert
    failures = [r for r in results if not r.success]
    successes = [r for r in results if r.success]

    # Must see at least one failure (the raise)
    assert len(failures) >= 1, "expected at least one failure"
    assert any(isinstance(r.exception, RuntimeError) for r in failures), (
        "expected RuntimeError in failures"
    )

    # Confirm that some files succeeded before the exit occurred
    assert len(successes) >= 1, "expected at least one success before exit"

    assert len(results) < 12, "expected fewer than total files due to exit"

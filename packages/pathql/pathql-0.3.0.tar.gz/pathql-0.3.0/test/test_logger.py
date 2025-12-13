"""
Test suite for PQueryStats logger integration and logging behaviors.
Covers: no logging, file logging, stdout logging, and app-level logging.
"""

import logging
import sys
from pathlib import Path

import pytest

from src.pathql._stats import PQueryStats


class DummyLogger(logging.Logger):
    records: list[logging.LogRecord]

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.records = []

    def handle(self, record: logging.LogRecord) -> None:
        self.records.append(record)


@pytest.fixture
def dummy_logger():
    logger = DummyLogger("dummy")
    return logger


def test_no_logging(monkeypatch: pytest.MonkeyPatch) -> None:
    """Test that no logging occurs if no logger is attached."""
    # Arrange
    stats = PQueryStats()
    # Act
    stats.add_matched_file("/foo")
    # Assert
    # No error should be raised, nothing to assert


def test_file_logging(tmp_path: Path) -> None:
    """Test logging to a file handler."""
    # Arrange
    log_file = tmp_path / "test.log"
    logger = logging.getLogger("file_logger")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(log_file)
    logger.addHandler(handler)
    stats = PQueryStats()
    stats.logger = logger
    stats.log_every_n = 2
    # Act & Assert
    stats.add_matched_file("/foo")
    handler.flush()
    with open(log_file) as f:
        contents = f.read()
    assert "matched" not in contents and "scanned" not in contents

    stats.add_matched_file("/bar")
    handler.flush()
    with open(log_file) as f:
        contents = f.read()
    assert "matched" in contents or "scanned" in contents


def test_stdout_logging(capfd: pytest.CaptureFixture[str]) -> None:
    """Test logging to stdout handler."""
    # Arrange
    logger = logging.getLogger("stdout_logger")
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler(sys.stdout)
    logger.addHandler(handler)
    stats = PQueryStats()
    stats.logger = logger
    stats.log_every_n = 2
    # Act & Assert
    stats.add_matched_file("/foo")
    handler.flush()
    out, _ = capfd.readouterr()
    assert "matched" not in out and "scanned" not in out

    stats.add_matched_file("/bar")
    handler.flush()
    out, _ = capfd.readouterr()
    assert "matched" in out or "scanned" in out


def test_app_level_logging(dummy_logger: DummyLogger) -> None:
    """Test logging using an app-level logger object."""
    # Arrange
    stats = PQueryStats()
    stats.logger = dummy_logger
    stats.log_every_n = 2
    # Act & Assert
    stats.add_matched_file("/foo")
    assert not any(
        "matched" in r.getMessage() or "scanned" in r.getMessage()
        for r in dummy_logger.records
    )

    stats.add_matched_file("/bar")
    assert any(
        "matched" in r.getMessage() or "scanned" in r.getMessage()
        for r in dummy_logger.records
    )

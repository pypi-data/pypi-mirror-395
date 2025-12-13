"""Tests for PQuery error handling behavior.

This module verifies how PQuery.files(continue_on_exc=...) responds when
TPath.is_file() raises exceptions:

When continue_on_exc=False, exceptions propagate and callers must handle them.
When continue_on_exc=True, exceptions are logged/recorded and iteration skips the failing path.
Uses a DummyTPath that optionally raises PermissionError from is_file() to
simulate filesystem access errors and assert both behaviors with AAA-style tests.
"""

from pathlib import Path

import pytest
from tpath import TPath

from src.pathql._pquery import PQuery


class DummyTPath(TPath):
    def __init__(self, path: str, raise_error: bool = False):
        super().__init__(Path(path))
        self._raise_error = raise_error

    def is_file(self, follow_symlinks: bool = True) -> bool:
        print(f"DummyTPath.is_file called for {self} (raise_error={self._raise_error})")
        if self._raise_error:
            print("DummyTPath raising PermissionError!")
            raise PermissionError("Simulated error")
        return True


def test_error_not_skipped(tmp_path: Path) -> None:
    """Test that errors are NOT skipped when continue_on_exc=False."""
    # Arrange
    fake_file = tmp_path / "fake.txt"
    fake_file.write_text("content")
    query = (
        PQuery()
        .from_(paths=DummyTPath(str(fake_file), raise_error=True))
        .where(lambda p: p.is_file())
    )
    # Act & Assert
    with pytest.raises(PermissionError, match="Simulated error"):
        list(query.files(continue_on_exc=False))


def test_error_skipped() -> None:
    """Test that errors ARE skipped when continue_on_exc=True."""
    # Arrange
    query = PQuery()
    query.start_paths = [DummyTPath("/fake", raise_error=True)]
    # Act
    result = list(query.files(continue_on_exc=True))
    # Assert
    assert result == [], "Expected no results when error is skipped"

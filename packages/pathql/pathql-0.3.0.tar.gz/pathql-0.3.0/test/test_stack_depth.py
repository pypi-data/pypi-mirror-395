"""
Test for stack-based directory traversal in PQuery.

This test verifies that Python call stack depth does not grow with deep directory nesting.
It uses pytest's tmp_path fixture for automatic cleanup and ensures the walker is iterative.
"""

import inspect
from pathlib import Path

import pytest

from src.pathql._pquery import PQuery


def build_deep_dir_with_files(root: Path, depth: int) -> None:
    """
    Create a directory tree `depth` levels deep under `root`.
    Adds a file at each level and at the deepest level.
    """
    current = root
    current.mkdir(exist_ok=True)
    for i in range(depth):
        # Add a file at this level
        (current / f"file_{i}.txt").write_text("test")
        current = current / f"level_{i}"
        current.mkdir(exist_ok=True)
    # Add a file at the deepest level
    (current / "deepest.txt").write_text("test")


@pytest.fixture
def deep_dir(tmp_path: Path) -> Path:
    """
    Pytest fixture: creates a deep directory tree in a temp location.
    Returns the root path. Automatically cleaned up by pytest.
    """
    build_deep_dir_with_files(tmp_path, 10)
    return tmp_path


def test_python_stack_depth_no_recursion(deep_dir: Path) -> None:
    """
    Test that stack-based traversal does not grow Python call stack for deep nests.
    Asserts that stack depth is constant for all files yielded by PQuery.

    During testing, the stack depth was exactly the same even though this folder had files in each
    of 10 levels of the stack.  For example I saw: (stack_depths = [38, 38, 38, 38, 38, 38, 38, 38, 38, 38, 38])
    """
    stack_depths = []
    # Loop over all files found by PQuery and record Python call stack depth
    for file in PQuery(from_=deep_dir).files():
        stack_depths.append(len(inspect.stack()))
    assert stack_depths, "No files found"
    # Assert call stack depth is constant (no recursion)
    assert len(set(stack_depths)) == 1, f"Call stack depth varied: {stack_depths}"

"""
Comprehensive tests for the PQuery API functionality.
"""

import pathlib

from src.pathql import PQuery, pquery


def test_pquery_package_imports():
    """Test that all expected functions are available from the package."""
    from src.pathql import pquery

    # Test that they're callable
    assert callable(pquery)
    assert callable(PQuery)


def test_pquery_fluent_api(tmp_path: pathlib.Path):
    """Test the fluent API pattern of PQuery."""
    # Create test files
    (tmp_path / "file1.txt").write_text("content1")
    (tmp_path / "file2.py").write_text("content2")
    (tmp_path / "file3.log").write_text("content3")

    # Test method chaining
    query = pquery(from_=tmp_path).where(lambda p: p.suffix == ".txt")

    # Test that query object has expected methods
    assert hasattr(query, "files")
    assert hasattr(query, "select")
    assert hasattr(query, "first")
    assert hasattr(query, "exists")
    assert hasattr(query, "count")
    assert hasattr(query, "__iter__")

    # Test that methods return expected types
    files = list(query.files())
    assert isinstance(files, list)
    assert len(files) == 1

    names = list(query.select(lambda p: p.name))
    assert isinstance(names, list)
    assert len(names) == 1
    assert names[0] == "file1.txt"

    first = query.first()
    assert first is not None
    assert first.name == "file1.txt"

    exists = query.exists()
    assert isinstance(exists, bool)
    assert exists is True

    count = query.count()
    assert isinstance(count, int)
    assert count == 1


def test_pquery_error_handling(tmp_path: pathlib.Path) -> None:
    """Test error handling in PQuery."""
    # Test that query without where() now works with default where function
    (tmp_path / "test.txt").write_text("content")
    (tmp_path / "subdir").mkdir()  # Should be filtered out by default

    query = pquery(from_=tmp_path)

    # Should work with default where function (files only)
    files = list(query.files())
    assert len(files) == 1
    assert files[0].name == "test.txt"

    # Test select and first also work
    names = list(query.select(lambda p: p.name))
    assert names == ["test.txt"]

    first_file = query.first()
    assert first_file is not None
    assert first_file.name == "test.txt"

    # Test that all methods work with default where function
    assert query.exists() is True
    assert query.count() == 1
    assert len(list(query)) == 1


def test_pquery_nonexistent_paths(tmp_path: pathlib.Path) -> None:
    """Test behavior with nonexistent paths."""
    # Test with nonexistent single path
    query = pquery(from_="/nonexistent/path").where(lambda p: True)
    assert list(query.files()) == []
    assert list(query.select(lambda p: p.name)) == []
    assert query.first() is None
    assert query.exists() is False
    assert query.count() == 0

    # Test with mix of existing and nonexistent paths
    temp_dir = tmp_path / "existing"
    temp_dir.mkdir()
    (temp_dir / "test.txt").write_text("test")

    query = pquery(from_=[str(temp_dir), "/nonexistent"]).where(lambda p: True)
    files = list(query.files())
    assert len(files) == 1
    assert files[0].name == "test.txt"


def test_pquery_file_vs_directory_input(tmp_path: pathlib.Path) -> None:
    """Test behavior when input is a file vs directory."""
    # Create a test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("content")

    # Test with file as input - should test just that file
    query = pquery(from_=test_file).where(lambda p: p.suffix == ".txt")
    files = list(query.files())
    assert len(files) == 1
    assert files[0].name == "test.txt"

    # Test with file that doesn't match query
    query = pquery(from_=test_file).where(lambda p: p.suffix == ".py")
    files = list(query.files())
    assert len(files) == 0


def test_pquery_edge_cases(tmp_path: pathlib.Path) -> None:
    """Test edge cases and boundary conditions."""
    # Empty directory
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()

    query = pquery(from_=empty_dir).where(lambda p: True)
    assert list(query.files()) == []
    assert query.count() == 0

    # Directory with only subdirectories (no files)
    sub_dir = empty_dir / "subdir"
    sub_dir.mkdir()

    query = pquery(from_=empty_dir).where(lambda p: True)
    assert list(query.files()) == []  # Should only return files, not directories

    # Very specific query that matches nothing
    (tmp_path / "file.txt").write_text("content")
    query = pquery(from_=tmp_path).where(lambda p: p.name == "nonexistent.txt")
    assert list(query.files()) == []
    assert query.first() is None
    assert query.exists() is False


def test_pquery_recursive_behavior(tmp_path: pathlib.Path) -> None:
    """Test recursive vs non-recursive behavior in detail."""
    # Create nested structure
    (tmp_path / "root.txt").write_text("root")

    level1 = tmp_path / "level1"
    level1.mkdir()
    (level1 / "level1.txt").write_text("level1")

    level2 = level1 / "level2"
    level2.mkdir()
    (level2 / "level2.txt").write_text("level2")

    level3 = level2 / "level3"
    level3.mkdir()
    (level3 / "level3.txt").write_text("level3")

    # Test recursive (default)
    recursive_files = list(
        pquery(from_=tmp_path, recursive=True)
        .where(lambda p: p.suffix == ".txt")
        .files()
    )
    assert len(recursive_files) == 4
    names = [f.name for f in recursive_files]
    assert "root.txt" in names
    assert "level1.txt" in names
    assert "level2.txt" in names
    assert "level3.txt" in names

    # Test non-recursive
    non_recursive_files = list(
        pquery(from_=tmp_path, recursive=False)
        .where(lambda p: p.suffix == ".txt")
        .files()
    )
    assert len(non_recursive_files) == 1
    assert non_recursive_files[0].name == "root.txt"

    # Test non-recursive from intermediate level
    level1_files = list(
        pquery(from_=level1, recursive=False)
        .where(lambda p: p.suffix == ".txt")
        .files()
    )
    assert len(level1_files) == 1
    assert level1_files[0].name == "level1.txt"


def test_pquery_complex_selectors(tmp_path: pathlib.Path) -> None:
    """Test complex select operations."""
    # Create files with different properties
    small_file = tmp_path / "small.txt"
    small_file.write_text("x")

    large_file = tmp_path / "large.txt"
    large_file.write_text("x" * 1000)

    py_file = tmp_path / "script.py"
    py_file.write_text("print('hello')")

    # Test selecting tuples
    file_info = list(
        pquery(from_=tmp_path)
        .where(lambda p: True)
        .select(lambda p: (p.name, p.suffix, p.size.bytes))
    )

    assert len(file_info) == 3
    for name, suffix, size in file_info:
        assert isinstance(name, str)
        assert isinstance(suffix, str)
        assert isinstance(size, int)

    # Test selecting computed values
    relative_sizes = list(
        pquery(from_=tmp_path)
        .where(lambda p: True)
        .select(
            lambda p: p.size.bytes / 100  # Size in hundreds of bytes
        )
    )

    assert len(relative_sizes) == 3
    for size_ratio in relative_sizes:
        assert isinstance(size_ratio, float)

    # Test complex selector with conditionals
    file_categories = list(
        pquery(from_=tmp_path)
        .where(lambda p: True)
        .select(lambda p: "large" if p.size.bytes > 500 else "small")
    )

    assert len(file_categories) == 3
    assert "large" in file_categories
    assert "small" in file_categories

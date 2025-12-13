"""
Tests for the new fluent PQuery API.
"""

import pathlib

from src.pathql import PQuery, pquery


def test_pquery_default_constructor(tmp_path: pathlib.Path) -> None:
    """Test that PQuery() defaults to current directory."""
    # Change to temp directory for this test
    import os

    original_cwd = os.getcwd()
    try:
        os.chdir(str(tmp_path))

        # Create test files in current directory
        (tmp_path / "test1.txt").write_text("content1")
        (tmp_path / "test2.py").write_text("content2")

        # Test default constructor
        query = PQuery().where(lambda p: True)
        files = list(query.files())

        assert len(files) == 2
        names = [f.name for f in files]
        assert "test1.txt" in names
        assert "test2.py" in names

    finally:
        os.chdir(original_cwd)


def test_pquery_fluent_from_methods(tmp_path: pathlib.Path):
    """Test the fluent from_() methods."""
    # Create multiple directories
    dir1 = tmp_path / "dir1"
    dir2 = tmp_path / "dir2"
    dir3 = tmp_path / "dir3"

    for d in [dir1, dir2, dir3]:
        d.mkdir()
        (d / f"file_{d.name}.txt").write_text(f"content from {d.name}")

    # Test single from_()
    query = PQuery().from_(paths=dir1).where(lambda p: p.suffix == ".txt")
    files = list(query.files())
    assert len(files) == 1
    assert files[0].name == "file_dir1.txt"

    # Test chaining from_() calls
    query = (
        PQuery().from_(paths=dir1).from_(paths=dir2).where(lambda p: p.suffix == ".txt")
    )
    files = list(query.files())
    assert len(files) == 2
    names = [f.name for f in files]
    assert "file_dir1.txt" in names
    assert "file_dir2.txt" in names

    # Test multiple from_() calls
    query = (
        PQuery()
        .from_(paths=dir1)
        .from_(paths=dir2)
        .from_(paths=dir3)
        .where(lambda p: p.suffix == ".txt")
    )
    files = list(query.files())
    assert len(files) == 3
    names = [f.name for f in files]
    assert "file_dir1.txt" in names
    assert "file_dir2.txt" in names
    assert "file_dir3.txt" in names


def test_pquery_recursive_method(tmp_path: pathlib.Path):
    """Test the recursive() method."""
    # Create nested structure
    (tmp_path / "root.txt").write_text("root")

    sub_dir = tmp_path / "subdir"
    sub_dir.mkdir()
    (sub_dir / "nested.txt").write_text("nested")

    # Test recursive(True) - default
    query = (
        PQuery()
        .from_(paths=tmp_path)
        .recursive(True)
        .where(lambda p: p.suffix == ".txt")
    )
    files = list(query.files())
    assert len(files) == 2
    names = [f.name for f in files]
    assert "root.txt" in names
    assert "nested.txt" in names

    # Test recursive(False)
    query = (
        PQuery()
        .from_(paths=tmp_path)
        .recursive(False)
        .where(lambda p: p.suffix == ".txt")
    )
    files = list(query.files())
    assert len(files) == 1
    assert files[0].name == "root.txt"


def test_pquery_method_chaining_order(tmp_path: pathlib.Path):
    """Test that method chaining works in any order."""
    # Create test structure
    dir1 = tmp_path / "dir1"
    dir2 = tmp_path / "dir2"

    for d in [dir1, dir2]:
        d.mkdir()
        (d / "file.txt").write_text("content")

        sub = d / "sub"
        sub.mkdir()
        (sub / "nested.txt").write_text("nested")

    # Test different chaining orders - all should produce same result

    # Order 1: from -> recursive -> where
    query1 = (
        PQuery()
        .from_(paths=dir1)
        .from_(paths=dir2)
        .recursive(False)
        .where(lambda p: p.suffix == ".txt")
    )
    files1 = list(query1.files())

    # Order 2: recursive -> from -> where
    query2 = (
        PQuery()
        .recursive(False)
        .from_(paths=dir1)
        .from_(paths=dir2)
        .where(lambda p: p.suffix == ".txt")
    )
    files2 = list(query2.files())

    # Order 3: where -> from -> recursive (this should fail since where must be last)
    # But we can test: recursive -> where -> from (where overrides the query, so this should work if we re-call where)
    query3 = (
        PQuery()
        .recursive(False)
        .from_(paths=dir1)
        .from_(paths=dir2)
        .where(lambda p: p.suffix == ".txt")
    )
    files3 = list(query3.files())

    # All should find the same files (only top-level .txt files)
    assert len(files1) == len(files2) == len(files3) == 2

    names1 = sorted([f.name for f in files1])
    names2 = sorted([f.name for f in files2])
    names3 = sorted([f.name for f in files3])

    assert names1 == names2 == names3 == ["file.txt", "file.txt"]


def test_pquery_convenience_function_compatibility(tmp_path: pathlib.Path):
    """Test that the pquery() convenience function still works."""
    # Create test files
    (tmp_path / "test1.txt").write_text("content1")
    (tmp_path / "test2.py").write_text("content2")

    # Test with no arguments (should default to current directory)
    import os

    original_cwd = os.getcwd()
    try:
        os.chdir(str(tmp_path))

        files = list(pquery().where(lambda p: True).files())
        assert len(files) == 2

    finally:
        os.chdir(original_cwd)

    # Test with from_ argument
    files = list(pquery(from_=tmp_path).where(lambda p: p.suffix == ".txt").files())
    assert len(files) == 1
    assert files[0].name == "test1.txt"

    # Test with list of paths
    files = list(pquery(from_=[tmp_path]).where(lambda p: True).files())
    assert len(files) == 2


def test_pquery_fluent_vs_convenience_equivalence(tmp_path: pathlib.Path):
    """Test that fluent API and convenience function produce equivalent results."""
    # Create test structure
    dir1 = tmp_path / "dir1"
    dir2 = tmp_path / "dir2"

    for d in [dir1, dir2]:
        d.mkdir()
        (d / "file.txt").write_text("content")
        (d / "file.py").write_text("code")

    # Fluent API
    fluent_files = list(
        PQuery()
        .from_(paths=dir1)
        .from_(paths=dir2)
        .recursive(True)
        .where(lambda p: p.suffix == ".txt")
        .files()
    )

    # Convenience function
    convenience_files = list(
        pquery(from_=[dir1, dir2], recursive=True)
        .where(lambda p: p.suffix == ".txt")
        .files()
    )

    # Should produce same results
    assert len(fluent_files) == len(convenience_files) == 2

    fluent_names = sorted([f.name for f in fluent_files])
    convenience_names = sorted([f.name for f in convenience_files])

    assert fluent_names == convenience_names


def test_pquery_complex_fluent_example(tmp_path: pathlib.Path):
    """Test a complex real-world-like example using the fluent API."""
    # Create a realistic directory structure
    src_dir = tmp_path / "src"
    test_dir = tmp_path / "test"
    docs_dir = tmp_path / "docs"

    for d in [src_dir, test_dir, docs_dir]:
        d.mkdir()

    # Add various files
    (src_dir / "main.py").write_text("x" * 1000)  # Large file
    (src_dir / "utils.py").write_text("small")
    (test_dir / "test_main.py").write_text("test code")
    (docs_dir / "README.md").write_text("documentation")
    (docs_dir / "large_doc.md").write_text("x" * 2000)  # Large doc

    # Complex query: Find files from src and test directories that are either:
    # - Python files larger than 500 bytes, OR
    # - Any files with "test" in the name
    large_py_or_test_files = list(
        PQuery()
        .from_(paths=src_dir)
        .from_(paths=test_dir)
        .recursive(True)
        .where(lambda p: (p.suffix == ".py" and p.size.bytes > 500) or "test" in p.name)
        .files()
    )

    assert len(large_py_or_test_files) == 2
    names = [f.name for f in large_py_or_test_files]
    assert "main.py" in names  # Large Python file
    assert "test_main.py" in names  # Has "test" in name

    # Should not include utils.py (small) or docs files
    assert "utils.py" not in names
    assert "README.md" not in names
    assert "large_doc.md" not in names


def test_pquery_error_handling_fluent(tmp_path: pathlib.Path) -> None:
    """Test error handling with fluent API."""
    # Test that calling files() without where() now works (has default where function)
    (tmp_path / "test.txt").write_text("content")
    (
        tmp_path / "subdir"
    ).mkdir()  # This should be filtered out by default where function

    query = PQuery().from_(paths=tmp_path)

    # Should not raise error and should return files only (not directories)
    files = list(query.files())
    assert len(files) == 1
    assert files[0].name == "test.txt"
    assert files[0].is_file()

    # Test error handling for nonexistent paths (should be handled gracefully)
    nonexistent_query = PQuery().from_(paths=tmp_path / "nonexistent")
    files = list(nonexistent_query.files())
    assert len(files) == 0  # Should return empty list, not error

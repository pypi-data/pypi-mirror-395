"""
Test lazy initialization of PQuery constructor parameters.
"""

from pathlib import Path

from src.pathql import PQuery


def test_default_constructor_lazy_initialization(tmp_path: Path) -> None:
    """Test that PQuery() applies defaults only when query is executed."""
    query: PQuery = PQuery()

    # Initially, working state should be empty
    assert query.start_paths == []
    assert query._query_func == []

    # Create temp files to test with
    (tmp_path / "test.txt").write_text("content")
    import os

    original_cwd = os.getcwd()
    try:
        os.chdir(str(tmp_path))
        # When we execute the query, defaults should be applied
        files = list(query.files())
        # Now working state should be populated
        assert len(query.start_paths) == 1
        assert str(query.start_paths[0]) == "."
        assert query.is_recursive is True
        assert len(query._query_func) > 0
        assert len(files) == 1
        assert files[0].name == "test.txt"
    finally:
        os.chdir(original_cwd)


def test_constructor_with_from_parameter(tmp_path: Path) -> None:
    """Test PQuery constructor with from_ parameter."""
    (tmp_path / "test.py").write_text("print('hello')")
    query = PQuery(from_=tmp_path)
    # Initially, working state should be empty
    assert query.start_paths == []
    assert query._query_func == []
    # Execute query to apply defaults
    files = list(query.files())
    # Should use the provided from_ path
    assert len(query.start_paths) == 1
    assert query.start_paths[0] == tmp_path
    assert query.is_recursive is True  # Default
    assert len(files) == 1
    assert files[0].name == "test.py"


def test_constructor_with_recursive_parameter(tmp_path: Path) -> None:
    """Test PQuery constructor with recursive parameter."""
    (tmp_path / "test.txt").write_text("content")
    # Create subdirectory with file
    subdir = tmp_path / "subdir"
    subdir.mkdir()
    (subdir / "nested.txt").write_text("nested")
    # Non-recursive query
    query = PQuery(from_=tmp_path, recursive=False)
    files = list(query.files())
    assert query.is_recursive is False
    assert len(files) == 1  # Only top-level file
    assert files[0].name == "test.txt"
    # Recursive query
    query2 = PQuery(from_=tmp_path, recursive=True)
    files2 = list(query2.files())
    assert query2.is_recursive is True
    assert len(files2) == 2  # Both files
    file_names = {f.name for f in files2}
    assert file_names == {"test.txt", "nested.txt"}


def test_constructor_with_where_parameter(tmp_path: Path) -> None:
    """Test PQuery constructor with where parameter."""
    (tmp_path / "test.py").write_text("python file")
    (tmp_path / "test.txt").write_text("text file")
    # Custom where function
    query = PQuery(from_=tmp_path, where=lambda p: p.suffix == ".py")
    files = list(query.files())
    assert len(files) == 1
    assert files[0].name == "test.py"


def test_constructor_all_parameters(tmp_path: Path) -> None:
    """Test PQuery constructor with all parameters."""
    (tmp_path / "large.txt").write_text("x" * 1000)
    (tmp_path / "small.txt").write_text("small")
    query = PQuery(from_=tmp_path, recursive=False, where=lambda p: p.size.bytes > 500)
    files = list(query.files())
    assert len(files) == 1
    assert files[0].name == "large.txt"


def test_fluent_methods_override_constructor(tmp_path: Path) -> None:
    """Test that fluent methods can override constructor parameters."""
    (tmp_path / "test.py").write_text("python")
    (tmp_path / "test.txt").write_text("text")
    # Constructor sets where, but fluent method overrides it
    query = PQuery(
        from_=tmp_path,
        where=lambda p: p.suffix == ".py",  # Would match only .py
    ).where(lambda p: p.suffix == ".txt")  # Override to match only .txt
    files = list(query.files())
    assert len(files) == 1
    assert files[0].name == "test.txt"


def test_lazy_initialization_with_chaining(tmp_path: Path) -> None:
    """Test that lazy initialization works with method chaining."""
    (tmp_path / "test.txt").write_text("content")
    # Chain methods before executing
    query = PQuery(from_=tmp_path).recursive(False).where(lambda p: p.suffix == ".txt")
    # Before execution, working state should still be empty
    assert query.start_paths == []
    # Execute and verify
    files = list(query.files())
    assert len(files) == 1
    assert files[0].name == "test.txt"
    # After execution, working state should be populated
    assert len(query.start_paths) == 1


def test_default_where_filters_files_only(tmp_path: Path) -> None:
    """Test that default where function filters out directories."""
    (tmp_path / "file.txt").write_text("content")
    (tmp_path / "subdir").mkdir()
    query = PQuery(from_=tmp_path)
    files = list(query.files())
    # Should only return the file, not the directory
    assert len(files) == 1
    assert files[0].name == "file.txt"
    assert files[0].is_file()

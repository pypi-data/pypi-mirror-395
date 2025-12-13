"""
Test for multiple where() detection in PQuery.
"""

import pathlib

from tpath import TPath

from src.pathql import PQuery


def test_multiple_where_calls_compose_as_and(tmp_path: pathlib.Path):
    """Test that multiple where() calls are combined with AND logic."""
    # Arrange - Create test files with different properties
    (tmp_path / "small.txt").write_text("x" * 100)  # 100 bytes, .txt
    (tmp_path / "large.txt").write_text("x" * 1000)  # 1000 bytes, .txt
    (tmp_path / "large.log").write_text("x" * 1000)  # 1000 bytes, .log
    (tmp_path / "medium.txt").write_text("x" * 500)  # 500 bytes, .txt

    # Act - Query with multiple where clauses: .txt files AND > 300 bytes
    results: list[TPath] = list(
        PQuery()
        .from_(paths=str(tmp_path))
        .where(lambda p: p.suffix == ".txt")  # Only .txt files
        .where(lambda p: p.size.bytes > 300)  # AND size > 300 bytes
        .files()
    )

    # Assert - Should find large.txt (1000 bytes, .txt) and medium.txt (500 bytes, .txt)
    # But NOT small.txt (100 bytes, .txt - too small)
    # And NOT large.log (1000 bytes, .log - wrong suffix)
    assert len(results) == 2
    result_names: set[str] = {r.name for r in results}
    assert result_names == {"large.txt", "medium.txt"}


def test_single_where_with_combined_logic_works(tmp_path: pathlib.Path):
    """Test that single where() with combined logic works correctly."""
    # Arrange - Create test files
    (tmp_path / "small.txt").write_text("x" * 10)  # 10 bytes, .txt
    (tmp_path / "large.txt").write_text("x" * 1000)  # 1000 bytes, .txt
    (tmp_path / "large.log").write_text("x" * 1000)  # 1000 bytes, .log

    # Act - Single where with combined logic should work
    results = list(
        PQuery()
        .from_(paths=str(tmp_path))
        .where(lambda p: p.suffix == ".txt" and p.size.bytes > 500)
        .files()
    )

    # Assert - Should find only large.txt
    assert len(results) == 1
    assert results[0].name == "large.txt"


def test_where_builds_list_of_lambdas(tmp_path: pathlib.Path):
    """Test that multiple where() calls build a list of lambda functions internally."""
    # Arrange - Create test files with various properties
    (tmp_path / "test1.txt").write_text("x" * 1000)  # .txt, large, contains 'test'
    (tmp_path / "test2.log").write_text("x" * 1000)  # .log, large, contains 'test'
    (tmp_path / "small.txt").write_text("x" * 100)  # .txt, small, contains 'small'
    (tmp_path / "data.txt").write_text("x" * 500)  # .txt, medium, contains 'data'
    (tmp_path / "test3.txt").write_text("x" * 2000)  # .txt, very large, contains 'test'

    # Act - Build query with multiple where conditions (demonstrating list building)
    results = list(
        PQuery()
        .from_(paths=str(tmp_path))
        .where(lambda p: p.suffix == ".txt")  # Must be .txt
        .where(lambda p: p.size.bytes > 200)  # Must be > 200 bytes
        .where(lambda p: "test" in p.name)  # Must contain 'test' in name
        .where(lambda p: p.size.bytes < 1500)  # Must be < 1500 bytes
        .files()
    )

    # Assert - Only test1.txt should match ALL conditions:
    # - .txt ✓, > 200 bytes ✓, name contains 'test' ✓, < 1500 bytes ✓
    # test2.log: wrong suffix
    # small.txt: too small
    # data.txt: name doesn't contain 'test'
    # test3.txt: too large
    assert len(results) == 1
    assert results[0].name == "test1.txt"


def test_where_accepts_list_of_lambdas(tmp_path: pathlib.Path):
    """Test that where() accepts a list of lambda functions in a single call."""
    # Arrange - Create test files
    (tmp_path / "foo.txt").write_text("x" * 1000)  # .txt, large, name contains 'foo'
    (tmp_path / "bar.txt").write_text("x" * 1000)  # .txt, large, name contains 'bar'
    (tmp_path / "foo.log").write_text("x" * 1000)  # .log, large, name contains 'foo'
    (tmp_path / "small.txt").write_text("x" * 100)  # .txt, small, name contains 'small'

    # Act - Use list of lambdas in single where() call
    results = list(
        PQuery()
        .from_(paths=str(tmp_path))
        .where(
            [
                lambda p: p.suffix == ".txt",  # Must be .txt
                lambda p: p.size.bytes > 500,  # Must be > 500 bytes
                lambda p: p.stem == "foo",  # Must have stem 'foo'
            ]
        )
        .files()
    )

    # Assert - Only foo.txt should match ALL conditions from the list
    # foo.txt: .txt ✓, > 500 bytes ✓, stem == 'foo' ✓
    # bar.txt: wrong stem
    # foo.log: wrong suffix
    # small.txt: too small
    assert len(results) == 1
    assert results[0].name == "foo.txt"

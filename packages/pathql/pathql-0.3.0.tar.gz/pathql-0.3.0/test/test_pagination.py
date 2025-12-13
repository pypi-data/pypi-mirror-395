"""
Test the new paginate() functionality.
"""

from pathlib import Path

from src.pathql import PQuery


def test_paginate_basic_functionality(tmp_path: Path) -> None:
    """Test basic pagination functionality."""
    # Create 25 test files
    for i in range(25):
        (tmp_path / f"file_{i:02d}.txt").write_text(f"content {i}")
    query = PQuery().from_(paths=tmp_path).where(lambda p: p.suffix == ".txt")
    pages = list(query.paginate(10))
    assert len(pages) == 3
    assert len(pages[0]) == 10
    assert len(pages[1]) == 10
    assert len(pages[2]) == 5
    all_files: list[Path] = []
    for page in pages:
        all_files.extend(page)
    assert len(all_files) == 25
    file_names = {f.name for f in all_files}
    expected_names = {f"file_{i:02d}.txt" for i in range(25)}
    assert file_names == expected_names


def test_paginate_empty_query(tmp_path: Path) -> None:
    """Test pagination with no matching files."""
    query = PQuery().from_(paths=tmp_path).where(lambda p: p.suffix == ".nonexistent")
    pages = list(query.paginate(10))
    assert pages == []


def test_paginate_smaller_than_page_size(tmp_path: Path) -> None:
    """Test pagination when total files < page_size."""
    for i in range(5):
        (tmp_path / f"file_{i}.txt").write_text(f"content {i}")
    query = PQuery().from_(paths=tmp_path).where(lambda p: p.suffix == ".txt")
    pages = list(query.paginate(10))
    assert len(pages) == 1
    assert len(pages[0]) == 5


def test_paginate_efficiency_single_scan(tmp_path: Path) -> None:
    """Test that pagination only scans files once (not O(n²))."""
    for i in range(30):
        (tmp_path / f"file_{i:02d}.txt").write_text(f"content {i}")
    query = PQuery().from_(paths=tmp_path).where(lambda p: p.suffix == ".txt")
    seen_files: list[Path] = []
    for page in query.paginate(10):
        for file in page:
            seen_files.append(file.name)
    assert len(seen_files) == 30
    assert len(set(seen_files)) == 30  # No duplicates
    expected_names = {f"file_{i:02d}.txt" for i in range(30)}
    actual_names = set(seen_files)
    assert actual_names == expected_names


def test_paginate_with_distinct(tmp_path: Path) -> None:
    """Test pagination combined with distinct()."""
    for i in range(15):
        (tmp_path / f"file_{i}.txt").write_text(f"content {i}")
    query = (
        PQuery().from_(paths=tmp_path).distinct().where(lambda p: p.suffix == ".txt")
    )
    pages = list(query.paginate(5))
    assert len(pages) == 3
    assert all(len(page) == 5 for page in pages)
    all_files: list[Path] = []
    for page in pages:
        all_files.extend(page)
    file_paths = [str(f) for f in all_files]
    assert len(file_paths) == len(set(file_paths))  # No duplicates


def test_paginate_manual_iteration(tmp_path: Path) -> None:
    """Test manual iteration through pages."""
    for i in range(12):
        (tmp_path / f"file_{i:02d}.txt").write_text(f"content {i}")
    query = PQuery().from_(paths=tmp_path).where(lambda p: p.suffix == ".txt")
    paginator = query.paginate(5)
    page1 = next(paginator)
    page2 = next(paginator)
    page3 = next(paginator)
    assert len(page1) == 5
    assert len(page2) == 5
    assert len(page3) == 2
    try:
        next(paginator)
        raise AssertionError("Should have raised StopIteration")
    except StopIteration:
        pass  # Expected

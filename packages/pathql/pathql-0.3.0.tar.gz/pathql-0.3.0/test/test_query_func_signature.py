"""
Tests for PQuery query_func signature validation.
"""

from pathlib import Path

import pytest

from src.pathql import PQuery


def test_where_lambda_with_two_params(tmp_path: Path):
    """
    Should raise TypeError when lambda with two params is passed to where().
    """
    (tmp_path / "file.txt").write_text("test")
    query = PQuery(from_=tmp_path)
    with pytest.raises(TypeError):
        query.where(lambda a, b: True)


def test_where_func_with_two_params(tmp_path: Path):
    """
    Should raise TypeError when function with two params is passed to where().
    """

    def func(a, b) -> bool:
        return True

    (tmp_path / "file.txt").write_text("test")
    query = PQuery(from_=tmp_path)
    with pytest.raises(TypeError):
        query.where(func)


def test_where_func_with_no_params(tmp_path: Path):
    """
    Should raise TypeError when function with no params is passed to where().
    """

    def func():
        return True

    (tmp_path / "file.txt").write_text("test")
    query = PQuery(from_=tmp_path)
    with pytest.raises(TypeError):
        query.where(func)

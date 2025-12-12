from pyclean.cli import find_pyproject, get_globs
from pathlib import Path
from .build_pyproject import build_pyproject
import pytest
import os

def test_expected_paths(tmp_path, monkeypatch):
    build_pyproject(tmp_path, monkeypatch)
    pyproject = find_pyproject()
    globs = get_globs(pyproject)

    expected = [
        "build",
        "dist",
        "**/__pycache__",
        ".pytest_cache"
    ]

    assert set(globs) == set(expected)

def test_missing_tool_section(tmp_path):
    py = tmp_path / "pyproject.toml"
    py.write_text("""
    [other]
    foo = 1
    """)
    with pytest.raises(Exception):
        get_globs(py)

def test_missing_pyclean_section(tmp_path):
    py = tmp_path / "pyproject.toml"
    py.write_text("""
    [tool]
    something = {}
    """)
    with pytest.raises(Exception):
        get_globs(py)

def test_missing_paths_list(tmp_path):
    py = tmp_path / "pyproject.toml"
    py.write_text("""
    [tool.pyclean]
    # no paths key
    """)
    with pytest.raises(Exception):
        get_globs(py)

def test_paths_list_not_a_list(tmp_path):
    py = tmp_path / "pyproject.toml"
    py.write_text("""
    [tool.pyclean]
    paths = "build"
    """)
    # Depending on your implementation, this might raise or return invalid type.
    with pytest.raises(Exception):
        get_globs(py)
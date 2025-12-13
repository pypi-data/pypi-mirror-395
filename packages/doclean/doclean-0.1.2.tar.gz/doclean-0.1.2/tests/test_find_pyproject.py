
from pyclean.cli import find_pyproject
from pathlib import Path
from .build_pyproject import build_pyproject
import pytest
import os

def test_no_pyproject_exception(tmp_path):
    """Test that get_pyproject raises exception when no pyproject.toml file exists."""
    
    with pytest.raises(Exception):    
        find_pyproject(tmp_path)


def test_pyproject_exists(tmp_path, monkeypatch):
    build_pyproject(tmp_path, monkeypatch)
    pyproject = find_pyproject()


def test_pyproject_exists_in_parent(tmp_path, monkeypatch):
    build_pyproject(tmp_path, monkeypatch)
    monkeypatch.chdir("src")
    pyproject = find_pyproject()


def test_pyproject_exists_in_parent_pass_in_path(tmp_path, monkeypatch):
    build_pyproject(tmp_path, monkeypatch)
    monkeypatch.chdir("..")
    pyproject = find_pyproject(Path("./my_project/src"))


def test_start_in_linked_dir(tmp_path, monkeypatch):
    build_pyproject(tmp_path, monkeypatch)
    pyproject = find_pyproject(Path("../link_to_project"))


def test_pyproject_in_grandparent(tmp_path, monkeypatch):
    build_pyproject(tmp_path, monkeypatch)
    monkeypatch.chdir("src/deep/deeper/deepest")
    pyproject = find_pyproject()

    print("\n")
    print("cwd:", os.getcwd())   
    print("pyproject:", pyproject)        


def test_pyproject_in_wrong_dir(tmp_path, monkeypatch):
    build_pyproject(tmp_path, monkeypatch)
    monkeypatch.chdir("../outside_project")
    
    with pytest.raises(Exception): 
        pyproject = find_pyproject()

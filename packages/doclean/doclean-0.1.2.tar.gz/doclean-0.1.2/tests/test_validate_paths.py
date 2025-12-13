from pyclean.cli import validate_paths
from .FS_Helper import helper
from pathlib import Path
import pytest

def test_matches_properly(helper):
    helper.make("src/a.txt", "foo")
    helper.make("src/b.txt", "bar")

    results = validate_paths(helper.root, [
        Path(helper.root / "src"),
    ])

    print(helper.root, results)

    assert set(results) == {
        helper.root / "src", 
    }    

def test_reject_root(helper):
    helper.make("src/a.txt", "foo")
    helper.make("src/b.txt", "bar")

    results = validate_paths(helper.root, [
        Path(helper.root / "src"),
        Path(helper.root),
    ])

    print(helper.root, results)

    assert set(results) == {
        helper.root / "src", 
    }        

def test_path_not_found(helper):
    helper.make("src/a.txt", "foo")
    helper.make("src/b.txt", "bar")

    results = validate_paths(helper.root, [
        Path(helper.root / "src"),
        Path(helper.root / "doc"),
    ])

    print(helper.root, results)

    assert set(results) == {
        helper.root / "src", 
    }            

def test_path_outside_project_0(helper):
    helper.make("proj/a.txt", "foo")
    helper.make("b.txt", "bar")

    results = validate_paths(helper.root / "proj", [
        Path(helper.root / "proj/a.txt"),
        Path(helper.root / "b.txt"),
    ])

    assert set(results) == {
        helper.root / "proj/a.txt", 
    }        

def test_path_outside_project_1(helper):
    helper.make("proj/a.txt", "foo")
    helper.make("b.txt", "bar")

    results = validate_paths(helper.root / "proj", [
        Path(helper.root / "proj/a.txt"),
        Path(helper.root / "proj" / ".." / "b.txt"),
    ])

    assert set(results) == {
        helper.root / "proj/a.txt", 
    }

def test_symlink_outside_project(helper):
    helper.make("../a.txt", "foo")
    helper.link_dir("link-src", "..")

    results = validate_paths(helper.root, [
        Path(helper.root / "link-src/a.txt"),
    ])

    assert set(results) == set()          

def test_reject_symlink_directory(helper):
    helper.make("src/a.txt", "foo")
    helper.link_file("src/b.txt", "src/a.txt")

    results = validate_paths(helper.root, [
        Path(helper.root / "src/b.txt"),
    ])

    assert set(results) == set()                   
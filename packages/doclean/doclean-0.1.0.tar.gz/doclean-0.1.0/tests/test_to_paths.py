from pyclean.cli import to_paths
from .FS_Helper import helper
import pytest

def test_to_paths_simple_files(helper):
    helper.make("src/a.txt", "foo")
    helper.make("src/b.txt", "bar")

    results = to_paths(helper.root, ["src/*.txt"])

    assert set(results) == {
        helper.root / "src/a.txt", 
        helper.root / "src/b.txt"
    }

def test_to_paths_simple_files(helper):
    helper.make("src/foo/a.txt", "foo")
    helper.make("src/deep/deeper/b.txt", "bar")
    helper.make("src/c.txt", "baz")
    helper.make("d.txt", "baz") # should not match

    results = to_paths(helper.root, ["src/**/*.txt"])

    assert set(results) == {
        helper.root / "src/foo/a.txt", 
        helper.root / "src/deep/deeper/b.txt",
        helper.root / "src/c.txt"
    }

def test_matches_src_dir(helper):
    helper.make("src/foo/a.txt", "foo")
    helper.make("src/foo/b.txt", "bar")

    results = to_paths(helper.root, ["src/"])

    assert set(results) == {
        helper.root / "src/", 
    }

def test_no_matches(helper):
    helper.make("src/a.txt", "foo")
    helper.make("src/b.txt", "bar")

    results = to_paths(helper.root, ["docs/*.md"])

    assert results == []
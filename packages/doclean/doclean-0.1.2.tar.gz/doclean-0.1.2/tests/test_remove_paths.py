from pyclean.cli import remove_paths
from .FS_Helper import helper
from pathlib import Path
import pytest

def test_remove_paths(helper):
    helper.make("src/a.txt", "foo")
    helper.make("src/b.txt", "bar")
    helper.make("src/c.txt", "baz")

    paths_to_remove = [
        Path(helper.root / "src/a.txt"),
        Path(helper.root / "src/c.txt"),
    ]

    remove_paths(paths_to_remove)

    assert (helper.root / "src/a.txt").exists() is False
    assert (helper.root / "src/b.txt").exists() is True
    assert (helper.root / "src/c.txt").exists() is False


def test_remove_paths_with_nonexistent_path(helper):
    helper.make("src/a.txt", "foo")
    helper.make("src/b.txt", "bar")

    paths_to_remove = [
        Path(helper.root / "src/a.txt"),
        Path(helper.root / "src/c.txt"),  # Non-existent path
    ]

    remove_paths(paths_to_remove)

    assert (helper.root / "src/a.txt").exists() is False
    assert (helper.root / "src/b.txt").exists() is True


def test_remove_paths_with_directory(helper):
    helper.make("src/dir/file1.txt", "foo")
    helper.make("src/dir/file2.txt", "bar")
    helper.make("src/file3.txt", "baz")

    paths_to_remove = [
        Path(helper.root / "src/dir"),
    ]

    remove_paths(paths_to_remove)

    assert (helper.root / "src/dir").exists() is False
    assert (helper.root / "src/file3.txt").exists() is True
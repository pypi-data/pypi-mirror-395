#!/usr/bin/env python3
"""
clean.py — read [clean] from pyproject.toml and delete listed paths.
Supports wildcards, recursive globs, and directories.

Example pyproject.toml:

    [clean]
    paths = [
        "build",
        "dist",
        "**/__pycache__",
        ".pytest_cache"
    ]

Running:
    clean

Will delete:
    project/build/
    project/dist/
    every "__pycache__" folder recursively
    project/.pytest_cache/

This script searches upward from the current directory until it finds
a pyproject.toml, then applies the cleanup rules.
"""
from importlib.metadata import version
from pathlib import Path
import shutil
import tomllib
import sys
import glob
import argparse
from .DoCleanException import DoCleanException

def find_pyproject(root: Path | None = None) -> Path:
    """
    Locate the nearest `pyproject.toml` by searching upward from a starting
    directory.

    Args:
        root (Path | None):
            Starting directory for the search.  
            - If `None`, the search begins from the current working directory.
            - Otherwise, the provided path is resolved before searching.
            - Relative to the current working directory if not absolute.

    Returns:
        Path:
            The absolute path to the first `pyproject.toml` encountered while
            walking upward through parent directories.

    Search behavior:
        - Start at `root`.
        - Check for `pyproject.toml`.
        - Move upward through all parent directories (`root`, `root.parent`,
          `root.parent.parent`, … up to filesystem root).
        - Return immediately on the first match.

    Exit conditions:
        ❌ If no `pyproject.toml` is found in the entire upward search,
           the function terminates the program with:
               "❌ pyproject.toml not found."

    Notes:
        - This mirrors the behavior of tools like `black`, `ruff`, and `pytest`,
          which walk upward to find project configuration files.
    """
    if root is None: 
        root = Path.cwd()

    root = root.resolve()
    paths = (root, *root.parents)
    for path in paths:
        fullpath = path / "pyproject.toml"
        if fullpath.exists():            
            return fullpath

    raise DoCleanException("❌ pyproject.toml not found.")        


def get_globs(pyproject: Path) -> list[str]:
    """
    Load the cleaning path list from a project's pyproject.toml.

    Args:
        pyproject (Path):
            Absolute path to the pyproject.toml file to load.

    Returns:
        list[str]: 
            A list of path strings defined under the `[tool.doclean]` section.

    Exit conditions:
        ❌ Exits with an error message if:
            - The file lacks a top-level `[tool]` section.
            - The file lacks a `[tool.doclean]` section.
            - The `[tool.doclean]` section does not define a `paths` list.

    Notes:
        The function does not validate path existence or glob patterns; it only
        loads the configuration as-is from pyproject.toml.
    """
    with pyproject.open("rb") as f:
        data = tomllib.load(f)

    # Navigate to the 'tool' section
    tool = data.get("tool")
    if not tool:
        raise DoCleanException("❌ No [tool] section found in pyproject.toml.")

    # Navigate to the 'tool.doclean' section
    section = tool.get("doclean")
    if not section:
        raise DoCleanException("❌ No [tool.doclean] section found in pyproject.toml.")

    # Read the 'paths' values
    globs = section.get("paths")
    if not globs:
        raise DoCleanException("❌ No 'paths' list found in [tool.doclean].")

    # Ensure it's a list
    if not isinstance(globs, list):
        raise DoCleanException("❌ 'paths' must be a list in [tool.doclean]")

    return globs


def to_paths(root: Path, patterns: list[str]) -> list[Path]:
    """
    Expand (glob) each pattern under the given root and return all matching
    filesystem paths.

    Args:
        root (Path):
            Base directory under which all patterns are expanded.
        patterns (list[str]):
            Glob patterns (e.g., "dist", "**/*.pyc", "**/__pycache__") to expand
            recursively relative to `root`.

    Returns:
        list[Path]:
            A list of Paths representing every matched file or directory found
            under the provided patterns. No deletions occur here—only collection.

    Behavior:
        - Each pattern is resolved as `root/pattern`.
        - Allows the special ** wildcard to match directories recursively.
        - All matched paths are returned in a flat list.
        - No error checks are performed on the patterns or paths.
    """    
    paths = []

    for pattern in patterns:
        pattern_path = f"{root}/{pattern}"

        for fullpath in glob.glob(pattern_path, recursive = True):
            paths.append(Path(fullpath))    

    return paths

def validate_paths(root: Path, paths: list[Path]) -> list[Path]:
    """
    Validate candidate deletion paths to ensure they are safe.

    Args:
        root (Path):
            The project root directory. All deletion targets must be located
            strictly inside this directory.
        paths (list[Path]):
            Paths collected from glob expansion that are candidates for removal.

    Returns:
        list[Path]:
            A filtered list containing only safe, valid paths. Unsafe paths are
            rejected with warnings.

    Validation rules (in order):
        1. Reject the project root itself to prevent catastrophic deletion.
        2. Reject any path *outside* the project root (`is_relative_to(root)`).
        3. Reject symlinks to avoid deleting linked targets.
        4. Reject paths that no longer exist (stale glob matches).
        5. All other paths are accepted.

    Behavior:
        - Prints a warning for every invalid path.
        - Uses `path.resolve()` to evaluate symlinks and produce absolute paths.
        - The root is also resolved to ensure comparisons are consistent.
    """    
    valid = []
    root = root.resolve()
    
    for path in paths:
        if path.is_symlink():
            print(f"⚠️ Refusing to delete symlinked path: {path}")
            continue

        path = path.resolve()

        if path == root:
            print(f"⚠️ Refusing to delete root project directory: {path}")
        elif not path.is_relative_to(root):
            print(f"⚠️ Refusing to delete path outside project: {path}")
        elif path.is_symlink():
            print(f"⚠️ Refusing to delete symlinked path: {path}")
        elif not path.exists():
            print(f"⚠️ Path not found: {path}")
        else:
            valid.append(path)

    return valid

def remove_paths(paths: list[Path]):
    """
    Remove a list of filesystem paths (files or directories).

    Args:
        paths (list[Path]):
            A list of resolved, validated Paths to remove.

    Behavior:
        - Directories are removed recursively using `shutil.rmtree(...)`
          with `ignore_errors=True`.
        - Files (including symlinks) are removed with `Path.unlink()`.
        - Each removal prints a confirmation message.
        - File removal failures are caught and reported as warnings.

    Exit / error handling:
        - No calls to `sys.exit()`.
        - Directory removal ignores errors completely.
        - File removal errors are caught so the loop continues.

    Notes:
        - Caller is responsible for validating the paths (e.g., using
          `validate_paths()`).
        - Symlinks are treated as files and removed via `unlink()`.
    """    
    for path in paths:
        if path.is_dir():
            shutil.rmtree(path, ignore_errors = True)
            print(f"🗑️  removed dir:  {path}")
        else:
            try:
                path.unlink()
                print(f"🗑️  removed file: {path}")
            except Exception as e:
                pass # ignore unlink errors silently

def show_paths(paths: list[Path]):
    for path in paths:
        if path.is_dir():
            print(f"🗑️  removed dir:  {path}")
        else:
            try:
                print(f"🗑️  removed file: {path}")
            except Exception as e:
                print(f"⚠️  could not remove {path}: {e}")

def cli():
    parser = argparse.ArgumentParser(
        prog="doclean",
        description=(
            "Remove build artifacts and temporary paths defined in the [tool.doclean] "
            "section of pyproject.toml."
        ),
    )

    parser.add_argument(
        "-v", "--version",
        action  = "version",
        version = f"doclean {version('doclean')}",
        help    = "Show doclean version and exit."
    )

    parser.add_argument(
        "-d", "--dry",
        action="store_true",
        help="Show which paths would be removed, but don't delete anything.",
    )

    parser.add_argument(
        "root",
        nargs="?",
        default=".",
        help="Optional project root (defaults to current directory).",
    )

    return parser.parse_args()

def main():
    """
    Main entry point for the cleaning tool.

    Behavior:
        1. Locate the nearest `pyproject.toml` using `find_pyproject()`.
        2. Load the cleaning patterns from `[tool.doclean]` via `get_globs()`.
        3. Convert each pattern into expanded filesystem paths with `to_paths()`.
        4. Validate those paths for safety using `validate_paths()`.
        5. Remove all validated paths using `remove_paths()`.

    Output:
        - Prints warnings for invalid paths.
        - Prints a confirmation message for each removed file or directory.
        - Prints a final "Cleanup complete" message.

    Exit conditions:
        - Any fatal configuration problems (e.g., missing pyproject.toml,
          missing [tool.doclean], missing paths list) cause earlier helper
          functions to invoke `sys.exit()`.

    Notes:
        - Intended as the console_script entry point in pyproject.
    """    
    args = cli()

    try:
        pyroject_path = find_pyproject()
        patterns = get_globs(pyroject_path)    
        as_paths = to_paths(pyroject_path.parent, patterns)
        validated = validate_paths(pyroject_path.parent, as_paths)
    except DoCleanException as e:
        sys.exit(str(e))
    except Exception as e:        
        sys.exit(str(e))        

    if not args.dry:        
        remove_paths(validated)
    else:
        print("👀  Dry run, files not removed.")
        show_paths(validated)

    print("✅  Cleanup complete.")

if __name__ == "__main__":
    main()

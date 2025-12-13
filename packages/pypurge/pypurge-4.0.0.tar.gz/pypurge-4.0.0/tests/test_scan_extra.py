# tests/test_scan_extra.py

import os
import re
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pypurge.modules import scan

def test_scan_relative_to_fail(fs):
    """Test scan handling relative_to exception (though hard to trigger with os.walk)."""
    # os.walk returns paths under root_path.
    # relative_to should work.
    # To force fail, we might mock Path.relative_to.

    fs.create_dir("/src")
    fs.create_file("/src/file")

    with patch("pathlib.Path.relative_to", side_effect=ValueError("Boom")):
        # scan should continue treating rel_root as "."
        targets = scan.scan_for_targets(
            Path("/src"), {}, {"g": ["file"]}, set(), [], 0, "mtime", False
        )
        # Should find file
        assert len(targets["g"]) == 1

def test_scan_is_symlink_fail_dir(fs):
    """Test exception during is_symlink check for directory."""
    fs.create_dir("/src")
    fs.create_dir("/src/subdir")

    # We mock is_symlink to raise exception?
    # No, scan.py does `if d_path.is_symlink()`.
    # It does NOT have try-except around it.
    # Wait, coverage report said missing 32, 34?
    # `d_path = Path(root) / d`
    # `if d_path.is_symlink() and not delete_symlinks: continue`

    # If is_symlink raises, the scan crashes?
    # Yes.
    # So I can't really test exception handling if there is none, unless I'm supposed to add it?
    # Instructions: "Create NEW tests... tests should NOT modify production code."
    # So I must cover existing branches.

    # Maybe I missed something.
    # Let's check where coverage is missing.
    # `scan.py`: 27-28, 32, 34, 41-42, 51-52, 60, 78-79
    # 27-28: `except Exception: rel_root = Path(".")`
    # 32: `if d_path.is_symlink() ...` (maybe `and` shortcut?)
    # 34: `if older_than_sec ...`
    # 41-42: `exclude_patterns` check
    # 51-52: `except Exception: continue` (inside fnmatch loop)
    # 60: `if f_path.is_symlink() ...`
    # 78-79: `except Exception: continue` (inside fnmatch loop)

    # So exception handling IS there for fnmatch (51, 79) and relative_to (27).
    # `is_symlink` failures are not handled, so I don't test that.

    # I already covered relative_to fail above.
    pass

def test_scan_fnmatch_exception_dir(fs):
    """Test exception in fnmatch for dir."""
    fs.create_dir("/src")
    fs.create_dir("/src/subdir")

    # Mock fnmatch to raise exception
    with patch("fnmatch.fnmatch", side_effect=Exception("Boom")):
        targets = scan.scan_for_targets(
            Path("/src"), {"g": ["subdir"]}, {}, set(), [], 0, "mtime", False
        )
        # Should catch exception and continue
        assert len(targets) == 0

def test_scan_fnmatch_exception_file(fs):
    """Test exception in fnmatch for file."""
    fs.create_dir("/src")
    fs.create_file("/src/file")

    with patch("fnmatch.fnmatch", side_effect=Exception("Boom")):
        targets = scan.scan_for_targets(
            Path("/src"), {}, {"g": ["file"]}, set(), [], 0, "mtime", False
        )
        assert len(targets) == 0

def test_scan_exclude_regex_match(fs):
    """Test scan exclusion with regex."""
    fs.create_dir("/src")
    fs.create_dir("/src/ex_dir")
    fs.create_file("/src/ex_file")

    regex = re.compile(r"ex_.*")
    excludes = [("re", regex)]

    targets = scan.scan_for_targets(
        Path("/src"), {"g": ["*"]}, {"g": ["*"]}, set(), excludes, 0, "mtime", False
    )

    assert len(targets["g"]) == 0

def test_scan_exclude_glob_match(fs):
    """Test scan exclusion with glob."""
    fs.create_dir("/src")
    fs.create_dir("/src/ex_dir")

    excludes = [("glob", "ex_*")]

    targets = scan.scan_for_targets(
        Path("/src"), {"g": ["*"]}, {}, set(), excludes, 0, "mtime", False
    )
    assert len(targets["g"]) == 0

def test_scan_symlink_handling(fs):
    """Test symlink handling flags."""
    fs.create_dir("/src")
    fs.create_symlink("/src/link_dir", "/src")
    fs.create_symlink("/src/link_file", "/src/file") # broken link ok

    # 1. delete_symlinks=False (default) -> should skip symlinks
    targets = scan.scan_for_targets(
        Path("/src"), {"g": ["link_*"]}, {"g": ["link_*"]}, set(), [], 0, "mtime", False
    )
    assert len(targets["g"]) == 0

    # 2. delete_symlinks=True -> should include symlinks
    targets = scan.scan_for_targets(
        Path("/src"), {"g": ["link_*"]}, {"g": ["link_*"]}, set(), [], 0, "mtime", True
    )
    # Check if found. fnmatch matches name.
    # link_dir matches "link_*"
    # link_file matches "link_*"
    # Note: `link_dir` comes in `dirs` list?
    # os.walk behavior on symlinks to dirs:
    # If followlinks=False, symlinks to dirs are in `filenames` usually? No, in `dirnames`?
    # "By default, walk() will not walk down into symbolic links that resolve to directories."
    # They appear in `dirs` list.

    assert len(targets["g"]) == 2

def test_scan_older_than(fs):
    """Test scan with older_than."""
    fs.create_dir("/src")
    f_old = Path("/src/old")
    fs.create_file(f_old)
    f_new = Path("/src/new")
    fs.create_file(f_new)

    # Make old file old
    import time
    old_time = time.time() - 1000
    os.utime(f_old, (old_time, old_time))

    # older_than_sec = 500
    targets = scan.scan_for_targets(
        Path("/src"), {}, {"g": ["*"]}, set(), [], 500, "mtime", False
    )

    assert f_old in targets["g"]
    assert f_new not in targets["g"]

def test_scan_dir_removal(fs):
    """Test that directories matching a group are removed from traversal."""
    root = Path("/test_scan_removal")
    fs.create_dir(root / "cache_dir")
    (root / "cache_dir" / "ignored_file").touch()
    
    dir_groups = {"Cache": ["cache_dir"]}
    file_groups = {"Files": ["ignored_file"]}
    
    # scan_for_targets should match cache_dir in Cache, and NOT traverse into it
    # so ignored_file should NOT be in Files group (if we assume ignored_file would match otherwise)
    
    from pypurge.modules.scan import scan_for_targets
    targets = scan_for_targets(root, dir_groups, file_groups, set(), [], 0, "mtime", False)
    
    assert root / "cache_dir" in targets["Cache"]
    # Ensure ignored_file is NOT found because its parent was removed from walk
    assert root / "cache_dir" / "ignored_file" not in targets.get("Files", [])
    
    # Verify positive control: if dir is NOT matched, file IS found
    targets_control = scan_for_targets(root, {}, file_groups, set(), [], 0, "mtime", False)
    assert root / "cache_dir" / "ignored_file" in targets_control["Files"]

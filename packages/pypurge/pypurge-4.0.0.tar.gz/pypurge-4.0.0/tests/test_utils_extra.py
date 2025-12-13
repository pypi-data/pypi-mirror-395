# tests/test_utils_extra.py

import time
import os
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pypurge.modules import utils

def test_get_size_symlink(fs):
    """Test get_size with a symlink."""
    file_path = Path("/test_file")
    fs.create_file(file_path, contents="content")
    symlink_path = Path("/test_symlink")
    fs.create_symlink(symlink_path, file_path)

    # utils.get_size returns int(path.lstat().st_size or 0)
    # For a symlink, st_size is length of target path string.
    size = utils.get_size(symlink_path)
    assert size == len(str(file_path))

def test_get_size_exception():
    """Test get_size catching outer exception."""
    path = MagicMock()
    path.is_symlink.side_effect = Exception("Boom")
    assert utils.get_size(path) == 0

def test_get_size_recursive_broken_symlink(fs):
    """Test get_size recursive with broken symlink inside."""
    dir_path = Path("/test_dir")
    fs.create_dir(dir_path)

    # Create broken symlink inside dir (target does not exist)
    symlink_path = dir_path / "link"
    fs.create_symlink(symlink_path, "/nonexistent")

    # sub.is_file() should be False (broken link)
    # sub.is_symlink() should be True
    # total += int(sub.lstat().st_size) -> len("/nonexistent") = 12

    assert utils.get_size(dir_path) == len("/nonexistent")

def test_get_size_recursive_exception(fs):
    """Test get_size recursive catching inner exception."""
    dir_path = Path("/test_dir")
    fs.create_dir(dir_path)
    file_path = dir_path / "file"
    fs.create_file(file_path, contents="content")

    # Mock rglob to return a mock that raises exception on is_file
    # Note: Since we are using pyfakefs, Path is mocked. We need to patch the class used by utils.
    # But patching Path.rglob on the class affects all instances.

    with patch("pathlib.Path.rglob") as mock_rglob:
        bad_path = MagicMock()
        bad_path.is_file.side_effect = Exception("Boom")
        mock_rglob.return_value = [bad_path]

        assert utils.get_size(dir_path) == 0

def test_is_old_enough_types(fs):
    """Test is_old_enough with different age_types."""
    p = Path("/test_file")
    fs.create_file(p)

    # Set times to be old enough (1000 seconds ago)
    now = time.time()
    old_time = now - 1000

    # os.utime sets (atime, mtime)
    os.utime(p, (old_time, old_time))

    # For ctime, it's trickier in linux/pyfakefs as it usually reflects creation or metadata change.
    # pyfakefs might allow setting it if we access the underlying object, but let's see.
    # If we can't easily set ctime in a cross-platform way or via os.utime,
    # we might rely on the fact that create_file set ctime to 'now' by default.
    # We need it to be old.

    # In pyfakefs, we can mess with the file object.
    file_obj = fs.get_object(str(p))
    file_obj.st_ctime = old_time

    assert utils.is_old_enough(p, 100, "atime")
    assert utils.is_old_enough(p, 100, "mtime")
    assert utils.is_old_enough(p, 100, "ctime")
    assert utils.is_old_enough(p, 100, "unknown") # Default to mtime

def test_is_old_enough_exception():
    """Test is_old_enough exception handling."""
    p = MagicMock()
    p.stat.side_effect = Exception("Boom")
    assert utils.is_old_enough(p, 100, "mtime") is False

def test_format_bytes_zero():
    assert utils.format_bytes(0) == "0B"

def test_format_bytes_large():
    # 1 TB = 1024**4
    assert utils.format_bytes(1024**4) == "1.00TB"
    # Edge of loop
    assert utils.format_bytes(1024**5) == "1024.00TB" # Loop stops at TB (index 4)

def test_sha256_of_file_empty(fs):
    p = Path("/empty")
    fs.create_file(p)
    expected = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert utils.sha256_of_file(p) == expected

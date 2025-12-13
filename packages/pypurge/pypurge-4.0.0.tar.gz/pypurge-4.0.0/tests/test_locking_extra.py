# tests/test_locking_extra.py

import os
import sys
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pypurge.modules import locking

def test_acquire_lock_fail_acquire_exception():
    """Test acquire_lock handling general exception during creation."""
    lock_path = Path("/tmp/test.lock")
    with patch("os.open", side_effect=Exception("Boom")):
        assert locking.acquire_lock(lock_path) is None

def test_acquire_lock_stale_cleanup_fail(fs):
    """Test acquire_lock when removing stale lock fails."""
    # Mock _pid_alive to return False (pid gone)
    with patch("pypurge.modules.locking._pid_alive", return_value=False):

        # We can use os.chmod to make directory non-writable, which prevents unlink.
        # But we must be careful with root paths in pyfakefs.
        # Let's use a subdirectory.

        subdir = "/var/lock_dir"
        if not fs.exists(subdir):
            fs.create_dir(subdir)

        lock_path_subdir = Path(subdir) / "lockfile"
        fs.create_file(lock_path_subdir, contents="pid:99999\nstarted:0.0\n")

        # Make parent directory read-only so unlink fails.
        # NOTE: os.chmod on pyfakefs might not enforce permission unless we run as non-root
        # or strict permission checks are enabled.
        # pyfakefs default user is root.

        # Let's switch to a non-root user?
        # fs.set_user_id(1000)
        # But that might break other things or require setup.

        # Simpler: just patch os.unlink?
        # But Path.unlink calls os.unlink.

        with patch("os.unlink", side_effect=Exception("Cannot unlink")):
             # Path.unlink calls os.unlink.
             assert locking.acquire_lock(lock_path_subdir) is None

def test_acquire_lock_read_exception(fs):
    """Test acquire_lock when reading existing lock fails."""
    lock_path = Path("/test.lock")
    fs.create_file(lock_path)

    # Make file a directory to trigger read error?
    # No, we want exists() to be True.

    fs.create_dir("/test_dir_lock")
    lock_path_dir = Path("/test_dir_lock")

    assert locking.acquire_lock(lock_path_dir) is None


def test_pid_alive_windows_psutil(monkeypatch):
    """Test _pid_alive on Windows with psutil."""
    # Simulate windows
    monkeypatch.setattr(sys, "platform", "win32")

    # Mock os.kill to raise generic exception (triggering windows block)
    with patch("os.kill", side_effect=Exception("Not on windows")):
        # Mock psutil
        mock_psutil = MagicMock()
        mock_psutil.pid_exists.return_value = True

        with patch.dict(sys.modules, {"psutil": mock_psutil}):
             assert locking._pid_alive(123) is True
             mock_psutil.pid_exists.assert_called_with(123)

def test_pid_alive_windows_psutil_fail(monkeypatch):
    """Test _pid_alive on Windows when psutil fails or missing."""
    monkeypatch.setattr(sys, "platform", "win32")
    with patch("os.kill", side_effect=Exception("Not on windows")):
        # Mock importing psutil to fail
        with patch("builtins.__import__", side_effect=Exception("No psutil")):
             # os.kill raises exception -> catch -> try win -> import psutil -> exception -> return True
             assert locking._pid_alive(123) is True

def test_pid_alive_non_windows_kill_exception():
    """Test _pid_alive when os.kill raises generic exception on non-windows."""
    with patch("sys.platform", "linux"):
        with patch("os.kill", side_effect=Exception("Boom")):
            # Should return True (conservative)
            assert locking._pid_alive(123) is True

def test_release_lock_exceptions():
    """Test release_lock exception handling."""
    lock_path = Path("/test.lock")

    # Case 1: os.close fails
    with patch("os.close", side_effect=Exception("Boom")):
        locking.release_lock(123, lock_path)

    # Case 2: unlink fails
    with patch("os.close"):
        with patch.object(Path, "unlink", side_effect=Exception("Boom")):
            locking.release_lock(123, lock_path)

def test_acquire_lock_malformed_content(fs):
    """Test acquire_lock with malformed content in existing lock."""
    lock_path = Path("/test.lock")
    fs.create_file(lock_path, contents="malformed")

    result = locking.acquire_lock(lock_path)
    assert result is not None
    os.close(result)

def test_acquire_lock_parse_error(fs):
    """Test acquire_lock with content that raises ValueError on parsing."""
    lock_path = Path("/test.lock")
    fs.create_file(lock_path, contents="pid:garbage\nstarted:garbage\n")

    result = locking.acquire_lock(lock_path)
    assert result is not None
    os.close(result)

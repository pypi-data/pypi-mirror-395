# tests/test_deletion_extra.py

import os
import stat
import shutil
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pypurge.modules import deletion

def test_force_rmtree_onerror(fs):
    """Test force_rmtree error handling callback."""
    # We want to test `onerror` inside `force_rmtree`.
    # `onerror` attempts `os.chmod` and then retries the function.

    dir_path = Path("/test_dir")

    # We will mock shutil.rmtree to NOT do anything but call our onerror callback manually
    # to simulate a failure? No, we can't easily access onerror from outside.

    # We must make `shutil.rmtree` fail.
    # In pyfakefs, shutil.rmtree uses os.remove/os.rmdir.
    # If we patch os.remove to raise PermissionError, rmtree should call onerror.

    # But previous attempt failed because call_count was 0.
    # This suggests shutil.rmtree didn't call os.remove or used a different one.
    # Or maybe it deleted directory first? (rmtree deletes contents first).

    # Let's try patching `shutil.rmtree` to call the onerror callback directly.
    # This ensures we cover the code inside onerror.

    with patch("shutil.rmtree") as mock_rmtree:
        def side_effect(path, onerror=None):
            # simulate failure by calling onerror
            if onerror:
                # onerror(func, path, exc_info)
                # func is typically os.remove or os.rmdir
                mock_func = MagicMock()
                mock_func.side_effect = [None] # Succeeds on retry

                # We need to simulate exception info
                exc_info = (PermissionError, PermissionError("Boom"), None)

                onerror(mock_func, str(path), exc_info)

        mock_rmtree.side_effect = side_effect

        deletion.force_rmtree(dir_path)

        # We can verify logic inside onerror via side effects (e.g. os.chmod call)
        # But we mocked chmod? No.
        # We can check if chmod was called.

        # But wait, inside onerror:
        # try: os.chmod(p, stat.S_IWUSR)
        # try: func(p)

        # So we should see os.chmod called on path.
        # And mock_func called.

    # We can patch os.chmod to verify it was called.
    with patch("os.chmod") as mock_chmod:
        with patch("shutil.rmtree") as mock_rmtree:
            mock_rmtree.side_effect = side_effect
            deletion.force_rmtree(dir_path)
            assert mock_chmod.called

def test_force_rmtree_onerror_chmod_fail(fs):
    """Test force_rmtree onerror when chmod fails."""
    dir_path = Path("/test_dir")

    with patch("shutil.rmtree") as mock_rmtree:
        def side_effect(path, onerror=None):
            if onerror:
                mock_func = MagicMock()
                onerror(mock_func, str(path), (Exception, Exception("Boom"), None))

        mock_rmtree.side_effect = side_effect

        with patch("os.chmod", side_effect=Exception("Chmod fail")):
            deletion.force_rmtree(dir_path)
            # Should not raise

def test_force_unlink_access_fail(fs):
    """Test force_unlink when access check says not writable."""
    p = Path("/test_file")
    fs.create_file(p)

    # Mock os.access to return False
    with patch("os.access", return_value=False):
        # And mock chmod
        with patch("os.chmod") as mock_chmod:
            deletion.force_unlink(p)
            mock_chmod.assert_called_with(p, stat.S_IWUSR)

def test_force_unlink_chmod_fail(fs):
    """Test force_unlink when chmod fails."""
    p = Path("/test_file")
    fs.create_file(p)

    with patch("os.access", return_value=False):
        with patch("os.chmod", side_effect=Exception("Boom")):
            # Should proceed to unlink
             deletion.force_unlink(p)
             assert not p.exists()

def test_force_unlink_exception(fs):
    """Test force_unlink when unlink raises exception."""
    p = Path("/test_file")
    fs.create_file(p)

    with patch.object(Path, "unlink", side_effect=Exception("Boom")):
        deletion.force_unlink(p)
        # Should catch and pass

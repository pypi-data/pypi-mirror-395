
import os
import stat
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest
from pypurge.modules.deletion import force_rmtree

@pytest.fixture
def protected_dir(fs):
    """Create a directory with a read-only file."""
    base_dir = Path("/test_force_rmtree")
    protected_file = base_dir / "protected_file"

    fs.create_dir(base_dir)
    fs.create_file(protected_file, contents="protected")

    # Make the file read-only
    os.chmod(protected_file, stat.S_IREAD)

    return base_dir, protected_file

def test_force_rmtree_removes_readonly_file(protected_dir):
    """Test that force_rmtree removes a directory containing a read-only file."""
    base_dir, protected_file = protected_dir

    # Verify that the file is initially read-only
    assert not (os.stat(protected_file).st_mode & stat.S_IWUSR)

    force_rmtree(base_dir)

    assert not base_dir.exists()

def test_force_rmtree_chmod_failure(protected_dir):
    """Test that force_rmtree handles chmod failures gracefully."""
    base_dir, protected_file = protected_dir

    with patch("os.chmod", side_effect=OSError("chmod failed")):
        force_rmtree(base_dir)
        # The directory should still be removed
        assert not base_dir.exists()

def test_force_rmtree_unlink_failure(protected_dir):
    """Test that force_rmtree handles unlink failures gracefully."""
    base_dir, protected_file = protected_dir

    with patch("os.unlink", side_effect=OSError("unlink failed")):
        force_rmtree(base_dir)
        # The directory should still exist because the onerror swallows the exception
        assert base_dir.exists()

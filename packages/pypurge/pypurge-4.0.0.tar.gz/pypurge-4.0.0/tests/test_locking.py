# tests/test_locking.py

import shutil
import unittest
from pathlib import Path
from pyfakefs import fake_filesystem_unittest
import os
import time
import signal

from pypurge.modules.locking import acquire_lock, release_lock, _pid_alive


class TestLocking(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()
        self.lock_path = Path("test.lock")
        # No need for shutil.rmtree or unlink as pyfakefs starts with empty fs

    def tearDown(self):
        if self.lock_path.is_dir():
            shutil.rmtree(self.lock_path)
        elif self.lock_path.exists():
            self.lock_path.unlink()

    def test_acquire_and_release_lock(self):
        lock_fd = acquire_lock(self.lock_path)
        self.assertIsNotNone(lock_fd)
        release_lock(lock_fd, self.lock_path)
        self.assertFalse(self.lock_path.exists())

    def test_lock_contention(self):
        lock_fd1 = acquire_lock(self.lock_path)
        self.assertIsNotNone(lock_fd1)
        lock_fd2 = acquire_lock(self.lock_path)
        self.assertIsNone(lock_fd2)
        release_lock(lock_fd1, self.lock_path)

    def test_stale_lock(self):
        lock_fd1 = acquire_lock(self.lock_path, stale_seconds=-1)
        self.assertIsNotNone(lock_fd1)
        release_lock(lock_fd1, self.lock_path)
        lock_fd2 = acquire_lock(self.lock_path, stale_seconds=-1)
        self.assertIsNotNone(lock_fd2)
        release_lock(lock_fd2, self.lock_path)

    def test_lock_file_is_dir(self):
        self.lock_path.mkdir()
        lock_fd = acquire_lock(self.lock_path)
        self.assertIsNone(lock_fd)

    def test_pid_alive_negative_pid(self):
        self.assertFalse(_pid_alive(-1))

    def test_pid_alive_nonexistent_pid(self):
        with unittest.mock.patch("os.kill", side_effect=ProcessLookupError):
            self.assertFalse(_pid_alive(99999)) # A PID that likely doesn't exist

    def test_pid_alive_permission_denied(self):
        with unittest.mock.patch("os.kill", side_effect=PermissionError):
            self.assertTrue(_pid_alive(1)) # PID 1 usually exists, but permission denied

    def test_pid_alive_other_exception(self):
        with unittest.mock.patch("os.kill", side_effect=Exception("Some other error")):
            self.assertTrue(_pid_alive(1)) # PID 1 usually exists, but some other error

    def test_pid_alive_windows_path(self):
        with unittest.mock.patch("os.kill", side_effect=Exception("Mocked os.kill exception")):
            with unittest.mock.patch("sys.platform", "win32"):
                mock_psutil = unittest.mock.Mock()
                mock_psutil.pid_exists.return_value = True
                with unittest.mock.patch.dict("sys.modules", {"psutil": mock_psutil}):
                    self.assertTrue(_pid_alive(123))
                    mock_psutil.pid_exists.assert_called_once_with(123)

    def test_pid_alive_windows_path_psutil_exception(self):
        with unittest.mock.patch("os.kill", side_effect=Exception("Mocked os.kill exception")):
            with unittest.mock.patch("sys.platform", "win32"):
                mock_psutil = unittest.mock.Mock()
                mock_psutil.pid_exists.side_effect = Exception("psutil error")
                with unittest.mock.patch.dict("sys.modules", {"psutil": mock_psutil}):
                    self.assertTrue(_pid_alive(123)) # Should return True on exception

if __name__ == "__main__":
    unittest.main()

# tests/test_backup.py

import shutil
import unittest
import unittest.mock
import zipfile
from pathlib import Path
from pyfakefs import fake_filesystem_unittest

from pypurge.modules.backup import backup_targets_atomic


class TestBackup(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()  # Initialize fake filesystem first
        self.test_dir = Path("test_backup_dir")
        self.fs.create_dir(self.test_dir)  # Create directory in fake filesystem

        self.backup_dir = Path("backup_dir")
        self.fs.create_dir(self.backup_dir)  # Create directory in fake filesystem

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        shutil.rmtree(self.backup_dir)

    def test_backup_targets_atomic(self):
        # Create test files and directories
        (self.test_dir / "file1.txt").write_text("hello")
        (self.test_dir / "subdir").mkdir()
        (self.test_dir / "subdir" / "file2.txt").write_text("world")
        targets = [self.test_dir / "file1.txt", self.test_dir / "subdir"]

        # Run the backup function
        result = backup_targets_atomic(targets, self.backup_dir, self.test_dir)
        self.assertIsNotNone(result)
        archive_path, sha = result
        self.assertTrue(archive_path.exists())
        self.assertTrue(archive_path.with_suffix(archive_path.suffix + ".sha256").exists())

        # Verify the contents of the zip file
        with zipfile.ZipFile(archive_path, "r") as zf:
            self.assertIn("file1.txt", zf.namelist())
            self.assertIn("subdir/file2.txt", zf.namelist())

    def test_backup_with_custom_name(self):
        (self.test_dir / "file1.txt").write_text("hello")
        targets = [self.test_dir / "file1.txt"]
        result = backup_targets_atomic(
            targets, self.backup_dir, self.test_dir, name="custom"
        )
        self.assertIsNotNone(result)
        archive_path, _ = result
        self.assertTrue(archive_path.name.startswith("custom_"))

    def test_backup_with_symlink(self):
        (self.test_dir / "file1.txt").write_text("hello")
        (self.test_dir / "link").symlink_to(self.test_dir / "file1.txt")
        targets = [self.test_dir / "link"]
        result = backup_targets_atomic(targets, self.backup_dir, self.test_dir)
        self.assertIsNotNone(result)
        archive_path, _ = result
        with zipfile.ZipFile(archive_path, "r") as zf:
            self.assertIn("cleanpy_symlink_manifest.json", zf.namelist())

    def test_backup_empty_targets(self):
        result = backup_targets_atomic([], self.backup_dir, self.test_dir)
        self.assertIsNotNone(result)
        archive_path, _ = result
        self.assertTrue(archive_path.exists())

    def test_backup_nonexistent_backup_root(self):
        backup_dir = Path("nonexistent_backup_dir")
        (self.test_dir / "file1.txt").write_text("hello")
        targets = [self.test_dir / "file1.txt"]
        result = backup_targets_atomic(targets, backup_dir, self.test_dir)
        self.assertIsNotNone(result)
        archive_path, _ = result
        self.assertTrue(archive_path.exists())
        shutil.rmtree(backup_dir)

    def test_backup_failure(self):
        with unittest.mock.patch("zipfile.ZipFile", side_effect=Exception):
            result = backup_targets_atomic([], self.backup_dir, self.test_dir)
            self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()

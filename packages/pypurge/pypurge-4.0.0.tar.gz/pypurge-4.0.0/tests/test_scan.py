# tests/test_scan.py

import shutil
import unittest
from pathlib import Path
from pyfakefs import fake_filesystem_unittest

from pypurge.modules.scan import scan_for_targets


class TestScan(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()  # Initialize fake filesystem first
        self.test_dir = Path("test_scan_dir")
        self.fs.create_dir(self.test_dir)  # Create directory in fake filesystem

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_scan_for_targets(self):
        # Create test files and directories
        (self.test_dir / "__pycache__").mkdir()
        (self.test_dir / "file1.pyc").touch()
        (self.test_dir / ".git").mkdir()
        (self.test_dir / "subdir").mkdir()
        (self.test_dir / "subdir" / "file2.pyc").touch()

        # Define scan parameters
        dir_groups = {"Python Caches": ["__pycache__"]}
        file_groups = {"Python Bytecode": ["*.pyc"]}
        exclude_dirs = {".git"}
        exclude_patterns = []
        older_than_sec = 0
        age_type = "mtime"
        delete_symlinks = False

        # Run the scan function
        targets = scan_for_targets(
            self.test_dir,
            dir_groups,
            file_groups,
            exclude_dirs,
            exclude_patterns,
            older_than_sec,
            age_type,
            delete_symlinks,
        )

        # Verify the results
        self.assertIn(
            self.test_dir / "__pycache__", targets["Python Caches"]
        )
        self.assertIn(
            self.test_dir / "file1.pyc", targets["Python Bytecode"]
        )
        all_targets = [p for p_list in targets.values() for p in p_list]
        self.assertNotIn(".git", [d.name for d in all_targets])
        self.assertIn(
            self.test_dir / "subdir" / "file2.pyc",
            targets["Python Bytecode"],
        )

    def test_scan_with_exclude_patterns(self):
        (self.test_dir / "file1.pyc").touch()
        (self.test_dir / "file2.log").touch()
        file_groups = {"all": ["*.pyc", "*.log"]}
        exclude_patterns = [("glob", "*.log")]
        targets = scan_for_targets(
            self.test_dir, {}, file_groups, set(), exclude_patterns, 0, "mtime", False
        )
        self.assertIn(self.test_dir / "file1.pyc", targets["all"])
        self.assertNotIn(self.test_dir / "file2.log", targets.get("all", []))

    def test_scan_older_than(self):
        (self.test_dir / "file1.pyc").touch()
        file_groups = {"all": ["*.pyc"]}
        targets = scan_for_targets(
            self.test_dir, {}, file_groups, set(), [], 1, "mtime", False
        )
        self.assertNotIn(self.test_dir / "file1.pyc", targets.get("all", []))

    def test_scan_with_symlinks(self):
        (self.test_dir / "file1.pyc").touch()
        (self.test_dir / "link").symlink_to(self.test_dir / "file1.pyc")
        file_groups = {"all": ["link"]}
        targets = scan_for_targets(
            self.test_dir, {}, file_groups, set(), [], 0, "mtime", True
        )
        self.assertIn(self.test_dir / "link", targets["all"])


if __name__ == "__main__":
    unittest.main()

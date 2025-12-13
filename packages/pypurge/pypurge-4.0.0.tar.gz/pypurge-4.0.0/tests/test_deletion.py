# tests/test_deletion.py

import shutil
import unittest
from pathlib import Path

from pypurge.modules.deletion import force_rmtree, force_unlink


class TestDeletion(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_dir")
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir()
        self.test_file = Path("test_file.txt")
        if self.test_file.exists():
            self.test_file.unlink()

    def tearDown(self):
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        if self.test_file.exists():
            self.test_file.unlink()

    def test_force_unlink(self):
        with open(self.test_file, "w") as f:
            f.write("hello")
        force_unlink(self.test_file)
        self.assertFalse(self.test_file.exists())

    def test_force_rmtree(self):
        with open(self.test_dir / "test_file.txt", "w") as f:
            f.write("hello")
        force_rmtree(self.test_dir)
        self.assertFalse(self.test_dir.exists())

    def test_force_rmtree_nonexistent(self):
        force_rmtree(Path("nonexistent_dir"))
        self.assertFalse(Path("nonexistent_dir").exists())

if __name__ == "__main__":
    unittest.main()

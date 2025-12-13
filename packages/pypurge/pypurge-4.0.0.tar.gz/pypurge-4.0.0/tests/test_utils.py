# tests/test_utils.py

import shutil
import unittest
from pathlib import Path
from pypurge.modules.utils import (
    format_bytes,
    get_size,
    is_old_enough,
    sha256_of_file,
)


class TestUtils(unittest.TestCase):
    def test_format_bytes(self):
        self.assertEqual(format_bytes(1024), "1.00KB")
        self.assertEqual(format_bytes(1024 * 1024), "1.00MB")

    def test_get_size(self):
        with open("test_file.txt", "w") as f:
            f.write("hello")
        self.assertEqual(get_size(Path("test_file.txt")), 5)
        Path("test_file.txt").unlink()

        test_dir = Path("test_dir")
        if test_dir.exists():
            shutil.rmtree(test_dir)
        test_dir.mkdir()
        with open(test_dir / "test_file.txt", "w") as f:
            f.write("hello")
        self.assertEqual(get_size(test_dir), 5)
        shutil.rmtree(test_dir)

    def test_is_old_enough(self):
        with open("test_file.txt", "w") as f:
            f.write("hello")
        self.assertFalse(is_old_enough(Path("test_file.txt"), 100, "mtime"))
        self.assertTrue(is_old_enough(Path("test_file.txt"), -100, "mtime"))
        Path("test_file.txt").unlink()

    def test_sha256_of_file(self):
        with open("test_file.txt", "w") as f:
            f.write("hello")
        self.assertEqual(
            sha256_of_file(Path("test_file.txt")),
            "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824",
        )
        Path("test_file.txt").unlink()


if __name__ == "__main__":
    unittest.main()

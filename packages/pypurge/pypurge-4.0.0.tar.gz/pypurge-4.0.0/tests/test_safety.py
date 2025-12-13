# tests/test_safety.py

import unittest
from pathlib import Path
from pypurge.modules.safety import is_dangerous_root


class TestSafety(unittest.TestCase):
    def test_is_dangerous_root(self):
        self.assertTrue(is_dangerous_root(Path("/")))
        self.assertTrue(is_dangerous_root(Path.home()))
        self.assertFalse(is_dangerous_root(Path("./safe_dir")))
        self.assertTrue(is_dangerous_root(Path("/usr")))
        self.assertTrue(is_dangerous_root(Path("/etc")))
        self.assertTrue(is_dangerous_root(Path("/var")))
        self.assertTrue(is_dangerous_root(Path("/tmp")))


if __name__ == "__main__":
    unittest.main()

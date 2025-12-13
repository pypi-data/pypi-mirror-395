# tests/test_ui.py

import io
import shutil
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from pypurge.modules.ui import (
    Colors,
    NullColors,
    get_colors,
    print_error,
    print_info,
    print_rich_preview,
    print_success,
    print_warning,
    summarize_groups,
)


class TestUi(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path("test_ui_dir")
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        self.test_dir.mkdir()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_colors(self):
        self.assertIsInstance(get_colors(True), Colors)
        self.assertIsInstance(get_colors(False), NullColors)

    def test_print_functions(self):
        colors = get_colors(False)
        with io.StringIO() as buf, redirect_stdout(buf):
            print_info("info", colors)
            self.assertIn("info", buf.getvalue())
        with io.StringIO() as buf, redirect_stdout(buf):
            print_success("success", colors)
            self.assertIn("success", buf.getvalue())
        with io.StringIO() as buf, redirect_stdout(buf):
            print_warning("warning", colors)
            self.assertIn("warning", buf.getvalue())
        with io.StringIO() as buf, redirect_stdout(buf):
            print_error("error", colors)
            self.assertIn("error", buf.getvalue())

    def test_print_rich_preview_truncation(self):
        """Test preview output truncation when many items exist."""
        targets = {"group1": []}
        sizes = {}
        for i in range(35):
            p = self.test_dir / f"file{i}"
            p.touch()
            targets["group1"].append(p)
            sizes[p] = 10
            
        colors = get_colors(True)
        with io.StringIO() as buf, redirect_stdout(buf):
            print_rich_preview(self.test_dir, targets, sizes, colors)
            output = buf.getvalue()
            self.assertIn("more items in this group", output)

    def test_summarize_groups(self):
        (self.test_dir / "file1").write_text("hello")
        (self.test_dir / "file2").write_text("world")
        targets = {
            "group1": [self.test_dir / "file1"],
            "group2": [self.test_dir / "file2"],
        }
        summary = summarize_groups(targets)
        self.assertEqual(len(summary), 2)
        self.assertEqual(summary[0][0], "group1")
        self.assertEqual(summary[0][1], 1)
        self.assertEqual(summary[0][2], 5)

    def test_print_rich_preview(self):
        (self.test_dir / "file1").write_text("hello")
        targets = {"group1": [self.test_dir / "file1"]}
        sizes = {self.test_dir / "file1": 5}
        colors = get_colors(False)
        with io.StringIO() as buf, redirect_stdout(buf):
            print_rich_preview(self.test_dir, targets, sizes, colors)
            output = buf.getvalue()
            self.assertIn("group1", output)
            self.assertIn("file1", output)


if __name__ == "__main__":
    unittest.main()

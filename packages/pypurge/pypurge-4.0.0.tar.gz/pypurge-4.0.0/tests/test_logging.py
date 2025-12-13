# tests/test_logging.py

import logging
import shutil
import unittest
from pathlib import Path
from unittest.mock import patch

from pypurge.modules.logging import setup_logging


class TestLogging(unittest.TestCase):
    def setUp(self):
        self.log_file = Path("test.log")
        if self.log_file.exists():
            self.log_file.unlink()

    def tearDown(self):
        if self.log_file.exists():
            self.log_file.unlink()

    def test_setup_logging_text(self):
        setup_logging("text", self.log_file, logging.INFO)
        logger = logging.getLogger("pypurge")
        logger.info("test")
        self.assertTrue(self.log_file.exists())
        self.assertIn("test", self.log_file.read_text())

    def test_setup_logging_json(self):
        setup_logging("json", self.log_file, logging.INFO)
        logger = logging.getLogger("pypurge")
        logger.info("test")
        self.assertTrue(self.log_file.exists())
        self.assertIn('"msg": "test"', self.log_file.read_text())

    def test_setup_logging_no_rotate(self):
        setup_logging("text", self.log_file, logging.INFO, rotate=False)
        logger = logging.getLogger("pypurge")
        logger.info("test")
        self.assertTrue(self.log_file.exists())


    def test_setup_logging_file_handler_fail(self):
        with patch("logging.FileHandler", side_effect=Exception("Mocked FileHandler Error")):
            with self.assertLogs("pypurge.modules.logging", level="WARNING") as cm:
                setup_logging("text", self.log_file, logging.INFO, rotate=False)
                self.assertIn("Failed to open log file", cm.output[0])
        self.assertFalse(self.log_file.exists())


if __name__ == "__main__":
    unittest.main()

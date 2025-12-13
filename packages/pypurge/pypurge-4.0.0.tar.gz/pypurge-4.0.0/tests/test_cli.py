# tests/test_cli.py

import shutil
import unittest
import unittest.mock
from pathlib import Path
from pyfakefs import fake_filesystem_unittest

from pypurge.cli import main


class TestCli(fake_filesystem_unittest.TestCase):
    def setUp(self):
        self.setUpPyfakefs()  # Initialize fake filesystem first
        self.test_dir = Path("test_cli_dir")
        self.fs.create_dir(self.test_dir)  # Create directory in fake filesystem

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_main_with_preview(self):
        (self.test_dir / "__pycache__").mkdir()
        argv = ["--preview", "--allow-root", "--allow-broad-root", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_version(self):
        argv = ["--version"]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_yes(self):
        (self.test_dir / "__pycache__").mkdir()
        argv = ["--yes", "--allow-root", "--allow-broad-root", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_clean_venv(self):
        (self.test_dir / ".venv").mkdir()
        argv = ["--yes", "--clean-venv", "--allow-root", "--allow-broad-root", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_exclude(self):
        (self.test_dir / "file.pyc").touch()
        argv = ["--yes", "--exclude", "*.pyc", "--allow-root", "--allow-broad-root", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)
        self.assertTrue((self.test_dir / "file.pyc").exists())

    def test_main_with_older_than(self):
        (self.test_dir / "file.pyc").touch()
        argv = ["--yes", "--older-than", "1", "--allow-root", "--allow-broad-root", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)
        self.assertTrue((self.test_dir / "file.pyc").exists())

    def test_main_with_force(self):
        (self.test_dir / "file.pyc").touch()
        argv = ["--yes", "--force", "--allow-root", "--allow-broad-root", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_backup(self):
        (self.test_dir / "file.pyc").touch()
        argv = ["--yes", "--backup", "--allow-root", "--allow-broad-root", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_no_color(self):
        (self.test_dir / "file.pyc").touch()
        argv = ["--yes", "--no-color", "--allow-root", "--allow-broad-root", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_delete_symlinks(self):
        (self.test_dir / "file.pyc").touch()
        (self.test_dir / "link").symlink_to(self.test_dir / "file.pyc")
        argv = ["--yes", "--delete-symlinks", "--allow-root", "--allow-broad-root", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_allow_broad_root(self):
        (self.test_dir / "__pycache__").mkdir()
        argv = ["--yes", "--allow-broad-root", "--allow-root", "/"]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_allow_root(self):
        (self.test_dir / "__pycache__").mkdir()
        argv = ["--yes", "--allow-root", "--allow-broad-root", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)

    def test_main_with_interactive_prompt_no(self):
        (self.test_dir / "__pycache__").mkdir()
        argv = ["--allow-root", "--allow-broad-root", str(self.test_dir)]
        with unittest.mock.patch("builtins.input", return_value="n"):
            exit_code = main(argv)
        self.assertEqual(exit_code, 2)

    def test_main_with_config_file(self):
        import json

        config = {"exclude_patterns": ["*.pyc"]}
        (self.test_dir / ".pypurge.json").write_text(json.dumps(config))
        file_path = self.test_dir / "file.pyc"
        file_path.touch()
        print(f"DEBUG: file_path exists before main: {file_path.exists()}")
        argv = ["--yes", "--allow-root", "--allow-broad-root", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)
        print(f"DEBUG: file_path exists after main: {file_path.exists()}")
        self.assertTrue(file_path.exists())

    def test_main_with_log_file(self):
        (self.test_dir / "file.pyc").touch()
        argv = ["--yes", "--log-file", "test.log", "--allow-root", "--allow-broad-root", str(self.test_dir)]
        exit_code = main(argv)
        self.assertEqual(exit_code, 0)
        self.assertTrue(Path("test.log").exists())
        Path("test.log").unlink()

    def test_main_signal_handling(self):
        import signal
        with unittest.mock.patch("signal.signal") as mock_signal:
            with unittest.mock.patch("sys.exit") as mock_sys_exit:
                with unittest.mock.patch("builtins.input", return_value="y"): # Mock input
                    # Create a dummy file to trigger cleanup logic
                    (self.test_dir / "__pycache__").mkdir()
                    argv = [str(self.test_dir), "--allow-root", "--allow-broad-root"]
                    main(argv) # Call main, which will register the signal handler

                    # Simulate sending a SIGINT
                    # The signal handler is registered with _release_all_and_exit
                    # We need to call the mock_signal's registered handler
                    # The handler is usually the second argument to signal.signal
                    # We assume SIGINT is registered.
                    registered_handler = mock_signal.call_args_list[0].args[1]
                    registered_handler(signal.SIGINT, None) # Call the handler directly

                    mock_sys_exit.assert_called_with(2) # EXIT_CANCELLED is 2


if __name__ == "__main__":
    unittest.main()

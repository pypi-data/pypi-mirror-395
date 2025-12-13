import json
import pytest
from unittest.mock import patch, mock_open
from pathlib import Path
from pypurge.modules.config_wizard import run_init_wizard

def test_wizard_happy_path(fs):
    """Test standard happy path with default answers."""
    # Inputs:
    # 1. Standard rules? y
    # 2. Custom dirs? (enter -> skip)
    # 3. Custom files? (enter -> skip)
    with patch("builtins.input", side_effect=["y", "", ""]):
        ret = run_init_wizard()
        assert ret == 0

    assert Path(".pypurge.json").exists()
    with open(".pypurge.json") as f:
        data = json.load(f)
        assert data["standard_rules"] is True
        assert data["exclude_dirs"] == []
        assert data["exclude_patterns"] == []

def test_wizard_custom_config(fs):
    """Test custom configuration entries."""
    inputs = [
        "n", # standard rules = no
        "node_modules, .venv", # custom dirs
        "*.log, temp_*" # custom files
    ]
    with patch("builtins.input", side_effect=inputs):
        ret = run_init_wizard()
        assert ret == 0

    with open(".pypurge.json") as f:
        data = json.load(f)
        assert data["standard_rules"] is False
        assert data["exclude_dirs"] == ["node_modules", ".venv"]
        assert data["exclude_patterns"] == ["*.log", "temp_*"]

def test_wizard_overwrite_abort(fs):
    """Test aborting when file exists."""
    fs.create_file(".pypurge.json", contents="{}")

    # inputs:
    # 1. Standard rules? y
    # 2. Custom dirs? ""
    # 3. Custom files? ""
    # 4. Overwrite? n
    inputs = ["y", "", "", "n"]
    with patch("builtins.input", side_effect=inputs):
        ret = run_init_wizard()
        assert ret == 0

    # Verify content wasn't changed
    with open(".pypurge.json") as f:
        assert f.read() == "{}"

def test_wizard_overwrite_confirm(fs):
    """Test overwriting when file exists."""
    fs.create_file(".pypurge.json", contents="old")

    inputs = ["y", "", "", "y"]
    with patch("builtins.input", side_effect=inputs):
        run_init_wizard()

    with open(".pypurge.json") as f:
        data = json.load(f)
        assert data["standard_rules"] is True

def test_wizard_overwrite_eof(fs):
    """Test EOF during overwrite prompt defaults to No."""
    fs.create_file(".pypurge.json", contents="old")

    # inputs:
    # 1. Standard rules? y
    # 2. Custom dirs? ""
    # 3. Custom files? ""
    # 4. Overwrite? EOF
    inputs = ["y", "", "", EOFError]

    # Side effect needs to handle mixed types if one is Exception class
    # But builtins.input side_effect can be an iterable.
    # If an element is an exception instance or class, it is raised.
    # However, list side_effect iterates.

    def side_effect(*args, **kwargs):
        val = inputs.pop(0)
        if val is EOFError:
            raise EOFError
        return val

    # We need a fresh inputs list for the side_effect function closure
    inputs = ["y", "", "", EOFError]

    with patch("builtins.input", side_effect=side_effect):
        ret = run_init_wizard()
        assert ret == 0

    # Should not have overwritten
    with open(".pypurge.json") as f:
        assert f.read() == "old"

def test_wizard_eof_defaults(fs):
    """Test EOFError triggers defaults."""
    with patch("builtins.input", side_effect=EOFError):
        ret = run_init_wizard()
        assert ret == 0

    with open(".pypurge.json") as f:
        data = json.load(f)
        assert data["standard_rules"] is True
        assert data["exclude_dirs"] == []
        assert data["exclude_patterns"] == []

def test_wizard_write_error(fs):
    """Test handling of write errors."""
    with patch("json.dump", side_effect=OSError("Disk full")):
        with patch("builtins.input", side_effect=["y", "", ""]):
            ret = run_init_wizard()
            assert ret == 1

# tests/test_safety_extra.py

import pytest
from pathlib import Path
from unittest.mock import MagicMock, patch
from pypurge.modules import safety

def test_is_dangerous_root_resolve_exception():
    """Test is_dangerous_root when resolve raises exception."""
    p = MagicMock()
    p.resolve.side_effect = Exception("Boom")
    assert safety.is_dangerous_root(p) is True

def test_is_dangerous_root_comparison_exception():
    """Test is_dangerous_root when comparison raises exception."""
    # We need to mock DANGEROUS_ROOTS to include something that causes exception during loop

    # If we inject a mock into DANGEROUS_ROOTS that raises exception on resolve()
    bad_root = MagicMock()
    bad_root.resolve.side_effect = Exception("Boom")

    # We need to patch DANGEROUS_ROOTS in the module
    # Since it's a set, we can construct a new set with our bad root

    with patch("pypurge.modules.safety.DANGEROUS_ROOTS", {bad_root}):
        # Passing a safe path
        p = Path("/safe/path/deep/enough")
        # It should continue past the exception and return False (if path is safe)
        assert safety.is_dangerous_root(p) is False

def test_is_dangerous_root_short_path():
    """Test is_dangerous_root with short paths."""
    # This covers line 26-27: if len(p_res.parts) <= 2: return True
    assert safety.is_dangerous_root(Path("/var")) is True
    assert safety.is_dangerous_root(Path("/tmp")) is True # /tmp is parts ('/', 'tmp') len=2
    assert safety.is_dangerous_root(Path("/")) is True # / is parts ('/',) len=1

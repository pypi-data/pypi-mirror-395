import json
import pytest
from pypurge.modules.config import validate_config, ConfigValidationError

def test_validate_config_valid(fs):
    """Test valid configuration passes validation."""
    valid_config = {
        "dir_groups": {"Custom": ["foo"]},
        "file_groups": {"Temp": ["*.tmp"]},
        "exclude_dirs": ["node_modules"],
        "exclude_patterns": ["*.bak"],
    }
    # It should not raise error
    validate_config(valid_config)

def test_validate_config_invalid_type(fs):
    """Test invalid configuration type raises error."""
    invalid_config = {
        "dir_groups": ["should be dict"],
    }
    with pytest.raises(ConfigValidationError) as excinfo:
        validate_config(invalid_config)
    assert "Configuration error" in str(excinfo.value)

def test_validate_config_invalid_structure(fs):
    """Test invalid structure (values not lists of strings)."""
    invalid_config = {
        "dir_groups": {"Custom": "should be list"},
    }
    with pytest.raises(ConfigValidationError) as excinfo:
        validate_config(invalid_config)
    assert "Configuration error" in str(excinfo.value)

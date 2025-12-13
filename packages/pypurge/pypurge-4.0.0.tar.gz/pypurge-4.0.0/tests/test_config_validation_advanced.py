import pytest
from pypurge.modules.config import validate_config, ConfigValidationError

def test_validate_config_invalid_regex(fs):
    """Test invalid regex in exclude_patterns raises ConfigValidationError."""
    invalid_config = {
        "exclude_patterns": ["re:[invalid_regex"],
    }
    with pytest.raises(ConfigValidationError) as excinfo:
        validate_config(invalid_config)

    assert "Invalid regex pattern" in str(excinfo.value) or "missing ]" in str(excinfo.value) or "unterminated character set" in str(excinfo.value)

def test_validate_config_valid_regex(fs):
    """Test valid regex in exclude_patterns passes validation."""
    valid_config = {
        "exclude_patterns": ["re:^test.*$"],
    }
    validate_config(valid_config)

def test_validate_config_mixed_patterns(fs):
    """Test mixed valid glob and regex patterns."""
    config = {
        "exclude_patterns": ["*.tmp", "re:^backup_\\d+"],
    }
    validate_config(config)

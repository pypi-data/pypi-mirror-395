# src/pypurge/modules/config.py

import json
import logging
import re
from pathlib import Path
from typing import Any

from jsonschema import validate, ValidationError

logger = logging.getLogger(__name__)

CONFIG_SCHEMA = {
    "type": "object",
    "properties": {
        "dir_groups": {
            "type": "object",
            "patternProperties": {
                ".*": {"type": "array", "items": {"type": "string"}}
            }
        },
        "file_groups": {
            "type": "object",
            "patternProperties": {
                ".*": {"type": "array", "items": {"type": "string"}}
            }
        },
        "exclude_dirs": {
            "type": "array",
            "items": {"type": "string"}
        },
        "exclude_patterns": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "additionalProperties": False
}

class ConfigValidationError(Exception):
    pass

def validate_config(config: dict[str, Any]) -> None:
    """
    Validates the configuration dictionary against the schema.
    Raises ConfigValidationError if invalid.
    """
    try:
        validate(instance=config, schema=CONFIG_SCHEMA)
    except ValidationError as e:
        raise ConfigValidationError(f"Configuration error: {e.message}") from e

    # Advanced Validation
    exclude_patterns = config.get("exclude_patterns", [])
    for pattern in exclude_patterns:
        if pattern.startswith("re:"):
            regex_str = pattern[3:]
            try:
                re.compile(regex_str)
            except re.error as e:
                raise ConfigValidationError(
                    f"Invalid regex pattern '{pattern}': {e}"
                )

def load_config(config_path: Path) -> dict[str, Any]:
    """
    Loads and validates the configuration from a file.
    """
    if not config_path.exists():
        return {}

    try:
        with open(config_path, "r") as f:
            config = json.load(f)

        validate_config(config)
        return config
    except json.JSONDecodeError as e:
        logger.error("Failed to parse config %s: %s", config_path, e)
        return {}
    except ConfigValidationError as e:
        logger.error("Invalid config %s: %s", config_path, e)
        return {}
    except Exception as e:
        logger.error("Unexpected error loading config %s: %s", config_path, e)
        return {}

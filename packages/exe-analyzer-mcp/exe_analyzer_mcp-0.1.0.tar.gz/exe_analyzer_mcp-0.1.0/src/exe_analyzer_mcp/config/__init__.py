"""Configuration module for exe-analyzer-mcp."""

import json
from pathlib import Path
from typing import Any

CONFIG_DIR = Path(__file__).parent


def load_config(filename: str) -> dict[str, Any]:
    """Load a JSON configuration file.

    Args:
        filename: Name of the configuration file (e.g., 'framework_signatures.json')

    Returns:
        Parsed JSON configuration as a dictionary
    """
    config_path = CONFIG_DIR / filename
    with open(config_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_framework_signatures() -> dict[str, Any]:
    """Load framework signature configuration."""
    return load_config("framework_signatures.json")


def load_compiler_signatures() -> dict[str, Any]:
    """Load compiler signature configuration."""
    return load_config("compiler_signatures.json")


def load_system_libraries() -> dict[str, Any]:
    """Load system libraries configuration."""
    return load_config("system_libraries.json")

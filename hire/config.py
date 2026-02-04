"""Configuration management."""

import json
from typing import Any

from .paths import get_config_path

DEFAULT_CONFIG = {
    "adapters": {
        "claude": {
            "command": "claude",
            "args": ["--dangerously-skip-permissions"]
        },
        "codex": {
            "command": "codex",
            "args": ["--full-auto"]
        },
        "gemini": {
            "command": "gemini",
            "args": ["-y"]
        }
    },
    "defaults": {
        "agent": "claude"
    }
}


def load_config() -> dict[str, Any]:
    """Load configuration from file, or return defaults."""
    config_path = get_config_path()
    if config_path.exists():
        with open(config_path) as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()


def save_config(config: dict[str, Any]) -> None:
    """Save configuration to file."""
    config_path = get_config_path()
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)


def get_adapter_config(agent: str) -> dict[str, Any]:
    """Get configuration for a specific adapter."""
    config = load_config()
    return config.get("adapters", {}).get(agent, {})

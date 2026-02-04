"""Configuration management."""

import copy
import json
from typing import Any

from .paths import get_config_path

# Default configuration
# NOTE: Auto-approve flags are enabled by default for convenience.
# These allow agents to execute actions without manual confirmation.
# Users can customize this in their config file (~/.hire/config.json).
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
        try:
            with open(config_path, encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError):
            # Fall back to defaults on error
            pass
    return copy.deepcopy(DEFAULT_CONFIG)


def save_config(config: dict[str, Any]) -> None:
    """Save configuration to file."""
    config_path = get_config_path()
    with open(config_path, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_adapter_config(agent: str) -> dict[str, Any]:
    """Get configuration for a specific adapter."""
    config = load_config()
    return config.get("adapters", {}).get(agent, {})

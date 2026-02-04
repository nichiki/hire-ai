"""XDG-compliant path management for hire CLI."""

import os
from pathlib import Path

APP_NAME = "hire"


def get_config_dir() -> Path:
    """Get XDG config directory (~/.config/hire/)."""
    xdg_config = os.environ.get("XDG_CONFIG_HOME", "")
    if xdg_config:
        base = Path(xdg_config)
    else:
        base = Path.home() / ".config"

    config_dir = base / APP_NAME
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir


def get_data_dir() -> Path:
    """Get XDG data directory (~/.local/share/hire/)."""
    xdg_data = os.environ.get("XDG_DATA_HOME", "")
    if xdg_data:
        base = Path(xdg_data)
    else:
        base = Path.home() / ".local" / "share"

    data_dir = base / APP_NAME
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir


def get_config_path() -> Path:
    """Get config file path (~/.config/hire/config.json)."""
    return get_config_dir() / "config.json"


def get_sessions_dir(agent: str | None = None) -> Path:
    """Get sessions directory for an agent.

    Args:
        agent: Agent name (claude, codex, gemini). If None, returns base sessions dir.

    Returns:
        Path to sessions directory.
    """
    sessions_dir = get_data_dir() / "sessions"
    if agent:
        sessions_dir = sessions_dir / agent
    sessions_dir.mkdir(parents=True, exist_ok=True)
    return sessions_dir

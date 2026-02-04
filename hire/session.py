"""Session management."""

import json
import uuid
from datetime import datetime
from typing import Any

from .paths import get_data_dir, get_sessions_dir


def create_session(agent: str, cli_session_id: str, name: str | None = None) -> dict[str, Any]:
    """Create a new session."""
    session = {
        "id": str(uuid.uuid4()),
        "cli_session_id": cli_session_id,
        "agent": agent,
        "name": name,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
    }
    save_session(session)
    return session


def save_session(session: dict[str, Any]) -> None:
    """Save a session to file."""
    session["updated_at"] = datetime.now().isoformat()
    sessions_dir = get_sessions_dir(session["agent"])

    # Use session ID as filename (1 file per session)
    filename = f"{session['id']}.json"
    filepath = sessions_dir / filename

    with open(filepath, "w") as f:
        json.dump(session, f, indent=2)

    # Update latest pointer
    latest_path = sessions_dir / "latest.json"
    with open(latest_path, "w") as f:
        json.dump({"session_id": session["id"], "filename": filename}, f)


def get_latest_session(agent: str) -> dict[str, Any] | None:
    """Get the latest session for an agent."""
    sessions_dir = get_sessions_dir(agent)
    latest_path = sessions_dir / "latest.json"

    if not latest_path.exists():
        return None

    with open(latest_path) as f:
        latest = json.load(f)

    filepath = sessions_dir / latest["filename"]
    if not filepath.exists():
        return None

    with open(filepath) as f:
        return json.load(f)


def get_session_by_id(session_id: str) -> dict[str, Any] | None:
    """Get a session by its ID (searches all agents)."""
    sessions_base = get_sessions_dir()

    if not sessions_base.exists():
        return None

    for agent_dir in sessions_base.iterdir():
        if not agent_dir.is_dir():
            continue
        for session_file in agent_dir.glob("*.json"):
            if session_file.name == "latest.json":
                continue
            with open(session_file) as f:
                session = json.load(f)
                if session["id"] == session_id or session["id"].startswith(session_id):
                    return session
    return None


def get_session_by_name(name: str) -> dict[str, Any] | None:
    """Get a session by its name (searches all agents)."""
    sessions_base = get_sessions_dir()

    if not sessions_base.exists():
        return None

    for agent_dir in sessions_base.iterdir():
        if not agent_dir.is_dir():
            continue
        for session_file in agent_dir.glob("*.json"):
            if session_file.name == "latest.json":
                continue
            with open(session_file) as f:
                session = json.load(f)
                if session.get("name") == name:
                    return session
    return None


def find_session(name_or_id: str) -> dict[str, Any] | None:
    """Find a session by name or ID."""
    # Try by name first
    session = get_session_by_name(name_or_id)
    if session:
        return session

    # Then try by ID
    return get_session_by_id(name_or_id)


def list_sessions(agent: str | None = None) -> list[dict[str, Any]]:
    """List all sessions, optionally filtered by agent."""
    sessions_base = get_sessions_dir()

    if not sessions_base.exists():
        return []

    sessions = []

    if agent:
        agent_dirs = [sessions_base / agent]
    else:
        agent_dirs = [d for d in sessions_base.iterdir() if d.is_dir()]

    for agent_dir in agent_dirs:
        if not agent_dir.exists():
            continue
        for session_file in agent_dir.glob("*.json"):
            if session_file.name == "latest.json":
                continue
            with open(session_file) as f:
                sessions.append(json.load(f))

    # Sort by updated_at descending
    sessions.sort(key=lambda s: s.get("updated_at", ""), reverse=True)
    return sessions


def delete_session(session: dict[str, Any]) -> bool:
    """Delete a session."""
    sessions_dir = get_sessions_dir(session["agent"])

    # Find and delete the session file
    for session_file in sessions_dir.glob("*.json"):
        if session_file.name == "latest.json":
            continue
        with open(session_file) as f:
            s = json.load(f)
            if s["id"] == session["id"]:
                session_file.unlink()

                # Update latest if needed
                latest_path = sessions_dir / "latest.json"
                if latest_path.exists():
                    with open(latest_path) as f:
                        latest = json.load(f)
                    if latest["session_id"] == session["id"]:
                        latest_path.unlink()

                return True
    return False

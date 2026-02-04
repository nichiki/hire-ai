"""Delete command implementation."""

import sys
from argparse import Namespace

from ..session import delete_session, find_session, list_sessions


def run_delete(args: Namespace) -> int:
    """Run the delete command."""
    name_or_id = getattr(args, "name_or_id", None)
    delete_all = getattr(args, "all", False)
    force = getattr(args, "force", False)

    # Delete all sessions
    if delete_all:
        sessions = list_sessions()
        if not sessions:
            print("No sessions to delete")
            return 0

        # Confirm deletion unless --force
        if not force:
            print(f"Delete all {len(sessions)} session(s)?")
            response = input("Type 'yes' to confirm: ")
            if response.lower() != "yes":
                print("Cancelled")
                return 0

        deleted = 0
        for session in sessions:
            if delete_session(session):
                deleted += 1

        print(f"Deleted {deleted} session(s)")
        return 0

    # Delete single session
    if not name_or_id:
        print("Error: Session name or ID required (or use --all)", file=sys.stderr)
        return 1

    try:
        session = find_session(name_or_id)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if not session:
        print(f"Error: Session not found: {name_or_id}", file=sys.stderr)
        return 1

    # Confirm deletion unless --force
    if not force:
        agent = session.get("agent", "")
        name = session.get("name", "-")
        print(f"Delete session {session['id'][:8]} ({agent}, name={name})?")
        response = input("Type 'yes' to confirm: ")
        if response.lower() != "yes":
            print("Cancelled")
            return 0

    if delete_session(session):
        print(f"Deleted session: {session['id'][:8]}")
        return 0
    else:
        print(f"Error: Failed to delete session", file=sys.stderr)
        return 1

"""Delete command implementation."""

import sys
from argparse import Namespace

from ..session import delete_session, find_session


def run_delete(args: Namespace) -> int:
    """Run the delete command."""
    name_or_id = args.name_or_id
    force = getattr(args, "force", False)

    session = find_session(name_or_id)

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

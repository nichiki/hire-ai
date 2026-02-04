"""Sessions command implementation."""

import json
from argparse import Namespace

from ..session import list_sessions


def run_sessions(args: Namespace) -> int:
    """Run the sessions command."""
    target = args.target
    output_json = getattr(args, "json", False)

    sessions = list_sessions(agent=target)

    if output_json:
        print(json.dumps(sessions, indent=2, ensure_ascii=False))
    else:
        if not sessions:
            if target:
                print(f"No sessions found for {target}")
            else:
                print("No sessions found")
            return 0

        # Print table header
        print(f"{'AGENT':<10} {'NAME':<20} {'ID':<10} {'UPDATED':<20}")
        print("-" * 62)

        for session in sessions:
            agent = session.get("agent", "")
            name = session.get("name", "-") or "-"
            session_id = session.get("id", "")[:8]
            updated = session.get("updated_at", "")[:19].replace("T", " ")

            print(f"{agent:<10} {name:<20} {session_id:<10} {updated:<20}")

    return 0

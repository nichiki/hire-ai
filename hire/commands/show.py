"""Show command implementation."""

import json
import sys
from argparse import Namespace

from ..session import find_session


def run_show(args: Namespace) -> int:
    """Run the show command."""
    name_or_id = args.name_or_id
    output_json = getattr(args, "json", False)

    try:
        session = find_session(name_or_id)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

    if not session:
        print(f"Error: Session not found: {name_or_id}", file=sys.stderr)
        return 1

    if output_json:
        print(json.dumps(session, indent=2, ensure_ascii=False))
    else:
        print(f"Session: {session.get('id')}")
        print(f"Agent:   {session.get('agent')}")
        print(f"Name:    {session.get('name', '-')}")
        print(f"CLI ID:  {session.get('cli_session_id')}")
        print(f"Created: {session.get('created_at')}")
        print(f"Updated: {session.get('updated_at')}")

    return 0

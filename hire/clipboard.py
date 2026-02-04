"""Clipboard utilities."""

import platform
import subprocess


def copy_to_clipboard(text: str) -> bool:
    """Copy text to system clipboard. Returns True on success."""
    system = platform.system()
    try:
        if system == "Darwin":  # macOS
            # Don't override env - let system locale handle it
            subprocess.run(
                ["pbcopy"],
                input=text,
                text=True,
                encoding="utf-8",
                check=True,
            )
        elif system == "Linux":
            # Try xclip first, fall back to xsel
            try:
                subprocess.run(
                    ["xclip", "-selection", "clipboard"],
                    input=text.encode("utf-8"),
                    check=True,
                )
            except FileNotFoundError:
                subprocess.run(
                    ["xsel", "--clipboard", "--input"],
                    input=text.encode("utf-8"),
                    check=True,
                )
        elif system == "Windows":
            subprocess.run(["clip"], input=text.encode("utf-8"), check=True)
        else:
            return False
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

"""Command modules.

Each command module exposes a stable run(...) -> int entry point.

The CLI parser lives in pup_clean.cli.
Behavior lives here.
"""

from pup_clean.commands import clean

__all__ = ["clean"]

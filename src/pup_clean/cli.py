"""Command-line interface.

This module parses arguments and
dispatches repository cleanup behavior.

Commands:
uv run pup-clean
uv run pup-clean --delete

Equivalent uvx usage after release:
uvx pup-clean
uvx pup-clean@latest
uvx pup-clean --delete
"""

import argparse
from collections.abc import Sequence
from pathlib import Path

from pup_clean.commands import clean

__all__ = ["build_parser", "main"]


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="pup-clean",
        description=(
            "Identify and remove known generated and disposable repository artifacts."
        ),
    )

    parser.add_argument(
        "--root",
        type=Path,
        default=None,
        help=(
            "Repository root to clean. Defaults to the nearest parent "
            "directory containing .git, or the current directory."
        ),
    )

    parser.add_argument(
        "--delete",
        action="store_true",
        help=(
            "Delete detected cleanup targets. Without this flag, "
            "pup-clean performs a dry run only."
        ),
    )

    parser.add_argument(
        "paths",
        nargs="*",
        type=Path,
        help=(
            "Optional repository-relative cleanup targets. "
            "When provided, operate only on detected targets matching these paths."
        ),
    )

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Run the command-line interface.

    Args:
        argv: Optional command-line arguments. If None, uses sys.argv.

    Returns:
        Exit code from the clean command.
    """
    parser = build_parser()
    args = parser.parse_args(argv)

    return clean.run(
        root=args.root,
        delete=args.delete,
        paths=tuple(args.paths),
    )


if __name__ == "__main__":
    raise SystemExit(main())

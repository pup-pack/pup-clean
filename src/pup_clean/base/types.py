"""Typed records."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

__all__ = [
    "CleanupKind",
    "CleanupTarget",
]


CleanupKind = Literal[
    "file",
    "directory",
]


@dataclass(frozen=True)
class CleanupTarget:
    """A known disposable repository target."""

    path: Path
    kind: CleanupKind

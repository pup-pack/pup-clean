"""Clean known disposable and source-generated repository artifacts."""

from importlib import resources
from pathlib import Path
import shutil
import tomllib
from typing import Any

from pup_core.inspect.detect import detect_repository
from pup_core.paths.safe import safe_repo_path

from pup_clean.base.types import CleanupTarget
from pup_clean.delete.terminal import print_cleanup_plan
from pup_clean.inspect.generated import discover_generated_paths

__all__ = ["run"]


def _load_defaults() -> dict[str, Any]:
    """Load explicit cleanup defaults from packaged TOML data."""
    defaults_file = (
        resources.files("pup_clean.commands").joinpath("data").joinpath("defaults.toml")
    )

    return tomllib.loads(defaults_file.read_text(encoding="utf-8"))


_DEFAULTS = _load_defaults()

_CLEANUP_FILES = tuple(_DEFAULTS["files"])
_CLEANUP_DIRECTORIES = tuple(_DEFAULTS["directories"])


def run(
    *,
    root: Path | None = None,
    delete: bool = False,
    paths: tuple[Path, ...] = (),
) -> int:
    """Preview or remove known disposable and generated repository artifacts.

    Args:
        root: Repository root. If None, detect the current repository root.
        delete: Whether to delete detected cleanup targets.
            False means dry-run only.
        paths: Optional repository-relative cleanup targets.
            When provided, operate only on detected targets matching these paths.

    Returns:
        Process exit code.
    """
    repository = detect_repository(root)
    targets = _detect_cleanup_targets(repository.root)

    if paths:
        selected_paths = set(paths)
        targets = tuple(target for target in targets if target.path in selected_paths)

    if delete:
        _delete_cleanup_targets(repository.root, targets)

    print_cleanup_plan(
        repository,
        targets,
        delete=delete,
    )

    return 0


def _detect_cleanup_targets(root: Path) -> tuple[CleanupTarget, ...]:
    """Detect explicit and source-generated cleanup targets."""
    targets: dict[Path, CleanupTarget] = {}

    # Explicit universal cleanup targets.
    for relative_path in _CLEANUP_FILES:
        absolute_path = safe_repo_path(root, relative_path)

        if absolute_path.is_file():
            path = Path(relative_path)
            targets[path] = CleanupTarget(
                path=path,
                kind="file",
            )

    for relative_path in _CLEANUP_DIRECTORIES:
        absolute_path = safe_repo_path(root, relative_path)

        if absolute_path.is_dir():
            path = Path(relative_path)
            targets[path] = CleanupTarget(
                path=path,
                kind="directory",
            )

    # Project-specific artifacts discovered by inspecting src/**/*.py.
    for relative_path in discover_generated_paths(root):
        absolute_path = safe_repo_path(root, relative_path)

        if absolute_path.is_file():
            targets[relative_path] = CleanupTarget(
                path=relative_path,
                kind="file",
            )

    return tuple(
        targets[path]
        for path in sorted(
            targets,
            key=lambda path: path.as_posix(),
        )
    )


def _delete_cleanup_targets(
    root: Path,
    targets: tuple[CleanupTarget, ...],
) -> None:
    """Delete detected cleanup targets."""
    for target in targets:
        absolute_path = safe_repo_path(root, target.path)

        if target.kind == "directory":
            if absolute_path.is_dir():
                shutil.rmtree(absolute_path)

        elif absolute_path.is_file():
            absolute_path.unlink()

"""Terminal reporting."""

from collections.abc import Sequence

from pup_core.base.types import RepositoryContext

from pup_clean.base.types import CleanupTarget

__all__ = ["print_cleanup_plan"]


def print_cleanup_plan(
    context: RepositoryContext,
    targets: Sequence[CleanupTarget],
    *,
    delete: bool,
) -> None:
    """Print the repository cleanup plan."""
    mode = "DELETE" if delete else "DRY RUN"

    print(f"[pup-clean] {mode}")  # noqa: T201
    print(f"[pup-clean] repo: {context.repo_name}")  # noqa: T201
    print(f"[pup-clean] root: {context.root}")  # noqa: T201
    print("")  # noqa: T201

    if not targets:
        print("[pup-clean] no cleanup targets found")  # noqa: T201
        return

    label = "DELETED" if delete else "WOULD DELETE"

    for target in targets:
        suffix = "/" if target.kind == "directory" else ""
        print(f"{label:13} {target.path.as_posix()}{suffix}")  # noqa: T201

    print("")  # noqa: T201
    print(f"[pup-clean] summary: {len(targets)} cleanup target(s)")  # noqa: T201

    if not delete:
        print(  # noqa: T201
            "[pup-clean] nothing deleted; rerun with --delete to apply cleanup"
        )

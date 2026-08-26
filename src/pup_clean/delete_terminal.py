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
    """Print the repository cleanup plan.

    Args:
        context (RepositoryContext): The repository context.
        targets (Sequence[CleanupTarget]): The list of cleanup targets.
        delete (bool): Whether to actually delete the targets or just perform a dry run.

    Returns:
        None
    """
    mode = "DELETE" if delete else "DRY RUN"

    print(f"[pup-clean] {mode}")
    print(f"[pup-clean] repo: {context.repo_name}")
    print(f"[pup-clean] root: {context.root}")
    print()

    if not targets:
        print("[pup-clean] no cleanup targets found")
        return

    label = "DELETED" if delete else "WOULD DELETE"

    for target in targets:
        suffix = "/" if target.kind == "directory" else ""
        print(f"{label:13} {target.path.as_posix()}{suffix}")

    print()
    print(f"[pup-clean] summary: {len(targets)} cleanup target(s)")

    if not delete:
        print("[pup-clean] nothing deleted; rerun with --delete to apply cleanup")

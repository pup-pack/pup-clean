"""Check the repository for self-consistency."""

from pathlib import Path

from pup_core.inspect.detect import detect_repository

from pup_clean.base.types import CheckResult
from pup_clean.checks.entry_points import check_entry_points
from pup_clean.checks.files import check_required_files
from pup_clean.checks.packages import check_package_structure
from pup_clean.checks.pyproject import check_pyproject
from pup_clean.delete.terminal import print_check_results

__all__ = ["run"]


def run(
    *,
    root: Path | None = None,
) -> int:
    """Check a repository for deterministic internal consistency.

    Args:
        root: Repository root. If None, detect the current repository root.

    Returns:
        Process exit code. Zero means all checks passed.
    """
    repository = detect_repository(root)

    results: list[CheckResult] = []

    results.extend(check_required_files(repository))

    pyproject_result = check_pyproject(repository.root)
    results.append(pyproject_result)

    results.append(check_package_structure(repository))

    if pyproject_result.passed:
        results.extend(check_entry_points(repository.root))

    print_check_results(repository, results)

    return 0 if all(result.passed for result in results) else 1

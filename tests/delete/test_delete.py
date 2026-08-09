"""Tests for pup-clean terminal reporting."""

from pathlib import Path

from pup_core.base.types import RepositoryContext
from pytest import CaptureFixture

from pup_clean.base.types import CleanupTarget
from pup_clean.delete.terminal import print_cleanup_plan


def _repository_context(tmp_path: Path) -> RepositoryContext:
    """Create a repository context for terminal reporting tests."""
    return RepositoryContext(
        root=tmp_path,
        github_handle="denisecase",
        repo_name="example-project",
        repo_url="https://github.com/denisecase/example-project",
        site_url="https://denisecase.github.io/example-project/",
        src_package="example_project",
        files=frozenset(),
    )


def test_print_cleanup_plan_dry_run(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    """Dry-run reporting should clearly show proposed deletions."""
    context = _repository_context(tmp_path)

    targets = (
        CleanupTarget(
            path=Path("project.log"),
            kind="file",
        ),
        CleanupTarget(
            path=Path("data/prepared/results.csv"),
            kind="file",
        ),
        CleanupTarget(
            path=Path("docs/images/generated_chart.png"),
            kind="file",
        ),
        CleanupTarget(
            path=Path(".pytest_cache"),
            kind="directory",
        ),
    )

    print_cleanup_plan(
        context,
        targets,
        delete=False,
    )

    captured = capsys.readouterr()

    assert "[pup-clean] DRY RUN" in captured.out
    assert "[pup-clean] repo: example-project" in captured.out
    assert f"[pup-clean] root: {tmp_path}" in captured.out

    assert "WOULD DELETE  project.log" in captured.out
    assert "WOULD DELETE  data/prepared/results.csv" in captured.out
    assert "WOULD DELETE  docs/images/generated_chart.png" in captured.out
    assert "WOULD DELETE  .pytest_cache/" in captured.out

    assert "[pup-clean] summary: 4 cleanup target(s)" in captured.out
    assert (
        "[pup-clean] nothing deleted; rerun with --delete to apply cleanup"
        in captured.out
    )


def test_print_cleanup_plan_delete(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    """Delete reporting should identify targets as deleted."""
    context = _repository_context(tmp_path)

    targets = (
        CleanupTarget(
            path=Path("project.log"),
            kind="file",
        ),
        CleanupTarget(
            path=Path("data/dw/sales.duckdb"),
            kind="file",
        ),
        CleanupTarget(
            path=Path("dist"),
            kind="directory",
        ),
    )

    print_cleanup_plan(
        context,
        targets,
        delete=True,
    )

    captured = capsys.readouterr()

    assert "[pup-clean] DELETE" in captured.out
    assert "DELETED       project.log" in captured.out
    assert "DELETED       data/dw/sales.duckdb" in captured.out
    assert "DELETED       dist/" in captured.out
    assert "[pup-clean] summary: 3 cleanup target(s)" in captured.out

    assert "WOULD DELETE" not in captured.out
    assert "nothing deleted" not in captured.out


def test_print_cleanup_plan_with_no_targets(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    """Reporting should handle a repository with nothing to clean."""
    context = _repository_context(tmp_path)

    print_cleanup_plan(
        context,
        (),
        delete=False,
    )

    captured = capsys.readouterr()

    assert "[pup-clean] DRY RUN" in captured.out
    assert "[pup-clean] repo: example-project" in captured.out
    assert "[pup-clean] no cleanup targets found" in captured.out

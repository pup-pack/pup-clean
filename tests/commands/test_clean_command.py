"""Tests for the clean command."""

from pathlib import Path

from pytest import CaptureFixture

from pup_clean.commands import clean


def test_clean_command_dry_run(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    """Dry run should report cleanup targets without deleting them."""
    (tmp_path / "project.log").write_text("Log content", encoding="utf-8")
    (tmp_path / ".coverage").write_text("Coverage data", encoding="utf-8")
    (tmp_path / ".mypy_cache").mkdir()
    (tmp_path / ".pytest_cache").mkdir()
    (tmp_path / ".ruff_cache").mkdir()
    (tmp_path / "build").mkdir()
    (tmp_path / "dist").mkdir()
    (tmp_path / "htmlcov").mkdir()
    (tmp_path / "site").mkdir()

    # Documentation source must be preserved.
    docs_images = tmp_path / "docs" / "images"
    docs_images.mkdir(parents=True)
    (docs_images / "example.png").write_text("keep", encoding="utf-8")

    exit_code = clean.run(root=tmp_path, delete=False)

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "[pup-clean] DRY RUN" in captured.out

    assert "WOULD DELETE  project.log" in captured.out
    assert "WOULD DELETE  .coverage" in captured.out
    assert "WOULD DELETE  .mypy_cache/" in captured.out
    assert "WOULD DELETE  .pytest_cache/" in captured.out
    assert "WOULD DELETE  .ruff_cache/" in captured.out
    assert "WOULD DELETE  build/" in captured.out
    assert "WOULD DELETE  dist/" in captured.out
    assert "WOULD DELETE  htmlcov/" in captured.out
    assert "WOULD DELETE  site/" in captured.out

    # The authored documentation file is not a cleanup target.
    assert "docs/images/example.png" not in captured.out

    # Dry run must not delete anything.
    assert (tmp_path / "project.log").exists()
    assert (tmp_path / ".coverage").exists()
    assert (tmp_path / ".mypy_cache").exists()
    assert (tmp_path / ".pytest_cache").exists()
    assert (tmp_path / ".ruff_cache").exists()
    assert (tmp_path / "build").exists()
    assert (tmp_path / "dist").exists()
    assert (tmp_path / "htmlcov").exists()
    assert (tmp_path / "site").exists()

    # Documentation source must remain untouched.
    assert (docs_images / "example.png").exists()


def test_clean_command_write(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    """Write mode should delete only detected cleanup targets."""
    (tmp_path / "project.log").write_text("Log content", encoding="utf-8")
    (tmp_path / ".coverage").write_text("Coverage data", encoding="utf-8")
    (tmp_path / ".mypy_cache").mkdir()
    (tmp_path / ".pytest_cache").mkdir()
    (tmp_path / ".ruff_cache").mkdir()
    (tmp_path / "build").mkdir()
    (tmp_path / "dist").mkdir()
    (tmp_path / "htmlcov").mkdir()
    (tmp_path / "site").mkdir()

    # Documentation source must be preserved.
    docs_images = tmp_path / "docs" / "images"
    docs_images.mkdir(parents=True)
    (docs_images / "example.png").write_text("keep", encoding="utf-8")

    exit_code = clean.run(root=tmp_path, delete=True)

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "[pup-clean] DELETE" in captured.out

    assert "DELETED       project.log" in captured.out
    assert "DELETED       .coverage" in captured.out
    assert "DELETED       .mypy_cache/" in captured.out
    assert "DELETED       .pytest_cache/" in captured.out
    assert "DELETED       .ruff_cache/" in captured.out
    assert "DELETED       build/" in captured.out
    assert "DELETED       dist/" in captured.out
    assert "DELETED       htmlcov/" in captured.out
    assert "DELETED       site/" in captured.out

    assert not (tmp_path / "project.log").exists()
    assert not (tmp_path / ".coverage").exists()
    assert not (tmp_path / ".mypy_cache").exists()
    assert not (tmp_path / ".pytest_cache").exists()
    assert not (tmp_path / ".ruff_cache").exists()
    assert not (tmp_path / "build").exists()
    assert not (tmp_path / "dist").exists()
    assert not (tmp_path / "htmlcov").exists()
    assert not (tmp_path / "site").exists()

    # Documentation source must remain untouched.
    assert (docs_images / "example.png").exists()


def test_clean_command_with_no_targets(
    tmp_path: Path,
    capsys: CaptureFixture[str],
) -> None:
    """A clean repository should succeed without deleting anything."""
    exit_code = clean.run(root=tmp_path, delete=False)

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "[pup-clean] no cleanup targets found" in captured.out

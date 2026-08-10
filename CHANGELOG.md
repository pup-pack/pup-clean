# Changelog

<!-- markdownlint-disable MD024 -->

All notable changes to this project will be documented in this file.

The format is based on **[Keep a Changelog](https://keepachangelog.com/en/1.1.0/)**
and this project adheres to **[Semantic Versioning](https://semver.org/spec/v2.0.0.html)**.

---

## [Unreleased]

---

## [0.1.1] - 2026-08-10

- updated the organization

---

## [0.1.0] - 2026-08-10

- transferred to pup-pack

---

## [0.0.5] - 2026-08-09

- updated README and docs/

---

## [0.0.4] - 2026-08-09

### Added

- Initial release of `pup-clean`.
- Added cleanup support for preparing instructor repositories for release as student project templates.
- Added dry-run cleanup reporting by default with explicit `--delete` required for deletion.
- Added removal of known generated development artifacts such as `project.log`,
  coverage output, caches, build artifacts, and generated documentation output.
- Added Python source inspection to discover project-specific generated data, database, and image artifacts.
- Added static path resolution for generated artifacts referenced through literals,
  `Path` objects, and simple path composition.
- Added conservative cleanup behavior that deletes only explicitly configured
  or confidently discovered generated artifacts.
- Added shared repository detection and safe repository-relative path handling using `pup-core`.
- Added concise terminal reporting of cleanup targets and actions.

---

## Notes on Versioning and Releases

- We use **SemVer**:
  - **MAJOR** - breaking changes
  - **MINOR** - backward-compatible additions
  - **PATCH** - fixes, documentation, tooling
- Versions are driven by git tags.
- Tag `vX.Y.Z` to release.
- Docs are deployed per version tag and aliased to **latest**.

## Release Procedure

Follow these steps when creating a new release.

### Task 1. Update release metadata

1. Update `CITATION.cff`: change `version` and `date-released`
2. Update `CHANGELOG.md`: move from unreleased, add entry, update links
3. Update `pyproject.toml`: update `[tool.hatch.version] fallback-version`

### Task 2. Validate

````shell
uv lock --upgrade
uv sync --upgrade
uv run pre-commit install

uv run pup-clean

git add -A
uv run pre-commit run --all-files
# rerun if changes made
uv run pre-commit run --all-files

uv run python -m pytest
uv run python -m pyright
uv run python -m zensical build

uv run python -c "import shutil; from pathlib import Path; shutil.rmtree(Path('dist'), ignore_errors=True)"

uv build
uvx twine check dist/*
```

### Task 4. Commit, push, tag

```shell
git add -A
git commit -m "Prepare X.Y.Z"
git push -u origin main
````

Verify actions run on GitHub. After success:

```shell
git tag vX.Y.Z -m "X.Y.Z"
git push origin vX.Y.Z
```

## Only As Needed (delete a tag)

```shell
git tag -d vX.Z.Y
git push origin :refs/tags/vX.Z.Y
```

## Links

[Unreleased]: https://github.com/pup-pack/pup-clean/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/pup-pack/pup-clean/releases/tag/v0.1.1
[0.1.0]: https://github.com/pup-pack/pup-clean/releases/tag/v0.1.0
[0.0.5]: https://github.com/pup-pack/pup-clean/releases/tag/v0.0.5
[0.0.4]: https://github.com/pup-pack/pup-clean/releases/tag/v0.0.4

<!-- markdownlint-enable MD024 -->

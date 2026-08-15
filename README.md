# pup-clean: Professional Python Project: Instructor Repo Cleaner

[![PyPI](https://img.shields.io/pypi/v/pup-clean?logo=pypi&label=pypi)](https://pypi.org/project/pup-clean/)
[![Docs Site](https://img.shields.io/badge/docs-site-blue?logo=github)](https://pup-pack.github.io/pup-clean/)
[![Repo](https://img.shields.io/badge/repo-GitHub-black?logo=github)](https://github.com/pup-pack/pup-clean)
[![Python 3.15](https://img.shields.io/badge/python-3.15%2B-blue?logo=python)](./pyproject.toml)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](./LICENSE)

[![CI](https://github.com/pup-pack/pup-clean/actions/workflows/ci-python-zensical.yml/badge.svg?branch=main)](https://github.com/pup-pack/pup-clean/actions/workflows/ci-python-zensical.yml)
[![Docs-Deploy](https://github.com/pup-pack/pup-clean/actions/workflows/deploy-zensical.yml/badge.svg?branch=main)](https://github.com/pup-pack/pup-clean/actions/workflows/deploy-zensical.yml)
[![Pre-Release](https://github.com/pup-pack/pup-clean/actions/workflows/pre-release.yml/badge.svg?branch=main)](https://github.com/pup-pack/pup-clean/actions/workflows/pre-release.yml)
[![Release](https://github.com/pup-pack/pup-clean/actions/workflows/release-pypi.yml/badge.svg)](https://github.com/pup-pack/pup-clean/actions/workflows/release-pypi.yml)
[![Links](https://github.com/pup-pack/pup-clean/actions/workflows/links.yml/badge.svg?branch=main)](https://github.com/pup-pack/pup-clean/actions/workflows/links.yml)
[![Dependabot](https://img.shields.io/badge/Dependabot-enabled-brightgreen.svg)](https://github.com/pup-pack/pup-clean/security)

<img
src="https://raw.githubusercontent.com/pup-pack/pup-clean/main/docs/images/pup.png"
alt="pup logo"
width="110">

> Opinionated professional Python repository cleaner

## Purpose

`pup-clean` prepares instructor repositories for release as student project
templates.

It removes known disposable development artifacts and inspects project source
code to discover generated data, database, and image artifacts that should not
be included in the student version of the repository.

Dry run is the default.
Nothing is deleted unless `--delete` is provided.

## Clean a Repository

```shell
# see what would be removed (dry run, the default)
uvx pup-clean

# use the latest published version
uvx pup-clean@latest

# remove all detected generated artifacts (CAUTION: DESTRUCTIVE)
uvx pup-clean --delete

# preview only specified cleanup targets
uvx pup-clean project.log data/prepared/sales.csv

# delete only specified detected cleanup targets (CAUTION: DESTRUCTIVE)
uvx pup-clean --delete project.log data/prepared/sales.csv docs/images/sales_by_region.png
```

## Developer Command Reference

<details>
<summary>Show command reference</summary>

### In a machine terminal

Open a machine terminal where you want the project:

```shell
git clone https://github.com/pup-pack/pup-clean

cd pup-clean
code .
```

### In a VS Code terminal

```shell
uv self update
uv python pin 3.15
uv python install
uv lock --upgrade
uv sync

uv run pre-commit install
uv run pre-commit autoupdate

git add -A
uv run pre-commit run --all-files
# repeat if changes were made
uv run pre-commit run --all-files

# run locally to test and see all detected cleanup targets
uv run pup-clean

# delete all detected cleanup targets (CAUTION: DESTRUCTIVE)
uv run pup-clean --delete

# preview only specified cleanup targets
uv run pup-clean project.log data/prepared/sales.csv

# delete only specified detected cleanup targets (CAUTION: DESTRUCTIVE)
uv run pup-clean --delete project.log data/prepared/sales.csv docs/images/sales_by_region.png

# types, tests, docs
uv run ty check
uv run python -m pytest
uv run python -m zensical build

# save progress
git add -A
git commit -m "update"
git push -u origin main
```

</details>

## Documentation

- [Documentation](https://pup-pack.github.io/pup-clean/)

## Annotations

[.annotations/annotations.md](./.annotations/annotations.md)

## Citation

[CITATION.cff](./CITATION.cff)

## License

[MIT](./LICENSE)

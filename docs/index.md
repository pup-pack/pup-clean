# pup-clean

<img src="images/pup.png" alt="pup-clean logo" width="110">

`pup-clean` prepares completed instructor Python repositories for release as
student project templates.

It removes known disposable development residue and inspects project source
code to identify generated artifacts created by the instructor solution.
It is designed for repositories that follow repeatable professional patterns
but still contain local, project-specific work.

## Purpose

Instructor repositories often contain files produced while developing,
running, testing, documenting, and verifying a completed project.

Examples include:

- `project.log`
- test, lint, and coverage artifacts
- build and distribution output
- generated documentation sites
- prepared data files
- generated databases and data warehouses
- generated charts and images
- other artifacts explicitly written by project source code

These files may be useful while developing and verifying the instructor
solution but should not necessarily be included when the repository is
released for student use.

`pup-clean` identifies these artifacts and provides a reviewable cleanup step
before release.

## Cleanup Model

`pup-clean` uses two complementary mechanisms.

1. **Known cleanup targets** identify universal generated development residue
   such as logs, caches, coverage files, build output, and generated
   documentation output.
2. **Source inspection** examines Python files under `src/` and identifies
   statically resolvable files created by known data-writing,
   database-writing, and image-writing operations.

This allows cleanup behavior to follow what a particular project actually
generates rather than assuming that a directory has the same role in every
project.

For example, `data/prepared/` may contain generated output in one project and
serve as input to another. The directory name alone does not determine whether
its contents should be removed.

## Safety Model

Dry run is the default.

Running:

```shell
uvx pup-clean
```

reports detected cleanup targets without deleting anything.

Deletion requires an explicit command:

```shell
uvx pup-clean --delete
```

Only known cleanup targets and artifacts confidently discovered from project
source code are eligible for deletion.

Dynamically constructed or otherwise unresolved output paths are not guessed.

Source inspection identifies exact generated files. It does not remove a
parent directory merely because that directory contains a generated file.

For example, if project code generates:

```text
docs/images/sales_by_region.png
```

that file may be identified for cleanup while other files in `docs/images/`
remain untouched.

## Instructor Workflow

A typical instructor release workflow is:

1. Complete and run the instructor solution.
2. Run `uvx pup-clean` and review the detected cleanup targets.
3. Run `uvx pup-clean --delete` to remove the approved generated artifacts.
4. Run project checks and tests.
5. Commit and push the cleaned repository.
6. Configure the GitHub repository as a template repository for student use.

## Shared Infrastructure

Repository detection and safe repository-relative path handling are provided by
[`pup-core`](https://github.com/denisecase/pup-core).

## See Also

- [API](./api.md)

# pup-clean

<img src="images/pup.png" alt="pup-clean logo" width="110">

`pup-clean` cleans common generated files and folders from Python repositories.

It removes known generated development artifacts and inspects project source
code to identify project-specific generated files.

## Purpose

`pup-clean` cleans common generated files and folders from Python repositories.
Examples include:

- `project.log`
- test, lint, and coverage artifacts
- build and distribution output
- generated documentation sites
- generated data files
- generated databases and data warehouses
- generated charts and images
- other artifacts explicitly written by project source code

Known cleanup targets are defined in:

- [`cleanup_defaults.toml`](https://github.com/pup-pack/pup-clean/blob/main/src/pup_clean/data/cleanup_defaults.toml)

Project-specific generated files are discovered by inspecting Python source
using rules defined in:

- [`generated_defaults.toml`](https://github.com/pup-pack/pup-clean/blob/main/src/pup_clean/data/generated_defaults.toml)

## Cleanup Model

`pup-clean` uses two complementary mechanisms.

1. **Known cleanup targets** identify common generated development artifacts
   such as logs, caches, coverage files, build output, and generated
   documentation output.

2. **Source inspection** examines Python files under `src/` and identifies
   statically resolvable files created by known data-writing,
   database-creation, and image-writing operations.

Source inspection allows cleanup behavior to reflect what a particular project
actually generates rather than assuming that a directory always has the same
role.

For example, `data/prepared/` may contain generated output in one project and
input files in another. The directory name alone does not determine whether
its contents are cleanup targets.

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

## Shared Infrastructure

Repository detection and safe repository-relative path handling are provided by
[`pup-core`](https://github.com/pup-pack/pup-core).

## See Also

- [API](./api.md)

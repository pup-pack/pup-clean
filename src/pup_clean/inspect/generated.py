"""Discover generated artifacts by inspecting Python source code.

This module statically inspects Python source files under `src/` and finds
paths passed to known data-writing, database-creation, and image-writing
operations.

The purpose is to identify artifacts created by running a project so that
pup-clean can remove instructor-generated outputs before a repository is
published.

Only statically resolvable generated file paths are returned.
Containing directories are not cleanup targets.
"""

import ast
from importlib import resources
from pathlib import Path
import tomllib
from typing import Any

__all__ = ["discover_generated_paths"]


def _load_defaults() -> dict[str, Any]:
    """Load source-inspection defaults from packaged TOML data."""
    defaults_file = (
        resources.files("pup_clean.inspect").joinpath("data").joinpath("defaults.toml")
    )

    return tomllib.loads(defaults_file.read_text(encoding="utf-8"))


_DEFAULTS = _load_defaults()

_DATA_WRITE_METHODS = frozenset(_DEFAULTS["data_write_methods"])

_IMAGE_WRITE_METHODS = frozenset(_DEFAULTS["image_write_methods"])

_DATABASE_CONNECT_FUNCTIONS = frozenset(_DEFAULTS["database_connect_functions"])

_GENERATED_DATA_SUFFIXES = frozenset(
    suffix.lower() for suffix in _DEFAULTS["generated_data_suffixes"]
)

_GENERATED_IMAGE_SUFFIXES = frozenset(
    suffix.lower() for suffix in _DEFAULTS["generated_image_suffixes"]
)


def discover_generated_paths(root: Path) -> tuple[Path, ...]:
    """Discover generated data artifacts referenced by project source code.

    Python files under ``src/`` are parsed using the AST. Known data-writing
    operations are inspected and statically resolvable output paths are
    returned.

    A path is returned only when it can be resolved from source code with
    sufficient confidence. Dynamic or ambiguous paths are ignored.

    Image files are explicitly excluded.

    Args:
        root: Repository root.

    Returns:
        Repository-relative paths for discovered generated artifacts.
    """
    src_root = root / "src"

    if not src_root.is_dir():
        return ()

    discovered: set[Path] = set()

    for source_path in sorted(src_root.rglob("*.py")):
        discovered.update(
            _discover_generated_paths_in_file(
                root=root,
                source_path=source_path,
            )
        )

    return tuple(sorted(discovered, key=lambda path: path.as_posix()))


def _discover_generated_paths_in_file(
    *,
    root: Path,
    source_path: Path,
) -> set[Path]:
    """Discover generated paths referenced by one Python source file."""
    try:
        source = source_path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(source_path))
    except OSError, SyntaxError, UnicodeError:
        return set()

    resolver = _PathResolver(root=root)
    resolver.collect_assignments(tree)

    visitor = _GeneratedPathVisitor(resolver=resolver)
    visitor.visit(tree)

    return visitor.generated_paths


class _GeneratedPathVisitor(ast.NodeVisitor):
    """Find statically resolvable generated artifact paths."""

    def __init__(self, *, resolver: _PathResolver) -> None:
        self.resolver = resolver
        self.generated_paths: set[Path] = set()

    def visit_Call(self, node: ast.Call) -> None:
        """Inspect calls that can create generated artifacts."""
        self._inspect_data_write(node)
        self._inspect_image_write(node)
        self._inspect_database_connect(node)

        self.generic_visit(node)

    def _inspect_data_write(self, node: ast.Call) -> None:
        """Inspect dataframe and similar data-writing method calls."""
        if not isinstance(node.func, ast.Attribute):
            return

        if node.func.attr not in _DATA_WRITE_METHODS:
            return

        path_node = _first_path_argument(node)

        if path_node is None:
            return

        self._add_resolved_path(path_node)

    def _inspect_image_write(self, node: ast.Call) -> None:
        """Inspect image-writing method calls."""
        if not isinstance(node.func, ast.Attribute):
            return

        if node.func.attr not in _IMAGE_WRITE_METHODS:
            return

        path_node = _first_path_argument(node)

        if path_node is None:
            return

        self._add_resolved_path(path_node)

    def _inspect_database_connect(self, node: ast.Call) -> None:
        """Inspect known file-backed database connection calls."""
        function_name = _qualified_call_name(node.func)

        if function_name not in _DATABASE_CONNECT_FUNCTIONS:
            return

        if not node.args:
            return

        self._add_resolved_path(node.args[0])

    def _add_resolved_path(self, node: ast.expr) -> None:
        """Resolve and record an eligible generated path."""
        path = self.resolver.resolve(node)

        if path is None:
            return

        if not _is_generated_artifact(path):
            return

        self.generated_paths.add(path)


class _PathResolver:
    """Resolve simple statically defined repository-relative paths."""

    def __init__(self, *, root: Path) -> None:
        self.root = root.resolve()
        self.assignments: dict[str, ast.expr] = {}

    def collect_assignments(self, tree: ast.AST) -> None:
        """Collect simple module-level and function-local assignments."""
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        self.assignments[target.id] = node.value

            elif isinstance(node, ast.AnnAssign) and (
                isinstance(node.target, ast.Name) and node.value is not None
            ):
                self.assignments[node.target.id] = node.value

    def resolve(
        self,
        node: ast.expr,
        *,
        seen: frozenset[str] = frozenset(),
    ) -> Path | None:
        """Resolve a simple path expression to a repository-relative path."""
        value = self._resolve_value(node, seen=seen)

        if value is None:
            return None

        path = Path(value)

        if path.is_absolute():
            try:
                return path.resolve().relative_to(self.root)
            except ValueError:
                return None

        normalized = Path(*path.parts)

        if ".." in normalized.parts:
            return None

        return normalized

    def _resolve_value(
        self,
        node: ast.expr,
        *,
        seen: frozenset[str],
    ) -> str | None:
        """Resolve a supported AST expression to a path string."""
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            return node.value

        if isinstance(node, ast.Name):
            if node.id in seen:
                return None

            assigned = self.assignments.get(node.id)

            if assigned is None:
                return None

            return self._resolve_value(
                assigned,
                seen=seen | {node.id},
            )

        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
            left = self._resolve_value(node.left, seen=seen)
            right = self._resolve_value(node.right, seen=seen)

            if left is None or right is None:
                return None

            return str(Path(left) / right)

        if isinstance(node, ast.Call):
            return self._resolve_path_constructor(node, seen=seen)

        return None

    def _resolve_path_constructor(
        self,
        node: ast.Call,
        *,
        seen: frozenset[str],
    ) -> str | None:
        """Resolve Path(...) and pathlib.Path(...) expressions."""
        function_name = _qualified_call_name(node.func)

        if function_name not in {
            "Path",
            "pathlib.Path",
        }:
            return None

        if len(node.args) != 1:
            return None

        return self._resolve_value(node.args[0], seen=seen)


def _first_path_argument(node: ast.Call) -> ast.expr | None:
    """Return the path argument from a known data-writing call."""
    if node.args:
        return node.args[0]

    for keyword in node.keywords:
        if keyword.arg in {
            "path",
            "path_or_buf",
            "excel_writer",
        }:
            return keyword.value

    return None


def _qualified_call_name(node: ast.expr) -> str | None:
    """Return a dotted name for a function or method expression."""
    if isinstance(node, ast.Name):
        return node.id

    if isinstance(node, ast.Attribute):
        prefix = _qualified_call_name(node.value)

        if prefix is None:
            return node.attr

        return f"{prefix}.{node.attr}"

    return None


def _is_generated_artifact(path: Path) -> bool:
    """Return whether a discovered output is eligible for cleanup."""
    suffix = path.suffix.lower()

    return suffix in _GENERATED_DATA_SUFFIXES or suffix in _GENERATED_IMAGE_SUFFIXES

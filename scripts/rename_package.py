#!/usr/bin/env python3
"""
Rename the template package (``src/example_pkg``) to a new package name and update references.

This script will:
- Rename ``src/example_pkg`` -> ``src/<new_pkg>``
- Update import paths in tests and source (``example_pkg`` -> ``<new_pkg>``)
- Update mypy targets in CI workflow, pre-commit config, and VS Code tasks
- Update README mentions of ``example_pkg``

Usage
-----
uv run python scripts/rename_package.py <new_package_name>

Notes
-----
- New package name must be a valid Python identifier (PEP 8 lowercase with underscores
    recommended).
- Safe to run once on a fresh template clone. Back up if running on a modified project.
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
OLD_PKG = "example_pkg"

REPLACEMENTS = [
    # (path, is_regex, patterns)
    # YAML/JSON/TOML and text files where package is referenced
    (".github/workflows/ci.yml", False, ["-p example_pkg"]),
    (".pre-commit-config.yaml", False, ['args: ["-p", "example_pkg"]']),
    (".vscode/tasks.json", False, ["mypy", "-p", "example_pkg"]),
    ("README.md", False, ["example_pkg"]),
]

CODE_GLOBS = [
    SRC,
    ROOT / "tests",
]


def validate_name(name: str) -> None:
    """Validate the provided package ``name`` and exit with a message if invalid.

    Rules enforced:
    - Must match ``[a-zA-Z_][a-zA-Z0-9_]*``.
    - Must not contain dashes (``-``) or dots (``.``).
    """
    if not re.fullmatch(r"[a-zA-Z_][a-zA-Z0-9_]*", name):
        raise SystemExit(
            (
                f"Invalid package name '{name}'. Use letters, digits, and underscores; "
                "cannot start with a digit."
            )
        )
    if "-" in name or "." in name:
        raise SystemExit("Use underscores, not dashes or dots, in package name.")


def rename_directory(old: Path, new: Path) -> None:
    """Move the package directory from ``old`` to ``new`` with basic safety checks."""
    if not old.exists():
        raise SystemExit(f"Expected to find package directory: {old}")
    if new.exists():
        raise SystemExit(f"Target package directory already exists: {new}")
    shutil.move(str(old), str(new))


def replace_in_file(path: Path, old: str, new: str) -> None:
    """Replace occurrences of ``old`` with ``new`` in a text file at ``path``.

    Non-text files or files that cannot be read are skipped silently.
    """
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return
    if old not in text:
        return
    text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")


def update_references(old_pkg: str, new_pkg: str) -> None:
    """Update occurrences of the package name in known config files and code/tests."""
    # Update explicit files with known patterns
    for relpath, _is_regex, patterns in REPLACEMENTS:
        fpath = ROOT / relpath
        if not fpath.exists():
            continue
        content = fpath.read_text(encoding="utf-8")
        new_content = content
        for pat in patterns:
            new_content = new_content.replace(old_pkg, new_pkg)
        if new_content != content:
            fpath.write_text(new_content, encoding="utf-8")

    # Update imports in code and tests
    for base in CODE_GLOBS:
        if not base.exists():
            continue
        for p in base.rglob("*"):
            if p.is_dir():
                continue
            if p.suffix in {".py", ".md", ".rst", ".txt", ".toml", ".yaml", ".yml", ".json"}:
                replace_in_file(p, old_pkg, new_pkg)


def main() -> None:
    """Program entry point: parse args, perform rename, and print next steps."""
    parser = argparse.ArgumentParser(
        description=("Rename the template package and update references.")
    )
    parser.add_argument("new_package", help="New package name (e.g., my_project)")
    args = parser.parse_args()

    new_pkg = args.new_package.strip()
    validate_name(new_pkg)

    old_dir = SRC / OLD_PKG
    new_dir = SRC / new_pkg

    rename_directory(old_dir, new_dir)
    update_references(OLD_PKG, new_pkg)

    print(f"Renamed package '{OLD_PKG}' -> '{new_pkg}'.")
    print("Next steps:")
    print("- Update project metadata in pyproject.toml if desired.")
    print("- Run tasks: 'setup:project' then 'verify' in VS Code, or:")
    print("  uv sync && uv run pre-commit install && uv run mypy -p", new_pkg)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Script to add SPDX license identifiers to all Python files."""

from pathlib import Path


def add_spdx_header(file_path: Path) -> bool:
    """Add SPDX header to a Python file if not already present.

    Args:
        file_path: Path to the Python file

    Returns:
        True if file was modified, False otherwise
    """
    content = file_path.read_text(encoding="utf-8")

    # Check if SPDX header already exists
    if "SPDX-License-Identifier" in content:
        return False

    # Add SPDX header at the beginning
    spdx_header = "# SPDX-License-Identifier: MIT\n"
    new_content = spdx_header + content

    file_path.write_text(new_content, encoding="utf-8")
    return True


def main() -> None:
    """Add SPDX headers to all Python files in the project."""
    project_root = Path(__file__).parent.parent

    # Find all Python files
    python_files = list(project_root.glob("**/*.py"))

    # Exclude virtual environments and build directories
    exclude_patterns = {"venv", ".venv", "env", ".env", "build", "dist", ".git", "__pycache__", "node_modules"}
    python_files = [f for f in python_files if not any(part in exclude_patterns for part in f.parts)]

    modified_count = 0
    for file_path in sorted(python_files):
        if add_spdx_header(file_path):
            print(f"Added SPDX header to: {file_path.relative_to(project_root)}")
            modified_count += 1
        else:
            print(f"Skipped (already has SPDX): {file_path.relative_to(project_root)}")

    print(f"\nModified {modified_count} files out of {len(python_files)} total Python files.")


if __name__ == "__main__":
    main()

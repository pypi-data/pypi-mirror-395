# SPDX-License-Identifier: MIT
"""Utility functions and helpers for miniflux-tui."""

from __future__ import annotations

import shutil
import subprocess  # nosec B404
import tomllib
from collections.abc import Generator, Iterator
from contextlib import contextmanager
from importlib import metadata
from pathlib import Path
from typing import Any

PYPROJECT_PATH = Path(__file__).resolve().parent.parent / "pyproject.toml"
REPO_ROOT = PYPROJECT_PATH.parent


def get_app_version() -> str:
    """Return the application version.

    When running from a git repository, returns branch and commit hash.
    When running an installed package (release), returns the version number.

    The preferred source for installed packages is the package metadata.
    This works both for editable installs and when installed from a wheel.
    When metadata isn't available, falls back to reading from pyproject.toml.

    Returns:
        - "branch/commit-hash" if running from a git repo
        - "version" if running an installed package
        - "unknown" if version cannot be determined
    """

    # Check if running from a git repository
    git_version = _get_git_version()
    if git_version:
        return git_version

    # If not in a git repo, try to get the installed package version
    last_metadata_error: Exception | None = None

    for distribution_name in _iter_distribution_candidates():
        try:
            return metadata.version(distribution_name)
        except metadata.PackageNotFoundError:
            pass
        except Exception as error:
            # Unexpected metadata errors should not crash the application. Try
            # any remaining candidates before falling back to the file-based
            # lookup instead.
            last_metadata_error = error

    if last_metadata_error is not None:
        return _get_version_from_pyproject()

    return _get_version_from_pyproject()


def _get_git_version() -> str | None:
    """Get version from git repository if running from checked-out source.

    Returns:
        - "branch/short-commit-hash" if in a git repo
        - None if not in a git repo or git is unavailable
    """

    try:
        # Check if .git directory exists
        git_dir = REPO_ROOT / ".git"
        if not git_dir.exists():
            return None

        # Find git executable in PATH
        git_executable = shutil.which("git")
        if not git_executable:
            return None

        # Get current branch name
        branch = subprocess.run(  # nosec B603
            [git_executable, "-C", str(REPO_ROOT), "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            timeout=2,
            check=False,
        )

        if branch.returncode != 0:
            return None

        branch_name = branch.stdout.strip()

        # Get short commit hash
        commit = subprocess.run(  # nosec B603
            [git_executable, "-C", str(REPO_ROOT), "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=2,
            check=False,
        )

        if commit.returncode != 0:
            return None

        commit_hash = commit.stdout.strip()

        return f"{branch_name}/{commit_hash}"

    except (OSError, subprocess.TimeoutExpired, FileNotFoundError):
        # git command not found or timeout - not in a git repo or git unavailable
        return None


def _get_version_from_pyproject() -> str:
    """Read the version from ``pyproject.toml`` if it is available."""

    try:
        if PYPROJECT_PATH.exists():
            data = tomllib.loads(PYPROJECT_PATH.read_text(encoding="utf-8"))
            version = data.get("project", {}).get("version")
            if version:
                return str(version)
    except (OSError, tomllib.TOMLDecodeError, AttributeError):
        return "unknown"

    return "unknown"


def _iter_distribution_candidates() -> Iterator[str]:
    """Yield potential distribution names that provide :mod:`miniflux_tui`.

    The canonical distribution name is ``miniflux-tui-py``. When the package is
    installed in editable mode the metadata lookup can, however, vary between
    environments. To make the lookup resilient we ask ``importlib.metadata`` for
    the distributions that provide ``miniflux_tui`` and try those as well.
    """

    seen: set[str] = set()

    def _unique(name: str) -> Iterator[str]:
        if name and name not in seen:
            seen.add(name)
            yield name

    yield from _unique("miniflux-tui-py")

    try:
        packages = metadata.packages_distributions()
    except (AttributeError, TypeError, ValueError):
        # packages_distributions() might not exist or might fail in some environments
        return

    for candidate in packages.get("miniflux_tui", []) or []:
        yield from _unique(candidate)


def get_star_icon(is_starred: bool) -> str:
    """Get star icon based on starred status.

    Args:
        is_starred: Whether the entry is starred

    Returns:
        Star icon character (filled or empty)
    """
    return "★" if is_starred else "☆"


def get_status_icon(is_unread: bool) -> str:
    """Get status icon based on read/unread status.

    Args:
        is_unread: Whether the entry is unread

    Returns:
        Status icon character (filled or empty)
    """
    return "●" if is_unread else "○"


@contextmanager
def api_call(screen: Any, operation_name: str = "Operation") -> Generator[Any, None, None]:
    """Context manager for safe API calls with error handling.

    Usage:
        with api_call(self, "marking entry as read") as client:
            if client is None:
                return
            await client.mark_as_read(entry_id)

    Args:
        screen: The screen instance (for notifications and logging)
        operation_name: Name of operation for error messages

    Yields:
        The API client instance
    """
    client = getattr(screen.app, "client", None)
    if not client:
        screen.notify("API client not available", severity="error")
        yield None
        return

    try:
        yield client
    except TimeoutError:
        screen.notify(f"Request timeout during {operation_name}", severity="error")
        screen.log(f"Timeout during {operation_name}")
    except ConnectionError:
        screen.notify(f"Connection failed during {operation_name}", severity="error")
        screen.log(f"Connection error during {operation_name}")
    except ValueError as e:
        screen.notify(f"Invalid input during {operation_name}: {e}", severity="error")
        screen.log(f"ValueError during {operation_name}: {e}")
    except Exception as e:
        screen.log(f"Unexpected error during {operation_name}: {e}")


def consolidate_blank_lines(text: str, max_consecutive: int = 2) -> str:
    """Consolidate multiple consecutive blank lines into a maximum number.

    This function reduces excessive whitespace in text content by limiting
    the number of consecutive blank lines to a specified maximum. Useful for
    cleaning up documentation and help text display.

    Args:
        text: Input text to consolidate
        max_consecutive: Maximum consecutive blank lines to keep (default: 2)

    Returns:
        Text with consolidated blank lines

    Example:
        >>> text = "Line 1\\n\\n\\n\\nLine 2\\n\\n\\nLine 3"
        >>> consolidate_blank_lines(text)
        'Line 1\\n\\nLine 2\\n\\nLine 3'
        >>> consolidate_blank_lines(text, max_consecutive=1)
        'Line 1\\nLine 2\\nLine 3'
    """
    lines = text.split("\n")
    result: list[str] = []
    blank_count = 0

    for line in lines:
        if line.strip() == "":
            blank_count += 1
            if blank_count <= max_consecutive:
                result.append(line)
        else:
            blank_count = 0
            result.append(line)

    return "\n".join(result)

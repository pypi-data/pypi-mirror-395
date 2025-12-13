# SPDX-License-Identifier: MIT
"""Atheris-based fuzz target for configuration parsing."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

import atheris

with atheris.instrument_imports():
    import tomllib

    from miniflux_tui.config import Config


def _cleanup_temp_file(path: Path | None) -> None:
    """Remove ``path`` if it exists."""

    if path is None:
        return

    try:
        path.unlink()
    except FileNotFoundError:
        # The file did not exist; cleanup is already complete.
        pass
    except OSError:
        # The file might already have been removed by the OS or another
        # concurrent fuzzing worker. Best effort cleanup is sufficient here.
        pass


def _test_one_input(data: bytes) -> None:
    """
    Atheris fuzzing entry point.

    Exercise ``Config.from_file`` using arbitrary input data.
    """

    if not data:
        return

    temp_path: Path | None = None
    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(data)
            temp_path = Path(tmp_file.name)

        try:
            Config.from_file(temp_path)
        except (ValueError, tomllib.TOMLDecodeError, TypeError):
            # Invalid or malformed documents are expected fuzz outcomes; stop
            # processing this input and let the fuzzer generate new cases.
            return
        except RecursionError:
            # Deeply nested tables can trigger Python's recursion limits in the
            # TOML parser. Treat these as benign for the fuzz target.
            pass
    finally:
        _cleanup_temp_file(temp_path)


# Atheris requires the fuzz target function to be named ``TestOneInput``; alias the
# snake_case implementation to satisfy both Atheris and static analysis tools.
TestOneInput = _test_one_input


def main() -> None:
    atheris.Setup(sys.argv, TestOneInput)
    atheris.Fuzz()


if __name__ == "__main__":
    main()

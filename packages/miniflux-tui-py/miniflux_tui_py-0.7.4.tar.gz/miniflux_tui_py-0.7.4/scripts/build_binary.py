# SPDX-License-Identifier: MIT
"""Build and package platform-specific executables for miniflux-tui.

This script invokes PyInstaller to create a single-file executable for the
current platform and then packages the result together with basic metadata.
It is intended to run inside CI on Linux, macOS, and Windows runners.
"""

from __future__ import annotations

import platform
import shutil
import subprocess
import sys
import tarfile
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = REPO_ROOT / "dist"
BUILD_ROOT = REPO_ROOT / "build"
ARTIFACT_DIR = BUILD_ROOT / "binary"
PACKAGE_STAGING_DIR = BUILD_ROOT / "package"
PYINSTALLER_WORK_DIR = BUILD_ROOT / "pyinstaller"


def normalize_arch(machine: str) -> str:
    """Normalize platform.machine() to common release labels."""
    normalized = machine.lower()
    if normalized in {"x86_64", "amd64"}:  # nosec: B105 - Non-sensitive architecture comparison
        return "amd64"
    if normalized in {"arm64", "aarch64"}:  # nosec: B105 - Non-sensitive architecture comparison
        return "arm64"
    return normalized


def package_name(system: str, arch: str) -> str:
    """Return canonical archive name sans extension."""
    system_map = {
        "Linux": "linux",
        "Darwin": "macos",
        "Windows": "windows",
    }
    slug = system_map.get(system, system.lower())
    return f"miniflux-tui-{slug}-{arch}"


def run_pyinstaller() -> None:
    """Run PyInstaller to create a single-file executable."""
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    if PYINSTALLER_WORK_DIR.exists():
        shutil.rmtree(PYINSTALLER_WORK_DIR)

    cmd = [
        sys.executable,
        "-m",
        "PyInstaller",
        "miniflux_tui/main.py",
        "--name",
        "miniflux-tui",
        "--onefile",
        "--clean",
        "--collect-data",
        "textual",
        "--collect-submodules",
        "textual",
        "--workpath",
        str(PYINSTALLER_WORK_DIR),
        "--specpath",
        str(PYINSTALLER_WORK_DIR),
    ]

    subprocess.run(cmd, check=True)


def ensure_dirs() -> None:
    """Prepare artifact directories."""
    if ARTIFACT_DIR.exists():
        shutil.rmtree(ARTIFACT_DIR)
    if PACKAGE_STAGING_DIR.exists():
        shutil.rmtree(PACKAGE_STAGING_DIR)

    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    PACKAGE_STAGING_DIR.mkdir(parents=True, exist_ok=True)


def stage_files(binary_path: Path) -> None:
    """Copy the executable and metadata files into a staging directory."""
    PACKAGE_STAGING_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(binary_path, PACKAGE_STAGING_DIR / binary_path.name)

    for filename in ("LICENSE", "README.md"):
        src = REPO_ROOT / filename
        if src.exists():
            shutil.copy2(src, PACKAGE_STAGING_DIR / filename)


def make_archive(base_name: str, system: str) -> Path:
    """Create a platform-appropriate archive from staged files."""
    archive_path: Path
    if system == "Windows":
        archive_path = ARTIFACT_DIR / f"{base_name}.zip"
        with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for item in PACKAGE_STAGING_DIR.iterdir():
                archive.write(item, arcname=item.name)
    else:
        archive_path = ARTIFACT_DIR / f"{base_name}.tar.gz"
        with tarfile.open(archive_path, "w:gz") as archive:
            for item in PACKAGE_STAGING_DIR.iterdir():
                archive.add(item, arcname=item.name)

    return archive_path


def main() -> int:
    """Entrypoint for building and packaging the executable."""
    run_pyinstaller()
    ensure_dirs()

    system = platform.system()
    arch = normalize_arch(platform.machine())
    base_name = package_name(system, arch)

    binary_name = "miniflux-tui.exe" if system == "Windows" else "miniflux-tui"
    binary_path = DIST_DIR / binary_name
    if not binary_path.exists():
        message = f"Expected binary not found at {binary_path}"
        raise FileNotFoundError(message)

    stage_files(binary_path)
    archive_path = make_archive(base_name, system)

    # Ensure build directories are clean for subsequent runs.
    shutil.rmtree(PACKAGE_STAGING_DIR)
    if PYINSTALLER_WORK_DIR.exists():
        shutil.rmtree(PYINSTALLER_WORK_DIR)

    print(f"Created archive at {archive_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

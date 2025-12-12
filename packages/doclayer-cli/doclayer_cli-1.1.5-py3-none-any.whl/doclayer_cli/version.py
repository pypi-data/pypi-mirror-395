from __future__ import annotations

import subprocess
from datetime import datetime
from importlib.metadata import version as pkg_version, PackageNotFoundError

# Try to get version from installed package metadata (PyPI install)
try:
    VERSION: str = pkg_version("doclayer-cli")
except PackageNotFoundError:
    VERSION = "1.1.5"  # Fallback for development

# Try to get git commit hash for dev builds
def _get_git_commit() -> str:
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return "release"

COMMIT: str = _get_git_commit()
BUILD_DATE: str = datetime.now().strftime("%Y-%m-%d")

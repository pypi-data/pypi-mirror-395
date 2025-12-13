"""
Utility functions for dev API.

Cross-platform helpers for finding executables, parsing output, etc.

Author: ForgeBase Development Team
Created: 2025-11-04
"""

import shutil
import sys
from pathlib import Path


def find_executable(name: str) -> str:
    """
    Find an executable in a cross-platform way.

    Searches for the executable in the following order:
    1. In PATH (using shutil.which)
    2. In the current virtualenv's bin/Scripts directory
    3. Falls back to just the name (letting subprocess handle errors)

    This makes the tool work on Windows, macOS, Linux, and with
    different virtualenv names (not just .venv).

    Args:
        name: Name of the executable (e.g., 'deptry', 'lint-imports')

    Returns:
        Path to the executable or the name itself

    Example:
        deptry_path = find_executable("deptry")
        subprocess.run([deptry_path, "src/"])
    """
    # Try to find in PATH first
    found = shutil.which(name)
    if found:
        return found

    # Try in the current virtualenv
    venv_base = Path(sys.executable).parent

    # Unix-like: bin/
    unix_path = venv_base / name
    if unix_path.exists():
        return str(unix_path)

    # Windows: Scripts/
    windows_path = venv_base / "Scripts" / f"{name}.exe"
    if windows_path.exists():
        return str(windows_path)

    windows_path_no_ext = venv_base / "Scripts" / name
    if windows_path_no_ext.exists():
        return str(windows_path_no_ext)

    # Fallback: return name and let subprocess handle errors
    return name

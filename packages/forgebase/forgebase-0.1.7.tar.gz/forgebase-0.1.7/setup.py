"""
Minimal setup.py for backward compatibility.

All configuration is now in pyproject.toml (PEP 621).
This file exists only for editable installs with older pip versions.

For modern pip (>=21.3), use:
    pip install -e .
    pip install -e ".[dev]"

Author: Jorge, The Forge
Created: 2025-11-03
"""

from setuptools import setup

# All metadata and configuration is now in pyproject.toml
# This minimal setup.py enables:
# 1. Editable installs with older pip versions
# 2. Backward compatibility with legacy tools
setup()

"""
ForgeBase Developer Tools.

Python APIs for AI agents and programmatic access to development tools.
Provides structured, machine-readable interfaces for scaffolding, testing,
quality checking, and component discovery.

Usage for AI Agents:
    from forgebase.dev.api import QualityChecker, ScaffoldGenerator
    from forgebase.dev import get_agent_quickstart

    # Access documentation programmatically
    guide = get_agent_quickstart()

    # Check code quality
    checker = QualityChecker()
    results = checker.run_all()

    # Generate boilerplate
    generator = ScaffoldGenerator()
    code = generator.create_usecase("CreateOrder")

Author: ForgeBase Development Team
Created: 2025-11-04
"""

import importlib.resources as resources
from pathlib import Path


def get_agent_quickstart() -> str:
    """
    Get the AI Agent Quick Start guide content.

    Returns the full markdown content of AI_AGENT_QUICK_START.md,
    useful for AI agents to understand available APIs.

    This documentation is embedded in the package and accessible
    even when installed via pip, without requiring internet access.

    :return: Markdown content as string
    :rtype: str

    Example::

        >>> from forgebase.dev import get_agent_quickstart
        >>> guide = get_agent_quickstart()
        >>> print(guide[:100])
        # ForgeBase AI Agent Quick Start Guide...
    """
    try:
        # Try to read from embedded package data
        if hasattr(resources, 'files'):
            # Python 3.9+
            doc_file = resources.files('forgebase._docs') / 'AI_AGENT_QUICK_START.md'
            return doc_file.read_text(encoding='utf-8')
        # Fallback for older Python
        import pkg_resources
        return pkg_resources.resource_string(
            'forgebase._docs',
            'AI_AGENT_QUICK_START.md'
        ).decode('utf-8')
    except (FileNotFoundError, ModuleNotFoundError, AttributeError):
        # Fallback: read from docs/agentes-ia/ if in development
        project_root = Path(__file__).parent.parent.parent.parent
        quickstart_path = project_root / 'docs' / 'agentes-ia' / 'inicio-rapido.md'
        if quickstart_path.exists():
            return quickstart_path.read_text(encoding='utf-8')
        # Legacy fallback
        legacy_path = project_root / 'AI_AGENT_QUICK_START.md'
        if legacy_path.exists():
            return legacy_path.read_text(encoding='utf-8')
        return (
            "# AI Agent Quick Start\n\n"
            "Documentation not found in package. "
            "Please visit: https://github.com/symlabs-ai/forgebase\n"
        )


def get_documentation_path() -> Path:
    """
    Get the path to included documentation.

    :return: Path to docs directory
    :rtype: Path

    Example::

        >>> from forgebase.dev import get_documentation_path
        >>> docs_path = get_documentation_path()
        >>> adr_files = list(docs_path.glob('adr/*.md'))
    """
    try:
        if hasattr(resources, 'files'):
            # Python 3.9+
            return Path(str(resources.files('forgebase'))) / 'docs'
        # Development fallback
        return Path(__file__).parent.parent.parent.parent / 'docs'
    except Exception:
        # Ultimate fallback
        return Path(__file__).parent.parent.parent.parent / 'docs'


__all__ = [
    'get_agent_quickstart',
    'get_documentation_path',
]

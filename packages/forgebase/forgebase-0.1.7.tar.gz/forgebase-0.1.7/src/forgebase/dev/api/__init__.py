"""
ForgeBase Developer API.

Programmatic interfaces for AI agents to interact with ForgeBase development tools.
All APIs return structured data (dataclasses/dicts) instead of formatted text.

Main APIs:
    - QualityChecker: Code quality validation (linting, type checking, architecture)
    - ScaffoldGenerator: Boilerplate code generation
    - ComponentDiscovery: Codebase component discovery and cataloging
    - TestRunner: Test execution with structured results

Author: ForgeBase Development Team
Created: 2025-11-04
"""

from forgebase.dev.api.discovery import ComponentDiscovery, DiscoveryResult
from forgebase.dev.api.quality import CheckResult, QualityChecker
from forgebase.dev.api.scaffold import ScaffoldGenerator, ScaffoldResult
from forgebase.dev.api.testing import TestResult, TestRunner

__all__ = [
    "QualityChecker",
    "CheckResult",
    "ScaffoldGenerator",
    "ScaffoldResult",
    "ComponentDiscovery",
    "DiscoveryResult",
    "TestRunner",
    "TestResult",
]

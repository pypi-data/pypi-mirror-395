"""
Quality Checking API for AI Agents.

Provides structured, machine-readable interfaces for code quality validation.
Returns dataclasses with detailed error information, suggestions, and metrics.

Usage:
    from forgebase.dev.api import QualityChecker

    checker = QualityChecker()

    # Run individual checks
    ruff_result = checker.run_ruff()
    if not ruff_result.passed:
        for error in ruff_result.errors:
            print(f"{error['file']}:{error['line']} - {error['message']}")

    # Run all checks
    results = checker.run_all()
    all_passed = all(r.passed for r in results.values())

Author: ForgeBase Development Team
Created: 2025-11-04
"""

import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class CheckResult:
    """
    Structured result from a quality check.

    Designed for AI agent consumption with machine-readable format.

    Attributes:
        tool: Name of the tool that ran (e.g., "ruff", "mypy")
        passed: Whether the check passed without errors
        errors: List of errors found, each with file, line, message, code
        warnings: List of warnings (non-blocking)
        suggestions: AI-actionable suggestions to fix issues
        duration: Time taken to run the check in seconds
        exit_code: Process exit code
        raw_output: Raw stdout/stderr for debugging
    """

    tool: str
    passed: bool
    errors: list[dict[str, Any]] = field(default_factory=list)
    warnings: list[dict[str, Any]] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    duration: float = 0.0
    exit_code: int = 0
    raw_output: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "tool": self.tool,
            "passed": self.passed,
            "errors": self.errors,
            "warnings": self.warnings,
            "suggestions": self.suggestions,
            "duration": self.duration,
            "exit_code": self.exit_code,
            "raw_output": self.raw_output,
        }

    @property
    def error_count(self) -> int:
        """Total number of errors."""
        return len(self.errors)

    @property
    def warning_count(self) -> int:
        """Total number of warnings."""
        return len(self.warnings)


class QualityChecker:
    """
    Quality checking API for AI agents.

    Runs code quality tools (Ruff, Mypy, import-linter, Deptry) and returns
    structured results suitable for programmatic analysis by AI agents.

    All methods return CheckResult objects with:
    - Structured error data (file, line, column, message, code)
    - AI-actionable suggestions
    - Timing metrics
    - Raw output for debugging

    Example:
        checker = QualityChecker()

        # Single check
        result = checker.run_ruff()
        if not result.passed:
            for error in result.errors:
                fix_code(error['file'], error['line'], error['code'])

        # All checks
        results = checker.run_all()
        report = {
            tool: {"passed": r.passed, "errors": len(r.errors)}
            for tool, r in results.items()
        }
    """

    def __init__(self, project_root: Path | None = None):
        """
        Initialize quality checker.

        Args:
            project_root: Root directory of project. Defaults to current directory.
        """
        self.project_root = project_root or Path.cwd()

    def run_ruff(self, paths: list[str] | None = None) -> CheckResult:
        """
        Run Ruff linter.

        Args:
            paths: Paths to check. Defaults to ["src/", "tests/"]

        Returns:
            CheckResult with structured Ruff output

        Example:
            result = checker.run_ruff()
            if not result.passed:
                # AI can reason about specific error codes
                for error in result.errors:
                    if error['code'] == 'F401':  # Unused import
                        remove_import(error['file'], error['line'])
        """
        if paths is None:
            paths = ["src/", "tests/"]

        start_time = time.time()

        try:
            result = subprocess.run(
                [sys.executable, "-m", "ruff", "check", *paths, "--output-format=json"],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            duration = time.time() - start_time

            # Parse JSON output if available
            errors = []
            if result.stdout.strip():
                import json
                try:
                    ruff_output = json.loads(result.stdout)
                    errors = [
                        {
                            "file": str(Path(item["filename"]).relative_to(self.project_root)),
                            "line": item["location"]["row"],
                            "column": item["location"]["column"],
                            "message": item["message"],
                            "code": item["code"],
                            "severity": "error",
                        }
                        for item in ruff_output
                    ]
                except (json.JSONDecodeError, KeyError):
                    pass

            suggestions = self._generate_ruff_suggestions(errors)

            return CheckResult(
                tool="ruff",
                passed=result.returncode == 0,
                errors=errors,
                suggestions=suggestions,
                duration=duration,
                exit_code=result.returncode,
                raw_output=result.stdout + result.stderr,
            )

        except FileNotFoundError:
            return CheckResult(
                tool="ruff",
                passed=False,
                errors=[{"message": "Ruff not installed", "severity": "error"}],
                suggestions=["Install Ruff: pip install ruff"],
            )

    def run_mypy(self, config_file: str = "scripts/mypy.ini") -> CheckResult:
        """
        Run Mypy type checker.

        Args:
            config_file: Path to mypy configuration file

        Returns:
            CheckResult with structured Mypy output

        Example:
            result = checker.run_mypy()
            for error in result.errors:
                if error['error_code'] == 'no-untyped-def':
                    add_type_hints(error['file'], error['line'])
        """
        start_time = time.time()

        try:
            result = subprocess.run(
                [sys.executable, "-m", "mypy", "--config-file", config_file],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            duration = time.time() - start_time

            # Parse Mypy output
            errors = self._parse_mypy_output(result.stdout)
            suggestions = self._generate_mypy_suggestions(errors)

            return CheckResult(
                tool="mypy",
                passed=result.returncode == 0,
                errors=errors,
                suggestions=suggestions,
                duration=duration,
                exit_code=result.returncode,
                raw_output=result.stdout + result.stderr,
            )

        except FileNotFoundError:
            return CheckResult(
                tool="mypy",
                passed=False,
                errors=[{"message": "Mypy not installed", "severity": "error"}],
                suggestions=["Install Mypy: pip install mypy"],
            )

    def run_import_linter(self, config_file: str = ".import-linter") -> CheckResult:
        """
        Run import-linter to validate architecture boundaries.

        Args:
            config_file: Path to import-linter configuration

        Returns:
            CheckResult with architecture violations

        Example:
            result = checker.run_import_linter()
            for error in result.errors:
                # AI understands architectural violations
                print(f"Layer {error['source']} imports {error['forbidden']}")
        """
        start_time = time.time()

        try:
            # Find lint-imports executable
            from forgebase.dev.api.utils import find_executable

            lint_imports = find_executable("lint-imports")

            result = subprocess.run(
                [lint_imports, "--config", config_file],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            duration = time.time() - start_time

            # Parse import-linter output
            errors = self._parse_import_linter_output(result.stdout)
            suggestions = self._generate_architecture_suggestions(errors)

            return CheckResult(
                tool="import-linter",
                passed=result.returncode == 0,
                errors=errors,
                suggestions=suggestions,
                duration=duration,
                exit_code=result.returncode,
                raw_output=result.stdout + result.stderr,
            )

        except FileNotFoundError:
            return CheckResult(
                tool="import-linter",
                passed=False,
                errors=[{"message": "import-linter not installed", "severity": "error"}],
                suggestions=["Install import-linter: pip install import-linter"],
            )

    def run_deptry(self, path: str = "src/") -> CheckResult:
        """
        Run Deptry to check dependency hygiene.

        Args:
            path: Path to check for dependencies

        Returns:
            CheckResult with dependency issues

        Example:
            result = checker.run_deptry()
            for error in result.errors:
                if error['type'] == 'DEP002':  # Obsolete dependency
                    remove_from_pyproject(error['package'])
        """
        start_time = time.time()

        try:
            from forgebase.dev.api.utils import find_executable

            deptry = find_executable("deptry")

            result = subprocess.run(
                [deptry, path],
                capture_output=True,
                text=True,
                cwd=self.project_root,
            )

            duration = time.time() - start_time

            errors = self._parse_deptry_output(result.stdout)
            suggestions = self._generate_dependency_suggestions(errors)

            return CheckResult(
                tool="deptry",
                passed=result.returncode == 0,
                errors=errors,
                suggestions=suggestions,
                duration=duration,
                exit_code=result.returncode,
                raw_output=result.stdout + result.stderr,
            )

        except FileNotFoundError:
            return CheckResult(
                tool="deptry",
                passed=False,
                errors=[{"message": "Deptry not installed", "severity": "error"}],
                suggestions=["Install Deptry: pip install deptry"],
            )

    def run_all(self) -> dict[str, CheckResult]:
        """
        Run all quality checks.

        Returns:
            Dictionary mapping tool name to CheckResult

        Example:
            results = checker.run_all()

            # AI can generate comprehensive report
            total_errors = sum(r.error_count for r in results.values())
            failed_tools = [name for name, r in results.items() if not r.passed]

            if failed_tools:
                print(f"Failed: {', '.join(failed_tools)}")
                print(f"Total errors: {total_errors}")
        """
        return {
            "ruff": self.run_ruff(),
            "mypy": self.run_mypy(),
            "import-linter": self.run_import_linter(),
            "deptry": self.run_deptry(),
        }

    # Parser methods

    def _parse_mypy_output(self, output: str) -> list[dict[str, Any]]:
        """Parse Mypy text output into structured errors."""
        errors = []
        for line in output.splitlines():
            # Format: file.py:line: error: message  [error-code]
            if ": error:" in line:
                parts = line.split(":")
                if len(parts) >= 3:
                    file = parts[0].strip()
                    try:
                        line_num = int(parts[1].strip())
                    except ValueError:
                        continue

                    message_part = ":".join(parts[3:]).strip()
                    message = message_part.split("[")[0].strip()
                    error_code = ""
                    if "[" in message_part and "]" in message_part:
                        error_code = message_part.split("[")[1].split("]")[0]

                    errors.append(
                        {
                            "file": file,
                            "line": line_num,
                            "message": message,
                            "error_code": error_code,
                            "severity": "error",
                        }
                    )
        return errors

    def _parse_import_linter_output(self, output: str) -> list[dict[str, Any]]:
        """Parse import-linter output into structured errors."""
        errors = []
        # Simplified parsing - can be enhanced
        if "Contracts: " in output and "broken" in output:
            lines = output.splitlines()
            for line in lines:
                if "->" in line and "imports" in line:
                    errors.append(
                        {
                            "message": line.strip(),
                            "severity": "error",
                            "type": "architecture-violation",
                        }
                    )
        return errors

    def _parse_deptry_output(self, output: str) -> list[dict[str, Any]]:
        """Parse Deptry output into structured errors."""
        errors = []
        for line in output.splitlines():
            if "DEP" in line:
                errors.append({"message": line.strip(), "severity": "error"})
        return errors

    # Suggestion generators

    def _generate_ruff_suggestions(self, errors: list[dict[str, Any]]) -> list[str]:
        """Generate AI-actionable suggestions from Ruff errors."""
        suggestions = []
        error_codes = {e.get("code") for e in errors if "code" in e}

        if "F401" in error_codes:
            suggestions.append("Remove unused imports with: ruff check --fix")
        if "I001" in error_codes:
            suggestions.append("Sort imports with: ruff check --fix")
        if "E501" in error_codes:
            suggestions.append("Format long lines with: ruff format")

        return suggestions

    def _generate_mypy_suggestions(self, errors: list[dict[str, Any]]) -> list[str]:
        """Generate AI-actionable suggestions from Mypy errors."""
        suggestions = []
        error_codes = {e.get("error_code") for e in errors if "error_code" in e}

        if "no-untyped-def" in error_codes:
            suggestions.append("Add type hints to function definitions")
        if "type-arg" in error_codes:
            suggestions.append("Add type parameters to generic types (e.g., dict[str, Any])")
        if "attr-defined" in error_codes:
            suggestions.append("Check for missing attributes or imports")

        return suggestions

    def _generate_architecture_suggestions(self, errors: list[dict[str, Any]]) -> list[str]:
        """Generate AI-actionable suggestions from architecture violations."""
        if errors:
            return [
                "Refactor imports to respect Clean Architecture boundaries",
                "Domain layer should not import from Application or Infrastructure",
                "Application layer should not import from Infrastructure",
            ]
        return []

    def _generate_dependency_suggestions(self, errors: list[dict[str, Any]]) -> list[str]:
        """Generate AI-actionable suggestions from dependency issues."""
        suggestions = []
        for error in errors:
            msg = error.get("message", "")
            if "DEP002" in msg:
                suggestions.append("Remove obsolete dependencies from pyproject.toml")
            elif "DEP003" in msg:
                suggestions.append("Add missing dependencies to pyproject.toml")
        return list(set(suggestions))

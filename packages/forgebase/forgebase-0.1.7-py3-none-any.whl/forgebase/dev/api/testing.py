"""
Testing API for AI Agents.

Provides programmatic test execution with structured results.

Usage:
    from forgebase.dev.api import TestRunner

    runner = TestRunner()

    # Run specific test types
    result = runner.run_unit_tests()
    if not result.passed:
        for failure in result.failures:
            analyze_and_fix(failure)

    # Run all tests
    results = runner.run_all()

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
class TestFailure:
    """Information about a test failure."""

    test_name: str
    file: str
    line: int = 0
    message: str = ""
    traceback: str = ""
    error_type: str = ""


@dataclass
class TestResult:
    """
    Result from test execution.

    Attributes:
        test_type: Type of tests run (unit, integration, property, contract)
        passed: Whether all tests passed
        total: Total number of tests
        passed_count: Number of tests that passed
        failed_count: Number of tests that failed
        skipped_count: Number of tests skipped
        failures: List of test failures with details
        duration: Time taken to run tests in seconds
        coverage: Test coverage percentage (if available)
        exit_code: Process exit code
        raw_output: Raw pytest output
    """

    test_type: str
    passed: bool
    total: int = 0
    passed_count: int = 0
    failed_count: int = 0
    skipped_count: int = 0
    failures: list[TestFailure] = field(default_factory=list)
    duration: float = 0.0
    coverage: float = 0.0
    exit_code: int = 0
    raw_output: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "test_type": self.test_type,
            "passed": self.passed,
            "total": self.total,
            "passed_count": self.passed_count,
            "failed_count": self.failed_count,
            "skipped_count": self.skipped_count,
            "failures": [f.__dict__ for f in self.failures],
            "duration": self.duration,
            "coverage": self.coverage,
            "exit_code": self.exit_code,
        }


class TestRunner:
    """
    Test execution API for AI agents.

    Runs pytest with structured output for programmatic analysis:
    - Detailed failure information
    - Coverage metrics
    - Timing data
    - Test categorization (unit, integration, property, contract)

    Example:
        runner = TestRunner()

        # Run unit tests
        result = runner.run_unit_tests()

        # AI analyzes failures
        for failure in result.failures:
            if "AssertionError" in failure.error_type:
                # Fix assertion
                fix_test_assertion(failure.file, failure.line)

        # Check coverage
        if result.coverage < 80:
            suggest_adding_tests()
    """

    def __init__(self, project_root: Path | None = None):
        """
        Initialize test runner.

        Args:
            project_root: Project root directory. Defaults to current directory.
        """
        self.project_root = project_root or Path.cwd()

    def run_unit_tests(self, verbose: bool = False) -> TestResult:
        """
        Run unit tests.

        Args:
            verbose: Whether to use verbose output

        Returns:
            TestResult with structured test results

        Example:
            result = runner.run_unit_tests()
            print(f"{result.passed_count}/{result.total} tests passed")
        """
        return self._run_pytest("unit", "tests/unit/", verbose)

    def run_integration_tests(self, verbose: bool = False) -> TestResult:
        """
        Run integration tests.

        Args:
            verbose: Whether to use verbose output

        Returns:
            TestResult with structured test results
        """
        return self._run_pytest("integration", "tests/integration/", verbose)

    def run_property_tests(self, verbose: bool = False) -> TestResult:
        """
        Run property-based tests.

        Args:
            verbose: Whether to use verbose output

        Returns:
            TestResult with structured test results
        """
        return self._run_pytest("property", "tests/property_based/", verbose)

    def run_contract_tests(self, verbose: bool = False) -> TestResult:
        """
        Run contract tests.

        Args:
            verbose: Whether to use verbose output

        Returns:
            TestResult with structured test results
        """
        return self._run_pytest("contract", "tests/contract_tests/", verbose)

    def run_all(self, verbose: bool = False) -> dict[str, TestResult]:
        """
        Run all test types.

        Args:
            verbose: Whether to use verbose output

        Returns:
            Dictionary mapping test type to TestResult

        Example:
            results = runner.run_all()

            # AI generates comprehensive report
            total_tests = sum(r.total for r in results.values())
            total_failures = sum(r.failed_count for r in results.values())

            print(f"Ran {total_tests} tests, {total_failures} failures")
        """
        return {
            "unit": self.run_unit_tests(verbose),
            "integration": self.run_integration_tests(verbose),
            "property": self.run_property_tests(verbose),
            "contract": self.run_contract_tests(verbose),
        }

    def _run_pytest(self, test_type: str, path: str, verbose: bool) -> TestResult:
        """Run pytest with structured output parsing."""
        start_time = time.time()

        # Build command
        cmd = [sys.executable, "-m", "pytest", path]
        if verbose:
            cmd.append("-v")

        # Disable coverage in pytest to avoid conflicts
        cmd.extend(["-o", "addopts="])

        try:
            result = subprocess.run(
                cmd, capture_output=True, text=True, cwd=self.project_root
            )

            duration = time.time() - start_time

            # Parse output
            test_result = self._parse_pytest_output(result.stdout, result.stderr, test_type)
            test_result.duration = duration
            test_result.exit_code = result.returncode
            test_result.passed = result.returncode == 0
            test_result.raw_output = result.stdout + result.stderr

            return test_result

        except FileNotFoundError:
            return TestResult(
                test_type=test_type,
                passed=False,
                exit_code=1,
                raw_output="pytest not found. Install with: pip install pytest",
            )

    def _parse_pytest_output(
        self, stdout: str, stderr: str, test_type: str
    ) -> TestResult:
        """Parse pytest output into structured result."""
        result = TestResult(test_type=test_type, passed=True)

        # Parse summary line: "X passed, Y failed"
        for line in stdout.splitlines():
            if " passed" in line or " failed" in line:
                # Extract numbers
                import re

                passed_match = re.search(r"(\d+) passed", line)
                failed_match = re.search(r"(\d+) failed", line)
                skipped_match = re.search(r"(\d+) skipped", line)

                if passed_match:
                    result.passed_count = int(passed_match.group(1))
                if failed_match:
                    result.failed_count = int(failed_match.group(1))
                if skipped_match:
                    result.skipped_count = int(skipped_match.group(1))

                result.total = (
                    result.passed_count + result.failed_count + result.skipped_count
                )

        # Parse failures
        if "FAILED" in stdout:
            failures = self._extract_failures(stdout)
            result.failures = failures

        return result

    def _extract_failures(self, output: str) -> list[TestFailure]:
        """Extract failure information from pytest output."""
        failures = []

        # Simple parsing - can be enhanced
        lines = output.splitlines()
        for i, line in enumerate(lines):
            if "FAILED" in line:
                # Extract test name
                test_name = line.split("FAILED")[1].strip()

                # Try to find error message in subsequent lines
                message = ""
                if i + 1 < len(lines):
                    message = lines[i + 1].strip()

                failures.append(
                    TestFailure(
                        test_name=test_name, file="", message=message, error_type="unknown"
                    )
                )

        return failures

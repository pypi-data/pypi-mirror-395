"""
Claude API Integration Example for ForgeBase.

This example shows how to integrate ForgeBase dev APIs with Claude API
for automated code quality, generation, and testing workflows.

Requirements:
    pip install anthropic

Usage:
    export ANTHROPIC_API_KEY="your-api-key"
    python examples/claude_api_integration.py

Author: ForgeBase Development Team
Created: 2025-11-04
"""

import json
import os
from typing import Any

from anthropic import Anthropic

from forgebase.dev.api import (
    ComponentDiscovery,
    QualityChecker,
    ScaffoldGenerator,
    TestRunner,
)


class ClaudeForgeBaseAgent:
    """
    AI Agent that uses Claude API + ForgeBase APIs for autonomous development.

    This agent can:
    - Analyze codebases
    - Generate new components
    - Check code quality
    - Fix errors autonomously
    - Run tests and analyze failures
    """

    def __init__(self, api_key: str | None = None):
        """
        Initialize Claude + ForgeBase agent.

        Args:
            api_key: Anthropic API key (default: ANTHROPIC_API_KEY env var)
        """
        self.client = Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))

        # Initialize ForgeBase APIs
        self.quality_checker = QualityChecker()
        self.scaffold_generator = ScaffoldGenerator()
        self.component_discovery = ComponentDiscovery()
        self.test_runner = TestRunner()

        # System prompt with ForgeBase instructions
        self.system_prompt = """You are an expert Python developer using ForgeBase framework.

IMPORTANT: You have access to ForgeBase Python APIs that return structured data.

Available APIs (already imported and instantiated):
1. quality_checker.run_all() - Returns CheckResult with structured errors
2. scaffold_generator.create_usecase(name, ...) - Returns ScaffoldResult with code
3. component_discovery.scan_project() - Returns DiscoveryResult with components
4. test_runner.run_all() - Returns TestResult with failures

Guidelines:
- Use error codes (F401, no-untyped-def, etc.) to determine fixes
- Access file, line, column directly from error dictionaries
- Modify generated code before writing files
- Always run quality checks before completing tasks

Respond with JSON containing:
{
    "analysis": "Your reasoning about the task",
    "actions": ["List of actions to take"],
    "code_changes": {"file": "content"},
    "next_steps": ["What to do next"]
}
"""

    def analyze_codebase(self) -> dict[str, Any]:
        """
        Analyze the codebase and report findings to Claude.

        Returns:
            Claude's analysis and recommendations
        """
        # Get structured component information
        discovery_result = self.component_discovery.scan_project()

        # Convert to JSON for Claude
        discovery_data = discovery_result.to_dict()

        # Ask Claude to analyze
        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            system=self.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"""Analyze this ForgeBase codebase structure:

{json.dumps(discovery_data, indent=2)}

Provide insights about:
1. Architecture (entities, use cases, repositories)
2. Potential issues or missing components
3. Recommendations for improvement
""",
                }
            ],
        )

        return {
            "discovery": discovery_data,
            "analysis": message.content[0].text if message.content else "",
        }

    def fix_quality_issues(self) -> dict[str, Any]:
        """
        Run quality checks and ask Claude to fix issues autonomously.

        Returns:
            Quality results and Claude's fixes
        """
        # Get structured quality results
        quality_results = self.quality_checker.run_all()

        # Convert to JSON for Claude
        quality_data = {
            tool: result.to_dict() for tool, result in quality_results.items()
        }

        # Ask Claude to fix
        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            system=self.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"""Quality check results from ForgeBase:

{json.dumps(quality_data, indent=2)}

For each error:
1. Identify the error code and file:line location
2. Determine the appropriate fix
3. Generate the corrected code

Focus on errors with codes like:
- F401 (unused import)
- F841 (unused variable)
- no-untyped-def (missing type hints)
- E501 (line too long)

Return JSON with code changes.
""",
                }
            ],
        )

        return {
            "quality_results": quality_data,
            "claude_fixes": message.content[0].text if message.content else "",
        }

    def generate_usecase(self, name: str, description: str) -> dict[str, Any]:
        """
        Generate a UseCase with Claude's customization.

        Args:
            name: UseCase name
            description: What the UseCase should do

        Returns:
            Generated code and Claude's enhancements
        """
        # Generate boilerplate
        scaffold_result = self.scaffold_generator.create_usecase(
            name=name,
            input_type=f"{name}Input",
            output_type=f"{name}Output",
        )

        if not scaffold_result.success:
            return {"error": scaffold_result.error}

        # Ask Claude to customize
        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            system=self.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"""ForgeBase generated this UseCase boilerplate:

```python
{scaffold_result.code}
```

Requirements: {description}

Enhance this code by:
1. Adding proper business logic in the execute() method
2. Adding validation in the Input DTO
3. Adding proper error handling
4. Ensuring type safety

Return the complete enhanced code.
""",
                }
            ],
        )

        return {
            "boilerplate": scaffold_result.code,
            "enhanced_code": message.content[0].text if message.content else "",
            "file_path": scaffold_result.file_path,
            "metadata": scaffold_result.metadata,
        }

    def run_tests_and_fix(self) -> dict[str, Any]:
        """
        Run tests and ask Claude to fix failures autonomously.

        Returns:
            Test results and Claude's fixes
        """
        # Get structured test results
        test_results = self.test_runner.run_all()

        # Convert to JSON for Claude
        test_data = {
            test_type: result.to_dict() for test_type, result in test_results.items()
        }

        # Ask Claude to analyze and fix
        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=4000,
            system=self.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"""Test results from ForgeBase:

{json.dumps(test_data, indent=2)}

For each test failure:
1. Analyze the error type and message
2. Locate the issue in the code (file:line provided)
3. Generate a fix

Return JSON with:
- Root cause analysis
- Proposed fixes with file paths
- Whether tests should pass after fixes
""",
                }
            ],
        )

        return {
            "test_results": test_data,
            "claude_analysis": message.content[0].text if message.content else "",
        }

    def autonomous_workflow(self, task: str) -> dict[str, Any]:
        """
        Complete autonomous development workflow.

        Args:
            task: High-level task description

        Returns:
            Complete workflow results
        """
        workflow_results: dict[str, Any] = {"task": task, "steps": []}

        # Step 1: Understand the codebase
        print("🔍 Step 1: Analyzing codebase...")
        analysis = self.analyze_codebase()
        workflow_results["steps"].append({"analysis": analysis})

        # Step 2: Ask Claude for implementation plan
        message = self.client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=2000,
            system=self.system_prompt,
            messages=[
                {
                    "role": "user",
                    "content": f"""Task: {task}

Codebase structure:
{json.dumps(analysis['discovery'], indent=2)}

Create an implementation plan using ForgeBase APIs:
1. What components to create (use scaffold_generator)
2. What to test (use test_runner)
3. Quality checks needed (use quality_checker)

Return a JSON plan.
""",
                }
            ],
        )

        plan = message.content[0].text if message.content else ""
        workflow_results["steps"].append({"plan": plan})

        # Step 3: Check initial quality
        print("✅ Step 2: Running quality checks...")
        quality = self.fix_quality_issues()
        workflow_results["steps"].append({"quality": quality})

        # Step 4: Run tests
        print("🧪 Step 3: Running tests...")
        tests = self.run_tests_and_fix()
        workflow_results["steps"].append({"tests": tests})

        return workflow_results


def example_1_analyze_codebase() -> None:
    """Example: Analyze codebase with Claude."""
    print("\n" + "=" * 60)
    print("Example 1: Codebase Analysis with Claude API")
    print("=" * 60)

    agent = ClaudeForgeBaseAgent()
    result = agent.analyze_codebase()

    print(f"\n📦 Found {result['discovery']['total_files_scanned']} files")
    print(f"📊 Entities: {len(result['discovery']['entities'])}")
    print(f"📊 UseCases: {len(result['discovery']['usecases'])}")
    print("\n🤖 Claude's Analysis:")
    print(result["analysis"])


def example_2_fix_quality() -> None:
    """Example: Autonomous quality fixing."""
    print("\n" + "=" * 60)
    print("Example 2: Autonomous Quality Fixing")
    print("=" * 60)

    agent = ClaudeForgeBaseAgent()
    result = agent.fix_quality_issues()

    # Show quality results
    for tool, data in result["quality_results"].items():
        status = "✅" if data["passed"] else "❌"
        print(f"\n{status} {tool}: {len(data['errors'])} errors")

    print("\n🤖 Claude's Fixes:")
    print(result["claude_fixes"])


def example_3_generate_usecase() -> None:
    """Example: Generate and enhance UseCase."""
    print("\n" + "=" * 60)
    print("Example 3: Generate UseCase with Claude")
    print("=" * 60)

    agent = ClaudeForgeBaseAgent()
    result = agent.generate_usecase(
        name="SendNotification",
        description="Send email/SMS notifications to users with templates and retry logic",
    )

    print(f"\n📝 Generated at: {result['file_path']}")
    print("\n🤖 Claude's Enhanced Code:")
    print(result["enhanced_code"][:500] + "...")


def example_4_autonomous_workflow() -> None:
    """Example: Complete autonomous workflow."""
    print("\n" + "=" * 60)
    print("Example 4: Autonomous Development Workflow")
    print("=" * 60)

    agent = ClaudeForgeBaseAgent()
    result = agent.autonomous_workflow(
        task="Add user authentication with JWT tokens and refresh logic"
    )

    print(f"\n🎯 Task: {result['task']}")
    print(f"📋 Completed {len(result['steps'])} steps")

    for i, step in enumerate(result["steps"], 1):
        print(f"\n  Step {i}: {list(step.keys())[0]}")


if __name__ == "__main__":
    print("🚀 Claude API + ForgeBase Integration Examples")
    print("=" * 60)

    # Check for API key
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("❌ Error: Set ANTHROPIC_API_KEY environment variable")
        print("   export ANTHROPIC_API_KEY='your-api-key'")
        exit(1)

    # Run examples
    try:
        example_1_analyze_codebase()
        example_2_fix_quality()
        example_3_generate_usecase()
        example_4_autonomous_workflow()

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback

        traceback.print_exc()

    print("\n" + "=" * 60)
    print("✅ Examples completed!")
    print("=" * 60)

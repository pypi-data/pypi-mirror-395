"""
ForgeBase Dev API - Examples for AI Agents.

This file demonstrates how AI coding agents should use ForgeBase's
programmatic APIs instead of CLI commands.

All APIs return structured data (dataclasses/dicts) suitable for
machine analysis and decision-making.

Author: ForgeBase Development Team
Created: 2025-11-04
"""

from forgebase.dev.api import (
    ComponentDiscovery,
    QualityChecker,
    ScaffoldGenerator,
    TestRunner,
)

# Example 1: Quality Checking
# ===========================


def example_quality_checking() -> None:
    """
    AI agent checks code quality and reasons about errors.

    Returns structured errors that AI can analyze and fix.
    """
    checker = QualityChecker()

    # Run all quality checks
    results = checker.run_all()

    # AI analyzes results
    for tool, result in results.items():
        print(f"\n{tool}: {'✅ PASSED' if result.passed else '❌ FAILED'}")

        if not result.passed:
            print(f"  Errors: {result.error_count}")
            print(f"  Duration: {result.duration:.2f}s")

            # AI can reason about specific errors
            for error in result.errors:
                if tool == "ruff" and error.get("code") == "F401":
                    # AI knows: F401 = unused import
                    file = error["file"]
                    line = error["line"]
                    print(f"  🤖 AI Action: Remove unused import in {file}:{line}")

                elif tool == "mypy" and error.get("error_code") == "no-untyped-def":
                    # AI knows: add type hints
                    file = error["file"]
                    line = error["line"]
                    print(f"  🤖 AI Action: Add type hints to {file}:{line}")

            # AI can use suggestions
            for suggestion in result.suggestions:
                print(f"  💡 Suggestion: {suggestion}")


# Example 2: Code Generation
# ===========================


def example_scaffolding() -> None:
    """
    AI agent generates code and modifies it before writing.

    Returns code as string for AI manipulation.
    """
    generator = ScaffoldGenerator()

    # Generate UseCase
    result = generator.create_usecase(
        name="CreateOrder",
        input_type="CreateOrderInput",
        output_type="CreateOrderOutput",
        repository="OrderRepositoryPort"
    )

    if result.success:
        print(f"\nGenerated {result.component_type}: {result.name}")
        print(f"Suggested path: {result.file_path}")
        print(f"Imports needed: {result.metadata['imports']}")

        # AI can modify code before writing
        code = result.code

        # Example: AI adds custom validation
        code = code.replace(
            "# TODO: Implement business logic here",
            """# Validate order
        if not input_dto.items:
            raise ValidationError("Order must have items")

        # Calculate total
        total = sum(item.price * item.quantity for item in input_dto.items)

        # Save order
        order = Order(items=input_dto.items, total=total)
        self.order_repository.save(order)"""
        )

        # AI writes to file
        # write_file(result.file_path, code)
        print("\n🤖 AI modified and saved code")
    else:
        print(f"❌ Generation failed: {result.error}")


# Example 3: Component Discovery
# ==============================


def example_discovery() -> None:
    """
    AI agent discovers and analyzes codebase architecture.

    Returns structured component information.
    """
    discovery = ComponentDiscovery()

    result = discovery.scan_project()

    print("\n📊 Project Analysis")
    print(f"  Total files scanned: {result.total_files_scanned}")
    print(f"  Total components: {result.total_components}")
    print(f"  Scan duration: {result.scan_duration:.2f}s")

    # AI analyzes architecture balance
    print("\n🏗️ Architecture Breakdown:")
    print(f"  Entities: {len(result.entities)}")
    print(f"  UseCases: {len(result.usecases)}")
    print(f"  Repositories: {len(result.repositories)}")
    print(f"  Ports: {len(result.ports)}")

    # AI can make architectural recommendations
    if len(result.usecases) < len(result.entities):
        print("\n🤖 AI Recommendation: Consider creating more UseCases")
        print("   Entities should have corresponding UseCases for operations")

    if len(result.repositories) < len(result.entities):
        print("\n🤖 AI Recommendation: Some entities may need repositories")

    # AI can detect unused components
    print("\n🔍 Component Details:")
    for entity in result.entities[:3]:  # Show first 3
        print(f"  - {entity.name} ({entity.file_path}:{entity.line_number})")
        if entity.docstring:
            print(f"    {entity.docstring}")


# Example 4: Test Execution
# =========================


def example_testing() -> None:
    """
    AI agent runs tests and analyzes failures.

    Returns structured test results.
    """
    runner = TestRunner()

    # Run unit tests
    result = runner.run_unit_tests()

    print("\n🧪 Unit Tests")
    print(f"  Passed: {result.passed_count}/{result.total}")
    print(f"  Failed: {result.failed_count}")
    print(f"  Duration: {result.duration:.2f}s")

    if not result.passed:
        print("\n❌ Test Failures:")
        for failure in result.failures:
            print(f"  - {failure.test_name}")
            print(f"    {failure.message}")

            # AI can reason about failures
            if "AssertionError" in failure.message:
                print("    🤖 AI Action: Fix assertion logic")
            elif "AttributeError" in failure.message:
                print("    🤖 AI Action: Check for missing attributes")

    # Run all test types
    all_results = runner.run_all()

    total_tests = sum(r.total for r in all_results.values())
    total_failures = sum(r.failed_count for r in all_results.values())

    print("\n📊 Full Test Suite:")
    print(f"  Total: {total_tests} tests")
    print(f"  Failures: {total_failures}")

    if total_failures == 0:
        print("  ✅ All tests passing!")
    else:
        print(f"  ❌ {total_failures} tests need fixing")


# Example 5: Complete AI Workflow
# ================================

def example_complete_workflow() -> None:
    """
    Complete AI agent workflow: analyze, generate, test, fix.

    Demonstrates how AI agents orchestrate multiple APIs.
    """
    print("\n" + "="*60)
    print("🤖 AI Agent Complete Workflow")
    print("="*60)

    # Step 1: Discover architecture
    print("\n📊 Step 1: Analyzing architecture...")
    discovery = ComponentDiscovery()
    disco_result = discovery.scan_project()
    print(f"  Found {len(disco_result.usecases)} UseCases")

    # Step 2: Generate new component (if needed)
    if len(disco_result.usecases) < 5:
        print("\n🏗️ Step 2: Generating new UseCase...")
        generator = ScaffoldGenerator()
        scaffold_result = generator.create_usecase("UpdateOrder")
        print(f"  Generated: {scaffold_result.name}")

    # Step 3: Run quality checks
    print("\n🔍 Step 3: Checking code quality...")
    checker = QualityChecker()
    quality_results = checker.run_all()
    passed = all(r.passed for r in quality_results.values())
    print(f"  Quality: {'✅ PASSED' if passed else '❌ FAILED'}")

    # Step 4: Run tests
    print("\n🧪 Step 4: Running tests...")
    runner = TestRunner()
    test_result = runner.run_unit_tests()
    print(f"  Tests: {test_result.passed_count}/{test_result.total} passed")

    # Step 5: AI decision making
    print("\n🤖 Step 5: AI Analysis & Decisions...")
    if not passed:
        print("  Decision: Fix quality issues before proceeding")
        total_errors = sum(r.error_count for r in quality_results.values())
        print(f"  Action: Fix {total_errors} quality issues")

    if test_result.failed_count > 0:
        print(f"  Decision: Fix {test_result.failed_count} failing tests")

    if passed and test_result.passed:
        print("  Decision: ✅ Ready to commit!")

    print("\n" + "="*60)


# Run examples
if __name__ == "__main__":
    print("ForgeBase Dev API - AI Agent Examples")
    print("=" * 60)

    print("\n\n1️⃣ Quality Checking Example")
    print("-" * 60)
    example_quality_checking()

    print("\n\n2️⃣ Code Generation Example")
    print("-" * 60)
    example_scaffolding()

    print("\n\n3️⃣ Component Discovery Example")
    print("-" * 60)
    example_discovery()

    print("\n\n4️⃣ Testing Example")
    print("-" * 60)
    example_testing()

    print("\n\n5️⃣ Complete Workflow Example")
    example_complete_workflow()

    print("\n\n" + "="*60)
    print("✅ All examples completed!")
    print("="*60)

#!/usr/bin/env python3
"""
Integration Demo: YAML Sync & Intent Tracking.

Demonstrates ForgeProcess ↔ ForgeBase integration through YAML synchronization
and cognitive coherence validation via intent tracking.

Run with:
    python examples/integration_demo.py

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import sys
import time
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from user_management.application import CreateUserInput, CreateUserUseCase
from user_management.infrastructure import InMemoryUserRepository

from forgebase.integration.intent_tracker import IntentTracker
from forgebase.integration.yaml_sync import YAMLSync


def print_section(title: str) -> None:
    """Print formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def demonstrate_yaml_sync():
    """Demonstrate YAML ↔ Code synchronization."""
    print_section("YAML ↔ Code Synchronization")

    sync = YAMLSync()

    # 1. Generate code from YAML spec
    print("1. Creating YAML specification...")

    yaml_spec = {
        'version': '1.0',
        'usecase': {
            'name': 'CreateUser',
            'description': 'Create a new user in the system',
            'inputs': [
                {'name': 'name', 'type': 'str', 'required': True},
                {'name': 'email', 'type': 'str', 'required': True}
            ],
            'outputs': [
                {'name': 'user_id', 'type': 'str'},
                {'name': 'name', 'type': 'str'},
                {'name': 'email', 'type': 'str'}
            ],
            'business_rules': [
                'Email must be unique',
                'Name cannot be empty',
                'Email must be valid format'
            ]
        }
    }

    # 2. Generate code
    print("\n2. Generating Python code from YAML...")
    generated_code = sync.generate_code(yaml_spec)

    print("✓ Code generated:")
    print("-" * 60)
    # Show first 20 lines
    lines = generated_code.split('\n')[:20]
    for line in lines:
        print(line)
    print("... (code continues) ...")
    print("-" * 60)

    # 3. Validate existing implementation
    print("\n3. Validating existing CreateUserUseCase...")

    drift = sync.detect_drift(CreateUserUseCase, yaml_spec)

    if drift:
        print(f"⚠️  Drift detected ({len(drift)} issues):")
        for issue in drift:
            print(f"  - {issue}")
    else:
        print("✓ No drift detected - implementation matches spec!")

    # 4. Export to YAML
    print("\n4. Exporting implementation to YAML...")

    export_path = Path("/tmp/create_user_exported.yaml")
    sync.export_to_yaml(CreateUserUseCase, export_path)

    print(f"✓ Exported to: {export_path}")

    if export_path.exists():
        print("\nExported YAML content:")
        print("-" * 60)
        print(export_path.read_text())
        print("-" * 60)


def demonstrate_intent_tracking():
    """Demonstrate intent tracking and coherence validation."""
    print_section("Intent Tracking & Cognitive Coherence")

    tracker = IntentTracker()
    repository = InMemoryUserRepository()
    usecase = CreateUserUseCase(user_repository=repository)

    # Scenario 1: Perfect coherence
    print("Scenario 1: Perfect Coherence")
    print("-" * 60)

    intent_id_1 = tracker.capture_intent(
        description="Create user with name and email",
        expected_outcome="User created successfully with valid email",
        source="forgeprocess",
        operation="create_user"
    )

    print(f"✓ Intent captured: {intent_id_1[:8]}...")

    # Execute
    start = time.time()
    try:
        input_dto = CreateUserInput(
            name="Alice Smith",
            email="alice@example.com"
        )
        output = usecase.execute(input_dto)
        outcome = f"User created successfully with valid email {output.email}"
        success = True
    except Exception as e:
        outcome = f"Failed: {e}"
        success = False

    duration_ms = (time.time() - start) * 1000

    # Record execution
    tracker.record_execution(
        intent_id=intent_id_1,
        actual_outcome=outcome,
        success=success,
        duration_ms=duration_ms,
        user_id=output.user_id if success else None
    )

    print(f"✓ Execution recorded: {outcome}")

    # Validate coherence
    report_1 = tracker.validate_coherence(intent_id_1)

    print("\n✓ Coherence Analysis:")
    print(f"  - Level: {report_1.coherence_level.value}")
    print(f"  - Similarity: {report_1.similarity_score:.2%}")
    print(f"  - Matches: {len(report_1.matches)}")
    print(f"  - Divergences: {len(report_1.divergences)}")

    if report_1.recommendations:
        print("\n  Recommendations:")
        for rec in report_1.recommendations:
            print(f"    - {rec}")

    # Scenario 2: Medium coherence (different wording)
    print("\n\nScenario 2: Medium Coherence (Different Wording)")
    print("-" * 60)

    intent_id_2 = tracker.capture_intent(
        description="Register new account",
        expected_outcome="Account registration complete",
        source="forgeprocess"
    )

    print(f"✓ Intent captured: {intent_id_2[:8]}...")

    # Execute
    start = time.time()
    try:
        input_dto = CreateUserInput(
            name="Bob Johnson",
            email="bob@example.com"
        )
        output = usecase.execute(input_dto)
        outcome = f"User {output.user_id} created with email {output.email}"
        success = True
    except Exception as e:
        outcome = f"Error: {e}"
        success = False

    duration_ms = (time.time() - start) * 1000

    tracker.record_execution(
        intent_id=intent_id_2,
        actual_outcome=outcome,
        success=success,
        duration_ms=duration_ms,
        user_id=output.user_id if success else None
    )

    print(f"✓ Execution recorded: {outcome}")

    report_2 = tracker.validate_coherence(intent_id_2)

    print("\n✓ Coherence Analysis:")
    print(f"  - Level: {report_2.coherence_level.value}")
    print(f"  - Similarity: {report_2.similarity_score:.2%}")

    if report_2.divergences:
        print("\n  Divergences:")
        for div in report_2.divergences:
            print(f"    - {div}")

    # Scenario 3: Divergent (failure case)
    print("\n\nScenario 3: Divergent (Failure Case)")
    print("-" * 60)

    intent_id_3 = tracker.capture_intent(
        description="Create user with duplicate email",
        expected_outcome="User created successfully",
        source="test"
    )

    print(f"✓ Intent captured: {intent_id_3[:8]}...")

    # Execute with duplicate email
    start = time.time()
    try:
        input_dto = CreateUserInput(
            name="Alice Clone",
            email="alice@example.com"  # Duplicate!
        )
        output = usecase.execute(input_dto)
        outcome = f"User created: {output.user_id}"
        success = True
    except Exception as e:
        outcome = f"Failed: {e}"
        success = False

    duration_ms = (time.time() - start) * 1000

    tracker.record_execution(
        intent_id=intent_id_3,
        actual_outcome=outcome,
        success=success,
        duration_ms=duration_ms
    )

    print(f"✓ Execution recorded: {outcome}")

    report_3 = tracker.validate_coherence(intent_id_3)

    print("\n✓ Coherence Analysis:")
    print(f"  - Level: {report_3.coherence_level.value}")
    print(f"  - Similarity: {report_3.similarity_score:.2%}")
    print(f"  - Success: {success}")

    if report_3.divergences:
        print("\n  Divergences:")
        for div in report_3.divergences:
            print(f"    - {div}")

    if report_3.recommendations:
        print("\n  Recommendations:")
        for rec in report_3.recommendations:
            print(f"    - {rec}")

    # Overall statistics
    print("\n\nOverall Statistics")
    print("-" * 60)

    stats = tracker.get_coherence_stats()

    print(f"✓ Total intents tracked: {stats['total_intents']}")
    print(f"✓ Average similarity: {stats['avg_similarity']:.2%}")
    print(f"✓ Success rate: {stats['success_rate']:.2%}")

    print("\n✓ Coherence distribution:")
    for level, count in stats['coherence_distribution'].items():
        print(f"  - {level}: {count}")

    # Export learning data
    print("\n\nExporting Learning Data")
    print("-" * 60)

    learning_data = tracker.export_learning_data()

    print(f"✓ Exported {len(learning_data)} learning examples")
    print("\nExample learning record:")
    if learning_data:
        import json
        print(json.dumps(learning_data[0], indent=2))


def main():
    """Run integration demonstrations."""
    print("\n" + "="*60)
    print("  ForgeBase Integration - YAML Sync & Intent Tracking")
    print("="*60)

    try:
        # 1. YAML Synchronization
        demonstrate_yaml_sync()

        # 2. Intent Tracking
        demonstrate_intent_tracking()

        # Success
        print_section("✅ All Demonstrations Complete!")

        print("""
This demonstration showed:
  ✓ YAML ↔ Code Synchronization
    - Generate code from YAML specs
    - Detect drift between spec and implementation
    - Export implementations to YAML

  ✓ Intent Tracking & Coherence Validation
    - Capture intentions before execution
    - Record actual execution results
    - Measure cognitive coherence
    - Generate recommendations for improvement
    - Export learning data for analysis

These features enable ForgeProcess and ForgeBase to maintain
cognitive coherence, creating a feedback loop for continuous
improvement and learning.

Next steps:
  - Integrate with ForgeProcess for real-time sync
  - Build ML models from learning data
  - Automate drift detection and correction
  - Create cognitive coherence dashboards
        """)

    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

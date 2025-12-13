#!/usr/bin/env python3
"""
Complete ForgeBase Flow Example.

This example demonstrates the entire ForgeBase architecture in action:
- Domain Layer: Entities (User) and ValueObjects (Email)
- Application Layer: UseCases (CreateUser), Ports, DTOs
- Infrastructure: Repository implementation
- Adapters: CLI interaction
- Observability: Metrics, logging, tracing

This shows how Clean Architecture + Hexagonal Architecture work together
with native observability to create maintainable, testable, and observable systems.

Run with:
    python examples/complete_flow.py

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from user_management.application import (
    CreateUserInput,
    CreateUserUseCase,
)
from user_management.domain import Email, User
from user_management.infrastructure import InMemoryUserRepository

from forgebase.core_init import ForgeBaseCore
from forgebase.domain.exceptions import BusinessRuleViolation, ValidationError


def print_section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")


def demonstrate_domain_layer():
    """Demonstrate domain entities and value objects."""
    print_section("1. Domain Layer - Entities & Value Objects")

    # Create valid email
    print("Creating valid email...")
    email = Email(address="john.doe@example.com")
    print(f"✓ Email created: {email}")
    print(f"  - Domain: {email.domain}")
    print(f"  - Local part: {email.local_part}")

    # Try invalid email
    print("\nTrying invalid email...")
    try:
        Email(address="not-an-email")
    except ValidationError as e:
        print(f"✗ Validation failed (expected): {e}")

    # Create user
    print("\nCreating user entity...")
    user = User(
        name="John Doe",
        email=email
    )
    user.validate()
    print(f"✓ User created: {user}")
    print(f"  - ID: {user.id}")
    print(f"  - Active: {user.is_active}")

    # Business rule: deactivation
    print("\nTesting business rules...")
    user.deactivate()
    print(f"✓ User deactivated: is_active={user.is_active}")

    try:
        user.activate()  # Should fail - business rule
    except BusinessRuleViolation as e:
        print(f"✗ Reactivation blocked (expected): {e}")

    return user


def demonstrate_application_layer():
    """Demonstrate application layer with UseCases."""
    print_section("2. Application Layer - UseCases & Ports")

    # Setup infrastructure
    print("Setting up repository (infrastructure)...")
    repository = InMemoryUserRepository()
    print(f"✓ Repository created: {repository.info()}")

    # Create UseCase with dependency injection
    print("\nCreating UseCase with dependency injection...")
    usecase = CreateUserUseCase(user_repository=repository)
    print("✓ CreateUserUseCase initialized")

    # Execute UseCase - Success case
    print("\nExecuting UseCase - Create first user...")
    input_dto = CreateUserInput(
        name="Alice Smith",
        email="alice@example.com"
    )

    output = usecase.execute(input_dto)
    print("✓ User created successfully!")
    print(f"  - User ID: {output.user_id}")
    print(f"  - Name: {output.name}")
    print(f"  - Email: {output.email}")
    print(f"  - Created at: {output.created_at}")

    # Execute UseCase - Duplicate email (business rule violation)
    print("\nExecuting UseCase - Try duplicate email...")
    try:
        duplicate_input = CreateUserInput(
            name="Alice Clone",
            email="alice@example.com"  # Same email!
        )
        usecase.execute(duplicate_input)
    except BusinessRuleViolation as e:
        print(f"✗ Duplicate email blocked (expected): {e}")

    # Create another user
    print("\nExecuting UseCase - Create second user...")
    input_dto2 = CreateUserInput(
        name="Bob Johnson",
        email="bob@example.com"
    )
    output2 = usecase.execute(input_dto2)
    print(f"✓ Second user created: {output2.user_id}")

    print(f"\nRepository now has {repository.count()} users")

    return repository, usecase


def demonstrate_observability():
    """Demonstrate observability features."""
    print_section("3. Observability - Metrics, Logging, Tracing")

    print("Initializing ForgeBase Core with observability...")

    # Initialize ForgeBase core
    core = ForgeBaseCore()
    core.bootstrap()

    print("✓ ForgeBase Core initialized")

    # Register UseCase
    repository = InMemoryUserRepository()
    usecase = CreateUserUseCase(user_repository=repository)
    core.register_usecase('create_user', usecase)

    print("✓ UseCase registered in core")

    # Execute with observability
    print("\nExecuting UseCase with full observability...")

    logger = core.container.get('logger')
    logger.info("Creating user with observability", operation="create_user")

    input_dto = CreateUserInput(
        name="Charlie Brown",
        email="charlie@example.com"
    )

    output = usecase.execute(input_dto)

    logger.info(
        "User created successfully",
        user_id=output.user_id,
        email=output.email
    )

    # Get metrics
    metrics = core.container.get('metrics')
    report = metrics.report()

    print("\n✓ Metrics collected:")
    if 'counters' in report and report['counters']:
        print("  Counters:")
        for name, value in report['counters'].items():
            print(f"    - {name}: {value}")
    if 'histograms' in report and report['histograms']:
        print("  Histograms:")
        for name, values in report['histograms'].items():
            if values:
                avg = sum(values) / len(values)
                print(f"    - {name}: avg={avg:.2f}ms, count={len(values)}")

    # Health check
    print("\n✓ System health check:")
    health = core.health_check()
    print(f"  - Healthy: {health['healthy']}")
    print(f"  - Components: {len(health['components'])}")
    print(f"  - UseCases: {health['components']['usecases']['count']}")

    core.shutdown()
    print("\n✓ Core shutdown complete")

    return core


def demonstrate_complete_integration():
    """Demonstrate complete integration flow."""
    print_section("4. Complete Integration - End-to-End Flow")

    # Initialize everything
    core = ForgeBaseCore()
    core.bootstrap()

    repository = InMemoryUserRepository()
    usecase = CreateUserUseCase(user_repository=repository)

    core.register_usecase('create_user', usecase)

    logger = core.container.get('logger')

    # Simulate multiple operations
    users_to_create = [
        ("Emma Watson", "emma@example.com"),
        ("Frank Ocean", "frank@example.com"),
        ("Grace Hopper", "grace@example.com")
    ]

    print(f"Creating {len(users_to_create)} users...")

    created_users = []
    for name, email in users_to_create:
        logger.info("Creating user", name=name, email=email)

        input_dto = CreateUserInput(name=name, email=email)
        output = usecase.execute(input_dto)

        created_users.append(output)
        print(f"  ✓ Created: {name} ({output.user_id})")

    print(f"\n✓ Successfully created {len(created_users)} users")

    # Verify repository state
    all_users = repository.find_all()
    print(f"\n✓ Repository contains {len(all_users)} users:")
    for user in all_users:
        print(f"  - {user.name} <{user.email}> [{'active' if user.is_active else 'inactive'}]")

    # Final health check
    health = core.health_check()
    print(f"\n✓ Final system health: {health['healthy']}")

    # Show system info
    info = core.info()
    print("\n✓ System information:")
    print(f"  - Initialized: {info['initialized']}")
    print(f"  - UseCases: {info['usecases']['count']}")
    print(f"  - Services: {len(info['services']['registered'])}")

    core.shutdown()

    return created_users


def main():
    """Run complete flow demonstration."""
    print("\n" + "="*60)
    print("  ForgeBase - Complete Flow Demonstration")
    print("  Cognitive Architecture in Action")
    print("="*60)

    try:
        # 1. Domain Layer
        demonstrate_domain_layer()

        # 2. Application Layer
        demonstrate_application_layer()

        # 3. Observability
        demonstrate_observability()

        # 4. Complete Integration
        demonstrate_complete_integration()

        # Success!
        print_section("✅ All Demonstrations Complete!")

        print("""
This example demonstrated:
  ✓ Domain Layer: Entities, ValueObjects, Business Rules
  ✓ Application Layer: UseCases, Ports, DTOs
  ✓ Infrastructure: Repository implementation
  ✓ Observability: Metrics, Logging, Health Checks
  ✓ Clean Architecture: Layer separation and dependency rules
  ✓ Hexagonal Architecture: Ports and Adapters pattern
  ✓ Cognitive Coherence: Reflexive, observable, maintainable

The system is reflexive (understands itself), autonomous (independent modules),
and coherent (consistent patterns throughout).

Next steps:
  - Explore examples/user_management/ for source code
  - Read docs/BACKLOG.md for architecture decisions
  - Run tests: python -m unittest discover tests/
  - Try creating your own UseCases and Adapters
        """)

    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

"""
ForgeBase Testing Infrastructure.

Provides comprehensive testing utilities for ForgeBase applications:
- ForgeTestCase: Cognitive test base class
- Fakes: In-memory implementations for testing
- Fixtures: Sample data and builders

:author: ForgeBase Development Team
:since: 2025-11-03
"""

from forgebase.testing.fakes import FakeLogger, FakeMetricsCollector, FakeRepository
from forgebase.testing.fixtures import (
    EntityBuilder,
    TestEntity,
    create_sample_entities,
    create_sample_entity,
)
from forgebase.testing.forge_test_case import ForgeTestCase

__all__ = [
    'ForgeTestCase',
    'FakeLogger',
    'FakeRepository',
    'FakeMetricsCollector',
    'EntityBuilder',
    'TestEntity',
    'create_sample_entity',
    'create_sample_entities',
]

"""
Sample data and fixtures for testing.

Provides builders and factories for creating test data with minimal boilerplate.
Supports fluent interfaces, reproducible generation, and common test scenarios.

Philosophy:
    Tests should focus on business logic, not data setup. Sample data builders
    provide sensible defaults while allowing customization where needed. This
    follows the Test Data Builder pattern from "Growing Object-Oriented Software
    Guided by Tests".

    Benefits:
    1. Readable - intent-revealing names
    2. Minimal boilerplate - one line creates complete objects
    3. Customizable - fluent interface for overrides
    4. Reproducible - seeded random generation
    5. Realistic - data that looks real

Use Cases:
    - Creating test entities quickly
    - Generating bulk test data
    - Consistent test data across tests
    - Regression test fixtures

Example::

    from forgebase.testing.fixtures.sample_data import EntityBuilder, random_email

    # Quick entity creation
    user = EntityBuilder().with_id("test-user").build()

    # Fluent customization
    admin = (
        EntityBuilder()
        .with_id("admin-1")
        .with_attribute("role", "admin")
        .with_attribute("email", "admin@example.com")
        .build()
    )

    # Generate multiple
    users = EntityBuilder().build_many(10)

    # Random data
    email = random_email()  # "user_a3f2@example.com"
    name = random_name()    # "Alice Johnson"

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import random
import string
import uuid
from datetime import datetime, timedelta
from typing import Any

from forgebase.domain.entity_base import EntityBase

# Random data generation

def random_string(length: int = 10, charset: str | None = None) -> str:
    """
    Generate random string.

    :param length: String length
    :type length: int
    :param charset: Character set (default: alphanumeric)
    :type charset: Optional[str]
    :return: Random string
    :rtype: str

    Example::

        s = random_string()  # "aB3xK9pQw2"
        hex_str = random_string(8, string.hexdigits)  # "A3F28E1D"
    """
    if charset is None:
        charset = string.ascii_letters + string.digits

    return ''.join(random.choice(charset) for _ in range(length))


def random_email(domain: str = "example.com") -> str:
    """
    Generate random email address.

    :param domain: Email domain
    :type domain: str
    :return: Random email
    :rtype: str

    Example::

        email = random_email()  # "user_a3f2@example.com"
        email = random_email("test.org")  # "user_x9k4@test.org"
    """
    username = "user_" + random_string(4).lower()
    return f"{username}@{domain}"


def random_name() -> str:
    """
    Generate random person name.

    :return: Random name
    :rtype: str

    Example::

        name = random_name()  # "Alice Johnson"
    """
    first_names = [
        "Alice", "Bob", "Carol", "David", "Eve", "Frank",
        "Grace", "Henry", "Iris", "Jack", "Kate", "Leo"
    ]

    last_names = [
        "Smith", "Johnson", "Williams", "Brown", "Jones",
        "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"
    ]

    return f"{random.choice(first_names)} {random.choice(last_names)}"


def random_int(min_val: int = 0, max_val: int = 100) -> int:
    """
    Generate random integer.

    :param min_val: Minimum value (inclusive)
    :type min_val: int
    :param max_val: Maximum value (inclusive)
    :type max_val: int
    :return: Random integer
    :rtype: int
    """
    return random.randint(min_val, max_val)


def random_float(min_val: float = 0.0, max_val: float = 100.0) -> float:
    """
    Generate random float.

    :param min_val: Minimum value
    :type min_val: float
    :param max_val: Maximum value
    :type max_val: float
    :return: Random float
    :rtype: float
    """
    return random.uniform(min_val, max_val)


def random_bool() -> bool:
    """
    Generate random boolean.

    :return: Random boolean
    :rtype: bool
    """
    return random.choice([True, False])


def random_date(
    start: datetime | None = None,
    end: datetime | None = None
) -> datetime:
    """
    Generate random datetime.

    :param start: Start date (default: 1 year ago)
    :type start: Optional[datetime]
    :param end: End date (default: now)
    :type end: Optional[datetime]
    :return: Random datetime
    :rtype: datetime
    """
    if end is None:
        end = datetime.utcnow()

    if start is None:
        start = end - timedelta(days=365)

    time_between = end - start
    random_seconds = random.randint(0, int(time_between.total_seconds()))

    return start + timedelta(seconds=random_seconds)


def random_choice(choices: list[Any]) -> Any:
    """
    Pick random item from list.

    :param choices: List of choices
    :type choices: List[Any]
    :return: Random choice
    :rtype: Any
    """
    return random.choice(choices)


def seed(value: int) -> None:
    """
    Seed random generator for reproducible tests.

    :param value: Seed value
    :type value: int

    Example::

        from forgebase.testing.fixtures.sample_data import seed, random_email

        seed(42)
        email1 = random_email()

        seed(42)
        email2 = random_email()

        assert email1 == email2  # Reproducible!
    """
    random.seed(value)


# Test data builders

class TestEntity(EntityBase):
    """
    Sample entity for testing.

    Simple entity with common attributes for test scenarios.

    :ivar name: Entity name
    :vartype name: str
    :ivar value: Numeric value
    :vartype value: int
    :ivar active: Active status
    :vartype active: bool
    :ivar metadata: Additional metadata
    :vartype metadata: Dict[str, Any]
    """

    def __init__(
        self,
        id: str | None = None,
        name: str = "Test Entity",
        value: int = 0,
        active: bool = True,
        metadata: dict[str, Any] | None = None
    ):
        """
        Initialize test entity.

        :param id: Entity ID
        :type id: Optional[str]
        :param name: Entity name
        :type name: str
        :param value: Numeric value
        :type value: int
        :param active: Active status
        :type active: bool
        :param metadata: Additional metadata
        :type metadata: Optional[Dict[str, Any]]
        """
        super().__init__(id)
        self.name = name
        self.value = value
        self.active = active
        self.metadata = metadata or {}

    def validate(self) -> None:
        """Validate entity state."""
        if not self.name:
            raise ValueError("Name cannot be empty")

        if self.value < 0:
            raise ValueError("Value cannot be negative")


class EntityBuilder:
    """
    Fluent builder for test entities.

    Provides convenient interface for creating entities with custom attributes.
    Follows the Builder pattern with method chaining.

    Example::

        # Simple entity
        entity = EntityBuilder().build()

        # Customized entity
        entity = (
            EntityBuilder()
            .with_id("test-123")
            .with_name("Custom Name")
            .with_value(100)
            .with_active(False)
            .with_metadata({"key": "value"})
            .build()
        )

        # Multiple entities
        entities = EntityBuilder().with_name("User").build_many(10)
    """

    def __init__(self):
        """Initialize builder with defaults."""
        self._id: str | None = None
        self._name = "Test Entity"
        self._value = 0
        self._active = True
        self._metadata: dict[str, Any] = {}
        self._attributes: dict[str, Any] = {}

    def with_id(self, id: str) -> 'EntityBuilder':
        """
        Set entity ID.

        :param id: Entity ID
        :type id: str
        :return: Builder for chaining
        :rtype: EntityBuilder
        """
        self._id = id
        return self

    def with_random_id(self) -> 'EntityBuilder':
        """
        Set random UUID as ID.

        :return: Builder for chaining
        :rtype: EntityBuilder
        """
        self._id = str(uuid.uuid4())
        return self

    def with_name(self, name: str) -> 'EntityBuilder':
        """
        Set entity name.

        :param name: Entity name
        :type name: str
        :return: Builder for chaining
        :rtype: EntityBuilder
        """
        self._name = name
        return self

    def with_random_name(self) -> 'EntityBuilder':
        """
        Set random person name.

        :return: Builder for chaining
        :rtype: EntityBuilder
        """
        self._name = random_name()
        return self

    def with_value(self, value: int) -> 'EntityBuilder':
        """
        Set numeric value.

        :param value: Numeric value
        :type value: int
        :return: Builder for chaining
        :rtype: EntityBuilder
        """
        self._value = value
        return self

    def with_random_value(
        self,
        min_val: int = 0,
        max_val: int = 100
    ) -> 'EntityBuilder':
        """
        Set random value.

        :param min_val: Minimum value
        :type min_val: int
        :param max_val: Maximum value
        :type max_val: int
        :return: Builder for chaining
        :rtype: EntityBuilder
        """
        self._value = random_int(min_val, max_val)
        return self

    def with_active(self, active: bool) -> 'EntityBuilder':
        """
        Set active status.

        :param active: Active status
        :type active: bool
        :return: Builder for chaining
        :rtype: EntityBuilder
        """
        self._active = active
        return self

    def with_metadata(self, metadata: dict[str, Any]) -> 'EntityBuilder':
        """
        Set metadata dictionary.

        :param metadata: Metadata
        :type metadata: Dict[str, Any]
        :return: Builder for chaining
        :rtype: EntityBuilder
        """
        self._metadata = metadata
        return self

    def with_attribute(self, key: str, value: Any) -> 'EntityBuilder':
        """
        Add custom attribute.

        :param key: Attribute name
        :type key: str
        :param value: Attribute value
        :type value: Any
        :return: Builder for chaining
        :rtype: EntityBuilder
        """
        self._attributes[key] = value
        return self

    def build(self) -> TestEntity:
        """
        Build the entity.

        :return: Constructed entity
        :rtype: TestEntity
        """
        entity = TestEntity(
            id=self._id,
            name=self._name,
            value=self._value,
            active=self._active,
            metadata=self._metadata.copy()
        )

        # Add custom attributes
        for key, value in self._attributes.items():
            setattr(entity, key, value)

        return entity

    def build_many(self, count: int) -> list[TestEntity]:
        """
        Build multiple entities with auto-generated IDs.

        :param count: Number of entities to create
        :type count: int
        :return: List of entities
        :rtype: List[TestEntity]

        Example::

            entities = EntityBuilder().with_name("User").build_many(10)
            assert len(entities) == 10
            assert all(e.name == "User" for e in entities)
            assert len(set(e.id for e in entities)) == 10  # Unique IDs
        """
        entities = []

        for i in range(count):
            # Create unique ID if not specified
            if self._id is None:
                builder = EntityBuilder()
                builder._name = self._name
                builder._value = self._value
                builder._active = self._active
                builder._metadata = self._metadata.copy()
                builder._attributes = self._attributes.copy()
                builder._id = f"{self._name.replace(' ', '_').lower()}_{i}"
                entities.append(builder.build())
            else:
                entities.append(self.build())

        return entities


# Common test scenarios

def create_sample_entity() -> TestEntity:
    """
    Create a single sample entity with random data.

    :return: Sample entity
    :rtype: TestEntity
    """
    return (
        EntityBuilder()
        .with_random_id()
        .with_random_name()
        .with_random_value()
        .build()
    )


def create_sample_entities(count: int = 10) -> list[TestEntity]:
    """
    Create multiple sample entities.

    :param count: Number of entities
    :type count: int
    :return: List of entities
    :rtype: List[TestEntity]
    """
    return [create_sample_entity() for _ in range(count)]


# Export convenience functions
__all__ = [
    # Random generators
    'random_string',
    'random_email',
    'random_name',
    'random_int',
    'random_float',
    'random_bool',
    'random_date',
    'random_choice',
    'seed',
    # Builders
    'EntityBuilder',
    'TestEntity',
    # Factories
    'create_sample_entity',
    'create_sample_entities',
]

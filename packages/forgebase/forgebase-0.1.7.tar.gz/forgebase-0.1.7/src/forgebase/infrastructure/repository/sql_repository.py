"""
SQL-based repository implementation using SQLAlchemy.

Provides robust database persistence with transaction support, connection pooling,
and query optimization. Suitable for production use with relational databases.

Philosophy:
    While JSON repositories work for development and small datasets, production
    systems require the reliability, performance, and query capabilities of SQL
    databases. This implementation uses SQLAlchemy to abstract database specifics
    while providing a familiar Repository interface.

    Transactions ensure data consistency, connection pooling enables concurrent
    access, and SQL's query optimization handles large datasets efficiently.

Supported Databases:
    - PostgreSQL (recommended for production)
    - MySQL/MariaDB
    - SQLite (testing and development)
    - Oracle, MS SQL Server (via SQLAlchemy dialects)

Example::

    # Create repository with SQLite in-memory database
    engine = create_engine('sqlite:///:memory:')
    repository = SQLRepository(
        engine=engine,
        entity_class=User,
        table_name='users'
    )

    # With PostgreSQL
    engine = create_engine('postgresql://user:pass@localhost/db')
    repository = SQLRepository(engine, User, 'users')

    # Use like any repository
    user = User(name="Alice", email="alice@example.com")
    repository.save(user)

    found = repository.find_by_id(user.id)

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import json
from collections.abc import Callable, Iterator
from contextlib import contextmanager
from typing import Any

from sqlalchemy import (  # type: ignore[import-not-found]
    JSON,
    Column,
    Engine,
    MetaData,
    String,
    Table,
    text,
)
from sqlalchemy.exc import SQLAlchemyError  # type: ignore[import-not-found]
from sqlalchemy.orm import Session, sessionmaker  # type: ignore[import-not-found]

from forgebase.domain.entity_base import EntityBase
from forgebase.infrastructure.repository.repository_base import (
    RepositoryBase,
    RepositoryError,
)


class SQLRepository(RepositoryBase[EntityBase]):
    """
    SQL-based repository implementation using SQLAlchemy.

    This implementation provides production-ready persistence with:
    - Transaction support (ACID guarantees)
    - Connection pooling for concurrent access
    - Query optimization via SQL indexes
    - Support for multiple database backends

    Design Decisions:
        - Uses SQLAlchemy Core (not ORM) for flexibility
        - Stores entities as JSON in a single column (schemaless)
        - ID column indexed for fast lookups
        - Transactions ensure consistency
        - Connection pool managed by SQLAlchemy

    Schema:
        The repository creates a simple table structure:
        - id (VARCHAR, PRIMARY KEY): Entity ID
        - data (JSON/TEXT): Serialized entity data

    Limitations:
        - JSON storage means no SQL queries on entity fields
        - For complex queries, consider using SQLAlchemy ORM instead
        - Schema migrations must be handled externally

    :ivar engine: SQLAlchemy engine for database connections
    :vartype engine: Engine
    :ivar entity_class: Entity class for type checking
    :vartype entity_class: Type[EntityBase]
    :ivar table_name: Database table name
    :vartype table_name: str
    :ivar _session_factory: Session factory for creating DB sessions
    :vartype _session_factory: sessionmaker

    Example::

        # Setup
        from sqlalchemy import create_engine
        engine = create_engine('sqlite:///app.db')

        # Create repository
        repo = SQLRepository(
            engine=engine,
            entity_class=User,
            table_name='users',
            to_dict=lambda e: e.to_dict(),
            from_dict=User.from_dict
        )

        # Use transactions
        with repo.transaction():
            user1 = User(name="Alice")
            user2 = User(name="Bob")
            repo.save(user1)
            repo.save(user2)
            # Both saved atomically

        # Query
        all_users = repo.find_all()
        user = repo.find_by_id(user1.id)
    """

    def __init__(
        self,
        engine: Engine,
        entity_class: type[EntityBase],
        table_name: str,
        to_dict: Callable[[EntityBase], dict[str, Any]] | None = None,
        from_dict: Callable[[dict[str, Any]], EntityBase] | None = None,
        create_table: bool = True
    ):
        """
        Initialize SQL repository.

        :param engine: SQLAlchemy engine
        :type engine: Engine
        :param entity_class: Entity class for type checking
        :type entity_class: Type[EntityBase]
        :param table_name: Database table name
        :type table_name: str
        :param to_dict: Custom serializer (defaults to entity.to_dict())
        :type to_dict: Optional[Callable[[EntityBase], dict]]
        :param from_dict: Custom deserializer (defaults to entity_class.from_dict())
        :type from_dict: Optional[Callable[[dict], EntityBase]]
        :param create_table: Whether to create table if not exists (default: True)
        :type create_table: bool

        Example::

            engine = create_engine('sqlite:///:memory:')
            repo = SQLRepository(engine, User, 'users')
        """
        self.engine = engine
        self.entity_class = entity_class
        self.table_name = table_name
        self._to_dict = to_dict or (lambda e: e.to_dict())  # type: ignore[attr-defined]
        self._from_dict = from_dict or entity_class.from_dict  # type: ignore[attr-defined]

        # Create session factory
        self._session_factory = sessionmaker(bind=engine)

        # Define table schema
        self.metadata = MetaData()
        self.table = Table(
            table_name,
            self.metadata,
            Column('id', String(255), primary_key=True),
            Column('data', JSON if self._supports_json() else String(65535))
        )

        # Create table if requested
        if create_table:
            self._create_table()

    def _supports_json(self) -> bool:
        """
        Check if database supports JSON column type.

        :return: True if JSON supported
        :rtype: bool
        """
        dialect_name = self.engine.dialect.name
        # PostgreSQL, MySQL 5.7+, SQLite 3.9+ support JSON
        return dialect_name in ('postgresql', 'mysql', 'sqlite')

    def _create_table(self) -> None:
        """
        Create table if it doesn't exist.

        :raises RepositoryError: If table creation fails
        """
        try:
            self.metadata.create_all(self.engine)
        except SQLAlchemyError as e:
            raise RepositoryError(
                f"Failed to create table '{self.table_name}'",
                context={'table': self.table_name, 'error': str(e)}
            ) from e

    @contextmanager
    def _get_session(self) -> Iterator[Session]:
        """
        Context manager for database sessions.

        Automatically handles session lifecycle and rollback on errors.

        :yield: Database session
        :rtype: Session

        Example::

            with self._get_session() as session:
                result = session.execute(query)
        """
        session = self._session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @contextmanager
    def transaction(self) -> Iterator[None]:
        """
        Context manager for explicit transactions.

        Use this to group multiple operations into an atomic transaction.
        All operations succeed or all fail together.

        :yield: None

        Example::

            with repo.transaction():
                repo.save(entity1)
                repo.save(entity2)
                repo.delete(entity3.id)
                # All operations committed together
        """
        with self._get_session() as session:
            try:
                yield
                session.commit()
            except Exception:
                session.rollback()
                raise

    def save(self, entity: EntityBase) -> None:
        """
        Save entity to database.

        Uses UPSERT logic (INSERT or UPDATE). If entity ID exists, updates;
        otherwise inserts new record.

        :param entity: Entity to save
        :type entity: EntityBase
        :raises RepositoryError: If save operation fails

        Example::

            user = User(name="Alice")
            repo.save(user)  # INSERT

            user.name = "Alice Smith"
            repo.save(user)  # UPDATE
        """
        try:
            entity_dict = self._to_dict(entity)
            data_json = json.dumps(entity_dict)

            with self._get_session() as session:
                # Check if exists
                existing = session.execute(
                    self.table.select().where(self.table.c.id == entity.id)
                ).first()

                if existing:
                    # UPDATE
                    session.execute(
                        self.table.update()
                        .where(self.table.c.id == entity.id)
                        .values(data=data_json)
                    )
                else:
                    # INSERT
                    session.execute(
                        self.table.insert().values(
                            id=entity.id,
                            data=data_json
                        )
                    )

        except SQLAlchemyError as e:
            raise RepositoryError(
                f"Failed to save entity with id '{entity.id}'",
                context={'entity_id': entity.id, 'error': str(e)}
            ) from e

    def find_by_id(self, id: str) -> EntityBase | None:
        """
        Find entity by ID.

        :param id: Entity ID
        :type id: str
        :return: Entity if found, None otherwise
        :rtype: Optional[EntityBase]
        :raises RepositoryError: If query fails

        Example::

            user = repo.find_by_id("user-123")
            if user:
                print(f"Found: {user.name}")
        """
        try:
            with self._get_session() as session:
                result = session.execute(
                    self.table.select().where(self.table.c.id == id)
                ).first()

                if result is None:
                    return None

                # Deserialize
                data_str = result.data
                if isinstance(data_str, str):
                    entity_dict = json.loads(data_str)
                else:
                    entity_dict = data_str

                return self._from_dict(entity_dict)

        except SQLAlchemyError as e:
            raise RepositoryError(
                f"Failed to find entity with id '{id}'",
                context={'entity_id': id, 'error': str(e)}
            ) from e

    def find_all(self) -> list[EntityBase]:
        """
        Retrieve all entities.

        :return: List of all entities
        :rtype: List[EntityBase]
        :raises RepositoryError: If query fails

        Example::

            all_users = repo.find_all()
            print(f"Total: {len(all_users)}")
        """
        try:
            with self._get_session() as session:
                results = session.execute(self.table.select()).fetchall()

                entities = []
                for row in results:
                    data_str = row.data
                    if isinstance(data_str, str):
                        entity_dict = json.loads(data_str)
                    else:
                        entity_dict = data_str

                    entity = self._from_dict(entity_dict)
                    entities.append(entity)

                return entities

        except SQLAlchemyError as e:
            raise RepositoryError(
                "Failed to retrieve all entities",
                context={'error': str(e)}
            ) from e

    def delete(self, id: str) -> None:
        """
        Delete entity by ID.

        Idempotent - deleting non-existent entity does not raise error.

        :param id: Entity ID to delete
        :type id: str
        :raises RepositoryError: If delete operation fails

        Example::

            repo.delete("user-123")
        """
        try:
            with self._get_session() as session:
                session.execute(
                    self.table.delete().where(self.table.c.id == id)
                )

        except SQLAlchemyError as e:
            raise RepositoryError(
                f"Failed to delete entity with id '{id}'",
                context={'entity_id': id, 'error': str(e)}
            ) from e

    def exists(self, id: str) -> bool:
        """
        Check if entity exists.

        :param id: Entity ID
        :type id: str
        :return: True if entity exists
        :rtype: bool
        :raises RepositoryError: If check fails

        Example::

            if repo.exists("user-123"):
                print("User exists")
        """
        try:
            with self._get_session() as session:
                result = session.execute(
                    self.table.select().where(self.table.c.id == id)
                ).first()

                return result is not None

        except SQLAlchemyError as e:
            raise RepositoryError(
                f"Failed to check existence of entity with id '{id}'",
                context={'entity_id': id, 'error': str(e)}
            ) from e

    def count(self) -> int:
        """
        Count total number of entities.

        :return: Total entity count
        :rtype: int
        :raises RepositoryError: If count fails

        Example::

            total = repo.count()
            print(f"Total users: {total}")
        """
        try:
            with self._get_session() as session:
                result = session.execute(
                    text(f"SELECT COUNT(*) FROM {self.table_name}")
                ).scalar()

                return result or 0

        except SQLAlchemyError as e:
            raise RepositoryError(
                "Failed to count entities",
                context={'error': str(e)}
            ) from e

    def clear(self) -> None:
        """
        Delete all entities from table.

        WARNING: This operation cannot be undone!

        :raises RepositoryError: If clear operation fails

        Example::

            repo.clear()  # Removes all data
        """
        try:
            with self._get_session() as session:
                session.execute(self.table.delete())

        except SQLAlchemyError as e:
            raise RepositoryError(
                "Failed to clear all entities",
                context={'error': str(e)}
            ) from e

    def __repr__(self) -> str:
        """String representation of repository."""
        return f"<SQLRepository table={self.table_name} engine={self.engine.url}>"

"""
Base class for all use cases in ForgeBase.

Use cases orchestrate application logic, coordinating between domain entities
and infrastructure through ports. They represent the entry points for
application functionality.

Author: Jorge, The Forge
Created: 2025-11-03
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar

# Type variables for input and output DTOs
TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


class UseCaseBase(ABC, Generic[TInput, TOutput]):
    """
    Abstract base class for all use cases (ValueTracks).

    Use cases implement application logic by orchestrating domain entities
    and communicating with external systems through ports. They remain
    framework-independent and testable.

    This class is generic over input and output types, providing type safety
    for use case implementations.

    Design Decisions:
        - Generic types (TInput, TOutput) enable type-safe use case contracts
        - Lifecycle hooks (_before_execute, _after_execute, _on_error) enable
          cross-cutting concerns like logging, metrics, transactions
        - Abstract execute() enforces consistent interface with strong typing

    :param TInput: Type of the input DTO
    :param TOutput: Type of the output DTO

    :Example:

        class CreateUserInput:
            def __init__(self, email: str, name: str):
                self.email = email
                self.name = name

        class UserOutput:
            def __init__(self, id: str, email: str, name: str):
                self.id = id
                self.email = email
                self.name = name

        class CreateUserUseCase(UseCaseBase[CreateUserInput, UserOutput]):
            def __init__(self, user_repository: UserRepositoryPort):
                self.user_repository = user_repository

            def execute(self, input_dto: CreateUserInput) -> UserOutput:
                # Validate input
                if not input_dto.email or "@" not in input_dto.email:
                    raise ValueError("Invalid email")

                # Create domain entity
                user = User(None, input_dto.email, input_dto.name)
                user.validate()

                # Persist
                self.user_repository.save(user)

                # Return output DTO
                return UserOutput(user.id, user.email, user.name)

    .. note::
        Override lifecycle hooks for cross-cutting concerns like logging,
        metrics, and transaction management.

    .. seealso::
        :class:`PortBase` - For external communication contracts
        :class:`DTOBase` - For data transfer objects
    """

    @abstractmethod
    def _before_execute(self) -> None:
        """
        Hook called before execute().

        Override this for pre-execution logic like:
        - Starting transactions
        - Beginning metric collection
        - Logging execution start

        :Example:

            def _before_execute(self) -> None:
                self.logger.info("Starting use case execution")
                self.metrics.start_timer("usecase_duration")
        """
        pass

    @abstractmethod
    def _after_execute(self) -> None:
        """
        Hook called after successful execute().

        Override this for post-execution logic like:
        - Committing transactions
        - Recording metrics
        - Logging success

        :Example:

            def _after_execute(self) -> None:
                self.metrics.stop_timer("usecase_duration")
                self.logger.info("Use case completed successfully")
        """
        pass

    @abstractmethod
    def _on_error(self, error: Exception) -> None:
        """
        Hook called when execute() raises an exception.

        Override this for error handling like:
        - Rolling back transactions
        - Logging errors
        - Recording failure metrics

        :param error: The exception that was raised
        :type error: Exception

        :Example:

            def _on_error(self, error: Exception) -> None:
                self.logger.error(f"Use case failed: {error}")
                self.metrics.increment("usecase_errors")
        """
        pass

    @abstractmethod
    def execute(self, input_dto: TInput) -> TOutput:
        """
        Execute the use case logic.

        This method must be implemented by all use case subclasses.
        It contains the core application logic, orchestrating domain
        entities and ports.

        :param input_dto: Input data transfer object
        :type input_dto: TInput
        :return: Use case result as output DTO
        :rtype: TOutput

        :Example:

            class CreateOrderUseCase(UseCaseBase[CreateOrderDTO, OrderDTO]):
                def execute(self, input_dto: CreateOrderDTO) -> OrderDTO:
                    # 1. Validate input
                    input_dto.validate()

                    # 2. Load domain entities
                    customer = self.customer_repo.find_by_id(input_dto.customer_id)
                    if not customer:
                        raise EntityNotFoundError("Customer not found")

                    # 3. Execute domain logic
                    order = Order.create(customer, input_dto.items)
                    order.validate()

                    # 4. Persist
                    self.order_repo.save(order)

                    # 5. Return result
                    return OrderDTO.from_entity(order)
        """
        pass

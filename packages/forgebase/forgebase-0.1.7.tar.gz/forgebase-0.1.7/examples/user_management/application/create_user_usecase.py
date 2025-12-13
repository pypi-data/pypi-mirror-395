"""
CreateUser UseCase for User Management.

Demonstrates a complete UseCase implementation with validation,
business logic, and observability.

:author: ForgeBase Development Team
:since: 2025-11-03
"""

from examples.user_management.application.ports import UserRepositoryPort
from examples.user_management.domain.email import Email
from examples.user_management.domain.user import User
from forgebase.application.dto_base import DTOBase
from forgebase.application.usecase_base import UseCaseBase
from forgebase.domain.exceptions import BusinessRuleViolation, ValidationError


class CreateUserInput(DTOBase):
    """
    Input DTO for CreateUser UseCase.

    Data Transfer Object that carries validated input data across
    layer boundaries.

    :ivar name: User's full name
    :vartype name: str
    :ivar email: User's email address
    :vartype email: str
    """

    def __init__(self, name: str, email: str):
        """
        Initialize input DTO.

        :param name: User's full name
        :type name: str
        :param email: User's email address
        :type email: str
        """
        self.name = name
        self.email = email

    def validate(self) -> None:
        """
        Validate input data.

        :raises ValidationError: If validation fails
        """
        if not self.name or not self.name.strip():
            raise ValidationError("Name is required")

        if not self.email or not self.email.strip():
            raise ValidationError("Email is required")

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'email': self.email
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'CreateUserInput':
        """Create from dictionary."""
        return cls(
            name=data.get('name', ''),
            email=data.get('email', '')
        )


class CreateUserOutput(DTOBase):
    """
    Output DTO for CreateUser UseCase.

    Carries the result of user creation back to the caller.

    :ivar user_id: Created user's identifier
    :vartype user_id: str
    :ivar name: User's name
    :vartype name: str
    :ivar email: User's email
    :vartype email: str
    :ivar created_at: When user was created
    :vartype created_at: str
    """

    def __init__(self, user_id: str, name: str, email: str, created_at: str):
        """
        Initialize output DTO.

        :param user_id: User identifier
        :type user_id: str
        :param name: User's name
        :type name: str
        :param email: User's email
        :type email: str
        :param created_at: Creation timestamp
        :type created_at: str
        """
        self.user_id = user_id
        self.name = name
        self.email = email
        self.created_at = created_at

    def validate(self) -> None:
        """Validate output data."""
        if not self.user_id:
            raise ValidationError("User ID is required")

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'user_id': self.user_id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'CreateUserOutput':
        """Create from dictionary."""
        return cls(
            user_id=data['user_id'],
            name=data['name'],
            email=data['email'],
            created_at=data['created_at']
        )


class CreateUserUseCase(UseCaseBase[CreateUserInput, CreateUserOutput]):
    """
    UseCase for creating a new user.

    Orchestrates the user creation process:
    1. Validates input
    2. Checks if email already exists
    3. Creates domain entity
    4. Persists via repository
    5. Returns output DTO

    This demonstrates the UseCase pattern: application-specific business logic
    that orchestrates domain objects and infrastructure ports.

    Type parameters:
        - TInput: CreateUserInput
        - TOutput: CreateUserOutput

    Example::

        # Setup dependencies
        repository = JSONUserRepository("users.json")
        usecase = CreateUserUseCase(user_repository=repository)

        # Execute
        input_dto = CreateUserInput(
            name="John Doe",
            email="john@example.com"
        )
        output = usecase.execute(input_dto)

        print(f"Created user: {output.user_id}")

    :ivar user_repository: User repository port
    :vartype user_repository: UserRepositoryPort
    """

    def __init__(self, user_repository: UserRepositoryPort):
        """
        Initialize UseCase with dependencies.

        :param user_repository: User repository implementation
        :type user_repository: UserRepositoryPort
        """
        self.user_repository = user_repository

    def execute(self, input_dto: CreateUserInput) -> CreateUserOutput:
        """
        Execute user creation.

        :param input_dto: Input data
        :type input_dto: CreateUserInput
        :return: Created user data
        :rtype: CreateUserOutput
        :raises ValidationError: If input is invalid
        :raises BusinessRuleViolation: If email already exists
        """
        # Validate input
        input_dto.validate()

        # Check if email already exists (business rule)
        existing_user = self.user_repository.find_by_email(input_dto.email)
        if existing_user is not None:
            raise BusinessRuleViolation(
                f"User with email '{input_dto.email}' already exists (ID: {existing_user.id})"
            )

        # Create domain entity
        email = Email(address=input_dto.email)
        user = User(
            name=input_dto.name,
            email=email
        )

        # Validate entity
        user.validate()

        # Persist
        self.user_repository.save(user)

        # Return output DTO
        return CreateUserOutput(
            user_id=user.id,
            name=user.name,
            email=str(user.email),
            created_at=user.created_at.isoformat()
        )

    def _before_execute(self) -> None:
        """Hook before execution."""
        # Could add logging, metrics, etc.
        pass

    def _after_execute(self) -> None:
        """Hook after execution."""
        # Could add cleanup, notifications, etc.
        pass

    def _on_error(self, error: Exception) -> None:
        """Hook on error."""
        # Could add error logging, rollback, etc.
        pass

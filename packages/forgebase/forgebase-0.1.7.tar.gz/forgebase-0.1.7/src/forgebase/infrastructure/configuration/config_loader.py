"""
Configuration Management System for ForgeBase.

This module implements a multi-source configuration system with clear precedence
rules and type-safe access. It supports loading configurations from multiple sources:
YAML files, JSON files, environment variables, CLI arguments, and hardcoded defaults.

The configuration precedence follows this order (highest to lowest):
    1. Environment variables (ENV)
    2. Configuration files (YAML/JSON)
    3. Hardcoded defaults

Philosophy:
    Configuration should be flexible, explicit, and environment-aware. This system
    allows developers to provide sensible defaults while enabling operators to override
    settings based on deployment context. Type-safe access prevents runtime errors
    from configuration mismatches.

Example::

    # Create loader with defaults
    loader = ConfigLoader(defaults={
        'app.name': 'ForgeBase',
        'app.debug': False,
        'db.host': 'localhost',
        'db.port': 5432
    })

    # Load from file
    loader.load_from_file('config.yaml')

    # Load from environment (prefix: FORGEBASE_)
    loader.load_from_env(prefix='FORGEBASE')

    # Type-safe access
    app_name = loader.get('app.name', str)
    debug_mode = loader.get('app.debug', bool)
    db_port = loader.get('db.port', int)

    # Check if key exists
    if loader.has('feature.enabled'):
        enabled = loader.get('feature.enabled', bool)

:author: ForgeBase Development Team
:since: 2025-11-03
"""

import json
import os
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, TypeVar

import yaml

T = TypeVar('T')


class ConfigurationError(Exception):
    """
    Exception raised for configuration-related errors.

    This includes: missing required keys, type mismatches, invalid file formats,
    and schema validation failures.
    """

    def __init__(self, message: str, key: str | None = None, context: dict[str, Any] | None = None):
        """
        Initialize configuration error.

        :param message: Error description
        :type message: str
        :param key: Configuration key that caused the error (optional)
        :type key: Optional[str]
        :param context: Additional context information (optional)
        :type context: Optional[Dict[str, Any]]
        """
        super().__init__(message)
        self.key = key
        self.context = context or {}


class ConfigValidator(ABC):
    """
    Abstract base for configuration validators.

    Validators can be used to enforce schema constraints on configuration values.
    Implement custom validators by extending this class.
    """

    @abstractmethod
    def validate(self, key: str, value: Any) -> bool:
        """
        Validate a configuration value.

        :param key: Configuration key being validated
        :type key: str
        :param value: Value to validate
        :type value: Any
        :return: True if valid
        :rtype: bool
        :raises ConfigurationError: If validation fails
        """
        pass


class TypeValidator(ConfigValidator):
    """
    Validates that a value matches an expected type.

    Example::

        validator = TypeValidator(int)
        validator.validate('port', 8080)  # OK
        validator.validate('port', '8080')  # Raises ConfigurationError
    """

    def __init__(self, expected_type: type):
        """
        Initialize type validator.

        :param expected_type: Expected Python type
        :type expected_type: Type
        """
        self.expected_type = expected_type

    def validate(self, key: str, value: Any) -> bool:
        """Validate type matches expected type."""
        if not isinstance(value, self.expected_type):
            raise ConfigurationError(
                f"Type mismatch for key '{key}': expected {self.expected_type.__name__}, got {type(value).__name__}",
                key=key,
                context={'expected_type': self.expected_type.__name__, 'actual_type': type(value).__name__}
            )
        return True


class RangeValidator(ConfigValidator):
    """
    Validates that a numeric value falls within a range.

    Example::

        validator = RangeValidator(min_value=1, max_value=65535)
        validator.validate('port', 8080)  # OK
        validator.validate('port', 70000)  # Raises ConfigurationError
    """

    def __init__(self, min_value: int | float | None = None, max_value: int | float | None = None):
        """
        Initialize range validator.

        :param min_value: Minimum allowed value (inclusive)
        :type min_value: Optional[Union[int, float]]
        :param max_value: Maximum allowed value (inclusive)
        :type max_value: Optional[Union[int, float]]
        """
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, key: str, value: Any) -> bool:
        """Validate value is within range."""
        if not isinstance(value, int | float):
            raise ConfigurationError(f"Range validation requires numeric value for key '{key}'", key=key)

        if self.min_value is not None and value < self.min_value:
            raise ConfigurationError(
                f"Value for key '{key}' is below minimum: {value} < {self.min_value}",
                key=key,
                context={'value': value, 'min': self.min_value}
            )

        if self.max_value is not None and value > self.max_value:
            raise ConfigurationError(
                f"Value for key '{key}' exceeds maximum: {value} > {self.max_value}",
                key=key,
                context={'value': value, 'max': self.max_value}
            )

        return True


class ConfigLoader:
    """
    Multi-source configuration loader with type-safe access.

    This loader implements the configuration management strategy for ForgeBase,
    supporting multiple sources with clear precedence rules. Configuration can
    be loaded from YAML files, JSON files, environment variables, and defaults.

    Precedence Order (highest to lowest):
        1. Environment variables
        2. Configuration files (last loaded file wins)
        3. Hardcoded defaults

    Features:
        - Nested key access using dot notation (e.g., 'database.host')
        - Type-safe getters with automatic type checking
        - Schema validation with custom validators
        - Environment variable mapping with configurable prefix
        - Support for YAML and JSON configuration files

    Example::

        # Initialize with defaults
        config = ConfigLoader(defaults={
            'app.name': 'MyApp',
            'app.port': 8000,
            'db.host': 'localhost'
        })

        # Load from configuration file
        config.load_from_file('config.yaml')

        # Override with environment variables
        config.load_from_env(prefix='MYAPP')

        # Type-safe access
        port = config.get('app.port', int)

        # Required value (raises if missing)
        db_host = config.get_required('db.host', str)

        # With default fallback
        debug = config.get('app.debug', bool, default=False)

    :ivar _config: Internal configuration dictionary
    :vartype _config: Dict[str, Any]
    :ivar _validators: Schema validators by key
    :vartype _validators: Dict[str, List[ConfigValidator]]
    """

    def __init__(self, defaults: dict[str, Any] | None = None):
        """
        Initialize configuration loader.

        :param defaults: Default configuration values
        :type defaults: Optional[Dict[str, Any]]
        """
        self._config: dict[str, Any] = defaults or {}
        self._validators: dict[str, list[ConfigValidator]] = {}
        self._loaded_files: list[str] = []

    def load_from_file(self, file_path: str | Path) -> None:
        """
        Load configuration from a YAML or JSON file.

        The file format is automatically detected based on the file extension.
        Supported formats: .yaml, .yml, .json

        :param file_path: Path to configuration file
        :type file_path: Union[str, Path]
        :raises ConfigurationError: If file not found or invalid format

        Example::

            loader.load_from_file('config.yaml')
            loader.load_from_file(Path('/etc/myapp/config.json'))
        """
        path = Path(file_path)

        if not path.exists():
            raise ConfigurationError(
                f"Configuration file not found: {path}",
                context={'file_path': str(path)}
            )

        try:
            with open(path, encoding='utf-8') as f:
                if path.suffix in ['.yaml', '.yml']:
                    data = yaml.safe_load(f)
                elif path.suffix == '.json':
                    data = json.load(f)
                else:
                    raise ConfigurationError(
                        f"Unsupported file format: {path.suffix}",
                        context={'file_path': str(path), 'suffix': path.suffix}
                    )

            if data is not None:
                flattened = self._flatten_dict(data)
                self._config.update(flattened)
                self._loaded_files.append(str(path))

        except (yaml.YAMLError, json.JSONDecodeError) as e:
            raise ConfigurationError(
                f"Failed to parse configuration file: {path}",
                context={'file_path': str(path), 'error': str(e)}
            ) from e

    def load_from_env(self, prefix: str = 'FORGEBASE') -> None:
        """
        Load configuration from environment variables.

        Environment variables are converted to configuration keys using the pattern:
        PREFIX_KEY_SUBKEY -> key.subkey

        For example, with prefix 'MYAPP':
            MYAPP_DB_HOST -> db.host
            MYAPP_APP_PORT -> app.port

        Values are automatically converted to appropriate types:
            - 'true'/'false' -> bool
            - Numeric strings -> int or float
            - Everything else -> str

        :param prefix: Environment variable prefix to filter by
        :type prefix: str

        Example::

            # With environment: FORGEBASE_DB_HOST=localhost
            loader.load_from_env(prefix='FORGEBASE')
            host = loader.get('db.host', str)  # Returns 'localhost'
        """
        prefix = prefix.upper()
        prefix_len = len(prefix) + 1  # +1 for underscore

        for env_key, env_value in os.environ.items():
            if env_key.upper().startswith(f"{prefix}_"):
                # Convert ENV_VAR_NAME to dot.notation.key
                config_key = env_key[prefix_len:].lower().replace('_', '.')

                # Convert value to appropriate type
                typed_value = self._convert_env_value(env_value)

                self._config[config_key] = typed_value

    def load_from_dict(self, data: dict[str, Any], flatten: bool = True) -> None:
        """
        Load configuration from a dictionary.

        :param data: Configuration data
        :type data: Dict[str, Any]
        :param flatten: Whether to flatten nested dicts to dot notation
        :type flatten: bool

        Example::

            loader.load_from_dict({
                'app': {'name': 'MyApp', 'port': 8000},
                'db': {'host': 'localhost'}
            })
            # Results in: app.name, app.port, db.host
        """
        if flatten:
            data = self._flatten_dict(data)

        self._config.update(data)

    def get(self, key: str, expected_type: type[T], default: T | None = None) -> T | None:
        """
        Get configuration value with type checking.

        :param key: Configuration key in dot notation
        :type key: str
        :param expected_type: Expected Python type
        :type expected_type: Type[T]
        :param default: Default value if key not found
        :type default: Optional[T]
        :return: Configuration value or default
        :rtype: Optional[T]
        :raises ConfigurationError: If type mismatch

        Example::

            port = config.get('app.port', int, default=8000)
            debug = config.get('app.debug', bool, default=False)
            name = config.get('app.name', str)
        """
        if key not in self._config:
            return default

        value = self._config[key]

        # Type checking
        if not isinstance(value, expected_type):
            # Try to convert if possible
            try:
                value = expected_type(value)
                self._config[key] = value  # Cache converted value
            except (ValueError, TypeError) as e:
                raise ConfigurationError(
                    f"Type mismatch for key '{key}': expected {expected_type.__name__}, got {type(value).__name__}",
                    key=key,
                    context={'expected_type': expected_type.__name__, 'actual_type': type(value).__name__}
                ) from e

        # Validate if validators are registered
        if key in self._validators:
            for validator in self._validators[key]:
                validator.validate(key, value)

        return value

    def get_required(self, key: str, expected_type: type[T]) -> T:
        """
        Get required configuration value.

        :param key: Configuration key in dot notation
        :type key: str
        :param expected_type: Expected Python type
        :type expected_type: Type[T]
        :return: Configuration value
        :rtype: T
        :raises ConfigurationError: If key not found or type mismatch

        Example::

            db_host = config.get_required('db.host', str)
        """
        if key not in self._config:
            raise ConfigurationError(
                f"Required configuration key not found: '{key}'",
                key=key
            )

        return self.get(key, expected_type)

    def has(self, key: str) -> bool:
        """
        Check if configuration key exists.

        :param key: Configuration key in dot notation
        :type key: str
        :return: True if key exists
        :rtype: bool
        """
        return key in self._config

    def set(self, key: str, value: Any) -> None:
        """
        Set configuration value programmatically.

        :param key: Configuration key in dot notation
        :type key: str
        :param value: Value to set
        :type value: Any

        Example::

            config.set('app.debug', True)
        """
        self._config[key] = value

    def register_validator(self, key: str, validator: ConfigValidator) -> None:
        """
        Register a validator for a configuration key.

        :param key: Configuration key to validate
        :type key: str
        :param validator: Validator instance
        :type validator: ConfigValidator

        Example::

            config.register_validator('app.port', RangeValidator(min_value=1, max_value=65535))
            config.register_validator('app.name', TypeValidator(str))
        """
        if key not in self._validators:
            self._validators[key] = []
        self._validators[key].append(validator)

    def validate_all(self) -> None:
        """
        Validate all configuration values against registered validators.

        :raises ConfigurationError: If any validation fails
        """
        for key, validators in self._validators.items():
            if key in self._config:
                value = self._config[key]
                for validator in validators:
                    validator.validate(key, value)

    def get_all(self) -> dict[str, Any]:
        """
        Get all configuration as a dictionary.

        :return: Complete configuration dictionary
        :rtype: Dict[str, Any]
        """
        return self._config.copy()

    def get_loaded_files(self) -> list[str]:
        """
        Get list of configuration files that have been loaded.

        :return: List of file paths
        :rtype: List[str]
        """
        return self._loaded_files.copy()

    def _flatten_dict(self, data: dict[str, Any], parent_key: str = '', separator: str = '.') -> dict[str, Any]:
        """
        Flatten nested dictionary to dot notation.

        Example:
            {'app': {'name': 'test', 'port': 8000}} -> {'app.name': 'test', 'app.port': 8000}
        """
        items = []
        for key, value in data.items():
            new_key = f"{parent_key}{separator}{key}" if parent_key else key
            if isinstance(value, dict):
                items.extend(self._flatten_dict(value, new_key, separator).items())
            else:
                items.append((new_key, value))
        return dict(items)

    def _convert_env_value(self, value: str) -> bool | int | float | str:
        """
        Convert environment variable string to appropriate Python type.

        Conversion rules:
            - 'true' (case-insensitive) -> True
            - 'false' (case-insensitive) -> False
            - Numeric strings -> int or float
            - Everything else -> str
        """
        # Boolean conversion
        if value.lower() in ('true', 'yes', '1'):
            return True
        if value.lower() in ('false', 'no', '0'):
            return False

        # Numeric conversion
        try:
            # Try int first
            if '.' not in value:
                return int(value)
            return float(value)
        except ValueError:
            pass

        # Return as string
        return value

    def __repr__(self) -> str:
        """String representation of ConfigLoader."""
        return f"<ConfigLoader keys={len(self._config)} files={len(self._loaded_files)}>"

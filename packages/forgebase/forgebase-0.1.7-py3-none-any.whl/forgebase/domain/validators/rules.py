"""
Domain validation rules for ForgeBase.

Reusable validation functions for enforcing domain constraints.
All validators raise ValidationError when validation fails.

Author: Jorge, The Forge
Created: 2025-11-03
"""

import re
from typing import Any

from forgebase.domain.exceptions import ValidationError


def not_null(value: Any, field_name: str = "Value") -> None:
    """
    Validate that value is not None.

    :param value: Value to validate
    :param field_name: Name of field for error message
    :raises ValidationError: If value is None
    """
    if value is None:
        raise ValidationError(f"{field_name} cannot be null")


def not_empty(value: str | None, field_name: str = "Value") -> None:
    """
    Validate that string is not empty or whitespace only.

    :param value: String to validate
    :param field_name: Name of field for error message
    :raises ValidationError: If string is None, empty, or whitespace
    """
    not_null(value, field_name)
    if not value or not value.strip():
        raise ValidationError(f"{field_name} cannot be empty")


def in_range(value: float, min_val: float, max_val: float,
             field_name: str = "Value") -> None:
    """
    Validate that numeric value is within range.

    :param value: Value to validate
    :param min_val: Minimum value (inclusive)
    :param max_val: Maximum value (inclusive)
    :param field_name: Name of field for error message
    :raises ValidationError: If value is outside range
    """
    if value < min_val or value > max_val:
        raise ValidationError(
            f"{field_name} must be between {min_val} and {max_val}, got {value}"
        )


def matches_pattern(value: str, pattern: str, field_name: str = "Value") -> None:
    """
    Validate that string matches regex pattern.

    :param value: String to validate
    :param pattern: Regex pattern
    :param field_name: Name of field for error message
    :raises ValidationError: If string doesn't match pattern
    """
    if not re.match(pattern, value):
        raise ValidationError(f"{field_name} doesn't match required pattern")


def min_length(value: str, length: int, field_name: str = "Value") -> None:
    """
    Validate minimum string length.

    :param value: String to validate
    :param length: Minimum length
    :param field_name: Name of field for error message
    :raises ValidationError: If string is too short
    """
    if len(value) < length:
        raise ValidationError(
            f"{field_name} must be at least {length} characters, got {len(value)}"
        )


def max_length(value: str, length: int, field_name: str = "Value") -> None:
    """
    Validate maximum string length.

    :param value: String to validate
    :param length: Maximum length
    :param field_name: Name of field for error message
    :raises ValidationError: If string is too long
    """
    if len(value) > length:
        raise ValidationError(
            f"{field_name} must be at most {length} characters, got {len(value)}"
        )


def one_of(value: Any, allowed_values: list[Any], field_name: str = "Value") -> None:
    """
    Validate that value is one of allowed values.

    :param value: Value to validate
    :param allowed_values: List of allowed values
    :param field_name: Name of field for error message
    :raises ValidationError: If value not in allowed list
    """
    if value not in allowed_values:
        raise ValidationError(
            f"{field_name} must be one of {allowed_values}, got {value}"
        )

"""rettX ID validation implementation.

This module provides format validation for rettX IDs using a
pre-compiled regex pattern for efficient matching.
"""

from rettxid._format import VALID_PATTERN


def validate_format(id: str) -> bool:  # noqa: A002
    """Check if a string matches the rettX ID v1 format.

    Validation is strict: the prefix must be lowercase, the body must be
    uppercase, and all characters must be from the ambiguity-safe alphabet.
    Use normalize() first if you need case-insensitive matching.

    Args:
        id: The string to validate.

    Returns:
        True if the string is a valid rettX ID format, False otherwise.
        Never raises exceptions for invalid input.

    Example:
        >>> validate_format('rettx-8GZ4-MK3P-1Q9L')
        True
        >>> validate_format('invalid')
        False
        >>> validate_format(None)
        False
    """
    # Handle non-string input gracefully
    if not isinstance(id, str):
        return False

    # Use pre-compiled regex for efficient matching
    return VALID_PATTERN.match(id) is not None

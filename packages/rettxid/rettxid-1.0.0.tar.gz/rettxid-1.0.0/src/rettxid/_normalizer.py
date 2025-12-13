"""Normalization functions for rettX ID v1.

This module provides functions to convert user input variations
into canonical rettX ID form.

Normalization steps:
1. Type check (must be string)
2. Strip leading/trailing whitespace
3. Extract alphanumeric characters after prefix
4. Validate extracted characters are from safe alphabet
5. Format with proper grouping and case
6. Return canonical form

Example:
    >>> from rettxid._normalizer import normalize
    >>> normalize("rettx-8gz4-mk3p-2q9a")
    'rettx-8GZ4-MK3P-2Q9A'
    >>> normalize("RETTX8GZ4MK3P2Q9A")
    'rettx-8GZ4-MK3P-2Q9A'
"""

import re

from rettxid._alphabet import SAFE_ALPHABET
from rettxid._format import (
    GROUP_SIZE,
    PREFIX,
    RANDOM_LENGTH,
    SEPARATOR,
)

# Set of valid characters for fast lookup (case-insensitive)
_SAFE_ALPHABET_SET: frozenset[str] = frozenset(SAFE_ALPHABET)
_SAFE_ALPHABET_UPPER_LOWER: frozenset[str] = frozenset(
    SAFE_ALPHABET + SAFE_ALPHABET.lower()
)

# Pattern to extract alphanumeric characters after optional prefix
# Matches: rettx followed by optional separator, then 12 alphanumeric chars
# Groups are optional separators (dash or space)
_EXTRACT_PATTERN: re.Pattern[str] = re.compile(
    r"^\s*rettx[- ]?([A-Za-z0-9]{4})[- ]?([A-Za-z0-9]{4})[- ]?([A-Za-z0-9]{4})\s*$",
    re.IGNORECASE,
)


def _extract_chars(input_str: str) -> str | None:
    """Extract the 12 random characters from input, if valid structure.

    Strips whitespace, removes separators, extracts alphanumeric portion
    after the rettx prefix.

    Args:
        input_str: The string to extract from.

    Returns:
        The 12 extracted characters (uppercase), or None if structure invalid.
    """
    match = _EXTRACT_PATTERN.match(input_str)
    if match:
        # Combine all captured groups and convert to uppercase
        return (match.group(1) + match.group(2) + match.group(3)).upper()
    return None


def _validate_extracted_chars(chars: str) -> bool:
    """Validate that all extracted characters are from the safe alphabet.

    Args:
        chars: The extracted characters (should be uppercase).

    Returns:
        True if all characters are valid, False otherwise.
    """
    if len(chars) != RANDOM_LENGTH:
        return False
    return all(c in _SAFE_ALPHABET_SET for c in chars)


def _format_canonical(chars: str) -> str:
    """Format validated characters into canonical rettX ID form.

    Args:
        chars: The 12 validated uppercase characters.

    Returns:
        The canonical rettX ID string.
    """
    groups = [chars[i : i + GROUP_SIZE] for i in range(0, len(chars), GROUP_SIZE)]
    return PREFIX + SEPARATOR.join(groups)


def normalize(id_str: str) -> str:
    """Normalize a string into canonical rettX ID form.

    Accepts various input formats and converts them to the canonical form:
    - Lowercase body → uppercase
    - Uppercase prefix → lowercase
    - Missing dashes → inserted
    - Spaces as separators → dashes
    - Leading/trailing whitespace → stripped

    Args:
        id_str: The string to normalize.

    Returns:
        The canonical rettX ID string.

    Raises:
        TypeError: If input is not a string.
        ValueError: If input cannot be normalized to a valid rettX ID.

    Example:
        >>> normalize("rettx-8gz4-mk3p-2q9a")
        'rettx-8GZ4-MK3P-2Q9A'
        >>> normalize("RETTX8GZ4MK3P2Q9A")
        'rettx-8GZ4-MK3P-2Q9A'
    """
    # T029: Type check first
    if not isinstance(id_str, str):
        raise TypeError(f"normalize() requires a string, got {type(id_str).__name__}")

    # Extract the random portion
    extracted = _extract_chars(id_str)
    if extracted is None:
        raise ValueError(f"Invalid rettX ID: {id_str!r}")

    # Validate all characters are from safe alphabet
    if not _validate_extracted_chars(extracted):
        raise ValueError(f"Invalid rettX ID: {id_str!r}")

    # Format and return canonical form
    return _format_canonical(extracted)

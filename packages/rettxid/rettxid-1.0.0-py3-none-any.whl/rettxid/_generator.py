"""rettX ID generation implementation.

This module provides the core ID generation functionality using
cryptographically secure randomness from the secrets module.
"""

import secrets

from rettxid._alphabet import SAFE_ALPHABET
from rettxid._format import GROUP_SIZE, PREFIX, RANDOM_LENGTH, SEPARATOR


def _generate_random_part(length: int = RANDOM_LENGTH) -> str:
    """Generate a random string of characters from the safe alphabet.

    Uses secrets.choice() for cryptographically secure random selection.

    Args:
        length: Number of random characters to generate (default: 12).

    Returns:
        A string of random uppercase characters from SAFE_ALPHABET.
    """
    return "".join(secrets.choice(SAFE_ALPHABET) for _ in range(length))


def _format_with_groups(chars: str) -> str:
    """Format a string of characters into dash-separated groups.

    Args:
        chars: A string of characters to format (must be GROUP_SIZE * GROUP_COUNT long).

    Returns:
        The characters formatted as 'XXXX-XXXX-XXXX'.

    Raises:
        ValueError: If chars length doesn't match expected RANDOM_LENGTH.
    """
    if len(chars) != RANDOM_LENGTH:
        raise ValueError(f"Expected {RANDOM_LENGTH} characters, got {len(chars)}")

    groups = [chars[i : i + GROUP_SIZE] for i in range(0, len(chars), GROUP_SIZE)]
    return SEPARATOR.join(groups)


def generate_rettx_id() -> str:
    """Generate a new cryptographically random rettX ID.

    Returns:
        A valid rettX ID in canonical format (e.g., 'rettx-8GZ4-MK3P-1Q9L').

    Raises:
        RuntimeError: If system entropy source is unavailable (extremely rare).

    Example:
        >>> generate_rettx_id()
        'rettx-8GZ4-MK3P-1Q9L'
    """
    random_chars = _generate_random_part()
    formatted_body = _format_with_groups(random_chars)
    return f"{PREFIX}{formatted_body}"

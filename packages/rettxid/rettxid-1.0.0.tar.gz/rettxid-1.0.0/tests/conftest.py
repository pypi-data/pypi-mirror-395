"""Shared pytest fixtures for rettxid tests."""

import pytest

from rettxid._alphabet import SAFE_ALPHABET
from rettxid._format import (
    GROUP_COUNT,
    GROUP_SIZE,
    PREFIX,
    RANDOM_LENGTH,
    SEPARATOR,
    TOTAL_LENGTH,
)


@pytest.fixture
def safe_alphabet() -> str:
    """Return the safe alphabet for rettX IDs."""
    return SAFE_ALPHABET


@pytest.fixture
def format_constants() -> dict[str, int | str]:
    """Return format constants as a dictionary."""
    return {
        "prefix": PREFIX,
        "group_size": GROUP_SIZE,
        "group_count": GROUP_COUNT,
        "separator": SEPARATOR,
        "random_length": RANDOM_LENGTH,
        "total_length": TOTAL_LENGTH,
    }


@pytest.fixture
def valid_id_examples() -> list[str]:
    """Return a list of valid rettX ID examples for testing."""
    return [
        "rettx-8GZ4-MK3P-2Q9A",
        "rettx-2NVF-7KQR-4TXB",
        "rettx-ABCD-EFGH-JKMN",
        "rettx-2345-6789-PQRT",
    ]


@pytest.fixture
def invalid_id_examples() -> list[str]:
    """Return a list of invalid rettX ID examples for testing."""
    return [
        "",  # Empty string
        "rettx-8GZ4-MK3P",  # Missing group
        "RETTX-8GZ4-MK3P-2Q9A",  # Uppercase prefix
        "rettx-8gz4-mk3p-2q9a",  # Lowercase body
        "rettx-8GO4-MK3P-2Q9A",  # Contains excluded 'O'
        "rettx-8G04-MK3P-2Q9A",  # Contains excluded '0'
        "rettx-8GI4-MK3P-2Q9A",  # Contains excluded 'I'
        "rettx-8GL4-MK3P-2Q9A",  # Contains excluded 'L'
        "rettx-8G14-MK3P-2Q9A",  # Contains excluded '1'
        "rettx-8GS4-MK3P-2Q9A",  # Contains excluded 'S'
        "rtx-8GZ4-MK3P-2Q9A",  # Wrong prefix
        "rettx8GZ4MK3P2Q9A",  # Missing dashes
        "rettx-8GZ4-MK3P-2Q9A-XXXX",  # Too many groups
        "rettx-",  # Prefix only
    ]

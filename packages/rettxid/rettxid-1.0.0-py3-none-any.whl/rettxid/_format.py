"""Format constants for rettX ID v1.

This module defines the structural constants for the rettX ID v1 format:
    rettx-XXXX-XXXX-XXXX

Where:
    - Prefix: "rettx-" (6 characters, lowercase)
    - Body: 3 groups of 4 characters from SAFE_ALPHABET
    - Separators: dashes between groups
    - Total length: 20 characters
"""

import re

from rettxid._alphabet import SAFE_ALPHABET

# Format structure
PREFIX: str = "rettx-"
GROUP_SIZE: int = 4
GROUP_COUNT: int = 3
SEPARATOR: str = "-"

# Derived constants
RANDOM_LENGTH: int = GROUP_SIZE * GROUP_COUNT  # 12 characters
TOTAL_LENGTH: int = len(PREFIX) + RANDOM_LENGTH + (GROUP_COUNT - 1)  # 20 characters

# Precompiled validation regex for strict format matching
# Pattern: rettx-[SAFE]{4}-[SAFE]{4}-[SAFE]{4}
# Uses \Z instead of $ to reject trailing newlines
_CHAR_CLASS = f"[{SAFE_ALPHABET}]"
_GROUP_PATTERN = f"{_CHAR_CLASS}{{{GROUP_SIZE}}}"
_BODY_PATTERN = SEPARATOR.join([_GROUP_PATTERN] * GROUP_COUNT)
VALID_PATTERN: re.Pattern[str] = re.compile(f"^{re.escape(PREFIX)}{_BODY_PATTERN}\\Z")

# Lenient pattern for normalization (extracts alphanumeric after prefix)
# Matches prefix (case-insensitive) followed by alphanumerics with optional separators
NORMALIZE_PATTERN: re.Pattern[str] = re.compile(
    r"^rettx[- ]?([A-Z0-9]{4})[- ]?([A-Z0-9]{4})[- ]?([A-Z0-9]{4})$",
    re.IGNORECASE,
)

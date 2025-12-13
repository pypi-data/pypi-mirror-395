"""rettxid - Generate, validate, and normalize rettX IDs.

rettX IDs are pseudonymous patient identifiers for the Rett Syndrome Europe
ecosystem. This library provides three pure functions for working with them.

Example:
    >>> from rettxid import generate_rettx_id, validate_format, normalize
    >>>
    >>> # Generate a new ID
    >>> patient_id = generate_rettx_id()
    >>> print(patient_id)  # e.g., 'rettx-8GZ4-MK3P-1Q9L'
    >>>
    >>> # Validate format
    >>> validate_format(patient_id)  # True
    >>> validate_format("invalid")   # False
    >>>
    >>> # Normalize user input
    >>> normalize("rettx-8gz4-mk3p-1q9l")  # 'rettx-8GZ4-MK3P-1Q9L'

Functions:
    generate_rettx_id: Generate a new cryptographically random rettX ID.
    validate_format: Check if a string matches rettX ID v1 format.
    normalize: Convert input to canonical rettX ID form.
"""

__version__ = "1.0.0"
__all__ = ["generate_rettx_id", "validate_format", "normalize"]

# Import real implementations
from rettxid._generator import generate_rettx_id
from rettxid._normalizer import normalize
from rettxid._validator import validate_format

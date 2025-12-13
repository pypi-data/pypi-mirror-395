"""Ambiguity-safe character alphabet for rettX IDs.

This module defines the character set used for generating the random portion
of rettX IDs. Characters are carefully selected to avoid visual ambiguity
when printed, displayed, or spoken.

Excluded characters:
    - 0 (zero): Confusable with O (letter O)
    - 1 (one): Confusable with I (letter I) and l (lowercase L)
    - I (letter I): Confusable with 1 (one) and l (lowercase L)
    - L (letter L): Confusable with 1 (one) and I (letter I)
    - O (letter O): Confusable with 0 (zero)
    - S (letter S): Confusable with 5 (five)

The remaining 27 characters provide sufficient entropy while ensuring
reliable transcription across print, display, and speech contexts.
"""

# 30-character ambiguity-safe alphabet
# Includes: 2-9, A-Z excluding I, L, O, S
SAFE_ALPHABET: str = "23456789ABCDEFGHJKMNPQRTUVWXYZ"

# Excluded characters for validation reference
EXCLUDED_CHARS: frozenset[str] = frozenset("01ILOS")

# Alphabet size for entropy calculations
ALPHABET_SIZE: int = len(SAFE_ALPHABET)  # 30

# Bits of entropy per character: log2(30) ≈ 4.91
BITS_PER_CHAR: float = 4.906890595608519

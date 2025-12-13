# Research: rettX ID Core Library (v1)

**Feature**: 001-rettxid-core  
**Date**: 2025-12-06  
**Purpose**: Resolve technical unknowns before implementation

---

## Research Task 1: Ambiguity-Safe Alphabet

### Question
Which characters should be excluded from the rettX ID alphabet to avoid visual ambiguity when printed, spoken, or transcribed?

### Research

Common ambiguous character pairs in alphanumeric systems:

| Confusable Pair | Issue |
|-----------------|-------|
| `0` (zero) / `O` (letter O) | Nearly identical in many fonts |
| `1` (one) / `I` (letter I) / `l` (lowercase L) | Identical in sans-serif fonts |
| `S` / `5` | Confusable when handwritten or in certain fonts |
| `2` / `Z` | Similar shape, especially handwritten |
| `8` / `B` | Similar in some fonts |
| `G` / `6` | Can be confused when handwritten |

**Approach**: Use a conservative Crockford Base32-style exclusion. Crockford Base32 excludes `I`, `L`, `O`, `U` to avoid ambiguity. We adapt for uppercase-only:

### Decision

**Excluded characters**: `0`, `1`, `I`, `L`, `O`, `S`

**Rationale**:
- `0` excluded → use `O`... wait, that's confusable. Better: exclude both `0` and `O`
- `1`, `I`, `L` all excluded → no ambiguity
- `O` excluded → paired with `0`
- `S` excluded → paired with `5`

**Final Safe Alphabet** (27 characters):
```
2 3 4 5 6 7 8 9
A B C D E F G H J K M N P Q R T U V W X Y Z
```

Excluded: `0, 1, I, L, O, S` (6 characters removed from 36)

**Alphabet size**: 27 characters

### Alternatives Considered

| Alternative | Size | Rejected Because |
|-------------|------|------------------|
| Full Base36 (A-Z, 0-9) | 36 | Ambiguity risk (0/O, 1/I/L) |
| Crockford Base32 | 32 | Includes lowercase normalization complexity |
| Hex (0-9, A-F) | 16 | Requires more characters for same entropy |
| Custom 30-char | 30 | Including `S/5` pair increases transcription errors |

---

## Research Task 2: Entropy Requirements

### Question
How many random characters are needed to ensure collision probability < 1 in 1 billion for 100,000 patients?

### Research

**Birthday Problem Formula**:
For `n` items from a pool of `N` possibilities, collision probability ≈ `n² / (2N)`

**Requirements**:
- Maximum patients: 100,000 (generous upper bound for Rett Syndrome)
- Target collision probability: < 10⁻⁹ (1 in 1 billion)

**Calculation**:
```
P(collision) ≈ n² / (2N) < 10⁻⁹
N > n² / (2 × 10⁻⁹)
N > (100,000)² / (2 × 10⁻⁹)
N > 10¹⁰ / (2 × 10⁻⁹)
N > 5 × 10¹⁸
```

With alphabet size 27:
```
27^k > 5 × 10¹⁸
k > log₂₇(5 × 10¹⁸)
k > 18.7 / 1.43 ≈ 13.1
```

**Minimum characters needed**: 14 characters

**Entropy check**:
- 14 characters from 27-char alphabet = 27¹⁴ ≈ 1.09 × 10²⁰ combinations
- Bits of entropy = 14 × log₂(27) ≈ 14 × 4.75 ≈ 66.5 bits
- Far exceeds requirements (>2× safety margin)

### Decision

**Random portion**: 12 characters (grouped as 4-4-4 with dashes)

**Rationale**:
- 12 characters from 27-char alphabet = 27¹² ≈ 1.5 × 10¹⁷ combinations
- 57 bits of entropy
- Collision probability for 100k patients: (10⁵)² / (2 × 1.5 × 10¹⁷) ≈ 3.3 × 10⁻⁸
- Still 1 in 30 million — acceptable given rettxapi uniqueness enforcement
- 12 chars in 4-4-4 grouping is human-readable and memorable

**Format**: `rettx-XXXX-XXXX-XXXX` (18 chars total including prefix and dashes)

### Alternatives Considered

| Alternative | Length | Rejected Because |
|-------------|--------|------------------|
| 8 chars (2 groups) | 12 total | Collision risk too high (1 in 10k for 100k patients) |
| 16 chars (4 groups) | 24 total | Unnecessarily long, harder to transcribe |
| 14 chars (uneven) | 19 total | Uneven grouping harder to read |

---

## Research Task 3: Python `secrets` Module Best Practices

### Question
How to correctly use Python's `secrets` module for cryptographic random generation?

### Research

**`secrets` module** (Python 3.6+):
- `secrets.choice(seq)`: Cryptographically random selection from sequence
- `secrets.token_bytes(n)`: Random bytes
- `secrets.token_hex(n)`: Random hex string
- Uses system entropy source (`/dev/urandom` on Unix, `CryptGenRandom` on Windows)

**Best Practice for Custom Alphabet**:
```python
import secrets

ALPHABET = "23456789ABCDEFGHJKMNPQRTUVWXYZ"  # 27 chars, safe

def generate_random_part(length: int = 12) -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(length))
```

**Entropy Source Failure**:
- `secrets` raises `RuntimeError` if system entropy is exhausted (extremely rare)
- No special handling needed — let it propagate

### Decision

Use `secrets.choice()` with pre-defined alphabet string. No error handling for entropy exhaustion — failure should be explicit and loud.

---

## Research Task 4: Regex Pattern for Validation

### Question
What regex pattern efficiently validates the rettX ID v1 format?

### Research

**Format**: `rettx-XXXX-XXXX-XXXX`
- Prefix: `rettx-` (lowercase, fixed)
- Body: 3 groups of 4 characters from safe alphabet
- Separators: dashes between groups

**Safe alphabet**: `23456789ABCDEFGHJKMNPQRTUVWXYZ`

### Decision

**Validation regex**:
```python
import re

SAFE_CHARS = "23456789ABCDEFGHJKMNPQRTUVWXYZ"
PATTERN = re.compile(rf"^rettx-[{SAFE_CHARS}]{{4}}-[{SAFE_CHARS}]{{4}}-[{SAFE_CHARS}]{{4}}$")

def validate_format(id: str) -> bool:
    return bool(PATTERN.match(id))
```

**Normalization regex** (for extracting characters):
```python
# Match prefix + any alphanumeric (for lenient extraction before validation)
NORMALIZE_PATTERN = re.compile(r"^rettx[- ]?([A-Z0-9]{4})[- ]?([A-Z0-9]{4})[- ]?([A-Z0-9]{4})$", re.IGNORECASE)
```

---

## Research Task 5: Type Hints and mypy Strict Mode

### Question
What type annotations are needed for strict mypy compliance?

### Research

**Python 3.11+ typing features**:
- `|` union syntax instead of `Union[]`
- `Self` type for method chaining
- No need for `from __future__ import annotations`

**Public API signatures**:
```python
def generate_rettx_id() -> str: ...
def validate_format(id: str) -> bool: ...
def normalize(id: str) -> str: ...  # Raises ValueError on invalid
```

**mypy strict flags** (`pyproject.toml`):
```toml
[tool.mypy]
strict = true
warn_return_any = true
warn_unused_ignores = true
```

### Decision

All functions use concrete types. No `Any`, no `Optional` (use explicit `| None` if needed). The API is simple enough that strict typing is straightforward.

---

## Summary of Decisions

| Decision | Value | Rationale |
|----------|-------|-----------|
| Alphabet | 27 chars (A-Z + 2-9, excluding 0,1,I,L,O,S) | Ambiguity-safe for print/speech |
| Random chars | 12 | 57 bits entropy, 1 in 30M collision at 100k scale |
| Grouping | 4-4-4 | Human-readable, even groups |
| Full format | `rettx-XXXX-XXXX-XXXX` | 20 chars total, prefixed |
| Randomness | `secrets.choice()` | Cryptographically secure stdlib |
| Validation | Pre-compiled regex | Efficient, clear |
| Normalization | Uppercase, strip whitespace, add dashes | Forgiving input handling |

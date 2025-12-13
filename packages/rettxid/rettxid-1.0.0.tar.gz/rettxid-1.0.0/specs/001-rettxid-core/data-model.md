# Data Model: rettX ID Core Library (v1)

**Feature**: 001-rettxid-core  
**Date**: 2025-12-06  
**Source**: [spec.md](spec.md), [research.md](research.md)

---

## Entities

### rettX ID (Value Object)

A rettX ID is a **string value** following a strict format. It is not a class or object in this library — it is represented as a plain Python `str`. The library provides functions to generate, validate, and normalize these strings.

**Canonical Format**: `rettx-XXXX-XXXX-XXXX`

| Component | Description | Example |
|-----------|-------------|---------|
| Prefix | Fixed lowercase identifier | `rettx-` |
| Group 1 | 4 characters from safe alphabet | `8GZ4` |
| Separator | Dash | `-` |
| Group 2 | 4 characters from safe alphabet | `MK3P` |
| Separator | Dash | `-` |
| Group 3 | 4 characters from safe alphabet | `1Q9L` |

**Total Length**: 16 characters (4 prefix + 12 random + 2 dashes... wait, let me recount)
- `rettx-` = 6 chars
- `XXXX-XXXX-XXXX` = 14 chars (12 alphanumeric + 2 dashes)
- **Total**: 20 characters

---

## Constants

### Safe Alphabet

The character set used for the random portion of rettX IDs.

```python
SAFE_ALPHABET: str = "23456789ABCDEFGHJKMNPQRTUVWXYZ"
```

| Property | Value |
|----------|-------|
| Size | 27 characters |
| Includes | A-Z (except I, L, O, S), 2-9 |
| Excludes | 0, 1, I, L, O, S |
| Rationale | Avoids visually ambiguous character pairs |

### Format Constants

```python
PREFIX: str = "rettx-"
GROUP_SIZE: int = 4
GROUP_COUNT: int = 3
SEPARATOR: str = "-"
RANDOM_LENGTH: int = 12  # GROUP_SIZE * GROUP_COUNT
TOTAL_LENGTH: int = 20   # len(PREFIX) + RANDOM_LENGTH + (GROUP_COUNT - 1)
```

### Validation Pattern

```python
VALID_PATTERN: re.Pattern[str] = re.compile(
    r"^rettx-[23456789ABCDEFGHJKMNPQRTUVWXYZ]{4}-[23456789ABCDEFGHJKMNPQRTUVWXYZ]{4}-[23456789ABCDEFGHJKMNPQRTUVWXYZ]{4}$"
)
```

---

## State Transitions

This library is **stateless**. There are no state transitions, no object lifecycle, no persistence.

| Operation | Input | Output | Side Effects |
|-----------|-------|--------|--------------|
| `generate_rettx_id()` | None | Valid rettX ID string | None (reads system entropy) |
| `validate_format(id)` | Any string | `True` or `False` | None |
| `normalize(id)` | String-like input | Canonical rettX ID or raises `ValueError` | None |

---

## Validation Rules

A string is a valid rettX ID v1 if and only if:

1. ✅ Starts with prefix `rettx-`
2. ✅ Contains exactly 3 groups of 4 characters
3. ✅ Groups are separated by dashes
4. ✅ All characters in groups are from `SAFE_ALPHABET`
5. ✅ Total length is exactly 20 characters

**Invalid examples**:
- `RETTX-8GZ4-MK3P-1Q9L` — prefix must be lowercase
- `rettx-8GZ4-MK3P` — missing third group
- `rettx-8GZ4-MK3P-1Q9L-EXTRA` — too many groups
- `rettx-8GO4-MK3P-1Q9L` — contains `O` (excluded character)
- `rettx-8gz4-mk3p-1q9l` — body must be uppercase

---

## Normalization Rules

Normalization transforms user input into canonical form:

| Input Variant | Transformation | Output |
|---------------|----------------|--------|
| Lowercase body | Uppercase | `rettx-8gz4-mk3p-1q9l` → `rettx-8GZ4-MK3P-1Q9L` |
| Leading/trailing whitespace | Strip | `  rettx-8GZ4-MK3P-1Q9L  ` → `rettx-8GZ4-MK3P-1Q9L` |
| Missing dashes | Insert | `rettx8GZ4MK3P1Q9L` → `rettx-8GZ4-MK3P-1Q9L` |
| Mixed case prefix | Lowercase | `RETTX-8GZ4-MK3P-1Q9L` → `rettx-8GZ4-MK3P-1Q9L` |
| Extra internal spaces | Remove | `rettx - 8GZ4 - MK3P - 1Q9L` → `rettx-8GZ4-MK3P-1Q9L` |

**Normalization does NOT fix**:
- Invalid characters (raises `ValueError`)
- Wrong length (raises `ValueError`)
- Completely malformed input (raises `ValueError`)

---

## Relationships

```
┌─────────────────────────────────────────────────────────────┐
│                    rettX Ecosystem                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐         ┌─────────────┐                   │
│  │  rettxid    │         │  rettxapi   │                   │
│  │  (library)  │────────▶│  (backend)  │                   │
│  │             │         │             │                   │
│  │ • generate  │         │ • assign    │                   │
│  │ • validate  │         │ • persist   │                   │
│  │ • normalize │         │ • enforce   │                   │
│  └─────────────┘         │   unique    │                   │
│        │                 └─────────────┘                   │
│        │                        │                          │
│        ▼                        ▼                          │
│  ┌─────────────┐         ┌─────────────┐                   │
│  │ CLI tools   │         │ Patient     │                   │
│  │ Migration   │         │ Records     │                   │
│  │ scripts     │         │ QR codes    │                   │
│  └─────────────┘         └─────────────┘                   │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**rettxid responsibilities**:
- Format definition
- ID generation (random)
- Format validation
- Input normalization

**rettxapi responsibilities** (out of scope for this library):
- Patient-to-ID assignment
- Uniqueness enforcement
- Persistence
- Collision detection

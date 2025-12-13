# Quickstart: rettxid

**Feature**: 001-rettxid-core  
**Date**: 2025-12-06

---

## Installation

```bash
pip install rettxid
```

Or from source:

```bash
git clone https://github.com/rett-syndrome-europe/rettxid.git
cd rettxid
pip install -e .
```

---

## Basic Usage

### Generate a new rettX ID

```python
from rettxid import generate_rettx_id

# Generate a unique patient identifier
patient_id = generate_rettx_id()
print(patient_id)  # e.g., 'rettx-8GZ4-MK3P-2Q9A'
```

### Validate a rettX ID

```python
from rettxid import validate_format

# Check if a string is a valid rettX ID
if validate_format(user_input):
    print("Valid rettX ID")
else:
    print("Invalid format")
```

### Normalize user input

```python
from rettxid import normalize

# Handle case variations and whitespace
try:
    canonical = normalize("  rettx-8gz4-mk3p-2q9a  ")
    print(canonical)  # 'rettx-8GZ4-MK3P-2Q9A'
except ValueError as e:
    print(f"Cannot normalize: {e}")
```

---

## Common Patterns

### Validate before storing

```python
from rettxid import validate_format

def save_patient(rettx_id: str, name: str) -> None:
    if not validate_format(rettx_id):
        raise ValueError(f"Invalid rettX ID: {rettx_id}")
    # Proceed with storage...
```

### Normalize on input, validate on output

```python
from rettxid import normalize, validate_format

def process_scanned_id(raw_scan: str) -> str:
    """Process QR scan or user input into canonical form."""
    canonical = normalize(raw_scan)  # Raises ValueError if invalid
    assert validate_format(canonical)  # Should always pass
    return canonical
```

### Generate and verify round-trip

```python
from rettxid import generate_rettx_id, validate_format

# Every generated ID is valid by construction
new_id = generate_rettx_id()
assert validate_format(new_id)  # Always True
```

---

## Development Setup

### Prerequisites

- Python 3.11+
- pip

### Install dev dependencies

```bash
pip install -e ".[dev]"
```

### Run tests

```bash
pytest
```

### Run type checker

```bash
mypy src/rettxid
```

### Run linter

```bash
ruff check src/rettxid tests
```

---

## Verification Checklist

After implementation, verify:

- [X] `generate_rettx_id()` returns valid format
- [X] `validate_format()` accepts generated IDs
- [X] `validate_format()` rejects invalid inputs
- [X] `normalize()` handles case and whitespace
- [X] `normalize()` raises `ValueError` for invalid input
- [X] No runtime dependencies in `pyproject.toml`
- [X] `mypy --strict` passes
- [X] `pytest --cov` shows >95% coverage

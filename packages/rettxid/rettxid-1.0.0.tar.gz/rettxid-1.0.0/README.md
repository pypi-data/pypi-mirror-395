# 🧬 **rettxid — RettX Patient Identifier Library**

[![CI](https://github.com/rett-europe/rettxid/actions/workflows/ci.yml/badge.svg)](https://github.com/rett-europe/rettxid/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/rettxid.svg)](https://badge.fury.io/py/rettxid)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

`rettxid` is the official Python library for generating and validating **rettX IDs**, the pseudonymous, GDPR-safe identifiers used across the **rettX European Rett Syndrome Patient Registry**.

A **rettX ID** is a stable, globally unique, non-PII, human-friendly identifier assigned to each patient record. It enables:

- safe cross-border data harmonization  
- pseudonymous linking of datasets  
- interoperability between registries, clinicians, and research groups  
- QR-based emergency and verification workflows  
- long-term governance for Rett Syndrome data in Europe  

This repository contains the **canonical reference implementation** of the rettX ID format and generation rules.

> **Important:** This library is **stateless**. It does *not* store rettX IDs or patient information.  
> Persistence and API endpoints are implemented in **rettxapi**.

---

## ✨ Features

- Pure Python implementation (Python 3.11+)
- Zero runtime dependencies (stdlib only)
- Cryptographically secure ID generation using `secrets` module
- Strict format validation with pre-compiled regex
- Input normalization (handles case variations, whitespace, missing dashes)
- Ambiguity-safe alphabet (excludes 0, 1, I, L, O, S)
- Full type annotations (PEP 561 compliant)
- 95%+ test coverage with property-based testing
- Designed for integration with rettxapi and other rettX services

---

## 📦 Installation

Once published to PyPI:

```bash
pip install rettxid
```

Or install directly from GitHub:

```bash
pip install git+https://github.com/rett-europe/rettxid.git
```

For development:

```bash
git clone https://github.com/rett-europe/rettxid.git
cd rettxid
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
pip install -e ".[dev]"
```

---

## 🚀 Usage

### Generate a New rettX ID

```python
from rettxid import generate_rettx_id

# Generate a new cryptographically random rettX ID
rid = generate_rettx_id()
print(rid)  
# → rettx-8GZ4-MK3P-2Q9A
```

### Validate Format

```python
from rettxid import validate_format

# Check if a string is a valid rettX ID format
validate_format("rettx-8GZ4-MK3P-2Q9A")  # → True
validate_format("rettx-8gz4-mk3p-2q9a")  # → False (lowercase body)
validate_format("invalid")               # → False
validate_format(None)                    # → False (doesn't raise)
```

### Normalize User Input

```python
from rettxid import normalize

# Convert various input formats to canonical form
normalize("rettx-8gz4-mk3p-2q9a")     # → "rettx-8GZ4-MK3P-2Q9A"
normalize("RETTX-8GZ4-MK3P-2Q9A")     # → "rettx-8GZ4-MK3P-2Q9A"
normalize("rettx8GZ4MK3P2Q9A")        # → "rettx-8GZ4-MK3P-2Q9A"
normalize("  rettx-8GZ4-MK3P-2Q9A  ") # → "rettx-8GZ4-MK3P-2Q9A"

# Raises ValueError for invalid input
normalize("invalid")  # → ValueError: Invalid rettX ID: 'invalid'

# Raises TypeError for non-string input  
normalize(None)       # → TypeError
```

---

## 📋 API Reference

### `generate_rettx_id() -> str`

Generate a new cryptographically random rettX ID.

- **Returns:** A valid rettX ID in format `rettx-XXXX-XXXX-XXXX`
- **Raises:** `RuntimeError` if system entropy is unavailable (rare)

### `validate_format(id: str) -> bool`

Check if a string matches the rettX ID v1 format.

- **Parameters:** `id` — The string to validate
- **Returns:** `True` if valid format, `False` otherwise
- **Note:** Never raises; returns `False` for any invalid input including non-strings

### `normalize(id: str) -> str`

Normalize a string into canonical rettX ID form.

- **Parameters:** `id` — The string to normalize
- **Returns:** The canonical rettX ID
- **Raises:** 
  - `ValueError` if input cannot be normalized
  - `TypeError` if input is not a string

---

## 🔐 Format Specification

The rettX ID v1 format:

```
rettx-XXXX-XXXX-XXXX
```

- **Prefix:** `rettx-` (6 characters, always lowercase)
- **Body:** 3 groups of 4 characters, separated by dashes
- **Alphabet:** 30 ambiguity-safe characters: `23456789ABCDEFGHJKMNPQRTUVWXYZ`
- **Excluded:** `0` (zero), `1` (one), `I`, `L`, `O`, `S` (visually confusable)
- **Total length:** 20 characters
- **Entropy:** ~59 bits (collision probability < 1 in 30 million at 100K scale)

---

## 🔗 Integration with rettxapi

This library:

- Generates rettX IDs  
- Validates rettX ID format  
- Normalizes user input

The **rettxapi backend**:

- Stores `rettx_id` inside patient documents  
- Ensures uniqueness  
- Provides public & internal API endpoints  
- Generates QR codes for rettX SOS  
- Handles authentication, authorization, and audit logging  

---

## 🧪 Testing

Run tests with:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=rettxid --cov-report=term-missing
```

Run type checking:

```bash
mypy src/rettxid --strict
```

Run linting:

```bash
ruff check src/rettxid tests
```

---

## 🗺️ Roadmap

- v1: ✅ Initial ID format definition and reference implementation  
- v2: Optional checksum support  
- v3: Backward-compatible decoding/format transitions  
- Governance specification for rettX ID lifecycle  
- Language bindings (Rust, TypeScript)  

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or PR.

---

## 📄 License

This project is licensed under the **MIT License**, a permissive open-source license ideal for libraries intended to be reused across registries, research tools, and backend services. See `LICENSE` for details.

---

## ❤️ About Rett Syndrome Europe

This project is maintained by **Rett Syndrome Europe (RSE)** as part of the **rettX** ecosystem — a pan-European effort to build harmonized, high-quality patient data infrastructure to support research, clinical care, and family empowerment.

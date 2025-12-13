# Implementation Plan: rettX ID Core Library (v1)

**Branch**: `001-rettxid-core` | **Date**: 2025-12-06 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/001-rettxid-core/spec.md`

## Summary

Implement the rettxid Python library providing three pure functions: `generate_rettx_id()`, `validate_format()`, and `normalize()`. The library generates cryptographically random pseudonymous identifiers using an ambiguity-safe alphabet, validates format compliance, and normalizes user input to canonical form. Zero runtime dependencies, full type coverage, >95% test coverage.

## Technical Context

**Language/Version**: Python 3.11+ (required for modern typing features like `Self`, `|` union syntax)  
**Primary Dependencies**: None (stdlib only: `secrets`, `re`, `string`)  
**Storage**: N/A (stateless library)  
**Testing**: pytest, pytest-cov, hypothesis (property-based testing)  
**Target Platform**: Any Python 3.11+ environment (Linux, macOS, Windows)  
**Project Type**: Single Python package  
**Performance Goals**: <1ms per function call  
**Constraints**: Zero runtime dependencies, no I/O, no mutable state  
**Scale/Scope**: ~200 LOC core library, ~500 LOC tests

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Invariant/Principle | Status | Compliance Notes |
|---------------------|--------|------------------|
| I. One Patient, One ID | ✅ PASS | Not enforced here (rettxapi responsibility) |
| II. Global Uniqueness | ✅ PASS | 57 bits entropy via `secrets`; collision <1 in 30M at 100k scale |
| III. Zero PII, Zero Meaning | ✅ PASS | Pure random from safe alphabet, no semantic encoding |
| IV. Immutability | ✅ PASS | Library doesn't mutate; stability is rettxapi's concern |
| V. Human & Machine Readable | ✅ PASS | 27-char ambiguity-safe alphabet, 4-4-4 grouping, normalization |
| VI. Purity & Statelessness | ✅ PASS | No I/O, no global state, only `secrets` entropy read |
| VII. Minimal Surface | ✅ PASS | Exactly 3 public functions in `__init__.py` |
| VIII. Backward Compatibility | ✅ PASS | v1 format versioned, all IDs valid forever |

**Gate Status**: ✅ PASSED (Pre-research) ✅ PASSED (Post-design)

## Project Structure

### Documentation (this feature)

```text
specs/001-rettxid-core/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (API contracts)
│   └── api.md
└── tasks.md             # Phase 2 output (created by /speckit.tasks)
```

### Source Code (repository root)

```text
src/
└── rettxid/
    ├── __init__.py      # Public API exports
    ├── _generator.py    # generate_rettx_id() implementation
    ├── _validator.py    # validate_format() implementation
    ├── _normalizer.py   # normalize() implementation
    ├── _alphabet.py     # Ambiguity-safe character set
    ├── _format.py       # v1 format constants (prefix, grouping)
    └── py.typed         # PEP 561 marker

tests/
├── conftest.py          # Shared fixtures
├── test_generator.py    # Generation tests
├── test_validator.py    # Validation tests
├── test_normalizer.py   # Normalization tests
├── test_roundtrip.py    # Property-based round-trip tests
└── test_edge_cases.py   # Edge case coverage

pyproject.toml           # Package configuration
```

**Structure Decision**: Single Python package (`src/rettxid/`) with internal modules prefixed with underscore. Public API exposed via `__init__.py`. Tests in parallel `tests/` directory.

## Complexity Tracking

> No violations — all gates passed. No complexity justification needed.

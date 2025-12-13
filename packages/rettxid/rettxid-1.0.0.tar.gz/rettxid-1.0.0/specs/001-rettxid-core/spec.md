# Feature Specification: rettX ID Core Library (v1)

**Feature Branch**: `001-rettxid-core`  
**Created**: 2025-12-06  
**Status**: Draft  
**Input**: rettX ID Format Specification v1 + Constitution v1.1.0

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Generate New rettX ID (Priority: P1)

As a **backend service developer** integrating with rettxapi, I need to generate new rettX IDs for patient records so that each patient receives a unique, pseudonymous identifier that can be stored and used across the rettX ecosystem.

**Why this priority**: This is the foundational capability. Without ID generation, the library has no purpose. Every downstream use case depends on this.

**Independent Test**: Can be fully tested by calling the generate function and verifying the output matches the expected format. Delivers immediate value as the primary library function.

**Acceptance Scenarios**:

1. **Given** the library is imported, **When** I call the generate function, **Then** I receive a string that matches the rettX ID v1 format
2. **Given** the library is imported, **When** I call the generate function multiple times, **Then** each result is different (with extremely high probability)
3. **Given** the library is imported, **When** I call the generate function, **Then** the result contains only the allowed character set (uppercase alphanumerics from the ambiguity-safe alphabet)
4. **Given** the library is imported, **When** I call the generate function, **Then** the result starts with the `rettx-` prefix

---

### User Story 2 - Validate rettX ID Format (Priority: P2)

As a **developer building import tools or forms**, I need to validate whether a given string is a valid rettX ID format so that I can reject malformed input before it reaches the database or causes downstream errors.

**Why this priority**: Validation is critical for data integrity. Systems receiving rettX IDs from external sources (forms, imports, QR scans) must verify format correctness before processing.

**Independent Test**: Can be fully tested by passing known valid and invalid strings and verifying the boolean result. Delivers value as a standalone guard for data quality.

**Acceptance Scenarios**:

1. **Given** a correctly formatted rettX ID (e.g., `rettx-6HF2-9QP8-4TXB`), **When** I call the validate function, **Then** it returns true
2. **Given** a string missing the `rettx-` prefix (e.g., `6HF2-9QP8-4TXB`), **When** I call the validate function, **Then** it returns false
3. **Given** a string with invalid characters (e.g., `rettx-6HF2-9QO8-4TXB` containing excluded letter `O`), **When** I call the validate function, **Then** it returns false (both `0` and `O` are excluded from the safe alphabet)
4. **Given** an empty string, **When** I call the validate function, **Then** it returns false
5. **Given** a string with incorrect grouping or length, **When** I call the validate function, **Then** it returns false
6. **Given** a lowercase but otherwise valid rettX ID, **When** I call the validate function, **Then** it returns false (validation is strict; use normalize first for case-insensitive matching)

---

### User Story 3 - Normalize rettX ID Input (Priority: P3)

As a **developer handling user-entered or scanned rettX IDs**, I need to normalize input strings into canonical form so that minor transcription variations (lowercase, extra spaces, inconsistent dashes) don't cause false mismatches.

**Why this priority**: Normalization improves user experience and data consistency. Users may type IDs in lowercase or with accidental whitespace; normalization makes the system forgiving without compromising validation.

**Independent Test**: Can be fully tested by passing strings with various formatting issues and verifying the normalized output matches canonical form. Delivers value for any user-facing input handling.

**Acceptance Scenarios**:

1. **Given** a lowercase valid rettX ID (e.g., `rettx-6hf2-9qp8-4txb`), **When** I call the normalize function, **Then** it returns the uppercase canonical form (`rettx-6HF2-9QP8-4TXB`)
2. **Given** a rettX ID with leading/trailing whitespace, **When** I call the normalize function, **Then** it returns the trimmed canonical form
3. **Given** a rettX ID with missing dashes but correct characters (e.g., `rettx6HF29QP84TXB`), **When** I call the normalize function, **Then** it returns the properly grouped form with dashes
4. **Given** a completely invalid string that cannot be normalized, **When** I call the normalize function, **Then** it raises an error indicating the input is not a valid rettX ID
5. **Given** an already canonical rettX ID, **When** I call the normalize function, **Then** it returns the same string unchanged

---

### Edge Cases

- What happens when the input is `None` or a non-string type? → Functions should handle gracefully (validate returns false, normalize raises error)
- What happens with Unicode characters or non-ASCII input? → Validation should reject; normalize should fail
- What happens with extremely long strings? → Validation should reject efficiently without resource exhaustion
- What happens with strings containing only the prefix `rettx-`? → Validation returns false (missing random portion)
- What happens with mixed valid/invalid characters? → Validation returns false
- How does the library behave when the system has no entropy source? → Generation should fail explicitly rather than produce weak IDs

## Requirements *(mandatory)*

### Functional Requirements

**Generation**:
- **FR-001**: Library MUST provide a function to generate new rettX IDs
- **FR-002**: Generated IDs MUST use cryptographically secure randomness
- **FR-003**: Generated IDs MUST contain sufficient entropy for global uniqueness (collision probability < 1 in 30 million at 100,000 patients scale)
- **FR-004**: Generated IDs MUST follow the v1 format: `rettx-` prefix followed by uppercase alphanumeric groups separated by dashes
- **FR-005**: Generated IDs MUST use only the ambiguity-safe character alphabet (excluding visually confusable characters)

**Validation**:
- **FR-006**: Library MUST provide a function to validate whether a string matches rettX ID v1 format
- **FR-007**: Validation MUST check the prefix is exactly `rettx-`
- **FR-008**: Validation MUST verify all characters are from the allowed alphabet
- **FR-009**: Validation MUST verify the grouping pattern matches v1 specification
- **FR-010**: Validation MUST return a boolean result (no exceptions for invalid input)
- **FR-011**: Validation MUST NOT check uniqueness or patient existence (out of scope)

**Normalization**:
- **FR-012**: Library MUST provide a function to normalize input into canonical rettX ID form
- **FR-013**: Normalization MUST convert the random portion to uppercase
- **FR-014**: Normalization MUST strip leading and trailing whitespace
- **FR-015**: Normalization MUST standardize dash placement according to v1 grouping rules
- **FR-016**: Normalization MUST raise an error for input that cannot be normalized to valid form
- **FR-017**: Normalization MUST be idempotent (normalizing a normalized ID returns the same result)

**Library Constraints** (per Constitution):
- **FR-018**: Library MUST NOT access filesystem, network, or databases
- **FR-019**: Library MUST NOT accept any PII as input
- **FR-020**: Library MUST have zero runtime dependencies (stdlib only)
- **FR-021**: Library MUST expose only the three public functions (generate, validate, normalize)

### Key Entities

- **rettX ID**: A pseudonymous patient identifier string following the v1 format. Attributes: prefix (`rettx-`), random portion (grouped alphanumerics), version (implicit v1).

### Assumptions

- ~~The exact v1 grouping pattern (number of groups, characters per group) will be defined during implementation based on entropy requirements~~ **RESOLVED**: 4-4-4 grouping (12 random chars, 57 bits entropy) per research.md
- The ambiguity-safe alphabet excludes `0`, `1`, `I`, `L`, `O`, `S` (6 chars) as defined in research.md
- Python 3.11+ is the target runtime (per README)
- The `secrets` module is available for cryptographic randomness

## Clarifications

### Session 2025-12-06

- Q: What should the rettX ID prefix be? → A: `rettx-` (not `rtx-`)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% of generated IDs pass format validation (round-trip consistency)
- **SC-002**: Generation produces unique IDs in 1 million consecutive calls (no duplicates in test runs)
- **SC-003**: Validation correctly classifies 100% of test cases (valid IDs return true, invalid IDs return false)
- **SC-004**: Normalization successfully converts 100% of case/whitespace variants to canonical form
- **SC-005**: All public functions execute in under 1ms per call on standard hardware
- **SC-006**: Library has zero runtime dependencies (verified by inspection of package metadata)
- **SC-007**: Test coverage exceeds 95% of all code paths
- **SC-008**: All public functions have complete type annotations that pass strict type checking

````markdown
# Tasks: rettX ID Core Library (v1)

**Input**: Design documents from `/specs/001-rettxid-core/`  
**Prerequisites**: plan.md ✅, spec.md ✅, research.md ✅, data-model.md ✅, contracts/api.md ✅, quickstart.md ✅

**Tests**: Included (property-based testing with hypothesis per plan.md)

**Organization**: Tasks grouped by user story to enable independent implementation and testing.

## Format: `[ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, package configuration, and foundational modules

- [X] T001 Create project directory structure per plan.md: `src/rettxid/`, `tests/`
- [X] T002 Create `pyproject.toml` with package metadata, Python 3.11+ requirement, and dev dependencies (pytest, pytest-cov, hypothesis, mypy, ruff)
- [X] T003 [P] Create `src/rettxid/py.typed` marker file for PEP 561 compliance
- [X] T004 [P] Create `.gitignore` with Python patterns (*.pyc, __pycache__, .venv, dist/, *.egg-info)
- [X] T005 [P] Create `tests/conftest.py` with shared pytest fixtures

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core constants and shared modules that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Create alphabet constants in `src/rettxid/_alphabet.py`: `SAFE_ALPHABET = "23456789ABCDEFGHJKMNPQRTUVWXYZ"` (30 chars)
- [X] T007 Create format constants in `src/rettxid/_format.py`: `PREFIX`, `GROUP_SIZE`, `GROUP_COUNT`, `SEPARATOR`, `RANDOM_LENGTH`, `TOTAL_LENGTH`, `VALID_PATTERN` regex
- [X] T008 Create `src/rettxid/__init__.py` with `__all__` exporting `generate_rettx_id`, `validate_format`, `normalize` (stubs only, raise NotImplementedError)
- [X] T009 Verify foundational setup: run `python -c "from rettxid import generate_rettx_id, validate_format, normalize"` succeeds

**Checkpoint**: Foundation ready — all constants defined, package importable, user story implementation can begin

---

## Phase 3: User Story 1 — Generate New rettX ID (Priority: P1) 🎯 MVP

**Goal**: Implement `generate_rettx_id()` function that produces cryptographically random IDs in v1 format

**Independent Test**: Call `generate_rettx_id()` and verify output matches regex `^rettx-[23456789ABCDEFGHJKMNPQRTUVWXYZ]{4}-[23456789ABCDEFGHJKMNPQRTUVWXYZ]{4}-[23456789ABCDEFGHJKMNPQRTUVWXYZ]{4}$`

### Tests for User Story 1

- [X] T010 [P] [US1] Create `tests/test_generator.py` with tests: output matches format, length is 20, prefix is `rettx-`, all chars from safe alphabet
- [X] T011 [P] [US1] Add property-based test in `tests/test_roundtrip.py`: 10,000 generated IDs all unique, all valid format (note: SC-002 requires 1M for production validation; use hypothesis for statistical confidence)

### Implementation for User Story 1

- [X] T012 [US1] Implement `_generate_random_part()` in `src/rettxid/_generator.py` using `secrets.choice()` with `SAFE_ALPHABET`
- [X] T013 [US1] Implement `_format_with_groups()` in `src/rettxid/_generator.py` to insert dashes every 4 chars
- [X] T014 [US1] Implement `generate_rettx_id()` in `src/rettxid/_generator.py`: combine prefix + formatted random part
- [X] T015 [US1] Export `generate_rettx_id` from `src/rettxid/__init__.py` (replace stub with real import)
- [X] T016 [US1] Run tests: `pytest tests/test_generator.py tests/test_roundtrip.py -v`

**Checkpoint**: User Story 1 complete — `generate_rettx_id()` works independently, MVP delivered

---

## Phase 4: User Story 2 — Validate rettX ID Format (Priority: P2)

**Goal**: Implement `validate_format()` function that strictly validates v1 format compliance

**Independent Test**: Call `validate_format()` with known valid/invalid strings, verify correct boolean results

### Tests for User Story 2

- [X] T017 [P] [US2] Create `tests/test_validator.py` with tests: valid IDs return True, missing prefix returns False, invalid chars return False, wrong length returns False, lowercase body returns False, empty/None returns False
- [X] T018 [P] [US2] Add edge case tests in `tests/test_edge_cases.py`: very long strings, Unicode chars, prefix-only, excluded chars (0, 1, I, L, O, S)

### Implementation for User Story 2

- [X] T019 [US2] Implement `validate_format(id: str) -> bool` in `src/rettxid/_validator.py` using pre-compiled `VALID_PATTERN` regex
- [X] T020 [US2] Handle non-string input: return `False` without raising (use `isinstance` check)
- [X] T021 [US2] Export `validate_format` from `src/rettxid/__init__.py` (replace stub with real import)
- [X] T022 [US2] Add round-trip test in `tests/test_roundtrip.py`: `validate_format(generate_rettx_id())` always True
- [X] T023 [US2] Run tests: `pytest tests/test_validator.py tests/test_edge_cases.py tests/test_roundtrip.py -v`

**Checkpoint**: User Story 2 complete — `validate_format()` works independently, can validate any input string

---

## Phase 5: User Story 3 — Normalize rettX ID Input (Priority: P3)

**Goal**: Implement `normalize()` function that converts user input variations into canonical form

**Independent Test**: Call `normalize()` with lowercase, whitespace-padded, and dash-free variants; verify canonical output

### Tests for User Story 3

- [X] T024 [P] [US3] Create `tests/test_normalizer.py` with tests: lowercase→uppercase, strip whitespace, insert dashes, uppercase prefix→lowercase, already canonical→unchanged
- [X] T025 [P] [US3] Add error tests in `tests/test_normalizer.py`: invalid chars raise ValueError, wrong length raises ValueError, non-string raises TypeError

### Implementation for User Story 3

- [X] T026 [US3] Implement `_extract_chars()` in `src/rettxid/_normalizer.py`: strip whitespace, remove dashes/spaces, extract alphanumeric portion
- [X] T027 [US3] Implement `_validate_extracted_chars()` in `src/rettxid/_normalizer.py`: verify all chars are in `SAFE_ALPHABET` (case-insensitive), correct length
- [X] T028 [US3] Implement `normalize(id: str) -> str` in `src/rettxid/_normalizer.py`: extract → validate → format → return canonical
- [X] T029 [US3] Add type check at start of `normalize()`: raise `TypeError` if input is not `str`
- [X] T030 [US3] Export `normalize` from `src/rettxid/__init__.py` (replace stub with real import)
- [X] T031 [US3] Add idempotence test in `tests/test_roundtrip.py`: `normalize(normalize(x)) == normalize(x)`
- [X] T032 [US3] Run tests: `pytest tests/test_normalizer.py tests/test_roundtrip.py -v`

**Checkpoint**: User Story 3 complete — `normalize()` works independently, handles all input variations

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Quality assurance, documentation, and final validation

- [X] T033 [P] Run full test suite with coverage: `pytest --cov=rettxid --cov-report=term-missing`
- [X] T034 [P] Run mypy strict mode: `mypy src/rettxid --strict`
- [X] T035 [P] Run ruff linter: `ruff check src/rettxid tests`
- [X] T036 Fix any type errors or lint issues found in T033-T035
- [X] T037 Verify coverage > 95% (per SC-007), add tests if needed
- [X] T038 Update `README.md` with installation, usage examples, and API reference
- [X] T039 Run quickstart.md verification checklist
- [X] T040 Final validation: `python -c "from rettxid import generate_rettx_id, validate_format, normalize; id = generate_rettx_id(); print(id, validate_format(id), normalize(id.lower()))"`

**Checkpoint**: All quality gates passed, library ready for release ✅

---

## Dependencies & Execution Order

### Phase Dependencies

```
Phase 1: Setup ──────────────┐
                             ▼
Phase 2: Foundational ───────┤
                             │
         ┌───────────────────┼───────────────────┐
         ▼                   ▼                   ▼
Phase 3: US1 (Generate) Phase 4: US2 (Validate) Phase 5: US3 (Normalize)
  [MVP]                    [Can use US1]         [Can use US1, US2]
         │                   │                   │
         └───────────────────┴───────────────────┘
                             │
                             ▼
Phase 6: Polish ─────────────┘
```

### User Story Dependencies

| Story | Depends On | Can Start After |
|-------|------------|-----------------|
| US1 (Generate) | Phase 2 only | T009 complete |
| US2 (Validate) | Phase 2 only | T009 complete |
| US3 (Normalize) | Phase 2 only | T009 complete |

**Note**: All user stories are independent and can be developed in parallel. US2 and US3 don't need US1's generate function to work — they operate on string inputs.

### Within Each User Story

1. Tests FIRST (TDD): Write tests, ensure they fail
2. Implementation: Core logic
3. Integration: Export from `__init__.py`
4. Verification: Run tests, confirm pass

### Parallel Opportunities

**Phase 1** — All [P] tasks can run in parallel:
- T003, T004, T005

**Phase 2** — Sequential (constants depend on each other)

**Phase 3-5** — User stories can run in parallel if team capacity allows:
- US1 (T010-T016)
- US2 (T017-T023)
- US3 (T024-T032)

**Phase 6** — All [P] tasks can run in parallel:
- T033, T034, T035

---

## Parallel Example: User Story 1

```bash
# Tests first (in parallel):
Task T010: "Create tests/test_generator.py with format validation tests"
Task T011: "Add property-based test in tests/test_roundtrip.py"

# Implementation (sequential within story):
Task T012: "Implement _generate_random_part() in src/rettxid/_generator.py"
Task T013: "Implement _format_with_groups() in src/rettxid/_generator.py"
Task T014: "Implement generate_rettx_id() in src/rettxid/_generator.py"
Task T015: "Export from __init__.py"
Task T016: "Run tests"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. ✅ Complete Phase 1: Setup
2. ✅ Complete Phase 2: Foundational
3. ✅ Complete Phase 3: User Story 1 (Generate)
4. **STOP and VALIDATE**: Test `generate_rettx_id()` independently
5. Ship MVP — generation capability is immediately useful

### Incremental Delivery

| Increment | User Stories | Value Delivered |
|-----------|--------------|-----------------|
| MVP | US1 | Generate new IDs |
| v1.1 | US1 + US2 | Generate + Validate |
| v1.2 | US1 + US2 + US3 | Full library |

### Parallel Team Strategy

With 2-3 developers after Phase 2:

- **Dev A**: User Story 1 (Generate) → Phase 6
- **Dev B**: User Story 2 (Validate) 
- **Dev C**: User Story 3 (Normalize)

All merge into `001-rettxid-core` branch, then Phase 6 quality gates.

---

## Notes

- All file paths are relative to repository root
- [P] tasks can run in parallel with other [P] tasks in same phase
- Each user story delivers independently testable functionality
- Commit after each task or logical group
- Run `pytest` after each implementation task to catch regressions early

````
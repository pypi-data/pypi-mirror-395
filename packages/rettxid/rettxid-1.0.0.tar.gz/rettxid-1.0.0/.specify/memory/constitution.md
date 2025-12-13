<!--
╔════════════════════════════════════════════════════════════════════════════╗
║                         SYNC IMPACT REPORT                                  ║
╠════════════════════════════════════════════════════════════════════════════╣
║ Version Change: 1.0.0 → 1.1.0 (Refocus on principles over implementation)  ║
║                                                                            ║
║ Modified Sections:                                                         ║
║   - Core Principles: Restructured around ecosystem invariants              ║
║   - Removed: Technical Constraints (implementation detail)                 ║
║   - Removed: API Contract (implementation detail)                          ║
║   - Added: rettX ID Invariants (ecosystem-level guarantees)                ║
║   - Added: Library Discipline (development principles)                     ║
║                                                                            ║
║ Principles (renamed/restructured):                                         ║
║   I. One Patient, One ID → NEW (ecosystem invariant)                       ║
║   II. Global Uniqueness → NEW (ecosystem invariant)                        ║
║   III. Zero PII, Zero Meaning → Expanded from "Zero PII"                   ║
║   IV. Immutability → NEW (ecosystem invariant)                             ║
║   V. Human & Machine Readable → NEW (ecosystem invariant)                  ║
║   VI. Purity & Statelessness → Retained (library discipline)               ║
║   VII. Minimal Surface → Simplified from "Minimal Public API"              ║
║   VIII. Backward Compatibility → Retained (library discipline)             ║
║                                                                            ║
║ Templates Compatibility:                                                   ║
║   ✅ plan-template.md - Constitution Check section compatible              ║
║   ✅ spec-template.md - Requirements section compatible                    ║
║   ✅ tasks-template.md - Phase structure compatible                        ║
║   ✅ checklist-template.md - No conflicts                                  ║
║   ✅ agent-file-template.md - No conflicts                                 ║
║                                                                            ║
║ Follow-up TODOs: None                                                      ║
╚════════════════════════════════════════════════════════════════════════════╝
-->

# rettxid Constitution

This constitution defines the **invariants** and **principles** that govern the rettX ID within the Rett Syndrome Europe ecosystem. It anchors what the identifier *means* and what guarantees it provides — constraints that cannot be broken by future changes.

---

## rettX ID Invariants

These are the **non-negotiable guarantees** that the rettX ID provides to the ecosystem. Any change that violates these invariants requires a new identifier system, not an amendment.

### I. One Patient, One ID

Every patient in the rettX ecosystem has **exactly one** rettX ID.

- A patient MUST NOT have multiple rettX IDs
- A rettX ID MUST NOT be shared between patients
- This 1:1 mapping is enforced by rettxapi, not this library

**Rationale**: The rettX ID is the canonical key for cross-system patient identification. Duplicates or splits would corrupt data linkage across registries.

### II. Global Uniqueness

A rettX ID is **globally unique** within the rettX ecosystem.

- No two patients may share the same rettX ID, regardless of country or registry
- Uniqueness is probabilistically guaranteed by sufficient entropy at generation
- Uniqueness enforcement (collision detection) is the responsibility of rettxapi

**Rationale**: The ID enables safe cross-border data harmonization. Global uniqueness is the foundation of pseudonymous linking.

### III. Zero PII, Zero Meaning (NON-NEGOTIABLE)

A rettX ID is **pseudonymous** and encodes **no information**.

- MUST NOT contain or encode any personally identifiable information
- MUST NOT encode timestamps, creation dates, or sequence numbers
- MUST NOT encode country codes, registry identifiers, or geographic data
- MUST NOT encode patient attributes (age, mutation type, severity, etc.)
- MUST NOT encode any semantic meaning whatsoever
- All entropy MUST come from cryptographically secure random generation

**Rationale**: GDPR compliance requires pseudonymous identifiers. Encoding any meaning creates inference risk and limits future flexibility.

### IV. Immutability

A rettX ID is **stable and permanent** once assigned.

- A patient's rettX ID MUST NOT change after assignment
- There is no "regenerate" or "rotate" operation for a patient
- If an ID must be retired (e.g., duplicate discovered), the old ID is tombstoned, not reassigned

**Rationale**: Stability enables long-term research cohorts, longitudinal studies, and trusted data linkage. Changing IDs would break references across systems.

### V. Human & Machine Readable

A rettX ID is designed for **both human and machine contexts**.

- MUST be readable and transcribable by humans (clinicians, families)
- MUST be unambiguous when printed, spoken, or displayed
- MUST be encodable in QR codes for emergency and verification workflows
- MUST survive common transcription errors via normalization (case, whitespace)

**Rationale**: The ID appears on cards, forms, QR codes, and emergency systems. It must work reliably across all these contexts.

---

## Library Discipline

These principles govern how the **rettxid library** implements the invariants above.

### VI. Purity & Statelessness

This library MUST remain **pure and stateless**.

- No filesystem access, network calls, or database connections
- No side effects beyond returning computed values
- No mutable global state
- No external service dependencies
- Functions are deterministic (except generation, which uses secure entropy)

**Rationale**: rettxid must be safely reusable across CLI tools, migration scripts, backend services, and future language bindings. Purity eliminates integration risks.

### VII. Minimal Surface

The public API MUST remain **small, stable, and obvious**.

- Expose only essential operations: generate, validate, normalize
- No domain logic (patients, registries, countries)
- No persistence, no uniqueness enforcement
- Internal helpers are private implementation details

**Rationale**: A minimal surface reduces maintenance burden, ensures stability, and keeps concerns properly separated. Domain logic belongs in rettxapi.

### VIII. Backward Compatibility

The rettX ID format and library API MUST remain **backward compatible**.

- Every valid rettX ID ever generated MUST remain valid forever
- Public API changes require semantic versioning discipline
- Deprecations MUST precede removals with adequate warning
- Format evolution (if ever needed) MUST be additive, not breaking

**Rationale**: Multiple services depend on this library. The ID format is embedded in patient records, QR codes, and external systems. Breaking changes would cascade across the ecosystem.

---

## Governance

### Constitution Authority

This constitution defines the **identity and guarantees** of the rettX ID. It supersedes implementation decisions. Any change that would violate the invariants in Section 1 is out of scope for this library.

### Amendment Process

1. Propose changes via pull request to this file
2. Invariant changes (Section 1) require ecosystem-wide review
3. Library discipline changes (Section 2) require maintainer approval
4. Include rationale and impact analysis
5. Update version and `LAST_AMENDED_DATE` upon merge

### Compliance Review

All changes to rettxid MUST verify:

- [ ] No invariant violations introduced
- [ ] No PII handling or encoding
- [ ] Backward compatibility preserved
- [ ] Separation of concerns maintained (no domain logic)

---

**Version**: 1.1.0 | **Ratified**: 2025-12-06 | **Last Amended**: 2025-12-06

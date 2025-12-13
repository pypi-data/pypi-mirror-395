"""Property-based round-trip tests for rettX IDs.

Uses hypothesis for property-based testing to verify invariants
across many generated inputs.
"""

from hypothesis import given, settings
from hypothesis import strategies as st

from rettxid import generate_rettx_id, normalize, validate_format
from rettxid._format import VALID_PATTERN


class TestGeneratorRoundtrip:
    """Property-based tests for generate_rettx_id()."""

    @settings(max_examples=10000)
    @given(st.integers(min_value=0, max_value=9999))
    def test_generated_ids_always_valid_format(self, _seed: int) -> None:
        """Every generated ID should match the valid format pattern."""
        result = generate_rettx_id()
        assert VALID_PATTERN.match(result) is not None

    def test_uniqueness_10000_ids(self) -> None:
        """10,000 generated IDs should all be unique.

        Note: SC-002 requires 1M for production validation.
        This test provides statistical confidence for CI runs.
        With 30^12 ≈ 5×10^17 combinations, 10k IDs have
        collision probability < 10^-10.
        """
        ids = [generate_rettx_id() for _ in range(10000)]
        unique_ids = set(ids)
        assert len(unique_ids) == len(ids), (
            f"Found {len(ids) - len(unique_ids)} duplicate IDs in 10,000 generations"
        )

    def test_format_consistency_across_many_generations(self) -> None:
        """All generated IDs should have consistent structure."""
        for _ in range(1000):
            result = generate_rettx_id()

            # Length check
            assert len(result) == 20

            # Structure check
            parts = result.split("-")
            assert len(parts) == 4
            assert parts[0] == "rettx"
            assert all(len(p) == 4 for p in parts[1:])

            # Pattern check
            assert VALID_PATTERN.match(result) is not None


class TestValidatorRoundtrip:
    """Round-trip tests for validate_format() with generate_rettx_id()."""

    def test_generated_id_always_validates(self) -> None:
        """Every generated ID should pass validation."""
        for _ in range(1000):
            generated = generate_rettx_id()
            assert validate_format(generated) is True, (
                f"Generated ID '{generated}' failed validation"
            )

    @settings(max_examples=10000)
    @given(st.integers(min_value=0, max_value=9999))
    def test_validate_after_generate_always_true(self, _seed: int) -> None:
        """Property: validate_format(generate_rettx_id()) is always True."""
        generated = generate_rettx_id()
        assert validate_format(generated) is True


class TestNormalizerRoundtrip:
    """Round-trip tests for normalize() with generate_rettx_id()."""

    def test_normalize_generated_id_unchanged(self) -> None:
        """Generated IDs are already canonical, so normalize should be identity."""
        for _ in range(1000):
            generated = generate_rettx_id()
            normalized = normalize(generated)
            assert normalized == generated, (
                f"Generated ID '{generated}' changed after normalize: '{normalized}'"
            )

    @settings(max_examples=10000)
    @given(st.integers(min_value=0, max_value=9999))
    def test_normalize_idempotent(self, _seed: int) -> None:
        """Property: normalize(normalize(x)) == normalize(x)."""
        generated = generate_rettx_id()
        once = normalize(generated)
        twice = normalize(once)
        assert once == twice, f"Normalization not idempotent: '{once}' != '{twice}'"

    def test_normalize_lowercase_idempotent(self) -> None:
        """Normalizing lowercase input twice equals once."""
        for _ in range(100):
            generated = generate_rettx_id()
            lowercase = generated.lower()
            once = normalize(lowercase)
            twice = normalize(once)
            assert once == twice

    def test_normalize_then_validate_always_true(self) -> None:
        """A normalized ID should always validate."""
        for _ in range(1000):
            generated = generate_rettx_id()
            # Try various transformations
            inputs = [
                generated,
                generated.lower(),
                generated.replace("-", ""),
                "  " + generated + "  ",
            ]
            for inp in inputs:
                normalized = normalize(inp)
                assert validate_format(normalized) is True, (
                    f"Normalized '{inp}' to '{normalized}' but validation failed"
                )

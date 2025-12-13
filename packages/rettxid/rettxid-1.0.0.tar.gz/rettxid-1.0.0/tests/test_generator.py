"""Tests for rettX ID generation."""

from rettxid import generate_rettx_id
from rettxid._alphabet import SAFE_ALPHABET
from rettxid._format import PREFIX, TOTAL_LENGTH, VALID_PATTERN


class TestGenerateRettxId:
    """Tests for generate_rettx_id() function."""

    def test_returns_string(self) -> None:
        """Generated ID should be a string."""
        result = generate_rettx_id()
        assert isinstance(result, str)

    def test_correct_length(self) -> None:
        """Generated ID should be exactly 20 characters."""
        result = generate_rettx_id()
        assert len(result) == TOTAL_LENGTH
        assert len(result) == 20

    def test_starts_with_prefix(self) -> None:
        """Generated ID should start with 'rettx-' prefix."""
        result = generate_rettx_id()
        assert result.startswith(PREFIX)
        assert result.startswith("rettx-")

    def test_matches_format_pattern(self) -> None:
        """Generated ID should match the v1 format regex."""
        result = generate_rettx_id()
        assert VALID_PATTERN.match(result) is not None

    def test_body_uses_safe_alphabet_only(self) -> None:
        """Generated ID body should only contain safe alphabet characters."""
        result = generate_rettx_id()
        # Extract body (everything after prefix, excluding dashes)
        body = result[len(PREFIX) :].replace("-", "")
        for char in body:
            assert char in SAFE_ALPHABET, f"Invalid char '{char}' not in safe alphabet"

    def test_body_is_uppercase(self) -> None:
        """Generated ID body should be uppercase."""
        result = generate_rettx_id()
        body = result[len(PREFIX) :]
        assert body == body.upper()

    def test_correct_grouping(self) -> None:
        """Generated ID should have correct 4-4-4 grouping with dashes."""
        result = generate_rettx_id()
        # Pattern: rettx-XXXX-XXXX-XXXX
        parts = result.split("-")
        assert len(parts) == 4  # prefix part + 3 groups
        assert parts[0] == "rettx"
        assert all(len(part) == 4 for part in parts[1:])

    def test_no_excluded_characters(self) -> None:
        """Generated ID should not contain excluded characters (0, 1, I, L, O, S)."""
        excluded = set("01ILOS")
        # Generate multiple IDs to increase confidence
        for _ in range(100):
            result = generate_rettx_id()
            body = result[len(PREFIX) :].replace("-", "")
            for char in body:
                assert char not in excluded, f"Excluded char '{char}' found in ID"

    def test_multiple_calls_produce_different_ids(self) -> None:
        """Multiple calls should produce different IDs (extremely high probability)."""
        ids = [generate_rettx_id() for _ in range(100)]
        unique_ids = set(ids)
        assert len(unique_ids) == len(ids), "Duplicate ID generated"

    def test_prefix_is_lowercase(self) -> None:
        """The prefix portion should be lowercase."""
        result = generate_rettx_id()
        prefix_part = result[: len(PREFIX)]
        assert prefix_part == prefix_part.lower()
        assert prefix_part == "rettx-"


class TestGenerateRettxIdStatistical:
    """Statistical tests for randomness quality."""

    def test_character_distribution(self) -> None:
        """Characters should be roughly uniformly distributed."""
        # Generate 1000 IDs and collect character frequencies
        char_counts: dict[str, int] = {}
        num_ids = 1000

        for _ in range(num_ids):
            result = generate_rettx_id()
            body = result[len(PREFIX) :].replace("-", "")
            for char in body:
                char_counts[char] = char_counts.get(char, 0) + 1

        # Each of 30 characters should appear roughly equally
        # With 1000 IDs × 12 chars = 12000 chars total
        # Expected per char ≈ 12000 / 30 = 400
        total_chars = num_ids * 12
        expected_per_char = total_chars / len(SAFE_ALPHABET)

        # Allow 50% deviation (very generous for statistical test)
        min_expected = expected_per_char * 0.5
        max_expected = expected_per_char * 1.5

        for char in SAFE_ALPHABET:
            count = char_counts.get(char, 0)
            assert min_expected <= count <= max_expected, (
                f"Character '{char}' appears {count} times, "
                f"expected between {min_expected:.0f} and {max_expected:.0f}"
            )

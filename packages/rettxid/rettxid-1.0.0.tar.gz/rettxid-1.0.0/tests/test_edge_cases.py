"""Edge case tests for rettX ID validation."""

import pytest

from rettxid import validate_format
from rettxid._alphabet import EXCLUDED_CHARS, SAFE_ALPHABET


class TestValidateFormatEdgeCases:
    """Edge case tests for validate_format()."""

    def test_very_long_string(self) -> None:
        """Very long strings should return False efficiently."""
        long_string = "rettx-" + "A" * 10000
        assert validate_format(long_string) is False

    def test_extremely_long_string(self) -> None:
        """Extremely long strings should not cause performance issues."""
        huge_string = "A" * 1_000_000
        assert validate_format(huge_string) is False

    def test_unicode_characters(self) -> None:
        """Unicode characters should return False."""
        assert validate_format("rettx-8GZ4-MK3P-2Q9Ą") is False  # Polish A
        assert validate_format("rettx-8GZ4-MK3P-2Q9日") is False  # Japanese
        assert validate_format("rettx-8GZ4-MK3P-2Q9🎉") is False  # Emoji

    def test_special_characters(self) -> None:
        """Special characters should return False."""
        assert validate_format("rettx-8GZ4-MK3P-2Q9!") is False
        assert validate_format("rettx-8GZ4-MK3P-2Q9@") is False
        assert validate_format("rettx-8GZ4-MK3P-2Q9#") is False
        assert validate_format("rettx-8GZ4-MK3P-2Q9$") is False

    def test_newlines_in_string(self) -> None:
        """Strings with newlines should return False."""
        assert validate_format("rettx-8GZ4\n-MK3P-2Q9A") is False
        assert validate_format("rettx-8GZ4-MK3P-2Q9A\n") is False
        assert validate_format("\nrettx-8GZ4-MK3P-2Q9A") is False

    def test_tabs_in_string(self) -> None:
        """Strings with tabs should return False."""
        assert validate_format("rettx-8GZ4\t-MK3P-2Q9A") is False
        assert validate_format("\trettx-8GZ4-MK3P-2Q9A") is False

    def test_leading_trailing_whitespace(self) -> None:
        """Strings with leading/trailing whitespace should return False."""
        assert validate_format(" rettx-8GZ4-MK3P-2Q9A") is False
        assert validate_format("rettx-8GZ4-MK3P-2Q9A ") is False
        assert validate_format("  rettx-8GZ4-MK3P-2Q9A  ") is False


class TestExcludedCharacters:
    """Verify all excluded characters are properly rejected."""

    @pytest.mark.parametrize("excluded_char", list(EXCLUDED_CHARS))
    def test_each_excluded_char_rejected(self, excluded_char: str) -> None:
        """Each excluded character should cause validation to fail."""
        # Replace first character of first group with excluded char
        test_id = f"rettx-{excluded_char}GZ4-MK3P-2Q9A"
        assert validate_format(test_id) is False, (
            f"Excluded character '{excluded_char}' should be rejected"
        )

    @pytest.mark.parametrize("safe_char", list(SAFE_ALPHABET[:10]))
    def test_safe_chars_accepted(self, safe_char: str) -> None:
        """Safe alphabet characters should be accepted."""
        # Create valid ID using safe char
        test_id = f"rettx-{safe_char}GZ4-MK3P-2Q9A"
        # This might fail if 'G' is replaced with something incompatible,
        # but all chars in SAFE_ALPHABET should work
        assert validate_format(test_id) is True, (
            f"Safe character '{safe_char}' should be accepted"
        )


class TestBoundaryConditions:
    """Boundary condition tests."""

    def test_minimum_valid_structure(self) -> None:
        """Minimum valid ID structure."""
        # Using all '2's (first char in safe alphabet)
        assert validate_format("rettx-2222-2222-2222") is True

    def test_maximum_valid_structure(self) -> None:
        """Maximum valid ID structure (all Z's)."""
        assert validate_format("rettx-ZZZZ-ZZZZ-ZZZZ") is True

    def test_single_char_difference_from_valid(self) -> None:
        """IDs differing by one char from valid should fail appropriately."""
        # Change prefix case
        invalid1 = "Rettx-8GZ4-MK3P-2Q9A"
        assert validate_format(invalid1) is False

        # Change one body char to lowercase
        invalid2 = "rettx-8gZ4-MK3P-2Q9A"
        assert validate_format(invalid2) is False

        # Change one body char to excluded
        invalid3 = "rettx-8GZ4-MK3P-2Q9O"  # O is excluded
        assert validate_format(invalid3) is False


class TestSimilarLookingStrings:
    """Tests for strings that look similar to valid IDs."""

    def test_mixed_case_prefix_variations(self) -> None:
        """Various prefix case combinations should fail."""
        assert validate_format("ReTtX-8GZ4-MK3P-2Q9A") is False
        assert validate_format("RETTX-8GZ4-MK3P-2Q9A") is False
        assert validate_format("Rettx-8GZ4-MK3P-2Q9A") is False

    def test_similar_prefixes(self) -> None:
        """Prefixes similar to 'rettx-' should fail."""
        assert validate_format("rettx_8GZ4-MK3P-2Q9A") is False  # underscore
        assert validate_format("rettx 8GZ4-MK3P-2Q9A") is False  # space
        assert validate_format("rettx:8GZ4-MK3P-2Q9A") is False  # colon

    def test_confusable_zero_and_o(self) -> None:
        """Both 0 and O should be rejected."""
        assert validate_format("rettx-0GZ4-MK3P-2Q9A") is False  # zero
        assert validate_format("rettx-OGZ4-MK3P-2Q9A") is False  # letter O

    def test_confusable_one_and_i_and_l(self) -> None:
        """1, I, and L should all be rejected."""
        assert validate_format("rettx-1GZ4-MK3P-2Q9A") is False  # one
        assert validate_format("rettx-IGZ4-MK3P-2Q9A") is False  # letter I
        assert validate_format("rettx-LGZ4-MK3P-2Q9A") is False  # letter L

"""Tests for rettX ID normalization."""

import pytest

from rettxid import normalize
from rettxid._alphabet import EXCLUDED_CHARS


class TestNormalizeBasic:
    """Basic normalization tests."""

    def test_returns_string(self) -> None:
        """normalize should return a string."""
        result = normalize("rettx-8GZ4-MK3P-2Q9A")
        assert isinstance(result, str)

    def test_canonical_id_unchanged(self) -> None:
        """Already canonical ID should return unchanged."""
        canonical = "rettx-8GZ4-MK3P-2Q9A"
        assert normalize(canonical) == canonical

    def test_lowercase_body_to_uppercase(self) -> None:
        """Lowercase body should be converted to uppercase."""
        result = normalize("rettx-8gz4-mk3p-2q9a")
        assert result == "rettx-8GZ4-MK3P-2Q9A"

    def test_uppercase_prefix_to_lowercase(self) -> None:
        """Uppercase prefix should be converted to lowercase."""
        result = normalize("RETTX-8GZ4-MK3P-2Q9A")
        assert result == "rettx-8GZ4-MK3P-2Q9A"

    def test_mixed_case_normalized(self) -> None:
        """Mixed case should be normalized correctly."""
        result = normalize("ReTtX-8gZ4-Mk3P-2q9A")
        assert result == "rettx-8GZ4-MK3P-2Q9A"


class TestNormalizeWhitespace:
    """Whitespace handling tests."""

    def test_strip_leading_whitespace(self) -> None:
        """Leading whitespace should be stripped."""
        result = normalize("  rettx-8GZ4-MK3P-2Q9A")
        assert result == "rettx-8GZ4-MK3P-2Q9A"

    def test_strip_trailing_whitespace(self) -> None:
        """Trailing whitespace should be stripped."""
        result = normalize("rettx-8GZ4-MK3P-2Q9A  ")
        assert result == "rettx-8GZ4-MK3P-2Q9A"

    def test_strip_both_whitespace(self) -> None:
        """Both leading and trailing whitespace should be stripped."""
        result = normalize("  rettx-8GZ4-MK3P-2Q9A  ")
        assert result == "rettx-8GZ4-MK3P-2Q9A"

    def test_strip_tabs_and_newlines(self) -> None:
        """Tabs and newlines should be stripped."""
        result = normalize("\t\nrettx-8GZ4-MK3P-2Q9A\n\t")
        assert result == "rettx-8GZ4-MK3P-2Q9A"


class TestNormalizeDashInsertion:
    """Dash insertion tests."""

    def test_insert_dashes_when_missing(self) -> None:
        """Dashes should be inserted when missing."""
        result = normalize("rettx8GZ4MK3P2Q9A")
        assert result == "rettx-8GZ4-MK3P-2Q9A"

    def test_insert_dashes_lowercase(self) -> None:
        """Dashes should be inserted and case normalized."""
        result = normalize("rettx8gz4mk3p2q9a")
        assert result == "rettx-8GZ4-MK3P-2Q9A"

    def test_spaces_instead_of_dashes(self) -> None:
        """Spaces should be converted to proper dashes."""
        result = normalize("rettx 8GZ4 MK3P 2Q9A")
        assert result == "rettx-8GZ4-MK3P-2Q9A"

    def test_mixed_separators(self) -> None:
        """Mixed dashes and spaces should be normalized."""
        result = normalize("rettx-8GZ4 MK3P-2Q9A")
        assert result == "rettx-8GZ4-MK3P-2Q9A"


class TestNormalizeIdempotence:
    """Idempotence tests."""

    def test_idempotent_canonical(self) -> None:
        """Normalizing a canonical ID should be idempotent."""
        canonical = "rettx-8GZ4-MK3P-2Q9A"
        assert normalize(normalize(canonical)) == normalize(canonical)

    def test_idempotent_lowercase(self) -> None:
        """Normalizing twice should equal normalizing once."""
        lowercase = "rettx-8gz4-mk3p-2q9a"
        assert normalize(normalize(lowercase)) == normalize(lowercase)

    def test_idempotent_no_dashes(self) -> None:
        """Normalizing dashless input twice should equal once."""
        no_dashes = "rettx8GZ4MK3P2Q9A"
        assert normalize(normalize(no_dashes)) == normalize(no_dashes)


class TestNormalizeAllSafeChars:
    """Test all safe alphabet characters normalize correctly."""

    def test_all_digits_in_safe_alphabet(self) -> None:
        """All digits from safe alphabet should normalize."""
        # Use only safe digits: 2-9
        result = normalize("rettx-2345-6789-2345")
        assert result == "rettx-2345-6789-2345"

    def test_all_letters_in_safe_alphabet(self) -> None:
        """All letters from safe alphabet should normalize."""
        # Use only safe letters
        result = normalize("rettx-ABCD-EFGH-JKMN")
        assert result == "rettx-ABCD-EFGH-JKMN"

    def test_lowercase_letters_normalized(self) -> None:
        """Lowercase safe letters should normalize to uppercase."""
        result = normalize("rettx-abcd-efgh-jkmn")
        assert result == "rettx-ABCD-EFGH-JKMN"


# =============================================================================
# ERROR TESTS (T025)
# =============================================================================


class TestNormalizeValueError:
    """ValueError tests for invalid input."""

    def test_empty_string_raises(self) -> None:
        """Empty string should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize("")

    def test_whitespace_only_raises(self) -> None:
        """Whitespace-only string should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize("   ")

    def test_wrong_prefix_raises(self) -> None:
        """Wrong prefix should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize("rtx-8GZ4-MK3P-2Q9A")

    def test_no_prefix_raises(self) -> None:
        """Missing prefix should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize("8GZ4-MK3P-2Q9A")

    def test_too_short_raises(self) -> None:
        """Too short input should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize("rettx-8GZ4-MK3P")

    def test_too_long_raises(self) -> None:
        """Too long input should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize("rettx-8GZ4-MK3P-2Q9A-XXXX")

    def test_invalid_string_raises(self) -> None:
        """Completely invalid string should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize("invalid")

    def test_prefix_only_raises(self) -> None:
        """Prefix-only input should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize("rettx-")


class TestNormalizeExcludedChars:
    """Tests for excluded characters."""

    @pytest.mark.parametrize("excluded_char", list(EXCLUDED_CHARS))
    def test_excluded_char_raises(self, excluded_char: str) -> None:
        """Each excluded character should raise ValueError."""
        test_input = f"rettx-{excluded_char}GZ4-MK3P-2Q9A"
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize(test_input)

    @pytest.mark.parametrize(
        "excluded_char", [c.lower() for c in EXCLUDED_CHARS if c.isalpha()]
    )
    def test_lowercase_excluded_char_raises(self, excluded_char: str) -> None:
        """Lowercase excluded characters should also raise ValueError."""
        test_input = f"rettx-{excluded_char}gz4-mk3p-2q9a"
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize(test_input)

    def test_zero_raises(self) -> None:
        """Zero (0) should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize("rettx-0GZ4-MK3P-2Q9A")

    def test_one_raises(self) -> None:
        """One (1) should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize("rettx-1GZ4-MK3P-2Q9A")

    def test_letter_o_raises(self) -> None:
        """Letter O should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize("rettx-OGZ4-MK3P-2Q9A")

    def test_letter_i_raises(self) -> None:
        """Letter I should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize("rettx-IGZ4-MK3P-2Q9A")

    def test_letter_l_raises(self) -> None:
        """Letter L should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize("rettx-LGZ4-MK3P-2Q9A")

    def test_letter_s_raises(self) -> None:
        """Letter S should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize("rettx-SGZ4-MK3P-2Q9A")


class TestNormalizeSpecialChars:
    """Tests for special characters."""

    def test_unicode_raises(self) -> None:
        """Unicode characters should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize("rettx-8GZ4-MK3P-2Q9日")

    def test_emoji_raises(self) -> None:
        """Emoji should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize("rettx-8GZ4-MK3P-2Q9🎉")

    def test_special_punctuation_raises(self) -> None:
        """Special punctuation should raise ValueError."""
        with pytest.raises(ValueError, match="Invalid rettX ID"):
            normalize("rettx-8GZ4-MK3P-2Q9!")


class TestNormalizeTypeError:
    """TypeError tests for non-string input."""

    def test_none_raises_type_error(self) -> None:
        """None should raise TypeError."""
        with pytest.raises(TypeError):
            normalize(None)  # type: ignore[arg-type]

    def test_integer_raises_type_error(self) -> None:
        """Integer should raise TypeError."""
        with pytest.raises(TypeError):
            normalize(12345)  # type: ignore[arg-type]

    def test_list_raises_type_error(self) -> None:
        """List should raise TypeError."""
        with pytest.raises(TypeError):
            normalize(["rettx-8GZ4-MK3P-2Q9A"])  # type: ignore[arg-type]

    def test_dict_raises_type_error(self) -> None:
        """Dict should raise TypeError."""
        with pytest.raises(TypeError):
            normalize({"id": "rettx-8GZ4-MK3P-2Q9A"})  # type: ignore[arg-type]

    def test_bytes_raises_type_error(self) -> None:
        """Bytes should raise TypeError."""
        with pytest.raises(TypeError):
            normalize(b"rettx-8GZ4-MK3P-2Q9A")  # type: ignore[arg-type]

    def test_float_raises_type_error(self) -> None:
        """Float should raise TypeError."""
        with pytest.raises(TypeError):
            normalize(3.14)  # type: ignore[arg-type]

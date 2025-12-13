"""Tests for rettX ID validation."""

from rettxid import validate_format
from rettxid._alphabet import SAFE_ALPHABET


class TestValidateFormat:
    """Tests for validate_format() function."""

    def test_returns_bool(self) -> None:
        """validate_format should return a boolean."""
        result = validate_format("rettx-8GZ4-MK3P-2Q9A")
        assert isinstance(result, bool)

    def test_valid_id_returns_true(self) -> None:
        """A correctly formatted rettX ID should return True."""
        assert validate_format("rettx-8GZ4-MK3P-2Q9A") is True

    def test_valid_ids_from_fixture(self, valid_id_examples: list[str]) -> None:
        """All valid example IDs should return True."""
        for id_str in valid_id_examples:
            assert validate_format(id_str) is True, f"Expected True for {id_str}"

    def test_invalid_ids_from_fixture(self, invalid_id_examples: list[str]) -> None:
        """All invalid example IDs should return False."""
        for id_str in invalid_id_examples:
            assert validate_format(id_str) is False, f"Expected False for {id_str}"


class TestValidateFormatPrefix:
    """Tests for prefix validation."""

    def test_missing_prefix_returns_false(self) -> None:
        """ID without prefix should return False."""
        assert validate_format("8GZ4-MK3P-2Q9A") is False

    def test_uppercase_prefix_returns_false(self) -> None:
        """ID with uppercase prefix should return False."""
        assert validate_format("RETTX-8GZ4-MK3P-2Q9A") is False

    def test_wrong_prefix_returns_false(self) -> None:
        """ID with wrong prefix should return False."""
        assert validate_format("rtx-8GZ4-MK3P-2Q9A") is False
        assert validate_format("rett-8GZ4-MK3P-2Q9A") is False
        assert validate_format("prefix-8GZ4-MK3P-2Q9A") is False

    def test_prefix_only_returns_false(self) -> None:
        """Prefix alone should return False."""
        assert validate_format("rettx-") is False
        assert validate_format("rettx") is False


class TestValidateFormatBody:
    """Tests for body validation."""

    def test_lowercase_body_returns_false(self) -> None:
        """ID with lowercase body should return False."""
        assert validate_format("rettx-8gz4-mk3p-2q9a") is False
        assert validate_format("rettx-8GZ4-mk3p-2Q9A") is False  # Mixed

    def test_invalid_characters_return_false(self) -> None:
        """ID with excluded characters should return False."""
        # 0 (zero)
        assert validate_format("rettx-8G04-MK3P-2Q9A") is False
        # 1 (one)
        assert validate_format("rettx-8G14-MK3P-2Q9A") is False
        # I (letter I)
        assert validate_format("rettx-8GI4-MK3P-2Q9A") is False
        # L (letter L)
        assert validate_format("rettx-8GL4-MK3P-2Q9A") is False
        # O (letter O)
        assert validate_format("rettx-8GO4-MK3P-2Q9A") is False
        # S (letter S)
        assert validate_format("rettx-8GS4-MK3P-2Q9A") is False

    def test_all_safe_alphabet_chars_valid(self) -> None:
        """IDs using all safe alphabet characters should be valid."""
        # Build a valid ID using first 12 chars of safe alphabet
        chars = SAFE_ALPHABET[:12]
        test_id = f"rettx-{chars[:4]}-{chars[4:8]}-{chars[8:12]}"
        assert validate_format(test_id) is True


class TestValidateFormatLength:
    """Tests for length validation."""

    def test_wrong_length_returns_false(self) -> None:
        """ID with wrong length should return False."""
        # Too short
        assert validate_format("rettx-8GZ4-MK3P") is False
        # Too long
        assert validate_format("rettx-8GZ4-MK3P-2Q9A-XXXX") is False

    def test_correct_length_is_20(self) -> None:
        """Valid ID should be exactly 20 characters."""
        valid_id = "rettx-8GZ4-MK3P-2Q9A"
        assert len(valid_id) == 20
        assert validate_format(valid_id) is True


class TestValidateFormatGrouping:
    """Tests for grouping validation."""

    def test_missing_dashes_returns_false(self) -> None:
        """ID without dashes should return False."""
        assert validate_format("rettx8GZ4MK3P2Q9A") is False

    def test_wrong_grouping_returns_false(self) -> None:
        """ID with wrong grouping should return False."""
        assert validate_format("rettx-8GZ4MK3P-2Q9A") is False
        assert validate_format("rettx-8GZ-4MK3P-2Q9A") is False
        assert validate_format("rettx-8GZ4-MK-3P2Q9A") is False

    def test_extra_dashes_returns_false(self) -> None:
        """ID with extra dashes should return False."""
        assert validate_format("rettx--8GZ4-MK3P-2Q9A") is False
        assert validate_format("rettx-8GZ4--MK3P-2Q9A") is False


class TestValidateFormatEmptyAndNone:
    """Tests for empty and None input."""

    def test_empty_string_returns_false(self) -> None:
        """Empty string should return False."""
        assert validate_format("") is False

    def test_none_returns_false(self) -> None:
        """None should return False (not raise)."""
        assert validate_format(None) is False  # type: ignore[arg-type]

    def test_whitespace_only_returns_false(self) -> None:
        """Whitespace-only string should return False."""
        assert validate_format("   ") is False
        assert validate_format("\t\n") is False


class TestValidateFormatNonString:
    """Tests for non-string input handling."""

    def test_integer_returns_false(self) -> None:
        """Integer input should return False."""
        assert validate_format(12345) is False  # type: ignore[arg-type]

    def test_list_returns_false(self) -> None:
        """List input should return False."""
        assert validate_format(["rettx-8GZ4-MK3P-2Q9A"]) is False  # type: ignore[arg-type]

    def test_dict_returns_false(self) -> None:
        """Dict input should return False."""
        assert validate_format({"id": "rettx-8GZ4-MK3P-2Q9A"}) is False  # type: ignore[arg-type]

    def test_bytes_returns_false(self) -> None:
        """Bytes input should return False."""
        assert validate_format(b"rettx-8GZ4-MK3P-2Q9A") is False  # type: ignore[arg-type]

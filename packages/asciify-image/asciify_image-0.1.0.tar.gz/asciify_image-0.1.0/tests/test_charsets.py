"""Tests for character sets."""

import pytest

from asciify.charsets import CHARSETS, get_charset


class TestCharsets:
    """Test character set functionality."""

    def test_all_charsets_exist(self) -> None:
        """Verify all expected charsets are defined."""
        expected = {"simple", "complex", "blocks", "symbols"}
        assert set(CHARSETS.keys()) == expected

    def test_charsets_not_empty(self) -> None:
        """Verify all charsets have characters."""
        for name, charset in CHARSETS.items():
            assert len(charset) > 0, f"Charset '{name}' is empty"

    def test_get_charset_valid(self) -> None:
        """Test getting valid charsets."""
        for name in CHARSETS:
            result = get_charset(name)
            assert result == CHARSETS[name]

    def test_get_charset_invalid(self) -> None:
        """Test getting invalid charset raises ValueError."""
        with pytest.raises(ValueError, match="Unknown charset"):
            get_charset("nonexistent")

    def test_simple_charset_contents(self) -> None:
        """Verify simple charset has expected characters."""
        simple = get_charset("simple")
        assert " " in simple  # Should have space for darkest
        assert "@" in simple  # Should have @ for lightest

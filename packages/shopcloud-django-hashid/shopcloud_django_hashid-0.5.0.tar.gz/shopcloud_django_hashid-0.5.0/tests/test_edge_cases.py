"""Edge case tests for HashidField.

Tests for boundary values and error conditions.
"""

import pytest

from hashid_field import BigHashidField, HashidField

# Maximum value for a signed 64-bit integer, used by BigIntegerField
MAX_SIGNED_BIGINT = (2**63) - 1
# Maximum value for a signed 32-bit integer, used by IntegerField
MAX_SIGNED_INT = (2**31) - 1


class TestEdgeCases:
    """Test edge cases and boundary values."""

    def test_max_bigint_value(self):
        """Test with MAX_SIGNED_BIGINT (2^63 - 1)."""
        field = BigHashidField()

        encoded = field.encode_id(MAX_SIGNED_BIGINT)
        decoded = field.decode_id(str(encoded))

        assert decoded == MAX_SIGNED_BIGINT

    def test_max_int_value(self):
        """Test with MAX_SIGNED_INT (2^31 - 1)."""
        field = HashidField()

        encoded = field.encode_id(MAX_SIGNED_INT)
        decoded = field.decode_id(str(encoded))

        assert decoded == MAX_SIGNED_INT

    def test_zero_value(self):
        """Test with ID = 0."""
        field = HashidField()
        encoded = field.encode_id(0)
        decoded = field.decode_id(str(encoded))
        assert decoded == 0

    def test_one_value(self):
        """Test with ID = 1."""
        field = HashidField()
        encoded = field.encode_id(1)
        decoded = field.decode_id(str(encoded))
        assert decoded == 1

    def test_empty_string_decode(self):
        """Empty string should raise ValueError."""
        field = HashidField()
        with pytest.raises(ValueError, match="Invalid hashid"):
            field.decode_id("")

    def test_invalid_hashid_decode(self):
        """Invalid hashid should raise ValueError."""
        field = HashidField()
        with pytest.raises(ValueError, match="Invalid hashid"):
            field.decode_id("invalid_hashid_string")

    def test_unicode_in_hashid(self):
        """Unicode characters should be rejected."""
        field = HashidField()
        with pytest.raises(ValueError, match="Invalid hashid"):
            field.decode_id("abc🔥def")

    def test_whitespace_hashid(self):
        """Whitespace-only hashid should be rejected."""
        field = HashidField()
        with pytest.raises(ValueError, match="Invalid hashid"):
            field.decode_id("   ")

    def test_special_characters_hashid(self):
        """Special characters should be rejected."""
        field = HashidField()
        with pytest.raises(ValueError, match="Invalid hashid"):
            field.decode_id("abc!@#def")

    def test_consistent_encoding(self):
        """Same value should always encode to same hashid."""
        field = HashidField(salt="test-salt")

        encoded1 = str(field.encode_id(42))
        encoded2 = str(field.encode_id(42))
        encoded3 = str(field.encode_id(42))

        assert encoded1 == encoded2 == encoded3

    def test_different_salts_different_hashids(self):
        """Different salts should produce different hashids."""
        field1 = HashidField(salt="salt-one")
        field2 = HashidField(salt="salt-two")

        encoded1 = str(field1.encode_id(42))
        encoded2 = str(field2.encode_id(42))

        assert encoded1 != encoded2

    def test_min_length_respected(self):
        """Minimum length parameter should be respected."""
        field = HashidField(min_length=15)
        encoded = str(field.encode_id(1))
        assert len(encoded) >= 15

    def test_prefix_handling(self):
        """Prefix should be correctly added and removed."""
        field = HashidField(prefix="pre_")

        encoded = str(field.encode_id(42))
        assert encoded.startswith("pre_")

        # Decode should work with prefix
        decoded = field.decode_id(encoded)
        assert decoded == 42

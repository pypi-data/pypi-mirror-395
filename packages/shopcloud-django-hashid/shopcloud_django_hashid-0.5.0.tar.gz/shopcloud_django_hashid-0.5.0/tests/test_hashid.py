"""Unit tests for Hashid class.

Tests for:
- T008: encoding/decoding
- T009: operators (__eq__, __int__, __str__, __hash__)
- T010: pickling (__getstate__, __setstate__)
"""

import pickle

import pytest


class TestHashidEncodingDecoding:
    """T008: Tests for Hashid class encoding and decoding."""

    def test_create_from_integer(self):
        """Hashid can be created from an integer."""
        from hashid_field.hashid import Hashid

        h = Hashid(123, salt="test-salt")
        assert h.id == 123
        assert isinstance(h.hashid, str)
        assert len(h.hashid) >= 1

    def test_create_from_hashid_string(self):
        """Hashid can be created from a hashid string."""
        from hashid_field.hashid import Hashid

        # First create a hashid to get the string
        h1 = Hashid(456, salt="test-salt")
        hashid_str = h1.hashid

        # Then create another from the string
        h2 = Hashid(hashid_str, salt="test-salt")
        assert h2.id == 456
        assert h2.hashid == hashid_str

    def test_same_salt_produces_same_hashid(self):
        """Same integer with same salt produces same hashid."""
        from hashid_field.hashid import Hashid

        h1 = Hashid(789, salt="same-salt")
        h2 = Hashid(789, salt="same-salt")
        assert h1.hashid == h2.hashid

    def test_different_salt_produces_different_hashid(self):
        """Same integer with different salt produces different hashid."""
        from hashid_field.hashid import Hashid

        h1 = Hashid(789, salt="salt-one")
        h2 = Hashid(789, salt="salt-two")
        assert h1.hashid != h2.hashid

    def test_min_length_respected(self):
        """Hashid respects minimum length parameter."""
        from hashid_field.hashid import Hashid

        h = Hashid(1, salt="test", min_length=10)
        assert len(h.hashid) >= 10

    def test_custom_alphabet(self):
        """Hashid uses custom alphabet when provided."""
        from hashid_field.hashid import Hashid

        alphabet = "abcdef1234567890"
        h = Hashid(123, salt="test", alphabet=alphabet)
        for char in h.hashid:
            assert char in alphabet

    def test_prefix_added(self):
        """Hashid adds prefix when provided."""
        from hashid_field.hashid import Hashid

        h = Hashid(123, salt="test", prefix="prefix_")
        assert h.hashid.startswith("prefix_")
        assert h.prefix == "prefix_"

    def test_invalid_hashid_raises_error(self):
        """Invalid hashid string raises ValueError."""
        from hashid_field.hashid import Hashid

        with pytest.raises(ValueError):
            Hashid("invalid-hashid-string", salt="test-salt")

    def test_negative_integer_raises_error(self):
        """Negative integer raises ValueError."""
        from hashid_field.hashid import Hashid

        with pytest.raises(ValueError):
            Hashid(-1, salt="test-salt")

    def test_zero_is_valid(self):
        """Zero is a valid integer value."""
        from hashid_field.hashid import Hashid

        h = Hashid(0, salt="test-salt")
        assert h.id == 0


class TestHashidOperators:
    """T009: Tests for Hashid operators."""

    def test_equality_same_id(self):
        """Two Hashids with same id are equal."""
        from hashid_field.hashid import Hashid

        h1 = Hashid(100, salt="salt")
        h2 = Hashid(100, salt="salt")
        assert h1 == h2

    def test_equality_different_salt_same_id(self):
        """Hashids with same id but different salt are equal."""
        from hashid_field.hashid import Hashid

        h1 = Hashid(100, salt="salt1")
        h2 = Hashid(100, salt="salt2")
        assert h1 == h2  # Equal because same underlying id

    def test_equality_with_integer(self):
        """Hashid equals its integer value."""
        from hashid_field.hashid import Hashid

        h = Hashid(42, salt="test")
        assert h == 42
        assert 42 == h

    def test_equality_with_string(self):
        """Hashid equals its hashid string."""
        from hashid_field.hashid import Hashid

        h = Hashid(42, salt="test")
        assert h == h.hashid
        assert h.hashid == h

    def test_inequality(self):
        """Two Hashids with different ids are not equal."""
        from hashid_field.hashid import Hashid

        h1 = Hashid(100, salt="salt")
        h2 = Hashid(200, salt="salt")
        assert h1 != h2

    def test_int_conversion(self):
        """int() returns the underlying integer."""
        from hashid_field.hashid import Hashid

        h = Hashid(999, salt="test")
        assert int(h) == 999

    def test_str_conversion(self):
        """str() returns the hashid string."""
        from hashid_field.hashid import Hashid

        h = Hashid(123, salt="test")
        assert str(h) == h.hashid
        assert isinstance(str(h), str)

    def test_repr(self):
        """repr() returns a useful representation."""
        from hashid_field.hashid import Hashid

        h = Hashid(123, salt="test")
        r = repr(h)
        assert "Hashid" in r
        assert h.hashid in r

    def test_hash_for_dict_key(self):
        """Hashid can be used as dictionary key."""
        from hashid_field.hashid import Hashid

        h = Hashid(123, salt="test")
        d = {h: "value"}
        assert d[h] == "value"
        # Also works with same id different object
        h2 = Hashid(123, salt="test")
        assert d[h2] == "value"

    def test_hash_in_set(self):
        """Hashid can be used in sets."""
        from hashid_field.hashid import Hashid

        h1 = Hashid(1, salt="test")
        h2 = Hashid(2, salt="test")
        h3 = Hashid(1, salt="test")  # Same as h1

        s = {h1, h2, h3}
        assert len(s) == 2

    def test_comparison_operators(self):
        """Comparison operators work with integers."""
        from hashid_field.hashid import Hashid

        h = Hashid(50, salt="test")
        assert h < 100
        assert h <= 50
        assert h <= 100
        assert h > 10
        assert h >= 50
        assert h >= 10

    def test_arithmetic_add(self):
        """Addition works with Hashid."""
        from hashid_field.hashid import Hashid

        h = Hashid(10, salt="test")
        assert h + 5 == 15
        assert 5 + h == 15

    def test_arithmetic_sub(self):
        """Subtraction works with Hashid."""
        from hashid_field.hashid import Hashid

        h = Hashid(10, salt="test")
        assert h - 3 == 7
        assert 20 - h == 10

    def test_arithmetic_mul(self):
        """Multiplication works with Hashid."""
        from hashid_field.hashid import Hashid

        h = Hashid(5, salt="test")
        assert h * 3 == 15
        assert 3 * h == 15

    def test_len(self):
        """len() returns length of hashid string."""
        from hashid_field.hashid import Hashid

        h = Hashid(123, salt="test", min_length=10)
        assert len(h) >= 10


class TestHashidPickling:
    """T010: Tests for Hashid pickling support."""

    def test_pickle_roundtrip(self):
        """Hashid survives pickle roundtrip."""
        from hashid_field.hashid import Hashid

        h = Hashid(12345, salt="pickle-test", min_length=8)
        pickled = pickle.dumps(h)
        unpickled = pickle.loads(pickled)

        assert unpickled.id == h.id
        assert unpickled.hashid == h.hashid

    def test_pickle_preserves_prefix(self):
        """Pickle preserves prefix."""
        from hashid_field.hashid import Hashid

        h = Hashid(100, salt="test", prefix="pk_")
        unpickled = pickle.loads(pickle.dumps(h))
        assert unpickled.prefix == "pk_"
        assert unpickled.hashid.startswith("pk_")

    def test_getstate(self):
        """__getstate__ returns serializable dict."""
        from hashid_field.hashid import Hashid

        h = Hashid(42, salt="test", min_length=5, prefix="x_")
        state = h.__getstate__()

        assert isinstance(state, dict)
        assert "id" in state or "_id" in state

    def test_setstate(self):
        """__setstate__ restores object from state."""
        from hashid_field.hashid import Hashid

        h1 = Hashid(42, salt="test", min_length=5)
        state = h1.__getstate__()

        h2 = Hashid.__new__(Hashid)
        h2.__setstate__(state)

        assert h2.id == 42

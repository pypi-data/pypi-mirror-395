"""Tests for migration compatibility.

Tests for T024: Migration deconstruct() and compatibility.
"""

from hashid_field import (
    BigHashidAutoField,
    BigHashidField,
    HashidAutoField,
    HashidField,
)
from hashid_field.conf import app_settings


class TestFieldDeconstruct:
    """T024: Tests for field deconstruct() method."""

    def test_hashid_field_deconstruct_path(self):
        """HashidField deconstructs with correct path."""
        field = HashidField()
        field.set_attributes_from_name("test_field")

        name, path, args, kwargs = field.deconstruct()

        assert path == "hashid_field.HashidField"

    def test_big_hashid_field_deconstruct_path(self):
        """BigHashidField deconstructs with correct path."""
        field = BigHashidField()
        field.set_attributes_from_name("test_field")

        name, path, args, kwargs = field.deconstruct()

        assert path == "hashid_field.BigHashidField"

    def test_hashid_auto_field_deconstruct_path(self):
        """HashidAutoField deconstructs with correct path."""
        field = HashidAutoField()
        field.set_attributes_from_name("test_field")

        name, path, args, kwargs = field.deconstruct()

        assert path == "hashid_field.HashidAutoField"

    def test_big_hashid_auto_field_deconstruct_path(self):
        """BigHashidAutoField deconstructs with correct path."""
        field = BigHashidAutoField()
        field.set_attributes_from_name("test_field")

        name, path, args, kwargs = field.deconstruct()

        assert path == "hashid_field.BigHashidAutoField"

    def test_deconstruct_excludes_defaults(self):
        """Deconstruct excludes default values."""
        field = HashidField()
        field.set_attributes_from_name("test_field")

        name, path, args, kwargs = field.deconstruct()

        # Default values should not be in kwargs
        assert "salt" not in kwargs or kwargs["salt"] != app_settings.salt
        assert (
            "min_length" not in kwargs
            or kwargs["min_length"] != app_settings.min_length
        )

    def test_deconstruct_includes_custom_salt(self):
        """Deconstruct includes custom salt."""
        field = HashidField(salt="custom-salt")
        field.set_attributes_from_name("test_field")

        name, path, args, kwargs = field.deconstruct()

        assert kwargs.get("salt") == "custom-salt"

    def test_deconstruct_includes_custom_min_length(self):
        """Deconstruct includes custom min_length."""
        field = HashidField(min_length=15)
        field.set_attributes_from_name("test_field")

        name, path, args, kwargs = field.deconstruct()

        assert kwargs.get("min_length") == 15

    def test_deconstruct_includes_custom_alphabet(self):
        """Deconstruct includes custom alphabet."""
        custom_alphabet = "abcdef1234567890"
        field = HashidField(alphabet=custom_alphabet)
        field.set_attributes_from_name("test_field")

        name, path, args, kwargs = field.deconstruct()

        assert kwargs.get("alphabet") == custom_alphabet

    def test_deconstruct_includes_prefix(self):
        """Deconstruct includes prefix when set."""
        field = HashidField(prefix="pk_")
        field.set_attributes_from_name("test_field")

        name, path, args, kwargs = field.deconstruct()

        assert kwargs.get("prefix") == "pk_"

    def test_deconstruct_preserves_standard_field_kwargs(self):
        """Deconstruct preserves standard Django field kwargs."""
        field = HashidField(null=True, blank=True, db_index=True)
        field.set_attributes_from_name("test_field")

        name, path, args, kwargs = field.deconstruct()

        assert kwargs.get("null") is True
        assert kwargs.get("blank") is True
        assert kwargs.get("db_index") is True

    def test_auto_field_deconstruct_includes_primary_key(self):
        """HashidAutoField deconstruct includes primary_key=True."""
        field = HashidAutoField()
        field.set_attributes_from_name("test_field")

        name, path, args, kwargs = field.deconstruct()

        # primary_key should be included as it's a required attribute
        # (Django's AutoField always has primary_key=True)
        assert field.primary_key is True


class TestMigrationCompatibility:
    """Tests for migration compatibility with original django-hashid-field."""

    def test_field_can_be_reconstructed(self):
        """Field can be reconstructed from deconstruct output."""
        original = HashidField(salt="test", min_length=10, prefix="x_")
        original.set_attributes_from_name("test_field")

        name, path, args, kwargs = original.deconstruct()

        # Reconstruct the field
        reconstructed = HashidField(*args, **kwargs)

        assert reconstructed.salt == original.salt
        assert reconstructed.min_length == original.min_length
        assert reconstructed.prefix == original.prefix

    def test_auto_field_can_be_reconstructed(self):
        """Auto field can be reconstructed from deconstruct output."""
        original = HashidAutoField(salt="test", min_length=12)
        original.set_attributes_from_name("id")

        name, path, args, kwargs = original.deconstruct()

        # Reconstruct the field
        reconstructed = HashidAutoField(*args, **kwargs)

        assert reconstructed.salt == original.salt
        assert reconstructed.min_length == original.min_length
        assert reconstructed.primary_key is True

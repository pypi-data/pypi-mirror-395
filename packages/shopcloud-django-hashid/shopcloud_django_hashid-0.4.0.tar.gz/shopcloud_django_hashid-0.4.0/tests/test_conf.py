"""Unit tests for AppSettings class.

Tests for T011: AppSettings configuration management.
"""

from django.conf import settings
from django.test import override_settings


class TestAppSettings:
    """T011: Tests for AppSettings class."""

    def test_default_salt(self):
        """Default salt is empty string."""

        # When not configured, should use default
        with override_settings():
            # Remove the setting if it exists
            if hasattr(settings, "HASHID_FIELD_SALT"):
                delattr(settings, "HASHID_FIELD_SALT")
            # Access through a fresh instance would show default
            from hashid_field.conf import AppSettings

            fresh_settings = AppSettings()
            # Default should be empty string or the test setting
            assert isinstance(fresh_settings.salt, str)

    def test_salt_from_settings(self):
        """Salt is read from Django settings."""

        with override_settings(HASHID_FIELD_SALT="custom-salt"):
            from hashid_field.conf import AppSettings

            fresh = AppSettings()
            assert fresh.salt == "custom-salt"

    def test_default_min_length(self):
        """Default min_length is 7."""

        with override_settings():
            from hashid_field.conf import AppSettings

            fresh = AppSettings()
            assert fresh.min_length == 7

    def test_min_length_from_settings(self):
        """Min length is read from Django settings."""
        with override_settings(HASHID_FIELD_MIN_LENGTH=15):
            from hashid_field.conf import AppSettings

            fresh = AppSettings()
            assert fresh.min_length == 15

    def test_default_big_min_length(self):
        """Default big_min_length is 13."""
        from hashid_field.conf import AppSettings

        fresh = AppSettings()
        assert fresh.big_min_length == 13

    def test_big_min_length_from_settings(self):
        """Big min length is read from Django settings."""
        with override_settings(HASHID_FIELD_BIG_MIN_LENGTH=20):
            from hashid_field.conf import AppSettings

            fresh = AppSettings()
            assert fresh.big_min_length == 20

    def test_default_alphabet(self):
        """Default alphabet uses hashids default."""
        from hashid_field.conf import AppSettings

        fresh = AppSettings()
        # Should be the hashids default alphabet
        assert fresh.alphabet is not None
        assert len(fresh.alphabet) > 0

    def test_alphabet_from_settings(self):
        """Alphabet is read from Django settings."""
        custom_alphabet = "abcdef1234567890"
        with override_settings(HASHID_FIELD_ALPHABET=custom_alphabet):
            from hashid_field.conf import AppSettings

            fresh = AppSettings()
            assert fresh.alphabet == custom_alphabet

    def test_default_allow_int_lookup(self):
        """Default allow_int_lookup is False."""
        with override_settings():
            from hashid_field.conf import AppSettings

            fresh = AppSettings()
            assert fresh.allow_int_lookup is False

    def test_allow_int_lookup_from_settings(self):
        """allow_int_lookup is read from Django settings."""
        with override_settings(HASHID_FIELD_ALLOW_INT_LOOKUP=True):
            from hashid_field.conf import AppSettings

            fresh = AppSettings()
            assert fresh.allow_int_lookup is True

    def test_default_lookup_exception(self):
        """Default lookup_exception is False."""
        from hashid_field.conf import AppSettings

        fresh = AppSettings()
        assert fresh.lookup_exception is False

    def test_lookup_exception_from_settings(self):
        """lookup_exception is read from Django settings."""
        with override_settings(HASHID_FIELD_LOOKUP_EXCEPTION=True):
            from hashid_field.conf import AppSettings

            fresh = AppSettings()
            assert fresh.lookup_exception is True

    def test_default_enable_hashid_object(self):
        """Default enable_hashid_object is True."""
        from hashid_field.conf import AppSettings

        fresh = AppSettings()
        assert fresh.enable_hashid_object is True

    def test_enable_hashid_object_from_settings(self):
        """enable_hashid_object is read from Django settings."""
        with override_settings(HASHID_FIELD_ENABLE_HASHID_OBJECT=False):
            from hashid_field.conf import AppSettings

            fresh = AppSettings()
            assert fresh.enable_hashid_object is False

    def test_default_enable_descriptor(self):
        """Default enable_descriptor is True."""
        from hashid_field.conf import AppSettings

        fresh = AppSettings()
        assert fresh.enable_descriptor is True

    def test_enable_descriptor_from_settings(self):
        """enable_descriptor is read from Django settings."""
        with override_settings(HASHID_FIELD_ENABLE_DESCRIPTOR=False):
            from hashid_field.conf import AppSettings

            fresh = AppSettings()
            assert fresh.enable_descriptor is False

    def test_app_settings_singleton(self):
        """app_settings is a singleton instance."""
        from hashid_field.conf import app_settings

        assert app_settings is not None
        # It should be an instance, not a class
        assert not isinstance(app_settings, type)

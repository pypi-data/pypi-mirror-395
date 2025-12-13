"""Configuration management for hashid_field.

Provides access to Django settings with sensible defaults.
"""

from __future__ import annotations

from django.conf import settings
from hashids import Hashids


class AppSettings:
    """Access Django settings with defaults for hashid_field.

    Settings:
        HASHID_FIELD_SALT: Global salt for encoding (default: "")
        HASHID_FIELD_MIN_LENGTH: Minimum hashid length (default: 7)
        HASHID_FIELD_BIG_MIN_LENGTH: Minimum length for BigHashidField (default: 13)
        HASHID_FIELD_ALPHABET: Character set for encoding (default: hashids default)
        HASHID_FIELD_ALLOW_INT_LOOKUP: Allow integer-based queries (default: False)
        HASHID_FIELD_LOOKUP_EXCEPTION: Raise on invalid lookups (default: False)
        HASHID_FIELD_ENABLE_HASHID_OBJECT: Return Hashid objects (default: True)
        HASHID_FIELD_ENABLE_DESCRIPTOR: Use descriptor for access (default: True)
    """

    # Default values
    DEFAULTS = {
        "salt": "",
        "min_length": 7,
        "big_min_length": 13,
        "alphabet": Hashids.ALPHABET,
        "allow_int_lookup": False,
        "lookup_exception": False,
        "enable_hashid_object": True,
        "enable_descriptor": True,
    }

    @property
    def salt(self) -> str:
        """Get the global salt for hashid encoding."""
        return getattr(settings, "HASHID_FIELD_SALT", self.DEFAULTS["salt"])

    @property
    def min_length(self) -> int:
        """Get the minimum hashid length."""
        return getattr(settings, "HASHID_FIELD_MIN_LENGTH", self.DEFAULTS["min_length"])

    @property
    def big_min_length(self) -> int:
        """Get the minimum hashid length for BigHashidField."""
        return getattr(
            settings, "HASHID_FIELD_BIG_MIN_LENGTH", self.DEFAULTS["big_min_length"]
        )

    @property
    def alphabet(self) -> str:
        """Get the alphabet for hashid encoding."""
        return getattr(settings, "HASHID_FIELD_ALPHABET", self.DEFAULTS["alphabet"])

    @property
    def allow_int_lookup(self) -> bool:
        """Check if integer-based lookups are allowed."""
        return getattr(
            settings, "HASHID_FIELD_ALLOW_INT_LOOKUP", self.DEFAULTS["allow_int_lookup"]
        )

    @property
    def lookup_exception(self) -> bool:
        """Check if exceptions should be raised on invalid lookups."""
        return getattr(
            settings, "HASHID_FIELD_LOOKUP_EXCEPTION", self.DEFAULTS["lookup_exception"]
        )

    @property
    def enable_hashid_object(self) -> bool:
        """Check if Hashid objects should be returned instead of strings."""
        return getattr(
            settings,
            "HASHID_FIELD_ENABLE_HASHID_OBJECT",
            self.DEFAULTS["enable_hashid_object"],
        )

    @property
    def enable_descriptor(self) -> bool:
        """Check if descriptor should be used for attribute access."""
        return getattr(
            settings,
            "HASHID_FIELD_ENABLE_DESCRIPTOR",
            self.DEFAULTS["enable_descriptor"],
        )


# Singleton instance
app_settings = AppSettings()

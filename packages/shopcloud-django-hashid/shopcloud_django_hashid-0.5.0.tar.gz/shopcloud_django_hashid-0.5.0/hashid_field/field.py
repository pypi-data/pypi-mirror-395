"""HashidField and BigHashidField implementations.

Django model fields that store integers in the database but represent
them as obfuscated hashid strings in Python.
"""

from __future__ import annotations

import logging
from typing import Any

from django import forms
from django.db import models
from hashids import Hashids

from hashid_field.conf import app_settings
from hashid_field.descriptor import HashidDescriptor
from hashid_field.hashid import Hashid
from hashid_field.lookups import register_lookups

logger = logging.getLogger(__name__)


class HashidFieldMixin:
    """Mixin providing hashid encoding/decoding logic for Django fields.

    Handles conversion between integer database values and Hashid Python objects.
    """

    # Field-specific parameters
    salt: str
    min_length: int
    alphabet: str
    prefix: str
    allow_int_lookup: bool
    enable_hashid_object: bool
    enable_descriptor: bool

    _hashids: Hashids | None = None

    def __init__(
        self,
        salt: str | None = None,
        min_length: int | None = None,
        alphabet: str | None = None,
        prefix: str = "",
        allow_int_lookup: bool | None = None,
        enable_hashid_object: bool | None = None,
        enable_descriptor: bool | None = None,
        **kwargs: Any,
    ) -> None:
        """Initialize the hashid field mixin.

        Args:
            salt: Salt for hashid encoding (default: from settings)
            min_length: Minimum hashid length (default: from settings)
            alphabet: Character set for encoding (default: from settings)
            prefix: Prefix for hashid strings
            allow_int_lookup: Allow integer-based queries (default: from settings)
            enable_hashid_object: Return Hashid objects (default: from settings)
            enable_descriptor: Use descriptor for access (default: from settings)
            **kwargs: Additional field arguments
        """
        self.salt = salt if salt is not None else app_settings.salt
        self.min_length = (
            min_length if min_length is not None else self._get_default_min_length()
        )
        self.alphabet = alphabet if alphabet is not None else app_settings.alphabet
        self.prefix = prefix
        self.allow_int_lookup = (
            allow_int_lookup
            if allow_int_lookup is not None
            else app_settings.allow_int_lookup
        )
        self.enable_hashid_object = (
            enable_hashid_object
            if enable_hashid_object is not None
            else app_settings.enable_hashid_object
        )
        self.enable_descriptor = (
            enable_descriptor
            if enable_descriptor is not None
            else app_settings.enable_descriptor
        )

        super().__init__(**kwargs)

    def _get_default_min_length(self) -> int:
        """Get the default minimum length. Override in BigHashidField."""
        return app_settings.min_length

    def get_hashids(self) -> Hashids:
        """Get or create the Hashids encoder instance."""
        if self._hashids is None:
            self._hashids = Hashids(
                salt=self.salt,
                min_length=self.min_length,
                alphabet=self.alphabet,
            )
        return self._hashids

    def encode_id(self, id_value: int) -> Hashid | str:
        """Encode an integer ID to a Hashid or string.

        Args:
            id_value: The integer ID to encode

        Returns:
            Hashid object or string depending on enable_hashid_object setting
        """
        logger.debug("Encoding ID %d to hashid", id_value)
        hashids = self.get_hashids()
        hashid = Hashid(
            id_value,
            salt=self.salt,
            min_length=self.min_length,
            alphabet=self.alphabet,
            prefix=self.prefix,
            hashids=hashids,
        )
        if self.enable_hashid_object:
            return hashid
        return str(hashid)

    def decode_id(self, hashid_value: str | Hashid) -> int:
        """Decode a hashid string or Hashid object to an integer.

        Args:
            hashid_value: The hashid string or Hashid to decode

        Returns:
            The decoded integer ID

        Raises:
            ValueError: If the hashid is invalid
        """
        logger.debug("Decoding hashid '%s' to ID", hashid_value)
        if isinstance(hashid_value, Hashid):
            return hashid_value.id

        hashids = self.get_hashids()

        # Remove prefix if present
        hashid_str = str(hashid_value)
        if self.prefix and hashid_str.startswith(self.prefix):
            hashid_str = hashid_str[len(self.prefix) :]

        decoded = hashids.decode(hashid_str)
        if not decoded:
            raise ValueError(f"Invalid hashid: {hashid_value}")
        return decoded[0]

    def contribute_to_class(self, cls: type, name: str, **kwargs: Any) -> None:
        """Add the descriptor to the model class."""
        super().contribute_to_class(cls, name, **kwargs)

        if self.enable_descriptor:
            setattr(cls, self.attname, HashidDescriptor(self))

    def get_prep_value(self, value: Any) -> int | None:
        """Prepare value for database storage.

        Args:
            value: The value to prepare (int, str, Hashid, or None)

        Returns:
            Integer for database storage, or None
        """
        if value is None:
            return None

        if isinstance(value, Hashid):
            return value.id

        if isinstance(value, int):
            return value

        if isinstance(value, str):
            try:
                return self.decode_id(value)
            except ValueError:
                logger.warning("Invalid hashid string in get_prep_value: %s", value)
                return None

        return super().get_prep_value(value)

    def from_db_value(
        self,
        value: Any,
        expression: Any,
        connection: Any,
    ) -> Hashid | str | None:
        """Convert database value to Python value.

        Args:
            value: The value from the database
            expression: The expression that produced the value
            connection: The database connection

        Returns:
            Hashid object, string, or None
        """
        if value is None:
            return None

        if isinstance(value, int):
            return self.encode_id(value)

        return value

    def to_python(self, value: Any) -> Hashid | int | None:
        """Convert value to Python representation.

        Args:
            value: The value to convert

        Returns:
            Hashid object or None
        """
        if value is None:
            return None

        if isinstance(value, Hashid):
            return value

        if isinstance(value, int):
            return self.encode_id(value)

        if isinstance(value, str):
            try:
                int_value = self.decode_id(value)
                return self.encode_id(int_value)
            except ValueError as err:
                raise ValueError(f"Invalid hashid: {value}") from err

        return value

    def deconstruct(self) -> tuple[str, str, list, dict]:
        """Return the field's deconstruction for migrations.

        Returns a tuple of (name, path, args, kwargs) that can be used
        to recreate the field.
        """
        name, path, args, kwargs = super().deconstruct()

        # Use the hashid_field path for migration compatibility
        if "HashidField" in self.__class__.__name__:
            if "Big" in self.__class__.__name__:
                if "Auto" in self.__class__.__name__:
                    path = "hashid_field.BigHashidAutoField"
                else:
                    path = "hashid_field.BigHashidField"
            else:
                if "Auto" in self.__class__.__name__:
                    path = "hashid_field.HashidAutoField"
                else:
                    path = "hashid_field.HashidField"

        # Only include non-default values
        if self.salt != app_settings.salt:
            kwargs["salt"] = self.salt

        if self.min_length != self._get_default_min_length():
            kwargs["min_length"] = self.min_length

        if self.alphabet != app_settings.alphabet:
            kwargs["alphabet"] = self.alphabet

        if self.prefix:
            kwargs["prefix"] = self.prefix

        if self.allow_int_lookup != app_settings.allow_int_lookup:
            kwargs["allow_int_lookup"] = self.allow_int_lookup

        if self.enable_hashid_object != app_settings.enable_hashid_object:
            kwargs["enable_hashid_object"] = self.enable_hashid_object

        if self.enable_descriptor != app_settings.enable_descriptor:
            kwargs["enable_descriptor"] = self.enable_descriptor

        return name, path, args, kwargs


class HashidCharFieldMixin:
    """Mixin for form field integration.

    Provides formfield() method that returns CharField widget instead of
    NumberInput for admin and forms.
    """

    def formfield(self, **kwargs: Any) -> forms.Field:
        """Return a CharField form field for this field.

        Args:
            **kwargs: Additional form field arguments

        Returns:
            CharField form field
        """
        defaults = {
            "form_class": forms.CharField,
        }
        defaults.update(kwargs)
        return super().formfield(**defaults)


class HashidField(HashidFieldMixin, HashidCharFieldMixin, models.IntegerField):
    """Django model field that stores integers as hashid strings.

    In the database, stores a standard integer. In Python, returns a Hashid
    object (or string) that can be used in URLs and displayed to users.

    Example:
        class Article(models.Model):
            external_id = HashidField(salt="my-salt")
    """

    description = "A hashid-encoded integer field"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def _get_default_min_length(self) -> int:
        """Get default minimum length for regular HashidField."""
        return app_settings.min_length


class BigHashidField(HashidFieldMixin, HashidCharFieldMixin, models.BigIntegerField):
    """Django model field for large hashid integers.

    Same as HashidField but uses BigIntegerField as the base.
    Default min_length is larger (13 vs 7) to accommodate larger IDs.

    Example:
        class BigTable(models.Model):
            external_id = BigHashidField(salt="my-salt")
    """

    description = "A hashid-encoded big integer field"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

    def _get_default_min_length(self) -> int:
        """Get default minimum length for BigHashidField."""
        return app_settings.big_min_length


# Register lookups
register_lookups(HashidField)
register_lookups(BigHashidField)

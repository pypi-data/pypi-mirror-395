"""HashidAutoField and BigHashidAutoField implementations.

Auto-incrementing primary key fields with hashid representation.
"""

from __future__ import annotations

from typing import Any

from django.db import models

from hashid_field.conf import app_settings
from hashid_field.field import HashidCharFieldMixin, HashidFieldMixin
from hashid_field.lookups import register_lookups


class HashidAutoField(HashidFieldMixin, HashidCharFieldMixin, models.AutoField):
    """Auto-incrementing primary key with hashid representation.

    Same as AutoField but displays and accepts hashid strings.
    Sets primary_key=True by default.

    Example:
        class Article(models.Model):
            id = HashidAutoField(primary_key=True)
    """

    description = "A hashid-encoded auto-incrementing primary key"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("primary_key", True)
        super().__init__(*args, **kwargs)

    def _get_default_min_length(self) -> int:
        """Get default minimum length for HashidAutoField."""
        return app_settings.min_length

    def deconstruct(self) -> tuple[str, str, list, dict]:
        """Return the field's deconstruction for migrations."""
        name, path, args, kwargs = super().deconstruct()
        # Override the path to use the package-level import
        path = "hashid_field.HashidAutoField"
        return name, path, args, kwargs


class BigHashidAutoField(HashidFieldMixin, HashidCharFieldMixin, models.BigAutoField):
    """Auto-incrementing big primary key with hashid representation.

    Same as BigAutoField but displays and accepts hashid strings.
    Sets primary_key=True by default.

    Example:
        class BigTable(models.Model):
            id = BigHashidAutoField(primary_key=True)
    """

    description = "A hashid-encoded big auto-incrementing primary key"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        kwargs.setdefault("primary_key", True)
        super().__init__(*args, **kwargs)

    def _get_default_min_length(self) -> int:
        """Get default minimum length for BigHashidAutoField."""
        return app_settings.big_min_length

    def deconstruct(self) -> tuple[str, str, list, dict]:
        """Return the field's deconstruction for migrations."""
        name, path, args, kwargs = super().deconstruct()
        # Override the path to use the package-level import
        path = "hashid_field.BigHashidAutoField"
        return name, path, args, kwargs


# Register lookups
register_lookups(HashidAutoField)
register_lookups(BigHashidAutoField)

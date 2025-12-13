"""Django REST Framework integration.

Provides HashidSerializerCharField for DRF serializers.
This module uses lazy imports to avoid requiring DRF as a dependency.
"""

from __future__ import annotations

import contextlib
from typing import TYPE_CHECKING, Any

from django.core.exceptions import FieldDoesNotExist

if TYPE_CHECKING:
    pass


def _get_rest_framework():
    """Lazy import of rest_framework to avoid ImportError when DRF not installed."""
    try:
        from rest_framework import serializers

        return serializers
    except ImportError as err:
        raise ImportError(
            "Django REST Framework is required for HashidSerializerCharField. "
            "Install it with: pip install djangorestframework"
        ) from err


class HashidSerializerCharField:
    """DRF serializer field for HashidField.

    Serializes Hashid objects to strings and deserializes strings back to Hashid.

    Usage:
        class MySerializer(serializers.ModelSerializer):
            id = HashidSerializerCharField(source_field='myapp.Model.id')

            class Meta:
                model = MyModel
                fields = ['id', 'name']
    """

    def __new__(cls, *args, **kwargs):
        """Create the actual field class dynamically to avoid import issues."""
        drf = _get_rest_framework()

        class _HashidSerializerCharField(drf.CharField):
            """Actual implementation of the serializer field."""

            def __init__(self, source_field: str | None = None, **kwargs):
                """Initialize the serializer field.

                Args:
                    source_field: Dotted path to the model field (e.g., 'myapp.Model.field')
                    **kwargs: Additional CharField arguments
                """
                self.source_field = source_field
                self._hashid_field = None
                super().__init__(**kwargs)

            def _get_hashid_field(self):
                """Get the HashidField instance from the model."""
                if self._hashid_field is not None:
                    return self._hashid_field

                if self.source_field:
                    from django.apps import apps

                    parts = self.source_field.rsplit(".", 2)
                    if len(parts) == 3:
                        app_label, model_name, field_name = parts
                        model = apps.get_model(app_label, model_name)
                        self._hashid_field = model._meta.get_field(field_name)
                    elif len(parts) == 2:
                        # Assume format is "Model.field" and try to get from context
                        pass

                # Try to get from parent serializer's model
                if self._hashid_field is None and hasattr(self, "parent"):
                    parent = self.parent
                    if hasattr(parent, "Meta") and hasattr(parent.Meta, "model"):
                        field_name = self.source or self.field_name
                        with contextlib.suppress(FieldDoesNotExist):
                            self._hashid_field = parent.Meta.model._meta.get_field(
                                field_name
                            )

                return self._hashid_field

            def to_representation(self, value: Any) -> str | None:
                """Convert Hashid to string for JSON output.

                Args:
                    value: The value to serialize (Hashid, int, or str)

                Returns:
                    String representation of the hashid, or None
                """
                if value is None:
                    return None

                from hashid_field.hashid import Hashid

                if isinstance(value, Hashid):
                    return str(value)
                if isinstance(value, int):
                    # Encode using the field if available
                    field = self._get_hashid_field()
                    if field and hasattr(field, "encode_id"):
                        return str(field.encode_id(value))
                    return str(value)
                return str(value)

            def to_internal_value(self, data: Any) -> Any:
                """Convert input data to internal value.

                Args:
                    data: The input data (hashid string or integer)

                Returns:
                    Hashid object or integer

                Raises:
                    ValidationError: If the hashid is invalid
                """
                if data is None:
                    return None

                from hashid_field.hashid import Hashid

                if isinstance(data, Hashid):
                    return data

                # Get the hashid field for decoding
                field = self._get_hashid_field()

                if isinstance(data, str):
                    if field and hasattr(field, "decode_id"):
                        try:
                            int_value = field.decode_id(data)
                            return field.encode_id(int_value)
                        except (ValueError, TypeError) as err:
                            from rest_framework.exceptions import ValidationError

                            raise ValidationError(f"Invalid hashid: {data}") from err
                    # Try to decode without field context
                    try:
                        from hashid_field.conf import app_settings

                        h = Hashid(
                            data,
                            salt=app_settings.salt,
                            min_length=app_settings.min_length,
                            alphabet=app_settings.alphabet,
                        )
                        return h
                    except ValueError as err:
                        from rest_framework.exceptions import ValidationError

                        raise ValidationError(f"Invalid hashid: {data}") from err

                if isinstance(data, int):
                    if field and hasattr(field, "encode_id"):
                        return field.encode_id(data)
                    from hashid_field.conf import app_settings

                    return Hashid(
                        data,
                        salt=app_settings.salt,
                        min_length=app_settings.min_length,
                        alphabet=app_settings.alphabet,
                    )

                return super().to_internal_value(data)

        return _HashidSerializerCharField(*args, **kwargs)

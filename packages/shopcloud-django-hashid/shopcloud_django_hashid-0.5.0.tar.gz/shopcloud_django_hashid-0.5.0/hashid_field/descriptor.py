"""HashidDescriptor for transparent hashid access on model instances.

Provides attribute access that automatically converts between integers
and Hashid objects.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from django.db.models import Model

    from hashid_field.field import HashidFieldMixin


class HashidDescriptor:
    """Descriptor for HashidField attribute access.

    Provides transparent conversion between raw integer values (stored
    in the model's __dict__) and Hashid objects (returned to the user).

    When getting: Returns a Hashid object (or string based on settings)
    When setting: Accepts int, str, Hashid, or None
    """

    def __init__(self, field: HashidFieldMixin) -> None:
        """Initialize the descriptor.

        Args:
            field: The HashidField this descriptor is for
        """
        self.field = field

    def __get__(
        self,
        obj: Model | None,
        objtype: type | None = None,
    ) -> Any:
        """Get the hashid value from the model instance.

        Args:
            obj: The model instance
            objtype: The model class

        Returns:
            Hashid object, string, or None depending on settings
        """
        if obj is None:
            return self

        # Get the raw value from the instance's __dict__
        value = obj.__dict__.get(self.field.attname)

        if value is None:
            return None

        # If it's already a Hashid, return it
        from hashid_field.hashid import Hashid

        if isinstance(value, Hashid):
            return value

        # Convert integer to Hashid
        if isinstance(value, int):
            return self.field.encode_id(value)

        # If it's a string, try to decode it first
        if isinstance(value, str):
            try:
                return self.field.encode_id(self.field.decode_id(value))
            except (ValueError, TypeError):
                return value

        return value

    def __set__(self, obj: Model, value: Any) -> None:
        """Set the hashid value on the model instance.

        Args:
            obj: The model instance
            value: The value to set (int, str, Hashid, or None)
        """
        if value is None:
            obj.__dict__[self.field.attname] = None
            return

        from hashid_field.hashid import Hashid

        if isinstance(value, Hashid):
            # Store the Hashid directly
            obj.__dict__[self.field.attname] = value
        elif isinstance(value, int):
            # Convert int to Hashid and store
            obj.__dict__[self.field.attname] = self.field.encode_id(value)
        elif isinstance(value, str):
            # Decode string and create Hashid
            try:
                int_value = self.field.decode_id(value)
                obj.__dict__[self.field.attname] = self.field.encode_id(int_value)
            except (ValueError, TypeError):
                # Store the string as-is (will fail validation later)
                obj.__dict__[self.field.attname] = value
        else:
            obj.__dict__[self.field.attname] = value

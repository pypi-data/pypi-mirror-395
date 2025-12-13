"""shopcloud-django-hashid: Drop-in replacement for django-hashid-field.

A Django model field that stores integers but represents them as
obfuscated hashid strings.
"""

from hashid_field.auto_field import BigHashidAutoField, HashidAutoField
from hashid_field.field import BigHashidField, HashidField
from hashid_field.hashid import Hashid

__all__ = [
    "Hashid",
    "HashidField",
    "BigHashidField",
    "HashidAutoField",
    "BigHashidAutoField",
]

__version__ = "0.4.0"

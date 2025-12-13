"""Tests for installation and import compatibility.

Tests for T034-T035: Installation and import verification.
"""


class TestPackageInstallation:
    """T034-T035: Tests for package installation."""

    def test_package_is_importable(self):
        """Package can be imported."""
        import hashid_field

        assert hashid_field is not None

    def test_hashid_field_import(self):
        """HashidField can be imported from hashid_field."""
        from hashid_field import HashidField

        assert HashidField is not None

    def test_big_hashid_field_import(self):
        """BigHashidField can be imported from hashid_field."""
        from hashid_field import BigHashidField

        assert BigHashidField is not None

    def test_hashid_auto_field_import(self):
        """HashidAutoField can be imported from hashid_field."""
        from hashid_field import HashidAutoField

        assert HashidAutoField is not None

    def test_big_hashid_auto_field_import(self):
        """BigHashidAutoField can be imported from hashid_field."""
        from hashid_field import BigHashidAutoField

        assert BigHashidAutoField is not None

    def test_hashid_import(self):
        """Hashid can be imported from hashid_field."""
        from hashid_field import Hashid

        assert Hashid is not None

    def test_version_available(self):
        """Package version is available."""
        import re

        import hashid_field

        assert hasattr(hashid_field, "__version__")
        # Check version follows semantic versioning format (X.Y.Z)
        assert re.match(r"^\d+\.\d+\.\d+$", hashid_field.__version__)

    def test_all_exports_defined(self):
        """__all__ is defined with expected exports."""
        import hashid_field

        assert hasattr(hashid_field, "__all__")
        expected = [
            "Hashid",
            "HashidField",
            "BigHashidField",
            "HashidAutoField",
            "BigHashidAutoField",
        ]
        for name in expected:
            assert name in hashid_field.__all__

    def test_field_is_django_field(self):
        """HashidField is a Django model field."""
        from django.db.models import Field

        from hashid_field import HashidField

        assert issubclass(HashidField, Field)

    def test_auto_field_is_django_auto_field(self):
        """HashidAutoField inherits from Django AutoField."""
        from django.db.models import AutoField

        from hashid_field import HashidAutoField

        # Check the MRO includes AutoField
        assert AutoField in HashidAutoField.__mro__

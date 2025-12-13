"""Tests for compatibility with original django-hashid-field.

Tests for T025: Output compatibility verification.
"""

import pytest
from hashids import Hashids

from hashid_field import (
    BigHashidAutoField,
    BigHashidField,
    HashidAutoField,
    HashidField,
)
from hashid_field.hashid import Hashid


class TestHashidOutputCompatibility:
    """T025: Tests verifying output matches expected hashid format."""

    def test_hashid_encoding_deterministic(self):
        """Same input produces same hashid."""
        h1 = Hashid(123, salt="test-salt")
        h2 = Hashid(123, salt="test-salt")

        assert h1.hashid == h2.hashid

    def test_hashid_encoding_matches_hashids_library(self):
        """Our encoding matches hashids library directly."""
        salt = "test-salt"
        min_length = 7
        test_id = 12345

        # Direct hashids encoding
        hashids = Hashids(salt=salt, min_length=min_length)
        expected = hashids.encode(test_id)

        # Our Hashid class encoding
        h = Hashid(test_id, salt=salt, min_length=min_length)

        assert h.hashid == expected

    def test_hashid_decoding_matches_hashids_library(self):
        """Our decoding matches hashids library directly."""
        salt = "test-salt"
        test_id = 98765

        # Encode with hashids library
        hashids = Hashids(salt=salt)
        encoded = hashids.encode(test_id)

        # Decode with our Hashid class
        h = Hashid(encoded, salt=salt)

        assert h.id == test_id

    def test_field_encoding_matches_hashids_library(self):
        """Field encoding matches hashids library."""
        salt = "field-salt"
        min_length = 7
        test_id = 42

        # Direct hashids encoding
        hashids = Hashids(salt=salt, min_length=min_length)
        expected = hashids.encode(test_id)

        # Field encoding
        field = HashidField(salt=salt, min_length=min_length)
        encoded = field.encode_id(test_id)

        assert str(encoded) == expected

    def test_alphabet_compatibility(self):
        """Custom alphabet produces expected output."""
        alphabet = "abcdef1234567890"
        test_id = 100

        # Direct hashids encoding
        hashids = Hashids(alphabet=alphabet)
        expected = hashids.encode(test_id)

        # Our encoding
        h = Hashid(test_id, alphabet=alphabet)

        assert h.hashid == expected

    def test_min_length_compatibility(self):
        """Min length produces padded output."""
        min_length = 15
        test_id = 1  # Small number that would normally produce short hashid

        h = Hashid(test_id, min_length=min_length)

        assert len(h.hashid) >= min_length

    def test_prefix_handling(self):
        """Prefix is correctly added and removed."""
        prefix = "user_"
        test_id = 123

        h = Hashid(test_id, prefix=prefix)

        assert h.hashid.startswith(prefix)
        assert h.id == test_id

        # Can create from prefixed string
        h2 = Hashid(h.hashid, prefix=prefix)
        assert h2.id == test_id


class TestAPICompatibility:
    """Tests for API compatibility with original library."""

    def test_field_has_salt_attribute(self):
        """Field has salt attribute."""
        field = HashidField(salt="my-salt")
        assert hasattr(field, "salt")
        assert field.salt == "my-salt"

    def test_field_has_min_length_attribute(self):
        """Field has min_length attribute."""
        field = HashidField(min_length=10)
        assert hasattr(field, "min_length")
        assert field.min_length == 10

    def test_field_has_alphabet_attribute(self):
        """Field has alphabet attribute."""
        alphabet = "abcdef"
        field = HashidField(alphabet=alphabet)
        assert hasattr(field, "alphabet")
        assert field.alphabet == alphabet

    def test_field_has_prefix_attribute(self):
        """Field has prefix attribute."""
        field = HashidField(prefix="pk_")
        assert hasattr(field, "prefix")
        assert field.prefix == "pk_"

    def test_field_has_allow_int_lookup_attribute(self):
        """Field has allow_int_lookup attribute."""
        field = HashidField(allow_int_lookup=True)
        assert hasattr(field, "allow_int_lookup")
        assert field.allow_int_lookup is True

    def test_hashid_has_id_property(self):
        """Hashid has id property."""
        h = Hashid(123)
        assert hasattr(h, "id")
        assert h.id == 123

    def test_hashid_has_hashid_property(self):
        """Hashid has hashid property."""
        h = Hashid(123)
        assert hasattr(h, "hashid")
        assert isinstance(h.hashid, str)

    def test_hashid_int_conversion(self):
        """Hashid supports int() conversion."""
        h = Hashid(456)
        assert int(h) == 456

    def test_hashid_str_conversion(self):
        """Hashid supports str() conversion."""
        h = Hashid(789)
        assert str(h) == h.hashid

    def test_hashid_equality_with_int(self):
        """Hashid equals its integer value."""
        h = Hashid(100)
        assert h == 100

    def test_hashid_equality_with_string(self):
        """Hashid equals its string representation."""
        h = Hashid(100)
        assert h == h.hashid


class TestNonPrimaryKeyUsage:
    """Tests for HashidField usage as non-primary-key field.

    This is the primary use case for many projects - using HashidField
    as a regular field for obfuscating reference IDs, not as a PK replacement.
    """

    def test_hashid_field_as_regular_field(self):
        """HashidField can be used as a regular (non-PK) field."""
        field = HashidField(salt="reference-salt")

        # Encode an ID
        encoded = field.encode_id(12345)
        assert str(encoded) is not None
        assert len(str(encoded)) >= 7

        # Decode back
        decoded = field.decode_id(str(encoded))
        assert decoded == 12345

    def test_hashid_field_manual_assignment(self):
        """HashidField allows manual integer assignment."""
        field = HashidField(salt="manual-salt")

        # Can encode any integer value
        for value in [1, 100, 999, 123456]:
            encoded = field.encode_id(value)
            decoded = field.decode_id(str(encoded))
            assert decoded == value

    def test_hashid_field_nullable(self):
        """HashidField can be nullable."""
        field = HashidField(null=True, blank=True)
        # Field should accept None
        prep_value = field.get_prep_value(None)
        assert prep_value is None

    def test_hashid_field_with_prefix(self):
        """HashidField supports prefix for different field types."""
        field = HashidField(salt="order-salt", prefix="order_")

        encoded = field.encode_id(42)
        assert str(encoded).startswith("order_")

        # Decode with prefix
        decoded = field.decode_id(str(encoded))
        assert decoded == 42

    def test_hashid_field_custom_min_length(self):
        """HashidField supports custom min_length."""
        field = HashidField(salt="custom-salt", min_length=15)

        encoded = field.encode_id(1)
        assert len(str(encoded)) >= 15

    def test_hashid_field_enable_hashid_object_false(self):
        """HashidField can return plain strings instead of Hashid objects."""
        field = HashidField(salt="string-salt", enable_hashid_object=False)

        encoded = field.encode_id(100)
        assert isinstance(encoded, str)

    def test_hashid_field_different_salts_different_output(self):
        """Different salts produce different hashids for same ID."""
        field1 = HashidField(salt="salt-one")
        field2 = HashidField(salt="salt-two")

        encoded1 = str(field1.encode_id(42))
        encoded2 = str(field2.encode_id(42))

        assert encoded1 != encoded2


@pytest.mark.django_db
class TestNonPrimaryKeyUsageORM:
    """ORM tests for HashidField as non-primary-key field.

    Tests that match how django-hashid-field is typically used in projects:
    - HashidField as a reference/external ID field (not PK)
    - Manual value assignment
    - Querying by hashid string
    """

    def test_reference_code_field_assignment(self, create_tables):
        """HashidField as reference_code can be assigned integer values."""
        from tests.testapp.models import Article, Comment

        article = Article.objects.create(title="Test")
        comment = Comment.objects.create(
            article=article,
            reference_code=12345,  # Assign integer directly
            content="Test comment",
        )

        # Stored value is encoded
        assert comment.reference_code is not None
        assert int(comment.reference_code) == 12345

    def test_reference_code_query_by_integer(self, create_tables):
        """Can query HashidField by integer value."""
        from tests.testapp.models import Article, Comment

        article = Article.objects.create(title="Test")
        Comment.objects.create(article=article, reference_code=100, content="C1")
        Comment.objects.create(article=article, reference_code=200, content="C2")

        result = Comment.objects.filter(reference_code=100)
        assert result.count() == 1
        assert result.first().content == "C1"

    def test_reference_code_query_by_hashid_string(self, create_tables):
        """Can query HashidField by hashid string."""
        from tests.testapp.models import Article, Comment

        article = Article.objects.create(title="Test")
        comment = Comment.objects.create(
            article=article, reference_code=555, content="Test"
        )

        hashid_str = str(comment.reference_code)
        result = Comment.objects.get(reference_code=hashid_str)
        assert result.content == "Test"

    def test_big_hashid_field_non_pk(self, create_tables):
        """BigHashidField works as non-PK field."""
        from tests.testapp.models import BigNumber

        obj = BigNumber.objects.create(big_ref=9876543210, value=100)

        assert int(obj.big_ref) == 9876543210
        assert len(str(obj.big_ref)) >= 13  # BigHashidField default min_length

    def test_nullable_hashid_field(self, create_tables):
        """Nullable HashidField can store None."""
        from tests.testapp.models import NullableHashid

        obj = NullableHashid.objects.create(optional_ref=None)
        assert obj.optional_ref is None

        obj.refresh_from_db()
        assert obj.optional_ref is None

    def test_nullable_hashid_field_with_value(self, create_tables):
        """Nullable HashidField can store values."""
        from tests.testapp.models import NullableHashid

        obj = NullableHashid.objects.create(optional_ref=42)
        assert int(obj.optional_ref) == 42

    def test_update_hashid_field(self, create_tables):
        """HashidField can be updated."""
        from tests.testapp.models import Article, Comment

        article = Article.objects.create(title="Test")
        comment = Comment.objects.create(
            article=article, reference_code=100, content="Test"
        )

        # Update the reference_code
        comment.reference_code = 200
        comment.save()

        comment.refresh_from_db()
        assert int(comment.reference_code) == 200

    def test_filter_comparison_operators(self, create_tables):
        """HashidField supports comparison operators in queries."""
        from tests.testapp.models import Article, Comment

        article = Article.objects.create(title="Test")
        for i in range(5):
            Comment.objects.create(
                article=article, reference_code=(i + 1) * 100, content=f"C{i}"
            )

        # Greater than
        result = Comment.objects.filter(reference_code__gte=300)
        assert result.count() == 3

        # Less than
        result = Comment.objects.filter(reference_code__lt=300)
        assert result.count() == 2


class TestImportCompatibility:
    """Tests for import path compatibility."""

    def test_import_hashid_field(self):
        """Can import HashidField from hashid_field."""
        from hashid_field import HashidField

        assert HashidField is not None

    def test_import_big_hashid_field(self):
        """Can import BigHashidField from hashid_field."""

        assert BigHashidField is not None

    def test_import_hashid_auto_field(self):
        """Can import HashidAutoField from hashid_field."""

        assert HashidAutoField is not None

    def test_import_big_hashid_auto_field(self):
        """Can import BigHashidAutoField from hashid_field."""

        assert BigHashidAutoField is not None

    def test_import_hashid(self):
        """Can import Hashid from hashid_field."""
        from hashid_field import Hashid

        assert Hashid is not None

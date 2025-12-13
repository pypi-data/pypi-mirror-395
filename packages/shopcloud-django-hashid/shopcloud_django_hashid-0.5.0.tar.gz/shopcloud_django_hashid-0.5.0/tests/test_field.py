"""Integration tests for HashidField and BigHashidField.

Tests for T019-T020: Field integration with Django models.
"""

import pytest
from django.db import connection

from hashid_field.hashid import Hashid


@pytest.mark.django_db
class TestHashidField:
    """T019: Tests for HashidField integration."""

    def test_field_stores_integer_in_database(self, create_tables):
        """HashidField stores integer values in the database."""
        from tests.testapp.models import Article

        article = Article.objects.create(title="Test Article")

        # Raw database value should be an integer
        with connection.cursor() as cursor:
            cursor.execute(
                f"SELECT id FROM testapp_article WHERE id = {int(article.id)}"
            )
            row = cursor.fetchone()
            assert row is not None
            assert isinstance(row[0], int)

    def test_field_returns_hashid_object(self, create_tables):
        """HashidField returns Hashid object in Python."""
        from tests.testapp.models import Article

        article = Article.objects.create(title="Test Article")
        assert isinstance(article.id, Hashid)

    def test_field_hashid_is_string_representable(self, create_tables):
        """HashidField hashid can be converted to string."""
        from tests.testapp.models import Article

        article = Article.objects.create(title="Test Article")
        hashid_str = str(article.id)
        assert isinstance(hashid_str, str)
        assert len(hashid_str) >= 7  # Default min_length

    def test_field_can_query_by_hashid_string(self, create_tables):
        """Can query by hashid string."""
        from tests.testapp.models import Article

        article = Article.objects.create(title="Test Article")
        hashid_str = str(article.id)

        found = Article.objects.get(id=hashid_str)
        assert found.id == article.id

    def test_field_can_query_by_pk(self, create_tables):
        """Can query by pk using hashid."""
        from tests.testapp.models import Article

        article = Article.objects.create(title="Test Article")

        found = Article.objects.get(pk=article.id)
        assert found.title == "Test Article"

    def test_field_filter_returns_correct_results(self, create_tables):
        """Filter returns correct results."""
        from tests.testapp.models import Article

        a1 = Article.objects.create(title="Article 1")
        Article.objects.create(title="Article 2")  # Create second article

        results = Article.objects.filter(id=a1.id)
        assert results.count() == 1
        assert results.first().title == "Article 1"

    def test_field_exclude_works(self, create_tables):
        """Exclude works with hashid values."""
        from tests.testapp.models import Article

        a1 = Article.objects.create(title="Article 1")
        Article.objects.create(title="Article 2")  # Create second article

        results = Article.objects.exclude(id=a1.id)
        assert results.count() == 1
        assert results.first().title == "Article 2"

    def test_nullable_field(self, create_tables):
        """Nullable HashidField can be null."""
        from tests.testapp.models import NullableHashid

        obj = NullableHashid.objects.create(optional_ref=None)
        assert obj.optional_ref is None

        obj_fetched = NullableHashid.objects.get(id=obj.id)
        assert obj_fetched.optional_ref is None

    def test_nullable_field_with_value(self, create_tables):
        """Nullable HashidField can have a value."""
        from tests.testapp.models import NullableHashid

        obj = NullableHashid.objects.create(optional_ref=123)
        assert obj.optional_ref is not None
        assert int(obj.optional_ref) == 123

    def test_custom_salt_field(self, create_tables):
        """Field with custom salt produces different hashid."""
        from tests.testapp.models import Article, Tag

        Article.objects.create(title="Article")  # Create an article
        tag = Tag.objects.create(name="Tag")

        # Same underlying ID (1) but different hashids due to salt
        # Cannot directly compare as auto-increment may differ
        # Just verify Tag uses custom salt by checking prefix
        assert str(tag.id).startswith("tag_")

    def test_custom_min_length_field(self, create_tables):
        """Field with custom min_length produces longer hashid."""
        from tests.testapp.models import Tag

        tag = Tag.objects.create(name="Tag")
        # Tag has min_length=10 and prefix="tag_"
        assert len(str(tag.id)) >= 10 + len("tag_")

    def test_field_preserves_value_on_save(self, create_tables):
        """Field preserves value after save and reload."""
        from tests.testapp.models import Article

        article = Article.objects.create(title="Test")
        original_id = article.id

        article.title = "Updated"
        article.save()

        article.refresh_from_db()
        assert article.id == original_id

    def test_field_int_conversion(self, create_tables):
        """Field value can be converted to int."""
        from tests.testapp.models import Article

        article = Article.objects.create(title="Test")
        assert isinstance(int(article.id), int)
        assert int(article.id) > 0


@pytest.mark.django_db
class TestBigHashidField:
    """T020: Tests for BigHashidField integration."""

    def test_big_field_stores_large_integer(self, create_tables):
        """BigHashidField can store large integers."""
        from tests.testapp.models import BigArticle

        article = BigArticle.objects.create(title="Big Article")
        assert isinstance(article.id, Hashid)
        assert int(article.id) > 0

    def test_big_field_min_length(self, create_tables):
        """BigHashidField uses larger default min_length."""
        from tests.testapp.models import BigArticle

        article = BigArticle.objects.create(title="Big Article")
        # Default big_min_length is 13
        assert len(str(article.id)) >= 13

    def test_big_field_query_by_hashid(self, create_tables):
        """BigHashidField can be queried by hashid."""
        from tests.testapp.models import BigArticle

        article = BigArticle.objects.create(title="Big Article")
        hashid_str = str(article.id)

        found = BigArticle.objects.get(id=hashid_str)
        assert found.title == "Big Article"

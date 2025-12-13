"""Integration tests for HashidAutoField and BigHashidAutoField.

Tests for T021-T022: Auto field integration with Django models.
"""

import pytest

from hashid_field import BigHashidAutoField, HashidAutoField
from hashid_field.hashid import Hashid


@pytest.mark.django_db
class TestHashidAutoField:
    """T021: Tests for HashidAutoField."""

    def test_auto_field_is_primary_key(self):
        """HashidAutoField is a primary key by default."""
        field = HashidAutoField()
        assert field.primary_key is True

    def test_auto_field_auto_increments(self, create_tables):
        """HashidAutoField auto-increments on creation."""
        from tests.testapp.models import Article

        a1 = Article.objects.create(title="Article 1")
        a2 = Article.objects.create(title="Article 2")
        a3 = Article.objects.create(title="Article 3")

        assert int(a1.id) == 1
        assert int(a2.id) == 2
        assert int(a3.id) == 3

    def test_auto_field_returns_hashid(self, create_tables):
        """HashidAutoField returns Hashid object."""
        from tests.testapp.models import Article

        article = Article.objects.create(title="Test")
        assert isinstance(article.id, Hashid)
        assert isinstance(article.pk, Hashid)

    def test_auto_field_pk_equals_id(self, create_tables):
        """pk and id are the same for primary key field."""
        from tests.testapp.models import Article

        article = Article.objects.create(title="Test")
        assert article.pk == article.id
        assert str(article.pk) == str(article.id)

    def test_auto_field_query_by_pk(self, create_tables):
        """Can query by pk with hashid."""
        from tests.testapp.models import Article

        article = Article.objects.create(title="Test")

        found = Article.objects.get(pk=article.pk)
        assert found.title == "Test"

    def test_auto_field_query_by_hashid_string(self, create_tables):
        """Can query by hashid string."""
        from tests.testapp.models import Article

        article = Article.objects.create(title="Test")
        hashid_str = str(article.pk)

        found = Article.objects.get(pk=hashid_str)
        assert found.title == "Test"

    def test_auto_field_unique_hashids(self, create_tables):
        """Each record gets a unique hashid."""
        from tests.testapp.models import Article

        articles = [Article.objects.create(title=f"Article {i}") for i in range(10)]
        hashids = [str(a.id) for a in articles]

        assert len(set(hashids)) == 10

    def test_auto_field_consistent_encoding(self, create_tables):
        """Same ID always produces same hashid (with same salt)."""
        from tests.testapp.models import Article

        article = Article.objects.create(title="Test")
        original_hashid = str(article.id)

        # Reload from database
        article.refresh_from_db()
        reloaded_hashid = str(article.id)

        assert original_hashid == reloaded_hashid


@pytest.mark.django_db
class TestBigHashidAutoField:
    """T022: Tests for BigHashidAutoField."""

    def test_big_auto_field_is_primary_key(self):
        """BigHashidAutoField is a primary key by default."""
        field = BigHashidAutoField()
        assert field.primary_key is True

    def test_big_auto_field_auto_increments(self, create_tables):
        """BigHashidAutoField auto-increments on creation."""
        from tests.testapp.models import BigArticle

        a1 = BigArticle.objects.create(title="Big Article 1")
        a2 = BigArticle.objects.create(title="Big Article 2")

        assert int(a1.id) == 1
        assert int(a2.id) == 2

    def test_big_auto_field_returns_hashid(self, create_tables):
        """BigHashidAutoField returns Hashid object."""
        from tests.testapp.models import BigArticle

        article = BigArticle.objects.create(title="Test")
        assert isinstance(article.id, Hashid)

    def test_big_auto_field_uses_big_min_length(self, create_tables):
        """BigHashidAutoField uses bigger default min_length."""
        from tests.testapp.models import BigArticle

        article = BigArticle.objects.create(title="Test")
        # Default big_min_length is 13
        assert len(str(article.id)) >= 13

    def test_big_auto_field_query_by_pk(self, create_tables):
        """Can query BigHashidAutoField by pk."""
        from tests.testapp.models import BigArticle

        article = BigArticle.objects.create(title="Test")

        found = BigArticle.objects.get(pk=article.pk)
        assert found.title == "Test"

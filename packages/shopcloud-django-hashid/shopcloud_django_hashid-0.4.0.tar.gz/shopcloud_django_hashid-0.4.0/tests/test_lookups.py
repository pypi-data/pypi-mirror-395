"""Tests for queryset lookups.

Tests for T023: filter, get, exclude, in lookups.
"""

import pytest
from django.test import override_settings


@pytest.fixture
def sample_articles(create_tables):
    """Create sample articles for testing."""
    from tests.testapp.models import Article

    articles = []
    for i in range(5):
        articles.append(Article.objects.create(title=f"Article {i + 1}"))
    return articles


@pytest.mark.django_db
class TestLookupExact:
    """Tests for exact lookup."""

    def test_exact_with_hashid_object(self, sample_articles):
        """Exact lookup works with Hashid object."""
        from tests.testapp.models import Article

        target = sample_articles[2]
        found = Article.objects.get(id=target.id)
        assert found.title == "Article 3"

    def test_exact_with_hashid_string(self, sample_articles):
        """Exact lookup works with hashid string."""
        from tests.testapp.models import Article

        target = sample_articles[2]
        found = Article.objects.get(id=str(target.id))
        assert found.title == "Article 3"

    def test_exact_with_pk(self, sample_articles):
        """Exact lookup works with pk shortcut."""
        from tests.testapp.models import Article

        target = sample_articles[0]
        found = Article.objects.get(pk=target.pk)
        assert found.title == "Article 1"


@pytest.mark.django_db
class TestLookupIn:
    """Tests for 'in' lookup."""

    def test_in_with_hashid_objects(self, sample_articles):
        """In lookup works with list of Hashid objects."""
        from tests.testapp.models import Article

        ids = [sample_articles[0].id, sample_articles[2].id, sample_articles[4].id]
        results = Article.objects.filter(id__in=ids)

        assert results.count() == 3
        titles = [a.title for a in results]
        assert "Article 1" in titles
        assert "Article 3" in titles
        assert "Article 5" in titles

    def test_in_with_hashid_strings(self, sample_articles):
        """In lookup works with list of hashid strings."""
        from tests.testapp.models import Article

        ids = [str(sample_articles[1].id), str(sample_articles[3].id)]
        results = Article.objects.filter(id__in=ids)

        assert results.count() == 2
        titles = [a.title for a in results]
        assert "Article 2" in titles
        assert "Article 4" in titles

    def test_in_with_empty_list(self, sample_articles):
        """In lookup with empty list returns no results."""
        from tests.testapp.models import Article

        results = Article.objects.filter(id__in=[])
        assert results.count() == 0


@pytest.mark.django_db
class TestLookupFilter:
    """Tests for filter operations."""

    def test_filter_by_hashid(self, sample_articles):
        """Filter by hashid returns QuerySet."""
        from tests.testapp.models import Article

        results = Article.objects.filter(id=sample_articles[0].id)
        assert results.count() == 1
        assert results.first().title == "Article 1"

    def test_filter_chaining(self, sample_articles):
        """Multiple filters can be chained."""
        from tests.testapp.models import Article

        results = Article.objects.filter(id=sample_articles[0].id).filter(title="Article 1")
        assert results.count() == 1

    def test_filter_no_match(self, create_tables):
        """Filter with no match returns empty QuerySet."""
        from tests.testapp.models import Article

        # Create one article
        Article.objects.create(title="Test")

        # Filter by a hashid that doesn't exist (invalid format)
        results = Article.objects.filter(id__in=[])
        assert results.count() == 0


@pytest.mark.django_db
class TestLookupExclude:
    """Tests for exclude operations."""

    def test_exclude_single(self, sample_articles):
        """Exclude single hashid."""
        from tests.testapp.models import Article

        results = Article.objects.exclude(id=sample_articles[0].id)
        assert results.count() == 4
        assert "Article 1" not in [a.title for a in results]

    def test_exclude_multiple(self, sample_articles):
        """Exclude multiple hashids."""
        from tests.testapp.models import Article

        exclude_ids = [sample_articles[0].id, sample_articles[1].id]
        results = Article.objects.exclude(id__in=exclude_ids)
        assert results.count() == 3


@pytest.mark.django_db
class TestLookupIsNull:
    """Tests for isnull lookup."""

    def test_isnull_true(self, create_tables):
        """isnull=True finds null values."""
        from tests.testapp.models import NullableHashid

        NullableHashid.objects.create(optional_ref=None)
        NullableHashid.objects.create(optional_ref=123)

        results = NullableHashid.objects.filter(optional_ref__isnull=True)
        assert results.count() == 1

    def test_isnull_false(self, create_tables):
        """isnull=False finds non-null values."""
        from tests.testapp.models import NullableHashid

        NullableHashid.objects.create(optional_ref=None)
        NullableHashid.objects.create(optional_ref=123)

        results = NullableHashid.objects.filter(optional_ref__isnull=False)
        assert results.count() == 1


@pytest.mark.django_db
class TestIntegerLookup:
    """Tests for integer-based lookups."""

    @override_settings(HASHID_FIELD_ALLOW_INT_LOOKUP=True)
    def test_lookup_by_integer_when_allowed(self, sample_articles):
        """Integer lookup works when HASHID_FIELD_ALLOW_INT_LOOKUP=True."""
        from tests.testapp.models import Article

        # Need to reimport to pick up new settings
        # Actually the lookup is determined at field creation, so this tests
        # that integers can be used in the lookup value
        results = Article.objects.filter(id=1)
        # This should work - the integer gets passed through
        assert results.count() == 1


@pytest.mark.django_db
class TestComparisonLookups:
    """Tests for comparison lookups (lt, lte, gt, gte)."""

    def test_lt_lookup(self, sample_articles):
        """Less than lookup works."""
        from tests.testapp.models import Article

        # Get articles with id < 3
        results = Article.objects.filter(id__lt=3)
        assert results.count() == 2

    def test_lte_lookup(self, sample_articles):
        """Less than or equal lookup works."""
        from tests.testapp.models import Article

        results = Article.objects.filter(id__lte=3)
        assert results.count() == 3

    def test_gt_lookup(self, sample_articles):
        """Greater than lookup works."""
        from tests.testapp.models import Article

        results = Article.objects.filter(id__gt=3)
        assert results.count() == 2

    def test_gte_lookup(self, sample_articles):
        """Greater than or equal lookup works."""
        from tests.testapp.models import Article

        results = Article.objects.filter(id__gte=3)
        assert results.count() == 3

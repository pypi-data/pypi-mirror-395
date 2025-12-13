"""Tests for Django ORM operations.

Tests for T042-T047: Full ORM compatibility (User Story 3).
"""

import pytest

from hashid_field.hashid import Hashid


@pytest.fixture
def article_with_comments(create_tables):
    """Create an article with comments for testing."""
    from tests.testapp.models import Article, Comment

    article = Article.objects.create(title="Test Article")
    for i in range(3):
        Comment.objects.create(
            article=article, reference_code=100 + i, content=f"Comment {i + 1}"
        )
    return article


@pytest.mark.django_db
class TestSelectRelated:
    """T042: Tests for select_related."""

    def test_select_related_from_comment(self, article_with_comments):
        """select_related works on ForeignKey to HashidField model."""
        from tests.testapp.models import Comment

        comments = Comment.objects.select_related("article").all()
        for comment in comments:
            assert comment.article.title == "Test Article"
            assert isinstance(comment.article.id, Hashid)


@pytest.mark.django_db
class TestPrefetchRelated:
    """T042: Tests for prefetch_related."""

    def test_prefetch_related_from_article(self, article_with_comments):
        """prefetch_related works on reverse relation."""
        from tests.testapp.models import Article

        article = Article.objects.prefetch_related("comment_set").get(
            id=article_with_comments.id
        )
        comments = list(article.comment_set.all())
        assert len(comments) == 3


@pytest.mark.django_db
class TestValues:
    """T043: Tests for values and values_list."""

    def test_values_returns_dict(self, create_tables):
        """values() returns dictionary with hashid values."""
        from tests.testapp.models import Article

        Article.objects.create(title="Test")
        result = Article.objects.values("id", "title").first()

        assert isinstance(result, dict)
        assert "id" in result
        assert "title" in result
        # values() returns the value through from_db_value (may be Hashid or int)
        assert result["id"] is not None

    def test_values_list_returns_tuple(self, create_tables):
        """values_list() returns tuple with hashid values."""
        from tests.testapp.models import Article

        Article.objects.create(title="Test")
        result = Article.objects.values_list("id", "title").first()

        assert isinstance(result, tuple)
        assert len(result) == 2

    def test_values_list_flat(self, create_tables):
        """values_list(flat=True) works."""
        from tests.testapp.models import Article

        for i in range(3):
            Article.objects.create(title=f"Test {i}")

        ids = list(Article.objects.values_list("id", flat=True))
        assert len(ids) == 3


@pytest.mark.django_db
class TestAnnotateAggregate:
    """T044: Tests for annotate and aggregate."""

    def test_count_aggregate(self, article_with_comments):
        """Count aggregation works."""
        from django.db.models import Count

        from tests.testapp.models import Article

        result = Article.objects.annotate(comment_count=Count("comment")).get(
            id=article_with_comments.id
        )
        assert result.comment_count == 3

    def test_aggregate(self, create_tables):
        """aggregate() works."""
        from django.db.models import Count

        from tests.testapp.models import Article

        for i in range(5):
            Article.objects.create(title=f"Test {i}")

        result = Article.objects.aggregate(total=Count("id"))
        assert result["total"] == 5


@pytest.mark.django_db
class TestFExpressions:
    """T045: Tests for F expressions."""

    def test_f_expression_in_filter(self, create_tables):
        """F expression in filter works."""
        from django.db.models import F

        from tests.testapp.models import BigNumber

        BigNumber.objects.create(big_ref=100, value=100)
        BigNumber.objects.create(big_ref=200, value=100)

        # Filter where big_ref equals value
        results = BigNumber.objects.filter(big_ref=F("value"))
        assert results.count() == 1

    def test_f_expression_in_update(self, create_tables):
        """F expression in update works."""
        from django.db.models import F

        from tests.testapp.models import BigNumber

        obj = BigNumber.objects.create(big_ref=50, value=10)

        BigNumber.objects.filter(id=obj.id).update(value=F("value") + 5)

        obj.refresh_from_db()
        assert obj.value == 15


@pytest.mark.django_db
class TestForeignKey:
    """T046: Tests for ForeignKey relationships."""

    def test_foreign_key_assignment(self, create_tables):
        """ForeignKey assignment works with hashid."""
        from tests.testapp.models import Article, Comment

        article = Article.objects.create(title="Test")
        comment = Comment.objects.create(
            article=article, reference_code=123, content="Test comment"
        )

        assert comment.article_id == int(article.id)

    def test_foreign_key_query(self, article_with_comments):
        """Filtering by ForeignKey works."""
        from tests.testapp.models import Comment

        comments = Comment.objects.filter(article=article_with_comments)
        assert comments.count() == 3

    def test_foreign_key_query_by_pk(self, article_with_comments):
        """Filtering by ForeignKey pk works."""
        from tests.testapp.models import Comment

        comments = Comment.objects.filter(article_id=article_with_comments.id)
        assert comments.count() == 3


@pytest.mark.django_db
class TestBulkOperations:
    """T047: Tests for bulk operations."""

    def test_bulk_create(self, create_tables):
        """bulk_create works with HashidField models."""
        from tests.testapp.models import Article

        articles = [Article(title=f"Article {i}") for i in range(10)]
        created = Article.objects.bulk_create(articles)

        assert len(created) == 10
        assert Article.objects.count() == 10

        # Each should have a valid hashid
        for article in Article.objects.all():
            assert isinstance(article.id, Hashid)
            assert int(article.id) > 0

    def test_get_or_create(self, create_tables):
        """get_or_create works."""
        from tests.testapp.models import Article

        article1, created1 = Article.objects.get_or_create(title="Unique Article")
        assert created1 is True
        assert isinstance(article1.id, Hashid)

        article2, created2 = Article.objects.get_or_create(title="Unique Article")
        assert created2 is False
        assert article1.id == article2.id

    def test_update_or_create(self, create_tables):
        """update_or_create works."""
        from tests.testapp.models import Article

        article1, created1 = Article.objects.update_or_create(
            title="Update Test", defaults={"title": "Update Test"}
        )
        assert created1 is True

        article2, created2 = Article.objects.update_or_create(
            id=article1.id, defaults={"title": "Updated Title"}
        )
        assert created2 is False
        assert article2.title == "Updated Title"


@pytest.mark.django_db
class TestQueryChaining:
    """Additional ORM query tests."""

    def test_filter_chain(self, create_tables):
        """Multiple filter calls work."""
        from tests.testapp.models import Article

        for i in range(5):
            Article.objects.create(title=f"Article {i}")

        results = Article.objects.filter(id__gte=2).filter(id__lte=4)
        assert results.count() == 3

    def test_order_by(self, create_tables):
        """order_by works with hashid field."""
        from tests.testapp.models import Article

        for i in range(5):
            Article.objects.create(title=f"Article {i}")

        ascending = list(Article.objects.order_by("id").values_list("id", flat=True))
        descending = list(Article.objects.order_by("-id").values_list("id", flat=True))

        assert ascending == sorted(ascending)
        assert descending == sorted(descending, reverse=True)

    def test_first_last(self, create_tables):
        """first() and last() work."""
        from tests.testapp.models import Article

        for i in range(3):
            Article.objects.create(title=f"Article {i}")

        first = Article.objects.order_by("id").first()
        last = Article.objects.order_by("id").last()

        assert int(first.id) < int(last.id)

    def test_exists(self, create_tables):
        """exists() works."""
        from tests.testapp.models import Article

        assert Article.objects.exists() is False

        Article.objects.create(title="Test")
        assert Article.objects.exists() is True

    def test_delete(self, create_tables):
        """delete() works."""
        from tests.testapp.models import Article

        article = Article.objects.create(title="To Delete")
        article_id = article.id

        article.delete()
        assert not Article.objects.filter(id=article_id).exists()

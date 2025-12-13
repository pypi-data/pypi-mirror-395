"""Tests for Django REST Framework integration.

Tests for T061-T063: DRF serialization (User Story 5).
"""

import pytest

# Skip all tests if DRF is not installed
pytest.importorskip("rest_framework")

from rest_framework import serializers

from hashid_field.hashid import Hashid
from hashid_field.rest import HashidSerializerCharField


class TestHashidSerializerCharField:
    """T061-T063: Tests for DRF HashidSerializerCharField."""

    def test_to_representation_with_hashid(self):
        """Serializes Hashid object to string."""
        field = HashidSerializerCharField()
        h = Hashid(123, salt="test")
        result = field.to_representation(h)

        assert isinstance(result, str)
        assert result == str(h)

    def test_to_representation_with_int(self):
        """Serializes integer to string."""
        field = HashidSerializerCharField()
        result = field.to_representation(42)

        assert isinstance(result, str)

    def test_to_representation_with_none(self):
        """Serializes None to None."""
        field = HashidSerializerCharField()
        result = field.to_representation(None)

        assert result is None

    def test_to_internal_value_with_hashid_string(self):
        """Deserializes hashid string to Hashid."""
        from hashid_field.conf import app_settings

        field = HashidSerializerCharField()

        # Create a valid hashid string using the same settings as the field will use
        h = Hashid(
            456,
            salt=app_settings.salt,
            min_length=app_settings.min_length,
            alphabet=app_settings.alphabet,
        )
        hashid_str = str(h)

        result = field.to_internal_value(hashid_str)

        assert isinstance(result, Hashid)
        assert result.id == 456

    def test_to_internal_value_with_int(self):
        """Deserializes integer to Hashid."""
        field = HashidSerializerCharField()
        result = field.to_internal_value(789)

        assert isinstance(result, Hashid)
        assert result.id == 789

    def test_to_internal_value_with_none(self):
        """Deserializes None to None."""
        field = HashidSerializerCharField()
        result = field.to_internal_value(None)

        assert result is None

    def test_to_internal_value_invalid_hashid(self):
        """Invalid hashid string raises ValidationError."""
        from rest_framework.exceptions import ValidationError

        field = HashidSerializerCharField()

        with pytest.raises(ValidationError):
            field.to_internal_value("invalid-hashid-string")


@pytest.mark.django_db
class TestModelSerializerIntegration:
    """Tests for integration with ModelSerializer."""

    def test_serialize_model_with_hashid(self, create_tables):
        """ModelSerializer serializes HashidField correctly."""
        from tests.testapp.models import Article

        class ArticleSerializer(serializers.ModelSerializer):
            class Meta:
                model = Article
                fields = ["id", "title"]

        article = Article.objects.create(title="Test Article")
        serializer = ArticleSerializer(article)

        data = serializer.data
        assert "id" in data
        assert "title" in data
        # The id should be serialized (either as Hashid or via default serialization)
        assert data["id"] is not None

    def test_serialize_multiple_models(self, create_tables):
        """Serializing multiple models works."""
        from tests.testapp.models import Article

        class ArticleSerializer(serializers.ModelSerializer):
            class Meta:
                model = Article
                fields = ["id", "title"]

        for i in range(3):
            Article.objects.create(title=f"Article {i}")

        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)

        data = serializer.data
        assert len(data) == 3

    def test_explicit_hashid_field_serializer(self, create_tables):
        """Explicit HashidSerializerCharField works in serializer."""
        from tests.testapp.models import Article

        class ArticleSerializer(serializers.ModelSerializer):
            id = HashidSerializerCharField(read_only=True)

            class Meta:
                model = Article
                fields = ["id", "title"]

        article = Article.objects.create(title="Test")
        serializer = ArticleSerializer(article)

        data = serializer.data
        assert isinstance(data["id"], str)

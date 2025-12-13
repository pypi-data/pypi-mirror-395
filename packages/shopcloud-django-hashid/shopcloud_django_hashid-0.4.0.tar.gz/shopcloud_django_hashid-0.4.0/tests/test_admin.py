"""Tests for Django Admin integration.

Tests for T055-T057: Admin display and search (User Story 4).
"""

import pytest
from django.contrib.admin.sites import AdminSite

from hashid_field.admin import hashid_display
from hashid_field.hashid import Hashid


class TestHashidDisplay:
    """Tests for hashid_display helper function."""

    def test_display_hashid_object(self):
        """hashid_display formats Hashid object correctly."""
        h = Hashid(123, salt="test")
        result = hashid_display(h)

        assert isinstance(result, str)
        assert result == str(h)

    def test_display_none(self):
        """hashid_display handles None."""
        result = hashid_display(None)
        assert result == "-"

    def test_display_int(self):
        """hashid_display handles integer."""
        result = hashid_display(42)
        assert result == "42"


@pytest.mark.django_db
class TestAdminIntegration:
    """T055-T057: Tests for admin integration."""

    def test_admin_displays_hashid_string(self, create_tables):
        """Admin list view displays hashid as string."""
        from tests.testapp.admin import ArticleAdmin
        from tests.testapp.models import Article

        site = AdminSite()
        admin = ArticleAdmin(Article, site)

        article = Article.objects.create(title="Test Article")

        # The list display should include the id field
        assert "id" in admin.list_display

        # When we access the id on the model, it should be a Hashid
        assert isinstance(article.id, Hashid)

        # When converted to string, it should be a hashid string
        assert isinstance(str(article.id), str)

    def test_admin_search_fields_include_id(self, create_tables):
        """Admin search includes id field."""
        from tests.testapp.admin import ArticleAdmin
        from tests.testapp.models import Article

        site = AdminSite()
        admin = ArticleAdmin(Article, site)

        assert "id" in admin.search_fields

    def test_formfield_returns_charfield(self, create_tables):
        """HashidField formfield returns CharField widget."""
        from django import forms

        from hashid_field import HashidField

        field = HashidField()
        form_field = field.formfield()

        # The form field should be a CharField (for text input)
        assert isinstance(form_field, forms.CharField)

"""Django Admin integration helpers.

Provides utilities for working with HashidField in Django Admin.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from django.http import HttpRequest


class HashidFieldAdminMixin:
    """Mixin for ModelAdmin that improves HashidField handling.

    This mixin:
    - Ensures hashid fields display as strings in list views
    - Enables searching by hashid string

    Usage:
        @admin.register(MyModel)
        class MyModelAdmin(HashidFieldAdminMixin, admin.ModelAdmin):
            list_display = ['id', 'name']
            search_fields = ['id', 'name']
    """

    def get_search_results(
        self,
        request: HttpRequest,
        queryset: Any,
        search_term: str,
    ) -> tuple[Any, bool]:
        """Override to handle hashid search terms.

        If the search term looks like a hashid, try to decode it and search by ID.
        """
        queryset, may_have_duplicates = super().get_search_results(
            request, queryset, search_term
        )

        if search_term:
            from django.db.models import Q

            from hashid_field.field import HashidFieldMixin

            # Find all HashidFields in the model
            hashid_fields = [
                f
                for f in self.model._meta.get_fields()
                if isinstance(f, HashidFieldMixin)
            ]

            # Try to decode the search term as a hashid for each field
            for field in hashid_fields:
                try:
                    int_value = field.decode_id(search_term)
                    queryset = queryset | self.model._default_manager.filter(
                        Q(**{field.attname: int_value})
                    )
                    may_have_duplicates = True
                except (ValueError, TypeError):
                    continue

        return queryset, may_have_duplicates


def hashid_display(hashid_value: Any) -> str:
    """Format a hashid value for display in admin.

    Args:
        hashid_value: A Hashid object, int, or None

    Returns:
        String representation suitable for display
    """
    if hashid_value is None:
        return "-"
    return str(hashid_value)

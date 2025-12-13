"""Django app configuration for hashid_field."""

from django.apps import AppConfig
from django.core import checks


class HashidFieldAppConfig(AppConfig):
    """App configuration for hashid_field."""

    name = "hashid_field"
    verbose_name = "Hashid Field"

    def ready(self) -> None:
        """Register system checks when the app is ready."""
        checks.register(check_salt, checks.Tags.security)


def check_salt(**kwargs):
    """Check if HASHID_FIELD_SALT is configured.

    Warns if the salt is empty, as this makes hashids predictable
    and undermines the obfuscation security aspect.
    """
    from hashid_field.conf import app_settings

    errors = []
    if not app_settings.salt:
        errors.append(
            checks.Warning(
                "HASHID_FIELD_SALT is not set. Using an empty salt is not secure.",
                hint="Set HASHID_FIELD_SALT in your project settings for proper obfuscation.",
                id="hashid_field.W001",
            )
        )
    return errors

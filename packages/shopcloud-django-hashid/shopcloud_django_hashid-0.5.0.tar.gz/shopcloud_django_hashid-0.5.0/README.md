# shopcloud-django-hashid

[![Tests](https://github.com/Talk-Point/shopcloud-django-hashid/actions/workflows/test.yml/badge.svg)](https://github.com/Talk-Point/shopcloud-django-hashid/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/shopcloud-django-hashid.svg)](https://badge.fury.io/py/shopcloud-django-hashid)
[![Coverage](https://codecov.io/gh/Talk-Point/shopcloud-django-hashid/branch/master/graph/badge.svg)](https://codecov.io/gh/Talk-Point/shopcloud-django-hashid)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Django 5.0+](https://img.shields.io/badge/django-5.0+-green.svg)](https://www.djangoproject.com/)

A drop-in replacement for [django-hashid-field](https://github.com/nshafer/django-hashid-field) with Django 5.x and 6.x support.

## Features

- **Drop-in compatible**: Same import paths and API as `django-hashid-field`
- **Django 5.x/6.x support**: Designed for modern Django versions
- **Zero migration effort**: Existing migrations work without changes
- **Identical hashid output**: Same salt produces same hashids
- **Full ORM support**: Works with all Django ORM operations
- **Django REST Framework integration**: Automatic serialization support
- **Thread-safe**: Safe for concurrent use in production

## Installation

```bash
pip install shopcloud-django-hashid
```

## Migration from django-hashid-field

```bash
pip uninstall django-hashid-field
pip install shopcloud-django-hashid
```

No code changes required. Your existing imports continue to work:

```python
from hashid_field import HashidField, HashidAutoField
from hashid_field import BigHashidField, BigHashidAutoField
from hashid_field import Hashid
```

Verify no migrations are needed:

```bash
python manage.py makemigrations --dry-run
# Should output: "No changes detected"
```

## Quick Start

### Model Definition

```python
from django.db import models
from hashid_field import HashidAutoField, HashidField

class Article(models.Model):
    id = HashidAutoField(primary_key=True)
    title = models.CharField(max_length=200)

class Comment(models.Model):
    id = HashidAutoField(primary_key=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    reference_code = HashidField()  # Non-primary key hashid
```

### Django Settings

```python
# settings.py

# Required: Set your salt (keep secret!)
HASHID_FIELD_SALT = "your-secret-salt-here"

# Optional: Customize defaults
HASHID_FIELD_MIN_LENGTH = 7
HASHID_FIELD_ALLOW_INT_LOOKUP = False
```

### Usage

```python
# Create
article = Article.objects.create(title="Hello World")
print(article.id)        # Hashid('kRm4x7')
print(str(article.id))   # 'kRm4x7'
print(int(article.id))   # 1

# Query by hashid string
article = Article.objects.get(pk='kRm4x7')
```

## Field Types

| Field | Base | Use Case |
|-------|------|----------|
| `HashidField` | `IntegerField` | General hashid storage |
| `BigHashidField` | `BigIntegerField` | Large integer hashids |
| `HashidAutoField` | `AutoField` | Primary key with hashid |
| `BigHashidAutoField` | `BigAutoField` | Big auto primary key |

## Settings

| Setting | Default | Description |
|---------|---------|-------------|
| `HASHID_FIELD_SALT` | `""` | Global salt for encoding |
| `HASHID_FIELD_MIN_LENGTH` | `7` | Minimum hashid length |
| `HASHID_FIELD_ALLOW_INT_LOOKUP` | `False` | Allow integer-based queries |
| `HASHID_FIELD_ENABLE_HASHID_OBJECT` | `True` | Return Hashid objects vs strings |

## Django REST Framework

If DRF is installed, HashidFields serialize automatically:

```python
from rest_framework import serializers
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title']
    # id will serialize as hashid string, e.g., "kRm4x7"
```

## Performance

- Fast encoding and decoding, suitable for production use
- Thread-safe: Yes, suitable for production environments

## Best Practices

1. **Set salt in production:**
   ```python
   # settings.py
   HASHID_FIELD_SALT = os.environ.get("HASHID_SALT", "your-secret-salt")
   ```

2. **Custom salts for sensitive fields:**
   ```python
   class Order(models.Model):
       id = HashidAutoField(primary_key=True, salt="order-specific-salt")
   ```

3. **Hashids are deterministic:** Same salt + same ID = same hashid

## Troubleshooting

| Problem | Cause | Solution |
|---------|-------|----------|
| "Invalid hashid" Error | Inconsistent salt | Set same salt in all environments |
| Performance issues | N+1 Queries | Use `select_related` and `prefetch_related` to eager-load related objects |
| Hashid changes | Salt changed | Never change salt in production |

## Settings Reference (Complete)

| Setting | Default | Description |
|---------|---------|-------------|
| `HASHID_FIELD_SALT` | `""` | Global salt for all fields |
| `HASHID_FIELD_MIN_LENGTH` | `7` | Minimum hashid length |
| `HASHID_FIELD_ALPHABET` | `hashids` library default | Allowed characters |
| `HASHID_FIELD_LOOKUP_EXCEPTION` | `False` | Raise exception on invalid lookups |
| `HASHID_FIELD_ALLOW_INT_LOOKUP` | `False` | Allow integer-based queries |
| `HASHID_FIELD_ENABLE_HASHID_OBJECT` | `True` | Return Hashid objects vs strings |

## Requirements

- Python 3.12+
- Django 5.0+
- hashids >= 1.3.1

## Publishing to PyPI (Maintainers)

This package uses PyPI Trusted Publishing for secure, token-free releases:

1. **Configure Trusted Publisher on PyPI**:
   - Log in to [pypi.org](https://pypi.org)
   - Go to your account → Publishing → Add a new trusted publisher
   - Set repository owner, name, and workflow file (`publish.yml`)

2. **Create a Release**:
   - Update version in `pyproject.toml` and `hashid_field/__init__.py`
   - Update `CHANGELOG.md`
   - Create a GitHub Release with a tag (e.g., `v0.1.0`)
   - The GitHub Action will automatically publish to PyPI

## License

MIT License - see [LICENSE](LICENSE) for details.

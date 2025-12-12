# 📚 Django Model Snapshots

> **Simple, efficient and intuitive version control for your Django models.**

[![Documentation](https://img.shields.io/badge/docs-live-brightgreen)](https://jotauses.github.io/django-model-snapshots/)
[![Tests](https://img.shields.io/badge/tests-passing-success)](https://github.com/jotauses/django-model-snapshots)
[![Coverage](https://img.shields.io/badge/coverage-94%25-success)](https://github.com/jotauses/django-model-snapshots)
[![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12%20|%203.13%20|%203.14-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-4.2%20|%205.0%20|%205.1%20|%205.2-green)](https://www.djangoproject.com/)

**Full Documentation**: [https://jotauses.github.io/django-model-snapshots/](https://jotauses.github.io/django-model-snapshots/)

## 📋 Requirements

*   **Python**: 3.10, 3.11, 3.12, 3.13, 3.14
*   **Django**: 4.2 (LTS), 5.0, 5.1, 5.2

---

## 🌟 Why Django Model Snapshots?

Tracking changes in your database shouldn't be a headache. You need a solution that is:

*   **Zero Config:** Just add a mixin and you're done.
*   **Ultra Efficient:** Optimized queries and bulk operations support.
*   **Flexible:** Automatic by default, but fully controllable when you need it.
*   **Developer Friendly:** Type-hinted, intuitive API (`as_of`, `between`).

## 🚀 Quick Start

### 1. Installation

```bash
pip install django-model-snapshots
```

### 2. Add to your App

Add `django_model_snapshots` to your `INSTALLED_APPS`:

```python
# settings.py
INSTALLED_APPS = [
    ...
    'django_model_snapshots',
    ...
]
```

### 3. Enable Versioning

Inherit from `VersionableMixin` in your model. That's it!

```python
from django.db import models
from django_model_snapshots import VersionableMixin

class Product(VersionableMixin, models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
```

Now, every time you `save()` or `delete()` a `Product`, a historical record is created automatically.

---

## 📖 Usage Guide

### Accessing History

Every versioned object gets a `.history` property. It's like a super-powered QuerySet.

```python
product = Product.objects.get(id=1)

# Get all versions
all_versions = product.history.all()

# Get the latest version
latest = product.history.latest()

# Get the earliest version
original = product.history.earliest()
```

### 🕰️ Time Travel (Efficient Querying)

Stop writing complex date filters. Use our intuitive API:

```python
from django.utils import timezone
from datetime import timedelta

# What did this product look like yesterday?
yesterday = timezone.now() - timedelta(days=1)
old_version = product.history.as_of(yesterday)

# Get all changes made last week
start = timezone.now() - timedelta(weeks=1)
end = timezone.now()
changes = product.history.between(start, end)
```

### 🎮 Manual Control

Sometimes you don't want to save every single keystroke. We give you full control.

**Disable Automatic Versioning:**

```python
class DraftPost(VersionableMixin, models.Model):
    title = models.CharField(max_length=100)
    
    # Disable auto-versioning for this model
    VERSIONING_AUTO = False 
```

**Force Versioning on Demand:**

Use the `force_versioning` context manager to create a version explicitly, even if `VERSIONING_AUTO` is False.

```python
from django_model_snapshots import force_versioning

post = DraftPost.objects.create(title="Draft") # No version created

# Make a major change and record it
with force_versioning():
    post.title = "Published"
    post.save() # Version created!
```

### ⚡ Performance & Bulk Operations

Creating thousands of records? Don't kill your database. Use `bulk_create_history`.

```python
from django_model_snapshots import bulk_create_history

products = [Product(name=f"Product {i}") for i in range(1000)]

# 1. Bulk create the main objects
Product.objects.bulk_create(products)

# 2. Bulk create their history (1 query!)
bulk_create_history(products)
```

### 🛠️ Configuration

**Select Specific Fields:**

By default, all fields are versioned. To save space, specify only what you need:

```python
class UserProfile(VersionableMixin, models.Model):
    bio = models.TextField()
    last_login = models.DateTimeField() # We might not want to version this
    
    # Only version the bio
    versioning_fields = ["bio"]
```

### 👮 Admin Integration

View history directly in the Django Admin.

```python
from django.contrib import admin
from django_model_snapshots import VersionAdmin
from .models import Product

@admin.register(Product)
class ProductAdmin(VersionAdmin):
    list_display = ("name", "price")
```

This adds a "History" button to the admin change view.

---

## 🧪 Running Tests

We use `pytest` for a robust testing suite.

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=django_model_snapshots
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1.  Fork the project
2.  Create your feature branch (`git checkout -b feature/AmazingFeature`)
3.  Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4.  Push to the branch (`git push origin feature/AmazingFeature`)
5.  Open a Pull Request

---

*Built for engineers who care about speed, clean code and type safety ❤️ by Joaquín Vázquez*

# Getting Started

## Installation

Install the package using pip:

```bash
pip install django-model-versions
```

## Configuration

Add `django_model_snapshots` to your `INSTALLED_APPS` in `settings.py`:

```python title="settings.py"
INSTALLED_APPS = [
    ...
    'django_model_snapshots',
    ...
]
```

## Quick Start

Inherit from `VersionableMixin` in your model. That's it!

```python title="models.py"
from django.db import models
from django_model_snapshots import VersionableMixin

class Product(VersionableMixin, models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
```

Now, every time you `save()` or `delete()` a `Product`, a historical record is created automatically.

```python
# Create a product (Version 1 created)
product = Product.objects.create(name="Laptop", price=1000)

# Update it (Version 2 created)
product.price = 900
product.save()

# Delete it (Version 3 created - deletion marker)
product.delete()
```

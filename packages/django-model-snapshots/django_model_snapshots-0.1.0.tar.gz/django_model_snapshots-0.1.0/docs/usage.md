# Usage Guide

## Accessing History

Every versioned object gets a `.history` property. It returns a `HistoryQuerySet` filtered for that object.

```python
product = Product.objects.get(id=1)

# Get all versions
all_versions = product.history.all()
```

## Efficient Querying (Time Travel)

Stop writing complex date filters. Use our intuitive API.

### `as_of(date)`

Get the version of the object as it existed at a specific time.

```python
from django.utils import timezone
from datetime import timedelta

yesterday = timezone.now() - timedelta(days=1)
old_version = product.history.as_of(yesterday)
```

### `between(start, end)`

Get all versions created within a time range.

```python
start = timezone.now() - timedelta(weeks=1)
end = timezone.now()
changes = product.history.between(start, end)
```

### `latest()`

Efficiently retrieve the most recent historical record.

```python
latest_version = product.history.latest()
```

### `earliest()`

Efficiently retrieve the oldest historical record.

```python
original_version = product.history.earliest()
```

## Admin Integration

To view history in the Django Admin, inherit from `VersionAdmin`.

```python title="admin.py"
from django.contrib import admin
from django_model_snapshots import VersionAdmin
from .models import Product

@admin.register(Product)
class ProductAdmin(VersionAdmin):
    list_display = ("name", "price")
```

This adds a **History** button to the change view of your model, allowing you to see a list of all historical changes.

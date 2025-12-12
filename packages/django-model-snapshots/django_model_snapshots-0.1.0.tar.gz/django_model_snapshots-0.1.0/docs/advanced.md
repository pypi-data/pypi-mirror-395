# Advanced Usage

## Manual Control

Sometimes you don't want to save every single keystroke. We give you full control.

### Disable Automatic Versioning

Set `VERSIONING_AUTO = False` on your model to disable automatic versioning on save/delete.

```python
class DraftPost(VersionableMixin, models.Model):
    title = models.CharField(max_length=100)
    
    # Disable auto-versioning for this model
    VERSIONING_AUTO = False 
```

### Force Versioning on Demand

Use the `force_versioning` context manager to create a version explicitly, even if `VERSIONING_AUTO` is False.

```python
from django_model_snapshots import force_versioning

post = DraftPost.objects.create(title="Draft") # No version created

# Make a major change and record it
with force_versioning():
    post.title = "Published"
    post.save() # Version created!
```

## Bulk Operations

Creating thousands of records? Don't kill your database with N+1 inserts. Use `bulk_create_history`.

```python
from django_model_snapshots import bulk_create_history

products = [Product(name=f"Product {i}") for i in range(1000)]

# 1. Bulk create the main objects
Product.objects.bulk_create(products)

# 2. Bulk create their history (1 query!)
bulk_create_history(products)
```

## Field Selection

By default, all fields are versioned. To save space, specify only what you need using `versioning_fields`.

```python
class UserProfile(VersionableMixin, models.Model):
    bio = models.TextField()
    last_login = models.DateTimeField() # We might not want to version this
    
    # Only version the bio
    versioning_fields = ["bio"]
```

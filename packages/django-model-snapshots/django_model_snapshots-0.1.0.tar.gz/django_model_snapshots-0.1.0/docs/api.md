# API Reference

## `VersionableMixin`

`django_model_snapshots.mixins.VersionableMixin`

Mixin to add versioning capabilities to a Django model.

**Attributes:**

*   `VERSIONING_AUTO` (bool): If `True` (default), creates a version on every `save()` and `delete()`.
*   `versioning_fields` (list[str], optional): List of field names to include in the history. If `None` (default), all fields are included.

**Properties:**

*   `history`: Returns a `HistoryQuerySet` filtered for the current instance.

---

## `HistoryQuerySet`

`django_model_snapshots.managers.HistoryQuerySet`

Custom QuerySet for historical models.

**Methods:**

### `as_of(date: datetime) -> Optional[Model]`

Returns the version of the object as it existed at the given date. Returns `None` if the object did not exist.

### `between(start: datetime, end: datetime) -> QuerySet`

Returns a QuerySet of versions that existed between the given start and end dates.

### `latest() -> Optional[Model]`

Returns the most recent historical record.

### `earliest() -> Optional[Model]`

Returns the oldest historical record.

---

## `force_versioning`

`django_model_snapshots.context.force_versioning`

Context manager to force versioning creation within a block, overriding `VERSIONING_AUTO=False`.

```python
with force_versioning():
    obj.save()
```

---

## `bulk_create_history`

`django_model_snapshots.utils.bulk_create_history`

**Signature:** `bulk_create_history(objs: List[Model], history_type: str = "+") -> None`

Efficiently creates history records for a list of objects in a single query.

*   `objs`: List of model instances (must be of the same class).
*   `history_type`: The type of history record ('+' for created, '~' for changed, '-' for deleted). Defaults to '+'.

---

## `VersionAdmin`

`django_model_snapshots.admin.VersionAdmin`

ModelAdmin subclass that adds a "History" button to the change view and renders a history list page.

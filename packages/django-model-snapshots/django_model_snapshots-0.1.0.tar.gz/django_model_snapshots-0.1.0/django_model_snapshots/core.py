import copy
from typing import Any, Optional, Type

from django.apps import apps
from django.db import models


def create_historical_record_model(
    model: Type[models.Model], versioning_fields: Optional[list[str]] = None
) -> Type[models.Model]:
    """
    Dynamically creates a historical model for the given model.
    """
    from .managers import HistoryManager

    attrs: dict[str, Any] = {
        "__module__": model.__module__,
        "objects": HistoryManager(),
    }
    # Copy fields
    for field in model._meta.fields:
        field_name = field.name

        if (
            versioning_fields
            and field_name not in versioning_fields
            and field_name != model._meta.pk.name
        ):
            continue

        new_field = copy.copy(field)
        if hasattr(field, "remote_field") and field.remote_field:
            new_field.remote_field = copy.copy(field.remote_field)

        if isinstance(field, models.ForeignKey):
            new_field.remote_field.on_delete = models.DO_NOTHING
            new_field.remote_field.related_name = "+"
            new_field.null = True
            new_field.blank = True
            new_field.db_constraint = False

        if isinstance(field, models.AutoField):
            new_field = models.IntegerField(name=field.name)
        elif isinstance(field, models.BigAutoField):
            new_field = models.BigIntegerField(name=field.name)

        # Ensure it's not unique in history (multiple versions of same object)
        new_field._unique = False  # pragma: no cover
        new_field.db_index = True

        # If it was the primary key, we need to make sure it's not PK in history
        if field.primary_key:
            new_field.primary_key = False
            new_field.serialize = True
            new_field._unique = False  # pragma: no cover
            new_field.db_index = True

        attrs[field_name] = new_field

    # Add history specific fields
    attrs["history_id"] = models.AutoField(primary_key=True)
    attrs["history_date"] = models.DateTimeField(auto_now_add=True)
    attrs["history_type"] = models.CharField(
        max_length=1,
        choices=(
            ("+", "Created"),
            ("~", "Changed"),
            ("-", "Deleted"),
        ),
    )

    # Add Meta
    class Meta:
        app_label = model._meta.app_label

    attrs["Meta"] = Meta

    name = f"{model.__name__}History"

    # Check if already registered to avoid RuntimeError
    try:
        return apps.get_model(model._meta.app_label, name, require_ready=False)
    except LookupError:
        pass

    return type(name, (models.Model,), attrs)

    return history_model

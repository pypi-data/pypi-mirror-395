from typing import Any, Type

from django.db import models

from .context import is_versioning_forced


def save_history(
    sender: Type[models.Model], instance: models.Model, created: bool, **kwargs: Any
) -> None:
    """
    Signal handler to save a historical record when a model is saved.
    """
    # Check if versioning is enabled for this model
    if not getattr(sender, "VERSIONING_AUTO", True) and not is_versioning_forced():
        return

    history_model = getattr(sender, "_history_model", None)

    history_type = "+" if created else "~"

    if history_model:
        data = {}
        cached_fields: list[str] = getattr(sender, "_cached_history_fields", [])

        for field_name in cached_fields:
            try:
                val = getattr(instance, field_name)
                data[field_name] = val
            except AttributeError:
                pass

        data["history_type"] = history_type

        pk_name = sender._meta.pk.name
        data[pk_name] = instance.pk

        history_model.objects.create(**data)


def delete_history(
    sender: Type[models.Model], instance: models.Model, **kwargs: Any
) -> None:
    """
    Signal handler to save a historical record when a model is deleted.
    """
    # Check if versioning is enabled for this model
    if not getattr(sender, "VERSIONING_AUTO", True) and not is_versioning_forced():
        return

    history_model = getattr(sender, "_history_model", None)

    data = {}
    cached_fields: list[str] = getattr(sender, "_cached_history_fields", [])

    for field_name in cached_fields:
        try:
            val = getattr(instance, field_name)
            data[field_name] = val
        except AttributeError:
            pass

    data["history_type"] = "-"
    pk_name = sender._meta.pk.name
    data[pk_name] = instance.pk

    if history_model:
        history_model.objects.create(**data)

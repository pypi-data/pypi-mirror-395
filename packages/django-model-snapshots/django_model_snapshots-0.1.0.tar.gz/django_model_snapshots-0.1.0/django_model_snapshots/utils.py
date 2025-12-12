from typing import List

from django.db import models


def bulk_create_history(objs: List[models.Model], history_type: str = "+") -> None:
    """
    Efficiently create history records for a list of objects.
    All objects must be of the same model class.
    """
    if not objs:
        return

    model = objs[0].__class__
    history_model = getattr(model, "_history_model", None)
    if not history_model:
        return

    history_objs: List[models.Model] = []

    # Use cached fields if available, otherwise calculate
    cached_fields: List[str] = getattr(model, "_cached_history_fields", [])

    if not cached_fields:
        # Pre-calculate field mapping to avoid repeated lookups
        for field in model._meta.fields:
            field_name = field.name
            if field_name == "id" or field_name == "pk":
                continue
            try:
                history_model._meta.get_field(field_name)
                cached_fields.append(field_name)
            except Exception:
                pass

    for obj in objs:
        data = {}
        for field_name in cached_fields:
            data[field_name] = getattr(obj, field_name)

        data["history_type"] = history_type

        pk_name = model._meta.pk.name
        data[pk_name] = obj.pk

        history_objs.append(history_model(**data))

    history_model.objects.bulk_create(history_objs)

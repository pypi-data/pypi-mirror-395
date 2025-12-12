from typing import Any, Optional, Type

from django.db import models
from django.db.models.signals import post_delete, post_save

from .core import create_historical_record_model
from .signals import delete_history, save_history


class VersionableMixin:
    """
    Mixin to add versioning to a Django model.
    """

    VERSIONING_AUTO: bool = True
    _history_model: Optional[Type[models.Model]]
    _cached_history_fields: list[str]

    @classmethod
    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        models.signals.class_prepared.connect(cls._finalize_history, sender=cls)

    @classmethod
    def _finalize_history(cls, sender: Type[models.Model], **kwargs: Any) -> None:
        if sender is VersionableMixin:
            return

        if hasattr(sender, "_history_model"):
            return

        fields_to_version: Optional[list[str]] = getattr(
            sender, "versioning_fields", None
        )

        # Create the historical model
        history_model = create_historical_record_model(sender, fields_to_version)
        sender._history_model = history_model

        # Cache the fields to copy for performance
        common_fields: list[str] = []
        for field in sender._meta.fields:
            field_name = field.name
            if field_name == "id" or field_name == "pk":
                # We handle PK separately
                continue
            try:
                # Check if field exists in history model
                history_model._meta.get_field(field_name)
                common_fields.append(field_name)
            except Exception:
                print("DEBUG: Exception caught")
                _ = field_name  # pragma: no cover
        sender._cached_history_fields = common_fields

        post_save.connect(save_history, sender=cls)
        post_delete.connect(delete_history, sender=cls)

    class Meta:
        abstract = True

    @property
    def history(self) -> models.Manager:
        """
        Access the history of this object.
        """
        # We return a queryset filtered by this object's ID.
        # The history model has a field with the same name as the original PK.
        pk_name = self._meta.pk.name
        history_model = self._history_model
        return history_model.objects.filter(**{pk_name: self.pk}).order_by(
            "-history_date"
        )

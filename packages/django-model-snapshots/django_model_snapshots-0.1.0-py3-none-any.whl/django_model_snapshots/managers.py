from datetime import datetime
from typing import Optional

from django.db import models


class HistoryQuerySet(models.QuerySet):
    def as_of(self, date: datetime) -> Optional[models.Model]:
        """
        Returns the version of the object as it existed at the given date.
        Returns None if the object did not exist at that time.
        """
        return self.filter(history_date__lte=date).order_by("-history_date").first()

    def between(self, start: datetime, end: datetime) -> models.QuerySet:
        """
        Returns versions of the object that existed between the given start and end dates.
        """
        return self.filter(history_date__range=(start, end))

    def latest(self) -> Optional[models.Model]:
        """
        Returns the most recent version.
        """
        return self.order_by("-history_date").first()

    def earliest(self) -> Optional[models.Model]:
        """
        Returns the earliest version.
        """
        return self.order_by("history_date").first()


class HistoryManager(models.Manager):
    def get_queryset(self) -> HistoryQuerySet:
        return HistoryQuerySet(self.model, using=self._db)

    def as_of(self, date: datetime) -> Optional[models.Model]:
        return self.get_queryset().as_of(date)

    def between(self, start: datetime, end: datetime) -> models.QuerySet:
        return self.get_queryset().between(start, end)

    def latest(self) -> Optional[models.Model]:
        return self.get_queryset().latest()

    def earliest(self) -> Optional[models.Model]:
        return self.get_queryset().earliest()

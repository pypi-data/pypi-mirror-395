from django.db import models

from django_model_snapshots.mixins import VersionableMixin


class BasicModel(VersionableMixin, models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()

    class Meta:
        app_label = "test_app"


class ConfiguredModel(VersionableMixin, models.Model):
    name = models.CharField(max_length=100)
    secret = models.CharField(max_length=100)

    versioning_fields = ["name"]

    class Meta:
        app_label = "test_app"


class DestructiveModel(VersionableMixin, models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "test_app"


class RelationalModel(VersionableMixin, models.Model):
    name = models.CharField(max_length=100)
    related = models.ForeignKey(BasicModel, on_delete=models.CASCADE)

    class Meta:
        app_label = "test_app"


class AdminModel(VersionableMixin, models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        app_label = "test_app"


class ExcludedFieldModel(VersionableMixin, models.Model):
    name = models.CharField(max_length=100)
    secret = models.CharField(max_length=100)
    versioning_fields = ["name"]

    class Meta:
        app_label = "test_app"

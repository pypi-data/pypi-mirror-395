import pytest
from django.db import models
from django_model_snapshots.mixins import VersionableMixin
from django_model_snapshots.context import force_versioning

class ManualVersionModel(VersionableMixin, models.Model):
    name = models.CharField(max_length=100)
    VERSIONING_AUTO = False
    
    class Meta:
        app_label = 'test_app'

@pytest.mark.django_db
def test_manual_versioning_disabled_by_default():
    obj = ManualVersionModel.objects.create(name="No Version")
    assert obj.history.count() == 0
    
    obj.name = "Updated"
    obj.save()
    assert obj.history.count() == 0
    
    obj.delete()
    # History is on the model class for deleted objects, but since we didn't create any...
    # We can check the history model directly
    assert ManualVersionModel._history_model.objects.count() == 0

@pytest.mark.django_db
def test_force_versioning_context():
    with force_versioning():
        obj = ManualVersionModel.objects.create(name="Versioned")
        
    assert obj.history.count() == 1
    assert obj.history.first().name == "Versioned"
    
    # Outside context, should not version
    obj.name = "Not Versioned Update"
    obj.save()
    assert obj.history.count() == 1
    
    # Inside context again
    with force_versioning():
        obj.name = "Versioned Update"
        obj.save()
        
    assert obj.history.count() == 2
    assert obj.history.first().name == "Versioned Update"

@pytest.mark.django_db
def test_force_versioning_delete():
    obj = ManualVersionModel.objects.create(name="To Delete")
    assert obj.history.count() == 0
    
    with force_versioning():
        obj.delete()
        
    # Check history model directly as instance is deleted
    history = ManualVersionModel._history_model.objects.all()
    assert history.count() == 1
    assert history.first().history_type == '-'
    assert history.first().name == "To Delete"

@pytest.mark.django_db
def test_nested_context():
    # Should handle nesting correctly (idempotent or stacked)
    # Our implementation uses a boolean set, so nesting just keeps it True.
    # But we need to ensure inner exit doesn't disable it if outer is still active?
    # ContextVar.reset restores previous value.
    
    with force_versioning():
        with force_versioning():
            obj = ManualVersionModel.objects.create(name="Nested")
            assert obj.history.count() == 1
        
        # Should still be enabled
        obj.name = "Outer"
        obj.save()
        assert obj.history.count() == 2
        
    # Should be disabled
    obj.name = "Disabled"
    obj.save()
    assert obj.history.count() == 2

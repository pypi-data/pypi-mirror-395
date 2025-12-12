import pytest
from django.utils import timezone
from datetime import timedelta
from tests.models import BasicModel
import time

@pytest.mark.django_db
def test_history_queries():
    # Create object and history
    obj = BasicModel.objects.create(name="Version 1", age=20)
    time.sleep(0.1) # Ensure time difference
    t1 = timezone.now()
    
    obj.name = "Version 2"
    obj.save()
    time.sleep(0.1)
    t2 = timezone.now()
    
    obj.name = "Version 3"
    obj.save()
    time.sleep(0.1)
    t3 = timezone.now()
    
    # Test as_of
    assert obj.history.as_of(t1).name == "Version 1"
    assert obj.history.as_of(t2).name == "Version 2"
    assert obj.history.as_of(t3).name == "Version 3"
    
    # Test between
    # Use a wider window to avoid microsecond precision issues
    start = t1 - timedelta(seconds=1)
    end = t2 + timedelta(seconds=1)
    versions = obj.history.between(start, end)
    
    # Should include Version 1 and Version 2
    # Note: t3 is after t2 + 1s (due to sleep 0.1s? No, sleep is 0.1s, so t3 is ~0.1s after t2)
    # Wait, t1 (v1) -> sleep 0.1 -> t2 (v2) -> sleep 0.1 -> t3 (v3)
    # t2 + 1s covers t3 as well!
    # We want strictly between t1 and t2.
    
    # Let's be more precise with the window
    # t1 is time of v1 creation (approx)
    # t2 is time of v2 update
    # t3 is time of v3 update
    
    # We want v1 and v2.
    # v1.history_date <= t1 (roughly)
    # v2.history_date <= t2
    # v3.history_date <= t3
    
    # Let's check the actual dates
    v1_date = obj.history.get(name="Version 1").history_date
    v2_date = obj.history.get(name="Version 2").history_date
    v3_date = obj.history.get(name="Version 3").history_date
    
    midpoint = v2_date + (v3_date - v2_date) / 2
    
    versions = obj.history.between(v1_date - timedelta(seconds=1), midpoint)
    
    assert versions.count() == 2
    names = set(v.name for v in versions)
    assert "Version 1" in names
    assert "Version 2" in names
    
    # Test latest
    assert obj.history.latest().name == "Version 3"
    
    # Test earliest
    assert obj.history.earliest().name == "Version 1"

@pytest.mark.django_db
def test_history_manager_direct_access():
    # Test accessing methods directly via the manager (not through instance.history)
    obj = BasicModel.objects.create(name="Direct Manager", age=30)
    
    HistoryModel = BasicModel._history_model
    
    assert HistoryModel.objects.latest().name == "Direct Manager"
    assert HistoryModel.objects.as_of(timezone.now()).name == "Direct Manager"

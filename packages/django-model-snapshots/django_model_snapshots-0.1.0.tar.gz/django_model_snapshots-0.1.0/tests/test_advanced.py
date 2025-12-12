import pytest

from tests.models import BasicModel


@pytest.mark.django_db
def test_history_property():
    obj = BasicModel.objects.create(name="Test", age=25)
    obj.name = "Updated"
    obj.save()

    assert obj.history.count() == 2
    assert obj.history.first().name == "Updated"
    assert obj.history.last().name == "Test"


@pytest.mark.django_db
def test_bulk_create_no_history():
    # bulk_create does not trigger signals, so history should NOT be created by default
    objs = [
        BasicModel(name="Bulk1", age=1),
        BasicModel(name="Bulk2", age=2),
    ]
    BasicModel.objects.bulk_create(objs)

    HistoryModel = BasicModel._history_model
    assert HistoryModel.objects.count() == 0

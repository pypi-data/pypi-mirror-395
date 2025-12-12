import pytest

from tests.models import BasicModel


@pytest.mark.django_db
def test_versioning_creation():
    # Create an instance
    obj = BasicModel.objects.create(name="Test", age=25)

    # Check if history model exists
    assert hasattr(BasicModel, "_history_model")
    HistoryModel = BasicModel._history_model

    # Check if history record was created
    assert HistoryModel.objects.count() == 1
    history = HistoryModel.objects.first()
    assert history.name == "Test"
    assert history.age == 25
    assert history.history_type == "+"


@pytest.mark.django_db
def test_versioning_update():
    obj = BasicModel.objects.create(name="Test", age=25)

    obj.name = "Updated"
    obj.save()

    HistoryModel = BasicModel._history_model
    assert HistoryModel.objects.count() == 2

    latest = HistoryModel.objects.last()
    assert latest.name == "Updated"
    assert latest.history_type == "~"


@pytest.mark.django_db
def test_versioning_delete():
    obj = BasicModel.objects.create(name="Test", age=25)
    obj.delete()

    HistoryModel = BasicModel._history_model
    assert HistoryModel.objects.count() == 2  # Create + Delete

    latest = HistoryModel.objects.last()
    assert latest.history_type == "-"

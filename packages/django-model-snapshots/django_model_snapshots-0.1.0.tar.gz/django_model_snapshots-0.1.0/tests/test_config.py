import pytest

from tests.models import ConfiguredModel


@pytest.mark.django_db
def test_field_configuration():
    obj = ConfiguredModel.objects.create(name="Public", secret="Hidden")

    HistoryModel = ConfiguredModel._history_model
    history = HistoryModel.objects.first()

    assert history.name == "Public"
    assert not hasattr(history, "secret")

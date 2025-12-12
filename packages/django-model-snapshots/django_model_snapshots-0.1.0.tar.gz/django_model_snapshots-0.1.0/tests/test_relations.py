import pytest

from tests.models import BasicModel, RelationalModel


@pytest.mark.django_db
def test_foreign_key_versioning():
    basic = BasicModel.objects.create(name="Parent", age=50)
    rel = RelationalModel.objects.create(name="Child", related=basic)

    # Check history
    history = rel.history.first()
    assert history.name == "Child"
    assert history.related == basic

    # Delete parent
    basic.delete()

    # Reload history
    history = RelationalModel._history_model.objects.get(pk=history.pk)
    # Accessing related might fail now if the row is gone
    try:
        print(history.related)
    except Exception:
        pass

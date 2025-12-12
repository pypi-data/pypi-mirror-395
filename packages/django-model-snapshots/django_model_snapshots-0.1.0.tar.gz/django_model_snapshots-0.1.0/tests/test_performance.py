import time

import pytest

from django_model_snapshots.utils import bulk_create_history
from tests.models import BasicModel


@pytest.mark.django_db
def test_performance_single_save():
    start = time.time()
    for i in range(100):
        BasicModel.objects.create(name=f"Test {i}", age=i)
    end = time.time()
    print(f"\n100 creates with history: {end - start:.4f}s")

    assert BasicModel._history_model.objects.count() == 100


@pytest.mark.django_db
def test_performance_bulk_create_history():
    objs = [BasicModel(name=f"Bulk {i}", age=i) for i in range(1000)]
    BasicModel.objects.bulk_create(objs)

    start = time.time()
    bulk_create_history(objs)
    end = time.time()
    print(f"\n1000 bulk history creates: {end - start:.4f}s")

    assert BasicModel._history_model.objects.count() == 1000

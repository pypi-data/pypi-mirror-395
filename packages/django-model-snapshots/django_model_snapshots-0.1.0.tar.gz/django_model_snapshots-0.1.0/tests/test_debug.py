import pytest
from django.apps import apps


@pytest.mark.django_db
def test_debug_models():
    print("Installed apps:", [app.label for app in apps.get_app_configs()])
    print("Registered models:", [m._meta.label for m in apps.get_models()])

    from tests.models import RelationalModel

    print("RelationalModel label:", RelationalModel._meta.label)

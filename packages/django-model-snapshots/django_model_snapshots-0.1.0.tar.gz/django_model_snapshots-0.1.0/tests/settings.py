SECRET_KEY = "fake-key"
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django_model_snapshots",
    "tests.apps.TestsConfig",
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}
USE_TZ = True

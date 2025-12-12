# Django Model Versions

> **Simple, efficient and intuitive version control for your Django models.**

[![Tests](https://img.shields.io/badge/tests-passing-success)](https://github.com/jotauses/django-model-versions)
[![Coverage](https://img.shields.io/badge/coverage-94%25-success)](https://github.com/jotauses/django-model-versions)
[![Python](https://img.shields.io/badge/python-3.14-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-5.0%2B-green)](https://www.djangoproject.com/)

---

## Why Django Model Versions?

Tracking changes in your database shouldn't be a headache. You need a solution that is:

*   **Zero Config:** Just add a mixin and you're done.
*   **Ultra Efficient:** Optimized queries and bulk operations support.
*   **Flexible:** Automatic by default, but fully controllable when you need it.
*   **Developer Friendly:** Type-hinted, intuitive API (`as_of`, `between`).

## Key Features

*   **Automatic Versioning**: Saves a copy of your model on every `save` and `delete`.
*   **Efficient Querying**: Time travel made easy with `as_of`, `between`, `latest`, and `earliest`.
*   **Manual Control**: Opt-out of automatic versioning and use context managers for specific updates.
*   **Bulk Operations**: Create history for thousands of records in a single query.
*   **Admin Integration**: Built-in support for viewing history in Django Admin.

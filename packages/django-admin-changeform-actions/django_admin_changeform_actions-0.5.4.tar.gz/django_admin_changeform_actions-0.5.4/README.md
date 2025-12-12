# django-admin-changeform-actions

[![Run pytest](https://github.com/cb109/django-admin-changeform-actions/actions/workflows/pytest.yml/badge.svg)](https://github.com/cb109/django-admin-changeform-actions/actions/workflows/pytest.yml)
[![Run tox](https://github.com/cb109/django-admin-changeform-actions/actions/workflows/tox.yml/badge.svg)](https://github.com/cb109/django-admin-changeform-actions/actions/workflows/tox.yml)

Replicates the admin
[actions](https://docs.djangoproject.com/en/dev/ref/contrib/admin/actions/)
dropdown (available on a model's `changelist` page) on each model
instance's `changeform` page.

<img src="https://raw.githubusercontent.com/cb109/django-admin-changeform-actions/refs/heads/main/docs/changeform_actions_ui.png" width="800">

Instead of targetting a selection the action will target the current
model instance only.

## Installation

Install the package:

```bash
pip install django-admin-changeform-actions
```

Modify your Django project like:

```py
# settings.py

INSTALLED_APPS = [
  "changeform_actions",  # Must be placed before Django's admin app!
  ...
  "django.contrib.admin",
]
```

```py
# urls.py

urlpatterns = [
  path("", include("changeform_actions.urls"))
]
```

```py
# admin.py

from changeform_actions import ChangeFormActionsMixin

class MyModelAdmin(ChangeFormActionsMixin, admin.ModelAdmin):
    actions = [...]
```

## Development Setup

This project uses [uv](https://docs.astral.sh/uv/) to handle python versions and dependencies.

```bash
uv sync
```

To do a new release, bump the version in `pyproject.toml`, then:
```bash
uv build
uv publish
```

## Tests

```bash
uv run pytest
```

Run test matrix of different python versions VS different django versions:
```bash
uv run tox
```

import pytest
from django.conf import settings
from django.contrib.auth.models import User
from django.test import Client
from django.urls import resolve, reverse

from tests.models import MyModel


@pytest.mark.django_db
class TestIntegration:
    def test_app_installed(self):
        assert "changeform_actions" in settings.INSTALLED_APPS

    def test_urls_included(self):
        match = resolve(reverse("changeform_actions:run_admin_changeform_action"))
        assert match.app_name == "changeform_actions"
        assert match.url_name == "run_admin_changeform_action"

    def test_admin_mixin_importable(self):
        from changeform_actions import ChangeFormActionsMixin

        assert ChangeFormActionsMixin is not None

    def test_changeform_has_actions_dropdown(self):
        # Setup
        User.objects.create_superuser("admin", "admin@example.com", "password")
        client = Client()
        client.login(username="admin", password="password")

        instance = MyModel.objects.create(name="Test")

        # Test: Get changeform page and check that the dropdown is present
        changeform_url: str = reverse("admin:tests_mymodel_change", args=[instance.pk])
        response = client.get(changeform_url)
        assert response.status_code == 200
        assert b'<select name="action"' in response.content


@pytest.mark.django_db
class TestRunAction:
    def test_run_action_needs_staff_user_login(self):
        # Setup
        User.objects.create_user("user", "user@example.com", "password")
        client = Client()
        client.login(username="user", password="password")

        instance = MyModel.objects.create(name="Test")

        # Test: Redirected to admin login instead
        run_action_url: str = reverse("changeform_actions:run_admin_changeform_action")
        response = client.post(
            run_action_url,
            data={
                "app_label": "tests",
                "model_name": "mymodel",
                "pk": str(instance.pk),
                "action": "add_copy_suffix",
            },
            HTTP_REFERER=reverse("admin:tests_mymodel_change", args=[instance.pk]),
        )
        assert response.status_code == 302
        assert response.url.startswith(reverse("admin:login"))

    def test_run_action(self):
        # Setup
        User.objects.create_superuser("admin", "admin@example.com", "password")
        client = Client()
        client.login(username="admin", password="password")

        instance = MyModel.objects.create(name="Test")

        # Test: Run action renames the model instance
        changeform_url: str = reverse("admin:tests_mymodel_change", args=[instance.pk])
        run_action_url: str = reverse("changeform_actions:run_admin_changeform_action")
        response = client.post(
            run_action_url,
            data={
                "app_label": "tests",
                "model_name": "mymodel",
                "pk": str(instance.pk),
                "action": "add_copy_suffix",
            },
            HTTP_REFERER=changeform_url,
            follow=True,
        )
        assert response.status_code == 200
        assert response.request["PATH_INFO"] == changeform_url

        instance.refresh_from_db()
        assert instance.name == "Test - copy"

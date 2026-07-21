from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.urls import reverse


class SupabaseEnvTests(SimpleTestCase):
    def test_publishable_key_is_available_for_public_code(self):
        self.assertTrue(settings.SUPABASE_URL)
        self.assertTrue(settings.SUPABASE_PUBLISHABLE_KEY)

    def test_secret_key_is_not_referenced_outside_backend_settings(self):
        project_root = Path(settings.BASE_DIR)
        allowed_files = {
            project_root / "config" / "settings.py",
            project_root / "config" / "supabase.py",
            project_root / "config" / "tests.py",
        }

        hits = []
        for path in project_root.rglob("*.py"):
            if path in allowed_files:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "SUPABASE_SECRET_KEY" in text:
                hits.append(str(path))

        self.assertEqual(
            hits,
            [],
            msg=f"SUPABASE_SECRET_KEY leaked into non-backend code: {hits}",
        )

    def test_no_supabase_keys_are_referenced_by_templates_or_frontend_files(self):
        frontend_suffixes = {".html", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte"}
        hits = []

        for path in Path(settings.BASE_DIR).rglob("*"):
            if not path.is_file() or path.suffix.lower() not in frontend_suffixes:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "SUPABASE_" in text or "DATABASE_URL" in text:
                hits.append(str(path))

        self.assertEqual(hits, [])


class ProtectedApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            username="secure-user",
            password="test-password",
        )

    def assertNoSecretValues(self, response):
        body = response.content.decode("utf-8")
        secrets = (
            settings.SECRET_KEY,
            settings.SUPABASE_SECRET_KEY,
            settings.SUPABASE_PUBLISHABLE_KEY,
            settings.DATABASES["default"].get("PASSWORD"),
        )
        for secret in secrets:
            if secret:
                self.assertNotIn(secret, body)

    def test_protected_profile_rejects_unauthenticated_access(self):
        response = self.client.get(reverse("protected-profile"))

        self.assertEqual(response.status_code, 401)
        self.assertNoSecretValues(response)

    def test_protected_profile_returns_no_secret_values(self):
        self.client.login(username="secure-user", password="test-password")

        response = self.client.get(reverse("protected-profile"))

        self.assertEqual(response.status_code, 200)
        self.assertNoSecretValues(response)
        self.assertEqual(response.json()["username"], "secure-user")

    def test_private_storage_endpoint_rejects_unauthenticated_access(self):
        response = self.client.post(
            reverse("private-storage-url"),
            data={"path": "customers/example.pdf"},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 401)
        self.assertNoSecretValues(response)

    @override_settings(SUPABASE_SIGNED_URL_TTL_SECONDS=60)
    @patch("config.views.create_private_storage_signed_url")
    def test_private_storage_endpoint_returns_short_lived_url_without_keys(self, signed_url):
        signed_url.return_value = {
            "signed_url": "https://example.supabase.co/storage/v1/object/sign/private/file?token=test",
            "expires_in": 60,
        }
        self.client.login(username="secure-user", password="test-password")

        response = self.client.post(
            reverse("private-storage-url"),
            data={"path": "customers/example.pdf", "expires_in": 60},
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["expires_in"], 60)
        self.assertNoSecretValues(response)

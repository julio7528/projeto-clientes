import json
import logging
import uuid
from pathlib import Path
from unittest.mock import patch

from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from .logging import SecretRedactionFilter
from .models import ProtectedFile
from .supabase import SupabaseServiceError, create_private_storage_signed_url


class SupabaseEnvTests(SimpleTestCase):
    def test_backend_supabase_configuration_is_available(self):
        self.assertTrue(settings.SUPABASE_URL)
        self.assertTrue(settings.SUPABASE_SECRET_KEY)
        self.assertIsInstance(settings.SUPABASE_PUBLISHABLE_KEY, str)

    def test_secret_key_is_not_referenced_outside_backend_allowlist(self):
        project_root = Path(settings.BASE_DIR)
        allowed_files = {
            project_root / "config" / "settings.py",
            project_root / "config" / "supabase.py",
            project_root / "config" / "tests.py",
            project_root / "usuarios" / "tests.py",
        }
        hits = []

        for path in project_root.rglob("*.py"):
            if path in allowed_files:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "SUPABASE_SECRET_KEY" in text:
                hits.append(str(path))

        self.assertEqual(hits, [])

    def test_no_supabase_keys_are_referenced_by_browser_files(self):
        browser_suffixes = {".html", ".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte"}
        hits = []

        for path in Path(settings.BASE_DIR).rglob("*"):
            if not path.is_file() or path.suffix.lower() not in browser_suffixes:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            if "SUPABASE_" in text or "DATABASE_URL" in text:
                hits.append(str(path))

        self.assertEqual(hits, [])


class LoggingRedactionTests(SimpleTestCase):
    @override_settings(LOG_REDACTED_SECRETS=("top-secret",))
    def test_sensitive_log_material_is_redacted(self):
        record = logging.LogRecord(
            "security-test",
            logging.WARNING,
            __file__,
            1,
            "top-secret Authorization: Bearer token-value "
            "postgresql://user:password@host/db "
            "https://example.supabase.co/storage/v1/object/sign/private/a?token=signed",
            (),
            None,
        )

        SecretRedactionFilter().filter(record)
        message = record.getMessage()

        self.assertNotIn("top-secret", message)
        self.assertNotIn("token-value", message)
        self.assertNotIn("password", message)
        self.assertNotIn("token=signed", message)


class SupabaseServiceTests(SimpleTestCase):
    @override_settings(SUPABASE_SIGNED_URL_TTL_SECONDS=60)
    @patch("config.supabase.urlopen")
    def test_requested_ttl_is_capped_by_configured_maximum(self, urlopen):
        response = urlopen.return_value.__enter__.return_value
        response.read.return_value = json.dumps({"signedURL": "/signed"}).encode()

        result = create_private_storage_signed_url("owners/file.pdf", expires_in=3600)
        sent_payload = json.loads(urlopen.call_args.args[0].data.decode())

        self.assertEqual(result["expires_in"], 60)
        self.assertEqual(sent_payload["expiresIn"], 60)


class ProtectedApiTests(TestCase):
    def setUp(self):
        self.client = Client()
        user_model = get_user_model()
        self.user_a = user_model.objects.create_user(
            email="user-a@example.test",
            nome_completo="User A",
            password="test-password",
        )
        self.user_b = user_model.objects.create_user(
            email="user-b@example.test",
            nome_completo="User B",
            password="test-password",
        )
        self.file_a = ProtectedFile.objects.create(
            owner=self.user_a,
            storage_path="owners/user-a/document.pdf",
            original_name="document.pdf",
        )
        self.file_b = ProtectedFile.objects.create(
            owner=self.user_b,
            storage_path="owners/user-b/private.pdf",
            original_name="private.pdf",
        )

    def assert_no_secret_values(self, response):
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

    def post_storage(self, payload, **extra):
        return self.client.post(
            reverse("private-storage-url"),
            data=json.dumps(payload),
            content_type="application/json",
            **extra,
        )

    def login_user_a(self):
        self.client.force_login(self.user_a)

    def test_anonymous_storage_access_is_rejected(self):
        response = self.post_storage({"arquivo_id": str(self.file_a.pk)})
        self.assertEqual(response.status_code, 401)
        self.assert_no_secret_values(response)

    @patch("config.views.create_private_storage_signed_url")
    def test_owner_receives_signed_url_with_no_cache_headers(self, signed_url):
        signed_url.return_value = {
            "signed_url": "https://example.supabase.co/signed?token=short",
            "expires_in": 60,
        }
        self.login_user_a()

        response = self.post_storage({"arquivo_id": str(self.file_a.pk)})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Cache-Control"], "no-store, private")
        self.assertEqual(response["Pragma"], "no-cache")
        signed_url.assert_called_once_with(self.file_a.storage_path, expires_in=None)
        self.assert_no_secret_values(response)

    @patch("config.views.create_private_storage_signed_url")
    def test_user_a_is_denied_access_to_user_b_file(self, signed_url):
        self.login_user_a()
        response = self.post_storage({"arquivo_id": str(self.file_b.pk)})

        self.assertEqual(response.status_code, 403)
        signed_url.assert_not_called()
        self.assert_no_secret_values(response)

    @patch("config.views.create_private_storage_signed_url")
    def test_administrator_can_access_any_owned_file(self, signed_url):
        administrator = get_user_model().objects.create_superuser(
            email="admin@example.test",
            nome_completo="Administrator",
            password="admin-password",
        )
        signed_url.return_value = {"signed_url": "https://example.test/signed", "expires_in": 60}
        self.client.force_login(administrator)

        response = self.post_storage({"arquivo_id": str(self.file_b.pk)})

        self.assertEqual(response.status_code, 200)
        signed_url.assert_called_once_with(self.file_b.storage_path, expires_in=None)

    def test_nonexistent_file_returns_404(self):
        self.login_user_a()
        response = self.post_storage({"arquivo_id": str(uuid.uuid4())})
        self.assertEqual(response.status_code, 404)
        self.assert_no_secret_values(response)

    @patch("config.views.create_private_storage_signed_url")
    def test_browser_supplied_storage_path_is_ignored(self, signed_url):
        signed_url.return_value = {"signed_url": "https://example.test/signed", "expires_in": 60}
        self.login_user_a()

        response = self.post_storage(
            {
                "arquivo_id": str(self.file_a.pk),
                "path": self.file_b.storage_path,
                "storage_path": "../../arbitrary-secret",
            }
        )

        self.assertEqual(response.status_code, 200)
        signed_url.assert_called_once_with(self.file_a.storage_path, expires_in=None)

    def test_malformed_json_is_rejected(self):
        self.login_user_a()
        response = self.client.post(
            reverse("private-storage-url"),
            data="{not-json",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)
        self.assert_no_secret_values(response)

    def test_missing_and_invalid_uuid_are_rejected(self):
        self.login_user_a()
        self.assertEqual(self.post_storage({}).status_code, 400)
        self.assertEqual(self.post_storage({"arquivo_id": "not-a-uuid"}).status_code, 400)

    def test_unsupported_method_is_rejected(self):
        self.login_user_a()
        response = self.client.get(reverse("private-storage-url"))
        self.assertEqual(response.status_code, 405)
        self.assert_no_secret_values(response)

    @override_settings(PRIVATE_STORAGE_REQUEST_MAX_BYTES=32)
    def test_excessive_request_body_is_rejected(self):
        self.login_user_a()
        response = self.post_storage({"arquivo_id": str(self.file_a.pk), "padding": "x" * 64})
        self.assertEqual(response.status_code, 413)

    @patch("config.views.create_private_storage_signed_url")
    def test_supabase_failure_is_sanitized(self, signed_url):
        signed_url.side_effect = SupabaseServiceError(
            f"upstream leaked {settings.SUPABASE_SECRET_KEY}"
        )
        self.login_user_a()

        response = self.post_storage({"arquivo_id": str(self.file_a.pk)})

        self.assertEqual(response.status_code, 502)
        self.assertEqual(response.json(), {"detail": "Private storage is unavailable."})
        self.assert_no_secret_values(response)

    def test_profile_requires_authentication_and_contains_no_secrets(self):
        anonymous = self.client.get(reverse("protected-profile"))
        self.assertEqual(anonymous.status_code, 401)
        self.assert_no_secret_values(anonymous)

        self.login_user_a()
        authenticated = self.client.get(reverse("protected-profile"))
        self.assertEqual(authenticated.status_code, 200)
        self.assert_no_secret_values(authenticated)


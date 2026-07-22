from io import StringIO

from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core.exceptions import ValidationError
from django.core.exceptions import FieldDoesNotExist
from django.core.management import call_command
from django.db.models.deletion import ProtectedError
from django.test import Client, TestCase
from django.urls import reverse

from config.models import ProtectedFile
from .permissions import can_access_owned_object, scope_owned_queryset


Usuario = get_user_model()


class UsuarioManagerTests(TestCase):
    def test_create_user_normalizes_email_and_hashes_password(self):
        user = Usuario.objects.create_user(
            email="  PESSOA@Example.COM ",
            nome_completo="Pessoa Teste",
            password="safe-test-password",
        )

        self.assertEqual(user.email, "pessoa@example.com")
        self.assertTrue(user.check_password("safe-test-password"))
        self.assertNotEqual(user.password, "safe-test-password")
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertIsNone(user.username)
        with self.assertRaises(FieldDoesNotExist):
            Usuario._meta.get_field("username")

    def test_create_user_requires_email(self):
        with self.assertRaises(ValueError):
            Usuario.objects.create_user(
                email="",
                nome_completo="Sem Email",
                password="safe-test-password",
            )

    def test_email_is_case_insensitively_unique(self):
        Usuario.objects.create_user(
            email="unique@example.com",
            nome_completo="Primeiro",
            password="safe-test-password",
        )

        with self.assertRaises(ValidationError):
            Usuario.objects.create_user(
                email="UNIQUE@EXAMPLE.COM",
                nome_completo="Segundo",
                password="safe-test-password",
            )

    def test_create_superuser_sets_required_flags(self):
        admin = Usuario.objects.create_superuser(
            email="admin@example.com",
            nome_completo="Administrador",
            password="safe-admin-password",
        )

        self.assertTrue(admin.is_active)
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_create_superuser_rejects_invalid_flags(self):
        with self.assertRaises(ValueError):
            Usuario.objects.create_superuser(
                email="invalid-admin@example.com",
                nome_completo="Admin Invalido",
                password="safe-admin-password",
                is_staff=False,
            )

    def test_cpf_is_normalized_validated_and_unique(self):
        user = Usuario.objects.create_user(
            email="cpf@example.com",
            nome_completo="Pessoa CPF",
            password="safe-test-password",
            cpf="529.982.247-25",
        )
        self.assertEqual(user.cpf, "52998224725")

        with self.assertRaises(ValidationError):
            Usuario.objects.create_user(
                email="cpf-invalid@example.com",
                nome_completo="CPF Invalido",
                password="safe-test-password",
                cpf="111.111.111-11",
            )


class AuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.password = "safe-test-password"
        self.user = Usuario.objects.create_user(
            email="login@example.com",
            nome_completo="Login Teste",
            password=self.password,
        )

    def test_email_login_creates_session(self):
        response = self.client.post(
            reverse("usuarios:login"),
            {"username": self.user.email, "password": self.password},
        )

        self.assertRedirects(response, reverse("clientes:list"))
        self.assertEqual(str(self.client.session["_auth_user_id"]), str(self.user.pk))

    def test_invalid_login_is_generic_and_does_not_leak_password_or_secrets(self):
        submitted_password = "password-that-must-not-leak"
        response = self.client.post(
            reverse("usuarios:login"),
            {"username": self.user.email, "password": submitted_password},
        )
        body = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "E-mail ou senha invalidos.")
        self.assertNotIn(submitted_password, body)
        self.assertNotIn(settings.SUPABASE_SECRET_KEY, body)
        self.assertNotIn(settings.SECRET_KEY, body)

    def test_inactive_user_cannot_authenticate(self):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])

        self.assertIsNone(authenticate(email=self.user.email, password=self.password))
        response = self.client.post(
            reverse("usuarios:login"),
            {"username": self.user.email, "password": self.password},
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_protected_profile_redirects_anonymous_user(self):
        response = self.client.get(reverse("usuarios:perfil"))
        self.assertRedirects(
            response,
            f"{reverse('usuarios:login')}?next={reverse('usuarios:perfil')}",
        )

    def test_logout_requires_post_and_invalidates_session(self):
        self.client.force_login(self.user)
        self.assertEqual(self.client.get(reverse("usuarios:logout")).status_code, 405)

        response = self.client.post(reverse("usuarios:logout"))
        self.assertRedirects(response, reverse("usuarios:login"))
        self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_honors_safe_local_next_and_rejects_external_next(self):
        local_target = reverse("usuarios:perfil")
        response = self.client.post(
            reverse("usuarios:login"),
            {"username": self.user.email, "password": self.password, "next": local_target},
        )
        self.assertRedirects(response, local_target)

        self.client.logout()
        response = self.client.post(
            reverse("usuarios:login"),
            {
                "username": self.user.email,
                "password": self.password,
                "next": "https://attacker.example/collect",
            },
        )
        self.assertRedirects(response, reverse("clientes:list"))

    def test_authenticated_user_is_redirected_away_from_login(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("usuarios:login"))
        self.assertRedirects(response, reverse("clientes:list"))

    def test_profile_uses_private_no_store_headers(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("usuarios:perfil"))
        self.assertEqual(response["Cache-Control"], "private, no-store")
        self.assertEqual(response["Pragma"], "no-cache")


class AuthorizationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_a = Usuario.objects.create_user(
            email="a@example.com",
            nome_completo="Usuario A",
            password="safe-test-password",
        )
        self.user_b = Usuario.objects.create_user(
            email="b@example.com",
            nome_completo="Usuario B",
            password="safe-test-password",
        )
        self.admin = Usuario.objects.create_superuser(
            email="admin@example.com",
            nome_completo="Administrador",
            password="safe-admin-password",
        )

    def test_admin_access_and_common_user_denial(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse("admin:index")).status_code, 200)

        self.client.force_login(self.user_a)
        response = self.client.get(reverse("admin:index"))
        self.assertEqual(response.status_code, 302)

    def test_user_edits_own_profile_without_privilege_escalation(self):
        self.client.force_login(self.user_a)
        response = self.client.post(
            reverse("usuarios:editar-perfil", args=[self.user_a.pk]),
            {
                "nome_completo": "Nome Atualizado",
                "telefone": "(65) 99999-9999",
                "cpf": "",
                "cargo": "Analista",
                "empresa": "Empresa",
                "setor": "Operacoes",
                "is_staff": "on",
                "is_superuser": "on",
                "is_active": "on",
            },
        )

        self.assertRedirects(response, reverse("usuarios:perfil"))
        self.user_a.refresh_from_db()
        self.assertEqual(self.user_a.nome_completo, "Nome Atualizado")
        self.assertEqual(self.user_a.telefone, "65999999999")
        self.assertFalse(self.user_a.is_staff)
        self.assertFalse(self.user_a.is_superuser)

    def test_user_cannot_edit_another_profile(self):
        self.client.force_login(self.user_a)
        response = self.client.post(
            reverse("usuarios:editar-perfil", args=[self.user_b.pk]),
            {"nome_completo": "Ataque"},
        )
        self.assertEqual(response.status_code, 403)
        self.user_b.refresh_from_db()
        self.assertEqual(self.user_b.nome_completo, "Usuario B")

    def test_admin_can_edit_another_profile(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("usuarios:editar-perfil", args=[self.user_b.pk]),
            {
                "nome_completo": "Editado pelo Admin",
                "telefone": "",
                "cpf": "",
                "cargo": "",
                "empresa": "",
                "setor": "",
            },
        )
        self.assertRedirects(
            response,
            reverse("admin:usuarios_usuario_change", args=[self.user_b.pk]),
        )

    def test_administrative_password_reset(self):
        self.client.force_login(self.admin)
        new_password = "new-safe-user-password"
        response = self.client.post(
            reverse("admin:auth_user_password_change", args=[self.user_b.pk]),
            {"password1": new_password, "password2": new_password},
        )

        self.assertEqual(response.status_code, 302)
        self.user_b.refresh_from_db()
        self.assertTrue(self.user_b.check_password(new_password))

    def test_file_ownership_and_reusable_scope_helpers(self):
        file_a = ProtectedFile.objects.create(
            owner=self.user_a,
            storage_path="owners/a/file.pdf",
        )
        file_b = ProtectedFile.objects.create(
            owner=self.user_b,
            storage_path="owners/b/file.pdf",
        )

        self.assertTrue(can_access_owned_object(self.user_a, file_a))
        self.assertFalse(can_access_owned_object(self.user_a, file_b))
        self.assertTrue(can_access_owned_object(self.admin, file_b))
        self.assertEqual(
            list(scope_owned_queryset(ProtectedFile.objects.all(), self.user_a, "owner")),
            [file_a],
        )
        self.assertEqual(scope_owned_queryset(ProtectedFile.objects.all(), self.admin, "owner").count(), 2)

        with self.assertRaises(ProtectedError):
            self.user_a.delete()


class MigrationSafetyTests(TestCase):
    def test_migrations_have_no_pending_model_changes(self):
        output = StringIO()
        call_command("makemigrations", "--check", "--dry-run", stdout=output)
        self.assertIn("No changes detected", output.getvalue())

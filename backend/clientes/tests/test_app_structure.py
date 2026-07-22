import ast
import importlib
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.db.models.deletion import PROTECT
from django.test import SimpleTestCase
from django.urls import reverse
from django.urls.exceptions import NoReverseMatch

from config.models import ProtectedFile


class ClientesAppStructureTests(SimpleTestCase):
    def test_modular_apps_are_loaded(self):
        self.assertEqual(apps.get_app_config("core").name, "core")
        self.assertEqual(apps.get_app_config("clientes").name, "clientes")
        self.assertEqual(apps.get_app_config("usuarios").name, "usuarios")
        self.assertEqual(settings.AUTH_USER_MODEL, "usuarios.Usuario")

    def test_clientes_has_definitive_model_and_initial_migration(self):
        clientes_config = apps.get_app_config("clientes")
        self.assertEqual(
            [model.__name__ for model in clientes_config.get_models()],
            ["Cliente"],
        )

        models_module = importlib.import_module("clientes.models")
        self.assertTrue(hasattr(models_module, "Cliente"))

        migration_files = sorted(
            path.name
            for path in (Path(settings.BASE_DIR) / "clientes" / "migrations").glob("*.py")
        )
        self.assertEqual(migration_files, ["0001_initial.py", "__init__.py"])

    def test_clientes_urlconf_is_namespaced_but_not_published(self):
        clientes_urls = importlib.import_module("clientes.urls")
        self.assertEqual(clientes_urls.app_name, "clientes")
        self.assertEqual(clientes_urls.urlpatterns, [])

        with self.assertRaises(NoReverseMatch):
            reverse("clientes:index")

    def test_existing_url_names_remain_compatible(self):
        self.assertEqual(reverse("usuarios:login"), "/usuarios/entrar/")
        self.assertEqual(reverse("usuarios:logout"), "/usuarios/sair/")
        self.assertEqual(reverse("usuarios:perfil"), "/usuarios/perfil/")
        self.assertEqual(reverse("protected-profile"), "/api/protected/profile/")
        self.assertEqual(reverse("private-storage-url"), "/api/storage/private-url/")

    def test_protected_file_remains_in_config_with_ownership_protected(self):
        self.assertEqual(ProtectedFile._meta.app_label, "config")
        self.assertEqual(ProtectedFile._meta.db_table, "config_protectedfile")

        owner_field = ProtectedFile._meta.get_field("owner")
        self.assertEqual(owner_field.remote_field.model._meta.label, "usuarios.Usuario")
        self.assertIs(owner_field.remote_field.on_delete, PROTECT)


class DependencyBoundaryTests(SimpleTestCase):
    forbidden_dependencies = {
        "core": {"config", "usuarios", "clientes"},
        "usuarios": {"clientes"},
        "clientes": {"config"},
    }

    def test_production_modules_respect_dependency_boundaries(self):
        violations = []
        backend_root = Path(settings.BASE_DIR)

        for app_name, forbidden_roots in self.forbidden_dependencies.items():
            for path in (backend_root / app_name).rglob("*.py"):
                if "tests" in path.parts or "migrations" in path.parts:
                    continue
                tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
                for node in ast.walk(tree):
                    imported_roots = self._imported_roots(node)
                    blocked = sorted(imported_roots & forbidden_roots)
                    if blocked:
                        violations.append(f"{path.relative_to(backend_root)}: {blocked}")

        self.assertEqual(violations, [])

    def test_new_apps_do_not_contain_secret_setting_names_or_values(self):
        forbidden_names = (
            "DATABASE" + "_URL",
            "DJANGO" + "_SECRET_KEY",
            "SUPABASE" + "_SECRET_KEY",
        )
        secret_values = tuple(value for value in settings.LOG_REDACTED_SECRETS if value)
        violations = []

        for app_name in ("core", "clientes"):
            for path in (Path(settings.BASE_DIR) / app_name).rglob("*.py"):
                source = path.read_text(encoding="utf-8")
                if any(name in source for name in forbidden_names):
                    violations.append(str(path))
                if any(secret in source for secret in secret_values):
                    violations.append(str(path))

        self.assertEqual(violations, [])

    @staticmethod
    def _imported_roots(node: ast.AST) -> set[str]:
        if isinstance(node, ast.Import):
            return {alias.name.split(".", maxsplit=1)[0] for alias in node.names}
        if isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            return {node.module.split(".", maxsplit=1)[0]}
        return set()

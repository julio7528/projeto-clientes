import uuid
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.test import SimpleTestCase

from core.models import UUIDTimestampedModel
from core.normalizers import normalize_digits, normalize_whitespace


class UUIDTimestampedModelTests(SimpleTestCase):
    def test_model_is_abstract_and_defines_expected_fields(self):
        self.assertTrue(UUIDTimestampedModel._meta.abstract)
        self.assertEqual(
            {field.name for field in UUIDTimestampedModel._meta.local_fields},
            {"id", "criado_em", "atualizado_em"},
        )

        id_field = UUIDTimestampedModel._meta.get_field("id")
        self.assertTrue(id_field.primary_key)
        self.assertFalse(id_field.editable)
        self.assertIsInstance(id_field.default(), uuid.UUID)
        self.assertTrue(UUIDTimestampedModel._meta.get_field("criado_em").auto_now_add)
        self.assertTrue(UUIDTimestampedModel._meta.get_field("atualizado_em").auto_now)

    def test_core_has_no_concrete_models_or_migrations(self):
        core_config = apps.get_app_config("core")
        self.assertEqual(list(core_config.get_models()), [])

        migration_files = sorted(
            path.name
            for path in (Path(settings.BASE_DIR) / "core" / "migrations").glob("*.py")
        )
        self.assertEqual(migration_files, ["__init__.py"])


class GenericNormalizerTests(SimpleTestCase):
    def test_normalize_digits_accepts_formatted_and_empty_values(self):
        self.assertEqual(normalize_digits("(65) 99999-8888"), "65999998888")
        self.assertEqual(normalize_digits(None), "")

    def test_normalize_whitespace_trims_and_collapses_whitespace(self):
        self.assertEqual(
            normalize_whitespace("  Maria\t  da\nSilva  "),
            "Maria da Silva",
        )
        self.assertEqual(normalize_whitespace(None), "")

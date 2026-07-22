from django.contrib.auth import get_user_model
from django.test import TestCase

from clientes.models import Cliente
from clientes.services import collect_duplicate_warnings


class DuplicateWarningTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        manager = get_user_model().objects
        cls.owner = manager.create_user(
            email="owner@example.test", password="test", nome_completo="Owner"
        )
        cls.other = manager.create_user(
            email="other@example.test", password="test", nome_completo="Other"
        )
        cls.admin = manager.create_superuser(
            email="admin@example.test", password="test", nome_completo="Admin"
        )
        cls.owned = Cliente.objects.create(
            tipo="PF", nome="Cliente Próprio", documento="52998224725",
            telefone="65999998888", cep="78890000",
            email="duplicate@example.test", criado_por=cls.owner,
        )
        cls.external = Cliente.objects.create(
            tipo="PJ", nome="Cliente Externo", documento="04252011000110",
            telefone="6533334444", cep="78890000",
            email="external@example.test", criado_por=cls.other,
        )

    def test_phone_and_email_warnings_are_normalized_generic_and_non_blocking(self):
        warnings = collect_duplicate_warnings(
            user=self.owner,
            telefone="(65) 99999-8888",
            email=" DUPLICATE@EXAMPLE.TEST ",
        )
        self.assertEqual([warning.field for warning in warnings], ["telefone", "email"])
        for warning in warnings:
            self.assertEqual(warning.count, 1)
            self.assertNotIn(self.owned.nome, warning.message)
            self.assertNotIn(str(self.owned.id), warning.message)
        another = Cliente(
            tipo="PF", nome="Outro Cliente", documento="11144477735",
            telefone="65999998888", cep="78890000",
            email="duplicate@example.test", criado_por=self.owner,
        )
        another.full_clean()

    def test_empty_values_and_edit_exclusion_return_no_warning(self):
        self.assertEqual(collect_duplicate_warnings(user=self.owner), [])
        self.assertEqual(
            collect_duplicate_warnings(
                user=self.owner,
                telefone=self.owned.telefone,
                email=self.owned.email,
                exclude_cliente_id=self.owned.id,
            ),
            [],
        )

    def test_user_isolation_and_administrator_global_scope(self):
        common = collect_duplicate_warnings(
            user=self.owner,
            telefone=self.external.telefone,
            email=self.external.email,
        )
        self.assertEqual(common, [])
        admin = collect_duplicate_warnings(
            user=self.admin,
            telefone=self.external.telefone,
            email=self.external.email,
        )
        self.assertEqual([warning.field for warning in admin], ["telefone", "email"])
        self.assertTrue(all(warning.count == 1 for warning in admin))

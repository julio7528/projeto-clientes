from unittest.mock import Mock

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.test import RequestFactory, TestCase

from clientes.admin import ClienteAdmin
from clientes.models import Cliente


class ClienteAdminTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.admin_user = get_user_model().objects.create_superuser(
            email="admin@example.test",
            password="test-password",
            nome_completo="Administrador",
        )

    def setUp(self):
        self.model_admin = ClienteAdmin(Cliente, admin.site)
        self.request = RequestFactory().post("/admin/clientes/cliente/")
        self.request.user = self.admin_user

    def test_registration_search_filters_readonly_and_masking(self):
        self.assertIsInstance(admin.site._registry[Cliente], ClienteAdmin)
        self.assertEqual(
            self.model_admin.search_fields,
            ("nome", "documento", "telefone", "email"),
        )
        self.assertIn("criado_por", self.model_admin.readonly_fields)
        self.assertIn("atualizado_por", self.model_admin.readonly_fields)
        pf = Cliente(documento="52998224725")
        pj = Cliente(documento="04252011000110")
        self.assertEqual(self.model_admin.documento_mascarado(pf), "***.***.***-25")
        self.assertEqual(self.model_admin.documento_mascarado(pj), "**.***.***/****-10")

    def test_save_model_assigns_protected_authorship(self):
        cliente = Cliente(
            tipo="PF", nome="Cliente Admin", documento="52998224725",
            telefone="65999998888", cep="78890000",
        )
        self.model_admin.save_model(self.request, cliente, form=None, change=False)
        self.assertEqual(cliente.criado_por, self.admin_user)
        self.assertEqual(cliente.atualizado_por, self.admin_user)

    def test_activate_and_deactivate_actions(self):
        cliente = Cliente.objects.create(
            tipo="PF", nome="Cliente Admin", documento="52998224725",
            telefone="65999998888", cep="78890000",
            criado_por=self.admin_user,
        )
        self.model_admin.message_user = Mock()
        queryset = Cliente.objects.filter(pk=cliente.pk)
        self.model_admin.inativar_clientes(self.request, queryset)
        cliente.refresh_from_db()
        self.assertEqual(cliente.situacao, "INATIVO")
        self.model_admin.ativar_clientes(self.request, queryset)
        cliente.refresh_from_db()
        self.assertEqual(cliente.situacao, "ATIVO")
        self.assertEqual(cliente.atualizado_por, self.admin_user)

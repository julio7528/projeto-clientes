from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from clientes.models import Cliente


def cliente_data(**overrides):
    data = {
        "tipo": "PF",
        "nome": "Pessoa Fictícia",
        "documento": "52998224725",
        "data_referencia": "",
        "email": "pessoa@example.test",
        "telefone": "65999998888",
        "cep": "78890000",
        "logradouro": "Rua Um",
        "numero": "10",
        "complemento": "",
        "bairro": "Centro",
        "cidade": "Cuiabá",
        "estado": "MT",
        "observacoes": "",
    }
    data.update(overrides)
    return data


def create_cliente(*, owner, **overrides):
    data = cliente_data(**overrides)
    if data["data_referencia"] == "":
        data["data_referencia"] = None
    return Cliente.objects.create(
        **data,
        criado_por=owner,
        atualizado_por=owner,
    )


class ClienteViewBase(TestCase):
    @classmethod
    def setUpTestData(cls):
        manager = get_user_model().objects
        cls.user = manager.create_user(
            email="user@example.test", password="test-password", nome_completo="Usuário"
        )
        cls.other = manager.create_user(
            email="other@example.test", password="test-password", nome_completo="Outro"
        )
        cls.admin = manager.create_superuser(
            email="admin@example.test", password="test-password", nome_completo="Admin"
        )

    def setUp(self):
        self.client.force_login(self.user)


class RouteProtectionTests(ClienteViewBase):
    def test_all_customer_pages_require_login(self):
        cliente = create_cliente(owner=self.user)
        self.client.logout()
        urls = (
            reverse("clientes:list"),
            reverse("clientes:create"),
            reverse("clientes:detail", args=[cliente.pk]),
            reverse("clientes:update", args=[cliente.pk]),
            reverse("clientes:activate", args=[cliente.pk]),
            reverse("clientes:deactivate", args=[cliente.pk]),
        )
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertTrue(response.url.startswith(reverse("usuarios:login")))

    def test_status_mutations_are_post_only_and_require_csrf(self):
        cliente = create_cliente(owner=self.user)
        url = reverse("clientes:deactivate", args=[cliente.pk])
        self.assertEqual(self.client.get(url).status_code, 405)

        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.user)
        self.assertEqual(csrf_client.post(url).status_code, 403)

    def test_sensitive_pages_use_private_no_store_headers(self):
        cliente = create_cliente(owner=self.user)
        for url in (
            reverse("clientes:list"),
            reverse("clientes:create"),
            reverse("clientes:detail", args=[cliente.pk]),
            reverse("clientes:update", args=[cliente.pk]),
        ):
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response["Cache-Control"], "private, no-store")
                self.assertEqual(response["Pragma"], "no-cache")


class ListAndOwnershipTests(ClienteViewBase):
    def test_common_user_sees_only_owned_records_with_masked_document(self):
        own = create_cliente(owner=self.user, nome="Cliente Próprio")
        external = create_cliente(
            owner=self.other,
            nome="Cliente Externo",
            tipo="PJ",
            documento="04252011000110",
            email="external@example.test",
            telefone="6533334444",
        )
        response = self.client.get(reverse("clientes:list"))
        body = response.content.decode()
        self.assertContains(response, own.nome)
        self.assertNotContains(response, external.nome)
        self.assertContains(response, "***.***.***-25")
        self.assertNotIn(own.documento, body)
        self.assertContains(response, "(65) 99999-8888")

    def test_administrator_sees_all_records(self):
        own = create_cliente(owner=self.user, nome="Cliente Próprio")
        external = create_cliente(
            owner=self.other, nome="Cliente Externo", tipo="PJ",
            documento="04252011000110", email="external@example.test",
            telefone="6533334444",
        )
        self.client.force_login(self.admin)
        response = self.client.get(reverse("clientes:list"))
        self.assertContains(response, own.nome)
        self.assertContains(response, external.nome)

    def test_cross_user_object_routes_return_404(self):
        external = create_cliente(owner=self.other)
        routes = (
            ("clientes:detail", "get"),
            ("clientes:update", "get"),
            ("clientes:activate", "post"),
            ("clientes:deactivate", "post"),
        )
        for route, method in routes:
            with self.subTest(route=route):
                response = getattr(self.client, method)(reverse(route, args=[external.pk]))
                self.assertEqual(response.status_code, 404)

    def test_administrator_can_access_external_detail(self):
        external = create_cliente(owner=self.other)
        self.client.force_login(self.admin)
        self.assertEqual(
            self.client.get(reverse("clientes:detail", args=[external.pk])).status_code,
            200,
        )


class CreationTests(ClienteViewBase):
    def test_pf_creation_sets_backend_authorship_and_active_status(self):
        payload = cliente_data(criado_por=str(self.other.pk), situacao="INATIVO")
        response = self.client.post(reverse("clientes:create"), payload)
        cliente = Cliente.objects.get(documento="52998224725")
        self.assertRedirects(response, reverse("clientes:detail", args=[cliente.pk]))
        self.assertEqual(cliente.criado_por, self.user)
        self.assertEqual(cliente.atualizado_por, self.user)
        self.assertEqual(cliente.situacao, "ATIVO")

    def test_pj_creation_and_type_shortcuts(self):
        response = self.client.get(reverse("clientes:create") + "?tipo=PJ")
        self.assertEqual(response.context["form"].initial["tipo"], "PJ")
        invalid = self.client.get(reverse("clientes:create") + "?tipo=XX")
        self.assertNotIn("tipo", invalid.context["form"].initial)

        payload = cliente_data(
            tipo="PJ", nome="Empresa Fictícia Ltda", documento="04252011000110"
        )
        response = self.client.post(reverse("clientes:create"), payload)
        cliente = Cliente.objects.get(documento="04252011000110")
        self.assertRedirects(response, reverse("clientes:detail", args=[cliente.pk]))

    def test_duplicate_document_is_blocked_with_generic_message(self):
        existing = create_cliente(owner=self.other, nome="Nome que não pode vazar")
        response = self.client.post(
            reverse("clientes:create"),
            cliente_data(nome="Novo Nome"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Já existe um cliente cadastrado com este documento.")
        self.assertNotContains(response, existing.nome)
        self.assertEqual(Cliente.objects.count(), 1)

    def test_invalid_form_preserves_submitted_safe_values_and_labels(self):
        response = self.client.post(
            reverse("clientes:create"),
            cliente_data(tipo="PJ", nome="Empresa Preservada", documento="inválido"),
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Empresa Preservada")
        self.assertContains(response, "Nome empresarial")
        self.assertEqual(Cliente.objects.count(), 0)


class DuplicateConfirmationTests(ClienteViewBase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.first = create_cliente(owner=cls.user, nome="Primeiro")
        cls.second = create_cliente(
            owner=cls.user,
            nome="Segundo",
            documento="11144477735",
            telefone="6533334444",
            email="second@example.test",
        )

    def candidate(self, **overrides):
        return cliente_data(
            nome="Candidato",
            documento="12345678909",
            **overrides,
        )

    def test_warning_requires_explicit_valid_confirmation(self):
        payload = self.candidate(
            telefone=self.first.telefone,
            email=self.first.email,
        )
        with self.assertNoLogs("clientes", level="INFO"):
            first_response = self.client.post(reverse("clientes:create"), payload)
        self.assertEqual(first_response.status_code, 200)
        self.assertContains(first_response, "Possível cadastro repetido")
        self.assertContains(first_response, "Já existe outro cliente com este telefone.")
        self.assertContains(first_response, "Já existe outro cliente com este e-mail.")
        self.assertFalse(Cliente.objects.filter(documento=payload["documento"]).exists())

        confirmed = {
            **payload,
            "confirmar_duplicidade": "1",
            "duplicate_confirmation_token": first_response.context["confirmation_token"],
        }
        response = self.client.post(reverse("clientes:create"), confirmed)
        cliente = Cliente.objects.get(documento=payload["documento"])
        self.assertRedirects(response, reverse("clientes:detail", args=[cliente.pk]))

    def test_changed_values_invalidate_stale_confirmation(self):
        first_payload = self.candidate(
            telefone=self.first.telefone,
            email=self.first.email,
        )
        first_response = self.client.post(reverse("clientes:create"), first_payload)
        changed = {
            **first_payload,
            "telefone": self.second.telefone,
            "email": self.second.email,
            "confirmar_duplicidade": "1",
            "duplicate_confirmation_token": first_response.context["confirmation_token"],
        }
        response = self.client.post(reverse("clientes:create"), changed)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Possível cadastro repetido")
        self.assertFalse(Cliente.objects.filter(documento=changed["documento"]).exists())
        self.assertNotEqual(
            response.context["confirmation_token"],
            first_response.context["confirmation_token"],
        )

    def test_other_users_duplicates_are_private_but_admin_checks_globally(self):
        external = create_cliente(
            owner=self.other,
            nome="Externo Privado",
            documento="98765432100",
            telefone="6566667777",
            email="private@example.test",
        )
        payload = self.candidate(
            telefone=external.telefone,
            email=external.email,
        )
        response = self.client.post(reverse("clientes:create"), payload)
        self.assertEqual(response.status_code, 302)

        Cliente.objects.filter(documento=payload["documento"]).delete()
        self.client.force_login(self.admin)
        response = self.client.post(reverse("clientes:create"), payload)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Possível cadastro repetido")
        self.assertNotContains(response, external.nome)


class DetailEditAndStatusTests(ClienteViewBase):
    def test_detail_uses_dynamic_labels_and_has_no_delete_control(self):
        cliente = create_cliente(owner=self.user)
        response = self.client.get(reverse("clientes:detail", args=[cliente.pk]))
        self.assertContains(response, "CPF")
        self.assertContains(response, "Data de nascimento")
        self.assertNotContains(response, "Excluir")

    def test_edit_preserves_creator_updates_author_and_excludes_self_warning(self):
        cliente = create_cliente(owner=self.user)
        payload = cliente_data(nome="Nome Atualizado")
        self.client.force_login(self.admin)
        response = self.client.post(reverse("clientes:update", args=[cliente.pk]), payload)
        cliente.refresh_from_db()
        self.assertRedirects(response, reverse("clientes:detail", args=[cliente.pk]))
        self.assertEqual(cliente.nome, "Nome Atualizado")
        self.assertEqual(cliente.criado_por, self.user)
        self.assertEqual(cliente.atualizado_por, self.admin)

    def test_activate_and_deactivate_are_idempotent_audited_and_do_not_delete(self):
        cliente = create_cliente(owner=self.user)
        deactivate = reverse("clientes:deactivate", args=[cliente.pk])
        activate = reverse("clientes:activate", args=[cliente.pk])
        self.client.post(deactivate)
        self.client.post(deactivate)
        cliente.refresh_from_db()
        self.assertEqual(cliente.situacao, "INATIVO")
        self.assertEqual(cliente.atualizado_por, self.user)
        self.client.post(activate)
        self.client.post(activate)
        cliente.refresh_from_db()
        self.assertEqual(cliente.situacao, "ATIVO")
        self.assertTrue(Cliente.objects.filter(pk=cliente.pk).exists())

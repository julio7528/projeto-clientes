import uuid
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError, connection, transaction
from django.db.models.deletion import PROTECT, SET_NULL
from django.test import TestCase
from django.utils import timezone

from clientes.choices import SituacaoCliente, TipoCliente, UnidadeFederativa
from clientes.models import Cliente


def valid_cliente(**overrides):
    data = {
        "tipo": TipoCliente.PF,
        "nome": "Cliente Fictício",
        "documento": "52998224725",
        "telefone": "65999998888",
        "cep": "78890000",
    }
    data.update(overrides)
    return Cliente(**data)


class ClienteModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email="owner@example.test",
            password="safe-test-password",
            nome_completo="Usuário Owner",
        )

    def test_valid_pf_and_pj_share_the_same_model(self):
        pf = valid_cliente(criado_por=self.user)
        pf.full_clean()
        pf.save()
        pj = valid_cliente(
            tipo=TipoCliente.PJ,
            nome="Empresa Fictícia Ltda",
            documento="04.252.011/0001-10",
            criado_por=self.user,
        )
        pj.full_clean()
        pj.save()
        self.assertEqual(Cliente.objects.count(), 2)

    def test_uuid_timestamps_default_status_and_string(self):
        cliente = valid_cliente(nome="Nome Exibido")
        cliente.full_clean()
        cliente.save()
        self.assertIsInstance(cliente.id, uuid.UUID)
        self.assertIsNotNone(cliente.criado_em)
        self.assertIsNotNone(cliente.atualizado_em)
        self.assertEqual(cliente.situacao, SituacaoCliente.ATIVO)
        self.assertEqual(str(cliente), "Nome Exibido")

    def test_normalization_is_idempotent_and_save_is_safe(self):
        cliente = valid_cliente(
            nome="  João   da Silva  ",
            documento="529.982.247-25",
            telefone="(65) 99999-8888",
            cep="78890-000",
            email="  CLIENTE@EXAMPLE.TEST ",
            logradouro="  Rua   Um ",
            numero=" S/N ",
            complemento="  Sala  2 ",
            bairro="  Centro ",
            cidade=" Cuiabá ",
            estado=" mt ",
            observacoes="  texto controlado  ",
        )
        cliente.normalize_fields()
        first = tuple(
            getattr(cliente, field)
            for field in (
                "nome", "documento", "telefone", "cep", "email", "logradouro",
                "numero", "complemento", "bairro", "cidade", "estado", "observacoes",
            )
        )
        cliente.normalize_fields()
        self.assertEqual(first, tuple(getattr(cliente, field) for field in (
            "nome", "documento", "telefone", "cep", "email", "logradouro",
            "numero", "complemento", "bairro", "cidade", "estado", "observacoes",
        )))
        cliente.full_clean()
        cliente.save()
        cliente.refresh_from_db()
        self.assertEqual(cliente.documento, "52998224725")
        self.assertEqual(cliente.telefone, "65999998888")
        self.assertEqual(cliente.cep, "78890000")
        self.assertEqual(cliente.email, "cliente@example.test")
        self.assertEqual(cliente.estado, "MT")

    def test_cross_field_required_email_uf_and_date_validation(self):
        invalid_cases = (
            ("tipo_documento", {"tipo": TipoCliente.PJ}),
            ("documento", {"documento": ""}),
            ("nome", {"nome": ""}),
            ("telefone", {"telefone": ""}),
            ("cep", {"cep": ""}),
            ("email", {"email": "inválido"}),
            ("estado", {"estado": "XX"}),
            ("data", {"data_referencia": timezone.localdate() + timedelta(days=1)}),
        )
        for label, overrides in invalid_cases:
            with self.subTest(label=label), self.assertRaises(ValidationError):
                valid_cliente(**overrides).full_clean()
        valid_cliente(email="", estado="").full_clean()

    def test_global_document_uniqueness_has_generic_error(self):
        first = valid_cliente(criado_por=self.user)
        first.full_clean()
        first.save()
        duplicate = valid_cliente(nome="Outro Nome")
        with self.assertRaises(ValidationError) as context:
            duplicate.full_clean()
        message = str(context.exception)
        self.assertIn("Já existe um cliente cadastrado com este documento.", message)
        self.assertNotIn(first.nome, message)
        self.assertNotIn(str(first.id), message)

    def test_authorship_on_delete_rules(self):
        criado_field = Cliente._meta.get_field("criado_por")
        atualizado_field = Cliente._meta.get_field("atualizado_por")
        self.assertIs(criado_field.remote_field.on_delete, PROTECT)
        self.assertIs(atualizado_field.remote_field.on_delete, SET_NULL)
        cliente = valid_cliente(criado_por=self.user, atualizado_por=self.user)
        cliente.full_clean()
        cliente.save()
        self.assertEqual(cliente.criado_por, self.user)
        self.assertEqual(cliente.atualizado_por, self.user)

    def test_activation_and_inactivation_are_idempotent(self):
        cliente = valid_cliente()
        cliente.inativar()
        cliente.inativar()
        self.assertEqual(cliente.situacao, SituacaoCliente.INATIVO)
        cliente.ativar()
        cliente.ativar()
        self.assertEqual(cliente.situacao, SituacaoCliente.ATIVO)

    def test_meta_choices_indexes_and_constraints(self):
        self.assertEqual(Cliente._meta.ordering, ("nome",))
        self.assertEqual(len(UnidadeFederativa.values), 27)
        self.assertEqual(set(TipoCliente.values), {"PF", "PJ"})
        expected_indexes = {
            "clientes_estado_cidade_idx",
            "clientes_tipo_situacao_idx",
            "clientes_criado_em_idx",
            "clientes_atualizado_em_idx",
        }
        self.assertEqual({index.name for index in Cliente._meta.indexes}, expected_indexes)
        for field_name in ("nome", "telefone", "email", "tipo", "situacao"):
            self.assertTrue(Cliente._meta.get_field(field_name).db_index)
        expected_constraints = {
            "clientes_tipo_valido_ck",
            "clientes_situacao_valida_ck",
            "clientes_documento_tipo_len_ck",
            "clientes_telefone_len_ck",
            "clientes_cep_len_ck",
        }
        self.assertEqual(
            {constraint.name for constraint in Cliente._meta.constraints},
            expected_constraints,
        )
        with connection.cursor() as cursor:
            constraints = connection.introspection.get_constraints(
                cursor,
                Cliente._meta.db_table,
            )
        self.assertTrue(expected_constraints.issubset(constraints))

    def test_database_constraints_reject_invalid_lengths_and_choices(self):
        invalid_rows = (
            {"tipo": "XX"},
            {"situacao": "INVALID"},
            {"documento": "5299822472"},
            {"telefone": "659999999"},
            {"cep": "7889000"},
        )
        for overrides in invalid_rows:
            with self.subTest(overrides=overrides):
                with self.assertRaises(IntegrityError), transaction.atomic():
                    Cliente.objects.create(**{
                        "tipo": "PF",
                        "nome": "Registro Inválido",
                        "documento": "52998224725",
                        "telefone": "65999998888",
                        "cep": "78890000",
                        **overrides,
                    })

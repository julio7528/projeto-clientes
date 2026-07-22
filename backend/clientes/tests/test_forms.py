from django.test import TestCase

from clientes.forms import ClienteForm


class ClienteFormTests(TestCase):
    def test_form_uses_explicit_safe_allowlist(self):
        form = ClienteForm()
        expected_model_fields = {
            "tipo", "nome", "documento", "data_referencia", "email", "telefone",
            "cep", "logradouro", "numero", "complemento", "bairro", "cidade",
            "estado", "observacoes",
        }
        self.assertTrue(expected_model_fields.issubset(form.fields))
        self.assertTrue(
            {"confirmar_duplicidade", "duplicate_confirmation_token"}.issubset(form.fields)
        )
        self.assertFalse(
            {"id", "situacao", "criado_em", "atualizado_em", "criado_por", "atualizado_por"}
            & set(form.fields)
        )

    def test_dynamic_labels_follow_pf_and_pj(self):
        pf = ClienteForm(initial={"tipo": "PF"})
        self.assertEqual(pf.fields["nome"].label, "Nome completo")
        self.assertEqual(pf.fields["documento"].label, "CPF")
        self.assertEqual(pf.fields["data_referencia"].label, "Data de nascimento")

        pj = ClienteForm(data={"tipo": "PJ"})
        self.assertEqual(pj.fields["nome"].label, "Nome empresarial")
        self.assertEqual(pj.fields["documento"].label, "CNPJ")
        self.assertEqual(pj.fields["data_referencia"].label, "Data de abertura")

    def test_form_accepts_formatted_values_without_javascript(self):
        form = ClienteForm(
            data={
                "tipo": "PF",
                "nome": "Pessoa Fictícia",
                "documento": "529.982.247-25",
                "telefone": "(65) 99999-8888",
                "cep": "78890-000",
                "email": "",
                "estado": "MT",
            }
        )
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["documento"], "52998224725")
        self.assertEqual(form.cleaned_data["telefone"], "65999998888")
        self.assertEqual(form.cleaned_data["cep"], "78890000")

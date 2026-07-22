from datetime import timedelta

from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from django.utils import timezone

from clientes.validators import (
    validate_cep,
    validate_cnpj,
    validate_cpf,
    validate_data_nao_futura,
    validate_documento,
    validate_nome,
    validate_telefone,
    validate_uf,
)


class DocumentoValidatorTests(SimpleTestCase):
    def test_cpf_accepts_formatted_and_unformatted_values(self):
        validate_cpf("529.982.247-25")
        validate_cpf("52998224725")

    def test_cpf_rejects_invalid_sizes_digits_letters_and_check_digits(self):
        invalid_values = (
            "5299822472",
            "529982247250",
            "11111111111",
            "52998224724",
            "5299822472A",
        )
        for value in invalid_values:
            with self.subTest(value=value), self.assertRaises(ValidationError):
                validate_cpf(value)

    def test_cnpj_accepts_formatted_and_unformatted_values(self):
        validate_cnpj("04.252.011/0001-10")
        validate_cnpj("04252011000110")

    def test_cnpj_rejects_invalid_sizes_digits_letters_and_check_digits(self):
        invalid_values = (
            "0425201100011",
            "042520110001100",
            "11111111111111",
            "04252011000111",
            "0425201100011A",
        )
        for value in invalid_values:
            with self.subTest(value=value), self.assertRaises(ValidationError):
                validate_cnpj(value)

    def test_documento_requires_consistency_with_type(self):
        validate_documento("PF", "52998224725")
        validate_documento("PJ", "04252011000110")
        for tipo, documento in (
            ("PF", "04252011000110"),
            ("PJ", "52998224725"),
            ("XX", "52998224725"),
        ):
            with self.subTest(tipo=tipo), self.assertRaises(ValidationError):
                validate_documento(tipo, documento)


class OtherValidatorTests(SimpleTestCase):
    def test_phone_accepts_ten_and_eleven_digits_with_formatting(self):
        validate_telefone("(65) 3333-4444")
        validate_telefone("(65) 99999-8888")

    def test_phone_rejects_invalid_value(self):
        for value in ("659999999", "659999999999", "65A99999999"):
            with self.subTest(value=value), self.assertRaises(ValidationError):
                validate_telefone(value)

    def test_cep_accepts_formatted_value_and_rejects_invalid_value(self):
        validate_cep("78890-000")
        for value in ("7889000", "788900000", "7889A000"):
            with self.subTest(value=value), self.assertRaises(ValidationError):
                validate_cep(value)

    def test_uf_accepts_empty_and_normalized_valid_value(self):
        validate_uf("")
        validate_uf(" mt ")
        with self.assertRaises(ValidationError):
            validate_uf("XX")

    def test_date_accepts_today_and_past_and_rejects_future(self):
        validate_data_nao_futura(timezone.localdate())
        validate_data_nao_futura(timezone.localdate() - timedelta(days=1))
        with self.assertRaises(ValidationError):
            validate_data_nao_futura(timezone.localdate() + timedelta(days=1))

    def test_name_requires_three_characters_and_letters(self):
        validate_nome("  João   Silva ")
        for value in ("Jo", "123", "***", ""):
            with self.subTest(value=value), self.assertRaises(ValidationError):
                validate_nome(value)

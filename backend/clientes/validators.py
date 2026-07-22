from datetime import date
from typing import Any

from django.core.exceptions import ValidationError
from django.utils import timezone

from core.normalizers import normalize_digits, normalize_whitespace

from .choices import TipoCliente, UF_VALUES


def _has_letters(value: Any) -> bool:
    return any(character.isalpha() for character in str(value or ""))


def _calculate_digit(digits: str, weights: tuple[int, ...]) -> str:
    total = sum(int(digit) * weight for digit, weight in zip(digits, weights))
    remainder = total % 11
    return "0" if remainder < 2 else str(11 - remainder)


def validate_cpf(value: str | None) -> None:
    digits = normalize_digits(value)
    if (
        _has_letters(value)
        or len(digits) != 11
        or len(set(digits)) == 1
        or _calculate_digit(digits[:9], tuple(range(10, 1, -1))) != digits[9]
        or _calculate_digit(digits[:10], tuple(range(11, 1, -1))) != digits[10]
    ):
        raise ValidationError("Informe um CPF válido.", code="invalid_cpf")


def validate_cnpj(value: str | None) -> None:
    digits = normalize_digits(value)
    first_weights = (5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
    second_weights = (6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)
    if (
        _has_letters(value)
        or len(digits) != 14
        or len(set(digits)) == 1
        or _calculate_digit(digits[:12], first_weights) != digits[12]
        or _calculate_digit(digits[:13], second_weights) != digits[13]
    ):
        raise ValidationError("Informe um CNPJ válido.", code="invalid_cnpj")


def validate_documento(tipo: str | None, documento: str | None) -> None:
    if tipo == TipoCliente.PF:
        validate_cpf(documento)
    elif tipo == TipoCliente.PJ:
        validate_cnpj(documento)
    else:
        raise ValidationError("Informe um tipo de cliente válido.", code="invalid_type")


def validate_telefone(value: str | None) -> None:
    if _has_letters(value) or len(normalize_digits(value)) not in (10, 11):
        raise ValidationError(
            "Informe um telefone com DDD e 10 ou 11 dígitos.",
            code="invalid_phone",
        )


def validate_cep(value: str | None) -> None:
    if _has_letters(value) or len(normalize_digits(value)) != 8:
        raise ValidationError("Informe um CEP com 8 dígitos.", code="invalid_cep")


def validate_uf(value: str | None) -> None:
    normalized = normalize_whitespace(value).upper()
    if normalized and normalized not in UF_VALUES:
        raise ValidationError(
            "Informe uma unidade federativa válida.",
            code="invalid_uf",
        )


def validate_data_nao_futura(value: date | None) -> None:
    if value is not None and (not isinstance(value, date) or value > timezone.localdate()):
        raise ValidationError("A data não pode estar no futuro.", code="future_date")


def validate_nome(value: str | None) -> None:
    normalized = normalize_whitespace(value)
    if len(normalized) < 3 or not any(character.isalpha() for character in normalized):
        raise ValidationError(
            "Informe um nome válido com pelo menos 3 caracteres.",
            code="invalid_name",
        )

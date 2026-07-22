import re

from django.core.exceptions import ValidationError


def normalize_digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def validate_cpf(value: str | None) -> None:
    if not value:
        return

    cpf = normalize_digits(value)
    if len(cpf) != 11 or cpf == cpf[0] * 11:
        raise ValidationError("CPF invalido.", code="invalid_cpf")

    for length in (9, 10):
        total = sum(int(cpf[index]) * (length + 1 - index) for index in range(length))
        digit = 11 - (total % 11)
        digit = 0 if digit >= 10 else digit
        if digit != int(cpf[length]):
            raise ValidationError("CPF invalido.", code="invalid_cpf")

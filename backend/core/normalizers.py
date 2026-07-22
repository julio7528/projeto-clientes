import re


def normalize_digits(value: str | None) -> str:
    """Retorna somente os dígitos de um valor textual opcional."""

    return re.sub(r"\D", "", value or "")


def normalize_whitespace(value: str | None) -> str:
    """Remove espaços externos e reduz sequências internas de whitespace."""

    return " ".join((value or "").split())

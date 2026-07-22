from dataclasses import dataclass
from typing import Any
from uuid import UUID

from core.normalizers import normalize_digits
from usuarios.permissions import scope_owned_queryset

from .models import Cliente


@dataclass(frozen=True, slots=True)
class DuplicateWarning:
    code: str
    field: str
    message: str
    count: int


def collect_duplicate_warnings(
    *,
    user: Any,
    telefone: str = "",
    email: str = "",
    exclude_cliente_id: UUID | str | None = None,
) -> list[DuplicateWarning]:
    if not getattr(user, "is_authenticated", False):
        return []

    queryset = scope_owned_queryset(Cliente.objects.all(), user)
    if exclude_cliente_id:
        queryset = queryset.exclude(pk=exclude_cliente_id)

    normalized_phone = normalize_digits(telefone)
    normalized_email = (email or "").strip().lower()
    warnings: list[DuplicateWarning] = []

    if normalized_phone:
        count = queryset.filter(telefone=normalized_phone).count()
        if count:
            warnings.append(
                DuplicateWarning(
                    code="duplicate_phone",
                    field="telefone",
                    message="Já existe outro cliente com este telefone.",
                    count=count,
                )
            )

    if normalized_email:
        count = queryset.filter(email=normalized_email).count()
        if count:
            warnings.append(
                DuplicateWarning(
                    code="duplicate_email",
                    field="email",
                    message="Já existe outro cliente com este e-mail.",
                    count=count,
                )
            )

    return warnings

from dataclasses import dataclass
import hashlib
from typing import Any
from uuid import UUID

from django.core import signing

from core.normalizers import normalize_digits
from usuarios.permissions import scope_owned_queryset

from .models import Cliente


@dataclass(frozen=True, slots=True)
class DuplicateWarning:
    code: str
    field: str
    message: str
    count: int


DUPLICATE_CONFIRMATION_SALT = "clientes.duplicate-confirmation"
DUPLICATE_CONFIRMATION_MAX_AGE = 15 * 60


def _duplicate_fingerprint(
    *,
    user: Any,
    telefone: str,
    email: str,
    exclude_cliente_id: UUID | str | None,
) -> str:
    payload = "|".join(
        (
            str(user.pk),
            normalize_digits(telefone),
            (email or "").strip().lower(),
            str(exclude_cliente_id or "new"),
        )
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def create_duplicate_confirmation_token(
    *,
    user: Any,
    telefone: str,
    email: str,
    exclude_cliente_id: UUID | str | None = None,
) -> str:
    fingerprint = _duplicate_fingerprint(
        user=user,
        telefone=telefone,
        email=email,
        exclude_cliente_id=exclude_cliente_id,
    )
    return signing.dumps(fingerprint, salt=DUPLICATE_CONFIRMATION_SALT, compress=True)


def is_duplicate_confirmation_valid(
    token: str,
    *,
    user: Any,
    telefone: str,
    email: str,
    exclude_cliente_id: UUID | str | None = None,
) -> bool:
    if not token:
        return False
    expected = _duplicate_fingerprint(
        user=user,
        telefone=telefone,
        email=email,
        exclude_cliente_id=exclude_cliente_id,
    )
    try:
        supplied = signing.loads(
            token,
            salt=DUPLICATE_CONFIRMATION_SALT,
            max_age=DUPLICATE_CONFIRMATION_MAX_AGE,
        )
    except signing.BadSignature:
        return False
    return supplied == expected


def mask_document(documento: str) -> str:
    digits = normalize_digits(documento)
    if len(digits) == 11:
        return f"***.***.***-{digits[-2:]}"
    if len(digits) == 14:
        return f"**.***.***/****-{digits[-2:]}"
    return "—"


def format_document(documento: str) -> str:
    digits = normalize_digits(documento)
    if len(digits) == 11:
        return f"{digits[:3]}.{digits[3:6]}.{digits[6:9]}-{digits[9:]}"
    if len(digits) == 14:
        return f"{digits[:2]}.{digits[2:5]}.{digits[5:8]}/{digits[8:12]}-{digits[12:]}"
    return "—"


def format_phone(telefone: str) -> str:
    digits = normalize_digits(telefone)
    if len(digits) == 10:
        return f"({digits[:2]}) {digits[2:6]}-{digits[6:]}"
    if len(digits) == 11:
        return f"({digits[:2]}) {digits[2:7]}-{digits[7:]}"
    return "—"


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

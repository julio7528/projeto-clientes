from dataclasses import dataclass
from datetime import date

from django.db.models import Q, QuerySet

from core.normalizers import normalize_digits, normalize_whitespace

from .choices import SituacaoCliente
from .models import Cliente

ORDERING_ALLOWLIST = frozenset({"nome", "criado_em", "atualizado_em", "cidade", "situacao"})


@dataclass(frozen=True, slots=True)
class ClienteFilterSpec:
    q: str = ""
    tipo: str = ""
    situacao: str = SituacaoCliente.ATIVO
    cidade: str = ""
    estado: str = ""
    criado_de: date | None = None
    criado_ate: date | None = None
    atualizado_de: date | None = None
    atualizado_ate: date | None = None
    ordenar: str = "nome"
    direcao: str = "asc"

    @classmethod
    def from_cleaned_data(cls, data: dict, *, default_active: bool = True):
        return cls(q=data.get("q", ""), tipo=data.get("tipo", ""), situacao=data.get("situacao", SituacaoCliente.ATIVO if default_active else ""), cidade=data.get("cidade", ""), estado=data.get("estado", ""), criado_de=data.get("criado_de"), criado_ate=data.get("criado_ate"), atualizado_de=data.get("atualizado_de"), atualizado_ate=data.get("atualizado_ate"), ordenar=data.get("ordenar") or "nome", direcao=data.get("direcao") or "asc")


def apply_cliente_filters(queryset: QuerySet[Cliente], spec: ClienteFilterSpec) -> QuerySet[Cliente]:
    query = normalize_whitespace(spec.q)
    digits = normalize_digits(query)
    if query:
        condition = Q(nome__icontains=query) | Q(email__icontains=query)
        if digits:
            condition |= Q(documento=digits) | Q(telefone=digits)
        queryset = queryset.filter(condition)
    for field, value in (("tipo", spec.tipo), ("situacao", spec.situacao), ("estado", spec.estado)):
        if value:
            queryset = queryset.filter(**{field: value})
    if spec.cidade:
        queryset = queryset.filter(cidade__icontains=normalize_whitespace(spec.cidade))
    for field, value, lookup in (("criado_em", spec.criado_de, "date__gte"), ("criado_em", spec.criado_ate, "date__lte"), ("atualizado_em", spec.atualizado_de, "date__gte"), ("atualizado_em", spec.atualizado_ate, "date__lte")):
        if value:
            queryset = queryset.filter(**{f"{field}__{lookup}": value})
    return queryset


def apply_cliente_ordering(queryset: QuerySet[Cliente], spec: ClienteFilterSpec) -> QuerySet[Cliente]:
    field = spec.ordenar if spec.ordenar in ORDERING_ALLOWLIST else "nome"
    prefix = "-" if spec.direcao == "desc" else ""
    return queryset.order_by(f"{prefix}{field}", "id")

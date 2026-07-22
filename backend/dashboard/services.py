from datetime import timedelta

from django.db.models import Count
from django.utils import timezone

from clientes.choices import SituacaoCliente, TipoCliente
from clientes.models import Cliente
from clientes.querying import ClienteFilterSpec, apply_cliente_filters


def dashboard_snapshot(queryset, *, situacao="", estado=""):
    spec = ClienteFilterSpec(situacao=situacao, estado=estado)
    scoped = apply_cliente_filters(queryset, spec)
    today = timezone.localdate()
    month_start = today.replace(day=1)
    incomplete = scoped.filter(email="") | scoped.filter(logradouro="", cidade="")
    daily = []
    for offset in range(29, -1, -1):
        day = today - timedelta(days=offset)
        daily.append({"date": day.isoformat(), "count": scoped.filter(criado_em__date=day).count()})
    return {
        "total": scoped.count(),
        "pf": scoped.filter(tipo=TipoCliente.PF).count(),
        "pj": scoped.filter(tipo=TipoCliente.PJ).count(),
        "active": scoped.filter(situacao=SituacaoCliente.ATIVO).count(),
        "inactive": scoped.filter(situacao=SituacaoCliente.INATIVO).count(),
        "new_registrations": scoped.filter(criado_em__date__gte=month_start).count(),
        "incomplete": incomplete.distinct().count(),
        "series": daily,
        "states": list(scoped.exclude(estado="").values("estado").annotate(count=Count("id")).order_by("-count", "estado")[:10]),
        "cities": list(scoped.exclude(cidade="").values("cidade").annotate(count=Count("id")).order_by("-count", "cidade")[:10]),
        "recent_created": scoped.order_by("-criado_em")[:5],
        "recent_updated": scoped.order_by("-atualizado_em")[:5],
    }

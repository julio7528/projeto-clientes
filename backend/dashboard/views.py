import json

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from core.http import private_no_store
from clientes.views import _owned_clientes

from .forms import DashboardFilterForm
from .services import dashboard_snapshot


@login_required
@private_no_store
def index(request):
    form = DashboardFilterForm(request.GET or None)
    data = form.cleaned_data if form.is_valid() else {}
    snapshot = dashboard_snapshot(_owned_clientes(request), situacao=data.get("situacao", ""), estado=data.get("estado", ""))
    snapshot["series_json"] = json.dumps(snapshot["series"], ensure_ascii=False)
    return render(request, "dashboard/index.html", {"form": form, **snapshot})

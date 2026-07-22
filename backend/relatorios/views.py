from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render

from core.http import private_no_store
from clientes.views import _owned_clientes

from .forms import ReportFilterForm
from .services import export_csv, export_pdf, export_xlsx, filtered_queryset, report_rows


@login_required
@private_no_store
def index(request):
    form = ReportFilterForm(request.GET or None)
    queryset = _owned_clientes(request)
    if form.is_valid():
        queryset = filtered_queryset(queryset, form.cleaned_data)
    rows_count = queryset.count()
    if request.GET.get("export"):
        if request.GET["export"] not in {"csv", "xlsx", "pdf"}:
            return HttpResponse("Formato de exportação inválido.", status=400)
        if rows_count > settings.REPORT_EXPORT_MAX_ROWS:
            return HttpResponse("Exportação excede o limite configurado.", status=413)
        response = {"csv": export_csv, "xlsx": export_xlsx, "pdf": export_pdf}.get(request.GET["export"])(queryset)
        response["Cache-Control"] = "no-store, private"
        response["Pragma"] = "no-cache"
        return response
    page = Paginator(queryset, 50).get_page(request.GET.get("page"))
    return render(request, "relatorios/index.html", {"form": form, "page": page, "rows": report_rows(page.object_list), "total": rows_count})

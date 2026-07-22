from uuid import UUID

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db import IntegrityError, transaction
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from core.http import private_no_store
from usuarios.permissions import scope_owned_queryset

from .choices import SituacaoCliente, TipoCliente
from .forms import ClienteForm
from .filters import ClienteSearchForm
from .models import Cliente
from .querying import ClienteFilterSpec, apply_cliente_filters, apply_cliente_ordering
from .services import (
    collect_duplicate_warnings,
    create_duplicate_confirmation_token,
    format_document,
    format_phone,
    is_duplicate_confirmation_valid,
    mask_document,
)


def _owned_clientes(request: HttpRequest):
    return scope_owned_queryset(Cliente.objects.all(), request.user)


def _owned_cliente_or_404(request: HttpRequest, pk: UUID) -> Cliente:
    return get_object_or_404(_owned_clientes(request), pk=pk)


def _render_form(
    request: HttpRequest,
    *,
    form: ClienteForm,
    cliente: Cliente | None = None,
    duplicate_warnings=None,
    confirmation_token: str = "",
) -> HttpResponse:
    response = render(
        request,
        "clientes/cliente_form.html",
        {
            "form": form,
            "cliente": cliente,
            "duplicate_warnings": duplicate_warnings or [],
            "confirmation_token": confirmation_token,
        },
    )
    response["Cache-Control"] = "private, no-store"
    response["Pragma"] = "no-cache"
    return response


def _duplicate_confirmation_required(
    request: HttpRequest,
    *,
    form: ClienteForm,
    cliente: Cliente,
    exclude_cliente_id: UUID | None,
):
    warnings = collect_duplicate_warnings(
        user=request.user,
        telefone=cliente.telefone,
        email=cliente.email,
        exclude_cliente_id=exclude_cliente_id,
    )
    if not warnings:
        return [], "", False
    confirmed = form.cleaned_data.get("confirmar_duplicidade", False)
    token = form.cleaned_data.get("duplicate_confirmation_token", "")
    valid = confirmed and is_duplicate_confirmation_valid(
        token,
        user=request.user,
        telefone=cliente.telefone,
        email=cliente.email,
        exclude_cliente_id=exclude_cliente_id,
    )
    new_token = create_duplicate_confirmation_token(
        user=request.user,
        telefone=cliente.telefone,
        email=cliente.email,
        exclude_cliente_id=exclude_cliente_id,
    )
    return warnings, new_token, not valid


@login_required
@private_no_store
def cliente_list(request: HttpRequest) -> HttpResponse:
    data = request.GET.copy()
    if "situacao" not in request.GET:
        data["situacao"] = SituacaoCliente.ATIVO
    form = ClienteSearchForm(data)
    queryset = _owned_clientes(request)
    if form.is_valid():
        spec = ClienteFilterSpec.from_cleaned_data(form.cleaned_data)
        queryset = apply_cliente_ordering(apply_cliente_filters(queryset, spec), spec)
    else:
        queryset = queryset.none()
    paginator = Paginator(queryset, 20)
    page = paginator.get_page(request.GET.get("page"))
    rows = [
        {
            "cliente": cliente,
            "documento": mask_document(cliente.documento),
            "telefone": format_phone(cliente.telefone),
        }
        for cliente in page.object_list
    ]
    query_params = request.GET.copy()
    query_params.pop("page", None)
    return render(request, "clientes/cliente_list.html", {"form": form, "page": page, "rows": rows, "query_string": query_params.urlencode(), "has_filters": bool(request.GET)})


@login_required
def cliente_create(request: HttpRequest) -> HttpResponse:
    initial = {}
    requested_type = request.GET.get("tipo")
    if requested_type in TipoCliente.values:
        initial["tipo"] = requested_type
    form = ClienteForm(request.POST or None, initial=initial)
    if request.method != "POST" or not form.is_valid():
        return _render_form(request, form=form)

    cliente = form.save(commit=False)
    cliente.criado_por = request.user
    cliente.atualizado_por = request.user
    cliente.situacao = SituacaoCliente.ATIVO
    try:
        cliente.full_clean()
    except ValidationError as error:
        form.add_error(None, error)
        return _render_form(request, form=form)

    warnings, token, requires_confirmation = _duplicate_confirmation_required(
        request,
        form=form,
        cliente=cliente,
        exclude_cliente_id=None,
    )
    if requires_confirmation:
        return _render_form(
            request,
            form=form,
            duplicate_warnings=warnings,
            confirmation_token=token,
        )

    try:
        with transaction.atomic():
            cliente.save()
    except IntegrityError:
        form.add_error(
            "documento",
            "JÃ¡ existe um cliente cadastrado com este documento.",
        )
        return _render_form(request, form=form)
    messages.success(request, "Cliente cadastrado com sucesso.")
    return redirect("clientes:detail", pk=cliente.pk)


@login_required
@private_no_store
def cliente_detail(request: HttpRequest, pk: UUID) -> HttpResponse:
    cliente = _owned_cliente_or_404(request, pk)
    return render(
        request,
        "clientes/cliente_detail.html",
        {
            "cliente": cliente,
            "documento_formatado": format_document(cliente.documento),
            "telefone_formatado": format_phone(cliente.telefone),
        },
    )


@login_required
def cliente_update(request: HttpRequest, pk: UUID) -> HttpResponse:
    cliente = _owned_cliente_or_404(request, pk)
    original_owner = cliente.criado_por
    form = ClienteForm(request.POST or None, instance=cliente)
    if request.method != "POST" or not form.is_valid():
        return _render_form(request, form=form, cliente=cliente)

    cliente = form.save(commit=False)
    cliente.criado_por = original_owner
    cliente.atualizado_por = request.user
    try:
        cliente.full_clean()
    except ValidationError as error:
        form.add_error(None, error)
        return _render_form(request, form=form, cliente=cliente)

    warnings, token, requires_confirmation = _duplicate_confirmation_required(
        request,
        form=form,
        cliente=cliente,
        exclude_cliente_id=cliente.pk,
    )
    if requires_confirmation:
        return _render_form(
            request,
            form=form,
            cliente=cliente,
            duplicate_warnings=warnings,
            confirmation_token=token,
        )

    try:
        with transaction.atomic():
            cliente.save()
    except IntegrityError:
        form.add_error(
            "documento",
            "JÃ¡ existe um cliente cadastrado com este documento.",
        )
        return _render_form(request, form=form, cliente=cliente)
    messages.success(request, "Cliente atualizado com sucesso.")
    return redirect("clientes:detail", pk=cliente.pk)


def _change_status(
    request: HttpRequest,
    *,
    pk: UUID,
    status: SituacaoCliente,
    success_message: str,
) -> HttpResponse:
    cliente = _owned_cliente_or_404(request, pk)
    cliente.situacao = status
    cliente.atualizado_por = request.user
    cliente.save(update_fields=("situacao", "atualizado_por", "atualizado_em"))
    messages.success(request, success_message)
    return redirect("clientes:detail", pk=cliente.pk)


@login_required
@require_POST
def cliente_activate(request: HttpRequest, pk: UUID) -> HttpResponse:
    return _change_status(
        request,
        pk=pk,
        status=SituacaoCliente.ATIVO,
        success_message="Cliente ativado com sucesso.",
    )


@login_required
@require_POST
def cliente_deactivate(request: HttpRequest, pk: UUID) -> HttpResponse:
    return _change_status(
        request,
        pk=pk,
        status=SituacaoCliente.INATIVO,
        success_message="Cliente inativado com sucesso.",
    )


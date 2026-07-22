from typing import Any

from django.contrib import admin, messages
from django.db.models import QuerySet
from django.http import HttpRequest
from django.utils import timezone

from .choices import SituacaoCliente
from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "nome",
        "tipo",
        "documento_mascarado",
        "situacao",
        "telefone",
        "cidade",
        "estado",
    )
    search_fields = ("nome", "documento", "telefone", "email")
    list_filter = ("tipo", "situacao", "estado", "criado_em", "atualizado_em")
    ordering = ("nome",)
    readonly_fields = ("criado_em", "atualizado_em", "criado_por", "atualizado_por")
    actions = ("ativar_clientes", "inativar_clientes")

    @admin.display(description="Documento")
    def documento_mascarado(self, obj: Cliente) -> str:
        if len(obj.documento) == 11:
            return f"***.***.***-{obj.documento[-2:]}"
        if len(obj.documento) == 14:
            return f"**.***.***/****-{obj.documento[-2:]}"
        return "***"

    def save_model(
        self,
        request: HttpRequest,
        obj: Cliente,
        form: Any,
        change: bool,
    ) -> None:
        if not change and obj.criado_por_id is None:
            obj.criado_por = request.user
        obj.atualizado_por = request.user
        obj.full_clean()
        super().save_model(request, obj, form, change)

    @admin.action(description="Ativar clientes selecionados")
    def ativar_clientes(self, request: HttpRequest, queryset: QuerySet[Cliente]) -> None:
        updated = queryset.update(
            situacao=SituacaoCliente.ATIVO,
            atualizado_por=request.user,
            atualizado_em=timezone.now(),
        )
        self.message_user(request, f"{updated} cliente(s) ativado(s).", messages.SUCCESS)

    @admin.action(description="Inativar clientes selecionados")
    def inativar_clientes(self, request: HttpRequest, queryset: QuerySet[Cliente]) -> None:
        updated = queryset.update(
            situacao=SituacaoCliente.INATIVO,
            atualizado_por=request.user,
            atualizado_em=timezone.now(),
        )
        self.message_user(request, f"{updated} cliente(s) inativado(s).", messages.SUCCESS)

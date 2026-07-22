from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import UsuarioAdminChangeForm, UsuarioCreationForm
from .models import Usuario


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    add_form = UsuarioCreationForm
    form = UsuarioAdminChangeForm
    model = Usuario
    ordering = ("email",)
    list_display = (
        "email",
        "nome_completo",
        "is_active",
        "is_staff",
        "is_superuser",
        "last_login",
        "date_joined",
    )
    list_filter = ("is_active", "is_staff", "is_superuser")
    search_fields = ("email", "nome_completo", "cpf")
    readonly_fields = ("last_login", "date_joined")
    filter_horizontal = ("groups", "user_permissions")
    actions = ("activate_users", "deactivate_users")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Perfil",
            {
                "fields": (
                    "nome_completo",
                    "telefone",
                    "cpf",
                    "cargo",
                    "foto",
                    "empresa",
                    "setor",
                    "observacoes",
                )
            },
        ),
        (
            "Acesso",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Datas", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "nome_completo",
                    "password1",
                    "password2",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )

    @admin.action(description="Ativar usuarios selecionados")
    def activate_users(self, request, queryset):
        queryset.update(is_active=True)

    @admin.action(description="Desativar usuarios selecionados")
    def deactivate_users(self, request, queryset):
        queryset.exclude(pk=request.user.pk).update(is_active=False)

    def has_module_permission(self, request):
        return request.user.is_active and request.user.is_staff and request.user.is_superuser

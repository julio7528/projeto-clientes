from uuid import UUID

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.http import HttpRequest, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from .forms import EmailAuthenticationForm, PerfilForm
from .models import Usuario
from .permissions import is_administrator


class EmailLoginView(LoginView):
    authentication_form = EmailAuthenticationForm
    template_name = "usuarios/login.html"
    redirect_authenticated_user = True


@require_POST
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect("usuarios:login")


@login_required
def perfil(request: HttpRequest) -> HttpResponse:
    return render(request, "usuarios/perfil.html", {"usuario_perfil": request.user})


@login_required
def editar_perfil(request: HttpRequest, usuario_id: UUID) -> HttpResponse:
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    if usuario.pk != request.user.pk and not is_administrator(request.user):
        return HttpResponseForbidden("Acesso negado.")

    form = PerfilForm(request.POST or None, instance=usuario)
    if request.method == "POST" and form.is_valid():
        form.save()
        if usuario.pk == request.user.pk:
            return redirect("usuarios:perfil")
        return redirect("admin:usuarios_usuario_change", usuario.pk)

    return render(
        request,
        "usuarios/editar_perfil.html",
        {"form": form, "usuario_perfil": usuario},
    )


class AlterarSenhaView(PasswordChangeView):
    template_name = "usuarios/alterar_senha.html"
    success_url = reverse_lazy("usuarios:perfil")

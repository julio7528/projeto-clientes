from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("entrar/", views.EmailLoginView.as_view(), name="login"),
    path("sair/", views.logout_view, name="logout"),
    path("perfil/", views.perfil, name="perfil"),
    path("perfil/<uuid:usuario_id>/editar/", views.editar_perfil, name="editar-perfil"),
    path("perfil/senha/", views.AlterarSenhaView.as_view(), name="alterar-senha"),
]

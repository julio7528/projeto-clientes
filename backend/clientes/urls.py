from django.urls import path

from . import views


app_name = "clientes"

urlpatterns = [
    path("", views.cliente_list, name="list"),
    path("novo/", views.cliente_create, name="create"),
    path("<uuid:pk>/", views.cliente_detail, name="detail"),
    path("<uuid:pk>/editar/", views.cliente_update, name="update"),
    path("<uuid:pk>/ativar/", views.cliente_activate, name="activate"),
    path("<uuid:pk>/inativar/", views.cliente_deactivate, name="deactivate"),
]

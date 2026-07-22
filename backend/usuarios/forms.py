from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserChangeForm,
    UserCreationForm,
)

from .models import Usuario
from .validators import normalize_digits


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(label="E-mail", max_length=254)

    error_messages = {
        "invalid_login": "E-mail ou senha invalidos.",
        "inactive": "E-mail ou senha invalidos.",
    }


class UsuarioCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = (
            "email",
            "nome_completo",
            "is_active",
            "is_staff",
            "is_superuser",
        )


class UsuarioAdminChangeForm(UserChangeForm):
    telefone = forms.CharField(max_length=15, required=False)
    cpf = forms.CharField(max_length=14, required=False)

    class Meta:
        model = Usuario
        fields = "__all__"

    def clean_telefone(self):
        return normalize_digits(self.cleaned_data["telefone"])

    def clean_cpf(self):
        return normalize_digits(self.cleaned_data["cpf"]) or None


class PerfilForm(forms.ModelForm):
    telefone = forms.CharField(max_length=15, required=False)
    cpf = forms.CharField(max_length=14, required=False)

    class Meta:
        model = Usuario
        fields = (
            "nome_completo",
            "telefone",
            "cpf",
            "cargo",
            "empresa",
            "setor",
        )

    def clean_telefone(self):
        return normalize_digits(self.cleaned_data["telefone"])

    def clean_cpf(self):
        return normalize_digits(self.cleaned_data["cpf"]) or None

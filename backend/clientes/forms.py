from django import forms

from core.normalizers import normalize_digits

from .choices import TipoCliente
from .models import Cliente


class ClienteForm(forms.ModelForm):
    documento = forms.CharField(max_length=18)
    telefone = forms.CharField(max_length=16)
    cep = forms.CharField(max_length=9)
    confirmar_duplicidade = forms.BooleanField(
        required=False,
        widget=forms.HiddenInput,
    )
    duplicate_confirmation_token = forms.CharField(
        required=False,
        widget=forms.HiddenInput,
    )

    class Meta:
        model = Cliente
        fields = (
            "tipo",
            "nome",
            "documento",
            "data_referencia",
            "email",
            "telefone",
            "cep",
            "logradouro",
            "numero",
            "complemento",
            "bairro",
            "cidade",
            "estado",
            "observacoes",
        )
        widgets = {
            "data_referencia": forms.DateInput(attrs={"type": "date"}),
            "observacoes": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        tipo = self._selected_type()
        self.fields["nome"].label = (
            "Nome empresarial" if tipo == TipoCliente.PJ else "Nome completo"
        )
        self.fields["documento"].label = "CNPJ" if tipo == TipoCliente.PJ else "CPF"
        self.fields["data_referencia"].label = (
            "Data de abertura" if tipo == TipoCliente.PJ else "Data de nascimento"
        )
        for field_name in ("documento", "telefone", "cep"):
            self.fields[field_name].widget.attrs["inputmode"] = "numeric"
        self.fields["documento"].widget.attrs["autocomplete"] = "off"
        self.fields["telefone"].widget.attrs["autocomplete"] = "tel"
        self.fields["email"].widget.attrs["autocomplete"] = "email"
        self.fields["cep"].widget.attrs["autocomplete"] = "postal-code"

    def _selected_type(self) -> str:
        if self.is_bound:
            return self.data.get(self.add_prefix("tipo"), "")
        if self.initial.get("tipo"):
            return self.initial["tipo"]
        if self.instance and self.instance.pk:
            return self.instance.tipo
        return TipoCliente.PF

    def clean_documento(self) -> str:
        return normalize_digits(self.cleaned_data["documento"])

    def clean_telefone(self) -> str:
        return normalize_digits(self.cleaned_data["telefone"])

    def clean_cep(self) -> str:
        return normalize_digits(self.cleaned_data["cep"])

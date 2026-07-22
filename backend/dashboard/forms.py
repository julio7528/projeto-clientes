from django import forms

from clientes.choices import SituacaoCliente, UnidadeFederativa


class DashboardFilterForm(forms.Form):
    situacao = forms.ChoiceField(required=False, choices=(("", "Todas"), *SituacaoCliente.choices))
    estado = forms.ChoiceField(required=False, choices=(("", "Todos"), *UnidadeFederativa.choices))

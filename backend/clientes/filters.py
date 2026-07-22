from django import forms

from core.normalizers import normalize_whitespace

from .choices import SituacaoCliente, TipoCliente, UnidadeFederativa


class ClienteSearchForm(forms.Form):
    q = forms.CharField(required=False, max_length=200, label="Busca")
    tipo = forms.ChoiceField(required=False, choices=(("", "Todos"), *TipoCliente.choices), label="Tipo")
    situacao = forms.ChoiceField(required=False, choices=(("", "Todos"), *SituacaoCliente.choices), label="Situação")
    cidade = forms.CharField(required=False, max_length=100, label="Cidade")
    estado = forms.ChoiceField(required=False, choices=(("", "Todos"), *UnidadeFederativa.choices), label="Estado")
    criado_de = forms.DateField(required=False, label="Criado de", widget=forms.DateInput(attrs={"type": "date"}))
    criado_ate = forms.DateField(required=False, label="Criado até", widget=forms.DateInput(attrs={"type": "date"}))
    atualizado_de = forms.DateField(required=False, label="Atualizado de", widget=forms.DateInput(attrs={"type": "date"}))
    atualizado_ate = forms.DateField(required=False, label="Atualizado até", widget=forms.DateInput(attrs={"type": "date"}))
    ordenar = forms.ChoiceField(required=False, choices=(("nome", "Nome"), ("criado_em", "Criação"), ("atualizado_em", "Atualização"), ("cidade", "Cidade"), ("situacao", "Situação")))
    direcao = forms.ChoiceField(required=False, choices=(("asc", "Crescente"), ("desc", "Decrescente")))

    def clean(self):
        cleaned = super().clean()
        for field in ("q", "cidade"):
            cleaned[field] = normalize_whitespace(cleaned.get(field, ""))
        for start, end in (("criado_de", "criado_ate"), ("atualizado_de", "atualizado_ate")):
            if cleaned.get(start) and cleaned.get(end) and cleaned[start] > cleaned[end]:
                self.add_error(end, "A data final deve ser igual ou posterior à inicial.")
        return cleaned

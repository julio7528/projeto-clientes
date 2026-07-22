from django import forms

from clientes.filters import ClienteSearchForm


class ReportFilterForm(ClienteSearchForm):
    relatorio = forms.ChoiceField(choices=(("geral", "Geral"), ("tipo", "Por tipo"), ("situacao", "Por situação"), ("geografico", "Por localidade"), ("criacao", "Por período de criação"), ("atualizacao", "Por período de atualização"), ("incompletos", "Incompletos")), label="Relatório")

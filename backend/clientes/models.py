from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.functions import Length

from core.models import UUIDTimestampedModel
from core.normalizers import normalize_digits, normalize_whitespace

from .choices import SituacaoCliente, TipoCliente, UnidadeFederativa
from .validators import (
    validate_cep,
    validate_data_nao_futura,
    validate_documento,
    validate_nome,
    validate_telefone,
    validate_uf,
)


models.CharField.register_lookup(Length)


class Cliente(UUIDTimestampedModel):
    tipo = models.CharField(max_length=2, choices=TipoCliente.choices, db_index=True)
    nome = models.CharField(max_length=200, db_index=True)
    documento = models.CharField(
        max_length=14,
        unique=True,
        error_messages={
            "unique": "Já existe um cliente cadastrado com este documento."
        },
    )
    data_referencia = models.DateField(null=True, blank=True)
    email = models.EmailField(blank=True, default="", db_index=True)
    telefone = models.CharField(max_length=11, db_index=True)
    cep = models.CharField(max_length=8)
    logradouro = models.CharField(max_length=200, blank=True)
    numero = models.CharField(max_length=20, blank=True)
    complemento = models.CharField(max_length=100, blank=True)
    bairro = models.CharField(max_length=100, blank=True)
    cidade = models.CharField(max_length=100, blank=True)
    estado = models.CharField(
        max_length=2,
        choices=UnidadeFederativa.choices,
        blank=True,
    )
    observacoes = models.TextField(blank=True)
    situacao = models.CharField(
        max_length=7,
        choices=SituacaoCliente.choices,
        default=SituacaoCliente.ATIVO,
        db_index=True,
    )
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="clientes_criados",
    )
    atualizado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clientes_atualizados",
    )

    class Meta:
        ordering = ("nome",)
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        indexes = [
            models.Index(fields=("estado", "cidade"), name="clientes_estado_cidade_idx"),
            models.Index(fields=("tipo", "situacao"), name="clientes_tipo_situacao_idx"),
            models.Index(fields=("criado_em",), name="clientes_criado_em_idx"),
            models.Index(fields=("atualizado_em",), name="clientes_atualizado_em_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(tipo__in=TipoCliente.values),
                name="clientes_tipo_valido_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(situacao__in=SituacaoCliente.values),
                name="clientes_situacao_valida_ck",
            ),
            models.CheckConstraint(
                condition=(
                    models.Q(tipo=TipoCliente.PF, documento__length=11)
                    | models.Q(tipo=TipoCliente.PJ, documento__length=14)
                ),
                name="clientes_documento_tipo_len_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(telefone__length__in=(10, 11)),
                name="clientes_telefone_len_ck",
            ),
            models.CheckConstraint(
                condition=models.Q(cep__length=8),
                name="clientes_cep_len_ck",
            ),
        ]

    def normalize_fields(self) -> None:
        self.nome = normalize_whitespace(self.nome)
        self.documento = normalize_digits(self.documento)
        self.email = (self.email or "").strip().lower()
        self.telefone = normalize_digits(self.telefone)
        self.cep = normalize_digits(self.cep)
        self.logradouro = normalize_whitespace(self.logradouro)
        self.numero = normalize_whitespace(self.numero)
        self.complemento = normalize_whitespace(self.complemento)
        self.bairro = normalize_whitespace(self.bairro)
        self.cidade = normalize_whitespace(self.cidade)
        self.estado = normalize_whitespace(self.estado).upper()
        self.observacoes = (self.observacoes or "").strip()

    def clean(self) -> None:
        super().clean()
        self.normalize_fields()
        errors: dict[str, list[ValidationError]] = {}
        if self.tipo not in TipoCliente.values:
            errors.setdefault("tipo", []).append(
                ValidationError(
                    "Informe um tipo de cliente válido.",
                    code="invalid_type",
                )
            )
        if self.situacao not in SituacaoCliente.values:
            errors.setdefault("situacao", []).append(
                ValidationError(
                    "Informe uma situação de cliente válida.",
                    code="invalid_status",
                )
            )
        validations = (
            ("nome", validate_nome, self.nome),
            ("documento", lambda value: validate_documento(self.tipo, value), self.documento),
            ("telefone", validate_telefone, self.telefone),
            ("cep", validate_cep, self.cep),
            ("data_referencia", validate_data_nao_futura, self.data_referencia),
            ("estado", validate_uf, self.estado),
        )
        for field, validator, value in validations:
            try:
                validator(value)
            except ValidationError as error:
                errors.setdefault(field, []).extend(error.error_list)
        if errors:
            raise ValidationError(errors)

    def full_clean(
        self,
        exclude=None,
        validate_unique: bool = True,
        validate_constraints: bool = True,
    ) -> None:
        self.normalize_fields()
        super().full_clean(
            exclude=exclude,
            validate_unique=validate_unique,
            validate_constraints=validate_constraints,
        )

    def save(self, *args, **kwargs) -> None:
        self.normalize_fields()
        super().save(*args, **kwargs)

    def ativar(self) -> None:
        self.situacao = SituacaoCliente.ATIVO

    def inativar(self) -> None:
        self.situacao = SituacaoCliente.INATIVO

    def __str__(self) -> str:
        return self.nome

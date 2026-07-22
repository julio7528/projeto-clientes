import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.functions import Lower

from .managers import UsuarioManager
from .validators import normalize_digits, validate_cpf


class Usuario(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = None
    first_name = None
    last_name = None
    email = models.EmailField("e-mail", unique=True)
    nome_completo = models.CharField(max_length=255)
    telefone = models.CharField(max_length=11, blank=True)
    cpf = models.CharField(
        max_length=11,
        unique=True,
        null=True,
        blank=True,
        validators=[validate_cpf],
    )
    cargo = models.CharField(max_length=120, blank=True)
    foto = models.CharField(
        max_length=1024,
        blank=True,
        help_text="Referencia interna backend-only para o Storage.",
    )
    empresa = models.CharField(max_length=255, blank=True)
    setor = models.CharField(max_length=120, blank=True)
    observacoes = models.TextField(blank=True)

    objects = UsuarioManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: list[str] = ["nome_completo"]

    class Meta:
        verbose_name = "usuario"
        verbose_name_plural = "usuarios"
        constraints = [
            models.UniqueConstraint(Lower("email"), name="usuarios_email_ci_unique"),
        ]

    def clean(self) -> None:
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email).strip().lower()
        self.telefone = normalize_digits(self.telefone)
        self.cpf = normalize_digits(self.cpf) or None
        validate_cpf(self.cpf)

    def save(self, *args, **kwargs) -> None:
        self.email = self.__class__.objects.normalize_email(self.email).strip().lower()
        self.telefone = normalize_digits(self.telefone)
        self.cpf = normalize_digits(self.cpf) or None
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.email

from typing import Any

from django.contrib.auth.base_user import BaseUserManager


class UsuarioManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email: str, password: str | None, **extra_fields: Any):
        if not email:
            raise ValueError("O e-mail e obrigatorio.")

        email = self.normalize_email(email).strip().lower()
        user = self.model(email=email, **extra_fields)
        user.clean()
        user.full_clean(exclude={"password"})
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, password: str | None = None, **extra_fields: Any):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(
        self,
        email: str,
        password: str | None = None,
        **extra_fields: Any,
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superusuario deve ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superusuario deve ter is_superuser=True.")

        return self._create_user(email, password, **extra_fields)

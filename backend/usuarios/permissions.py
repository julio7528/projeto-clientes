from typing import Any

from django.db.models import QuerySet


def is_administrator(user: Any) -> bool:
    return bool(user.is_authenticated and user.is_staff and user.is_superuser)


def can_access_owned_object(user: Any, obj: Any, owner_attr: str = "owner") -> bool:
    if is_administrator(user):
        return True
    return getattr(obj, f"{owner_attr}_id") == user.pk


def scope_owned_queryset(
    queryset: QuerySet,
    user: Any,
    owner_field: str = "criado_por",
) -> QuerySet:
    if is_administrator(user):
        return queryset
    return queryset.filter(**{owner_field: user})

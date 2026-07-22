from collections.abc import Callable
from functools import wraps
from typing import ParamSpec, TypeVar

from django.http import HttpResponse


P = ParamSpec("P")
R = TypeVar("R", bound=HttpResponse)


def private_no_store(view: Callable[P, R]) -> Callable[P, R]:
    """Impede armazenamento de respostas autenticadas com dados pessoais."""

    @wraps(view)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        response = view(*args, **kwargs)
        response["Cache-Control"] = "private, no-store"
        response["Pragma"] = "no-cache"
        return response

    return wrapper

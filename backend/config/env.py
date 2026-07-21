from decouple import Csv, config
from django.core.exceptions import ImproperlyConfigured


def required_env(name):
    value = config(name, default="")
    if not str(value).strip():
        raise ImproperlyConfigured(f"Missing required environment variable: {name}")
    return value


def optional_env(name, default=""):
    return config(name, default=default)


def bool_env(name, default=False):
    return config(name, default=default, cast=bool)


def int_env(name, default=0):
    return config(name, default=default, cast=int)


def csv_env(name, default=""):
    return config(name, default=default, cast=Csv())

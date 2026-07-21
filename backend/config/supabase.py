import json
from dataclasses import dataclass
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from django.conf import settings


class SupabaseServiceError(RuntimeError):
    pass


@dataclass(frozen=True)
class SupabaseServiceConfig:
    url: str
    secret_key: str
    private_storage_bucket: str
    signed_url_ttl_seconds: int


def get_supabase_config():
    return SupabaseServiceConfig(
        url=settings.SUPABASE_URL.rstrip("/"),
        secret_key=settings.SUPABASE_SECRET_KEY,
        private_storage_bucket=settings.SUPABASE_PRIVATE_STORAGE_BUCKET,
        signed_url_ttl_seconds=settings.SUPABASE_SIGNED_URL_TTL_SECONDS,
    )


def _validate_storage_path(object_path):
    clean_path = object_path.strip().lstrip("/")
    if not clean_path or ".." in clean_path.split("/"):
        raise ValueError("Invalid storage object path.")
    return clean_path


def create_private_storage_signed_url(object_path, expires_in=None):
    service_config = get_supabase_config()
    clean_path = _validate_storage_path(object_path)
    ttl = expires_in or service_config.signed_url_ttl_seconds
    ttl = max(1, min(int(ttl), service_config.signed_url_ttl_seconds))

    object_url = quote(clean_path, safe="/")
    endpoint = (
        f"{service_config.url}/storage/v1/object/sign/"
        f"{service_config.private_storage_bucket}/{object_url}"
    )
    payload = json.dumps({"expiresIn": ttl}).encode("utf-8")
    request = Request(
        endpoint,
        data=payload,
        method="POST",
        headers={
            "apikey": service_config.secret_key,
            "Authorization": f"Bearer {service_config.secret_key}",
            "Content-Type": "application/json",
        },
    )

    try:
        with urlopen(request, timeout=10) as response:
            data = json.loads(response.read().decode("utf-8"))
    except HTTPError as exc:
        raise SupabaseServiceError(f"Supabase Storage rejected the request: {exc.code}") from exc
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise SupabaseServiceError("Supabase Storage request failed.") from exc

    signed_url = data.get("signedURL") or data.get("signedUrl")
    if not signed_url:
        raise SupabaseServiceError("Supabase Storage did not return a signed URL.")

    if signed_url.startswith("/"):
        signed_url = f"{service_config.url}{signed_url}"

    return {
        "signed_url": signed_url,
        "expires_in": ttl,
    }

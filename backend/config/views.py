import json
import logging
import uuid
from functools import wraps

from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from .models import ProtectedFile
from .supabase import SupabaseServiceError, create_private_storage_signed_url

logger = logging.getLogger(__name__)


def _authenticated_api(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"detail": "Authentication required."}, status=401)
        return view_func(request, *args, **kwargs)

    return wrapper


def _private_response(data, *, status=200):
    response = JsonResponse(data, status=status)
    response["Cache-Control"] = "no-store, private"
    response["Pragma"] = "no-cache"
    return response


@require_GET
@_authenticated_api
def protected_profile(request):
    return JsonResponse(
        {
            "id": request.user.pk,
            "username": request.user.get_username(),
            "is_staff": request.user.is_staff,
        }
    )


@require_POST
@_authenticated_api
def private_storage_url(request):
    try:
        content_length = int(request.META.get("CONTENT_LENGTH") or 0)
        if content_length > settings.PRIVATE_STORAGE_REQUEST_MAX_BYTES:
            return _private_response({"detail": "Request body is too large."}, status=413)

        raw_body = request.body
        if len(raw_body) > settings.PRIVATE_STORAGE_REQUEST_MAX_BYTES:
            return _private_response({"detail": "Request body is too large."}, status=413)

        payload = json.loads(raw_body.decode("utf-8") or "{}")
        if not isinstance(payload, dict):
            raise ValueError

        raw_file_id = payload["arquivo_id"]
        file_id = uuid.UUID(str(raw_file_id))
        expires_in = payload.get("expires_in")
        if expires_in is not None and (
            isinstance(expires_in, bool) or not isinstance(expires_in, int)
        ):
            raise ValueError

        try:
            protected_file = ProtectedFile.objects.select_related("owner").get(pk=file_id)
        except ProtectedFile.DoesNotExist:
            return _private_response({"detail": "File not found."}, status=404)

        if protected_file.owner_id != request.user.pk:
            return _private_response({"detail": "Access denied."}, status=403)

        data = create_private_storage_signed_url(
            protected_file.storage_path,
            expires_in=expires_in,
        )
    except KeyError:
        return _private_response({"detail": "Missing required field: arquivo_id."}, status=400)
    except (TypeError, ValueError, UnicodeDecodeError, json.JSONDecodeError):
        return _private_response({"detail": "Invalid storage request."}, status=400)
    except SupabaseServiceError:
        logger.warning("Supabase private Storage signing failed")
        return _private_response({"detail": "Private storage is unavailable."}, status=502)

    return _private_response(data)

import json

from django.http import JsonResponse
from django.views.decorators.http import require_GET, require_POST

from .supabase import SupabaseServiceError, create_private_storage_signed_url


def _authenticated_api(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse({"detail": "Authentication required."}, status=401)
        return view_func(request, *args, **kwargs)

    return wrapper


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
        payload = json.loads(request.body.decode("utf-8") or "{}")
        object_path = payload["path"]
        expires_in = payload.get("expires_in")
        data = create_private_storage_signed_url(object_path, expires_in=expires_in)
    except KeyError:
        return JsonResponse({"detail": "Missing required field: path."}, status=400)
    except (TypeError, ValueError, json.JSONDecodeError):
        return JsonResponse({"detail": "Invalid storage request."}, status=400)
    except SupabaseServiceError:
        return JsonResponse({"detail": "Private storage is unavailable."}, status=502)

    return JsonResponse(data)

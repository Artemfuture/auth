from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from access.services import PermissionService


def permission_required(resource, permission):
    def decorator(view_method):
        @wraps(view_method)
        def wrapper(view, request, *args, **kwargs):
            if not request.user.is_authenticated:
                return Response(
                    {"detail": "Unauthorized"},
                    status=status.HTTP_401_UNAUTHORIZED,
                )

            if not PermissionService.has_permission(
                request.user,
                resource,
                permission,
            ):
                return Response(
                    {"detail": "Forbidden"},
                    status=status.HTTP_403_FORBIDDEN,
                )

            return view_method(
                view,
                request,
                *args,
                **kwargs,
            )

        return wrapper

    return decorator

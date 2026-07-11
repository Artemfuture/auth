from django.utils.deprecation import MiddlewareMixin

from users.models import User
from .jwt_service import JWTService
from access.models import BlacklistedToken


class JWTAuthenticationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        request.user = None

        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return

        if not auth_header.startswith("Bearer "):
            return

        token = auth_header.split(" ")[1]

        if BlacklistedToken.objects.filter(token=token).exists():
            return

        payload = JWTService.decode_token(token)

        if payload is None:
            return

        try:
            user = User.objects.get(id=payload["user_id"], is_active=True)

            request.user = user

        except User.DoesNotExist:
            return

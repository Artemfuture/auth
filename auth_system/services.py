from .jwt_service import JWTService


class AuthService:
    @staticmethod
    def login(user):
        token = JWTService.generate_token(user.id)

        return {
            "access_token": token,
            "token_type": "Bearer",
        }

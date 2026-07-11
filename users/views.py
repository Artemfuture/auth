from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from auth_system.jwt_service import JWTService
from .serializers import RegisterSerializer, LoginSerializer, UpdateProfileSerializer
from auth_system.permissions import permission_required

from datetime import datetime

from access.models import BlacklistedToken


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(
            {"message": "Пользователь успешно зарегистрирован."},
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        token = JWTService.generate_token(user.id)

        return Response(
            {
                "access_token": token,
                "token_type": "Bearer",
            },
            status=status.HTTP_200_OK,
        )


class MeView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return Response(
            {
                "id": request.user.id,
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
            }
        )


class LogoutView(APIView):
    def post(self, request):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(
                {"detail": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token = auth_header.split(" ")[1]

        payload = JWTService.decode_token(token)

        if payload is None:
            return Response(
                {"detail": "Invalid token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        BlacklistedToken.objects.get_or_create(
            token=token, expires_at=datetime.fromtimestamp(payload["exp"])
        )

        return Response(
            {"message": "Logout successful."},
            status=status.HTTP_200_OK,
        )


class ProfileView(APIView):
    def put(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Unauthorized"},
                status=401,
            )

        serializer = UpdateProfileSerializer(
            request.user,
            data=request.data,
            partial=True,
        )

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)

    def delete(self, request):
        if not request.user.is_authenticated:
            return Response(
                {"detail": "Unauthorized"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        request.user.is_active = False
        request.user.save()

        return Response({"message": "Account deleted."})

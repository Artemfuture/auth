from rest_framework import serializers

from .models import User
from access.models import Role, UserRole


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "last_name",
            "first_name",
            "middle_name",
            "email",
            "password",
            "password_repeat",
        )

    def validate(self, attrs):
        if attrs["password"] != attrs["password_repeat"]:
            raise serializers.ValidationError({"password": "Пароли не совпадают."})

        if User.objects.filter(email=attrs["email"]).exists():
            raise serializers.ValidationError(
                {"email": "Пользователь с таким email уже существует."}
            )

        return attrs

    def create(self, validated_data):
        validated_data.pop("password_repeat")

        password = validated_data.pop("password")

        user = User.objects.create_user(password=password, **validated_data)

        role = Role.objects.get(name="User")

        UserRole.objects.create(user=user, role=role)

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({"detail": "Неверный email или пароль."})

        if not user.is_active:
            raise serializers.ValidationError({"detail": "Аккаунт удален."})

        if not user.check_password(password):
            raise serializers.ValidationError({"detail": "Неверный email или пароль."})

        attrs["user"] = user

        return attrs


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "middle_name",
            "email",
        )

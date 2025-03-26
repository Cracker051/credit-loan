import jwt
from rest_framework import serializers

from backend.authorize.models import Role, User


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(trim_whitespace=False)


class RegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.only("pk").all())

    @staticmethod
    def validate_email(value: str) -> str:
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("USER_ALREADY_EXISTS")
        return value


class TokenSerializer(serializers.Serializer):
    token = serializers.CharField()

    @staticmethod
    def validate_token(value: str) -> str:
        # Just to check structe of jwt, algorithm doesn`t matter
        try:
            jwt.decode(value, algorithms=None)
        except jwt.exceptions.DecodeError as e:
            if "Not enough segments" == str(e):
                raise serializers.ValidationError(str(e))
        return value

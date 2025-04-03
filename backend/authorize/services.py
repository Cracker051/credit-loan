from typing import override

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from backend.authorize.const import JWT_ERRORS, TokenType
from backend.authorize.models import Role, User
from backend.authorize.utils import generate_token, get_jwt_credentials
from backend.base.services import BaseService


class LoginService(BaseService):
    def __init__(self, username: str, password: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.username = username
        self.password = password

    def authenticate_user(self) -> dict:
        user = authenticate(username=self.username, password=self.password)
        if user is None:
            raise ValidationError("WRONG_CREDENTIALS")

        return get_jwt_credentials(user)

    @override
    @property
    def response(self) -> Response:
        handler = self.authenticate_user()
        return Response(handler, status=200)


class RegisterUserService(BaseService):
    def __init__(self, first_name: str, last_name: str, email: str, password: str, role: Role, **kwargs) -> None:
        super().__init__(**kwargs)
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.role = role

    def register_user(self) -> dict:
        user = User.objects.create_user(
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            password=self.password,
            role=self.role,
        )
        return get_jwt_credentials(user)

    @property
    def response(self) -> Response:
        handler = self.register_user()
        return Response(handler, status=201)


class RenewAccessTokenService(BaseService):
    def __init__(self, token: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.token = token

    def renew_access_token(self) -> dict:
        """Because we don`t store refresh tokens anywhere, decoding it and verify"""
        try:
            payload = jwt.decode(self.token, settings.SECRET_KEY, algorithms=[settings.AUTH_HASH_ALGORITHM])
        except JWT_ERRORS as e:
            raise ValidationError(str(e))

        if payload.get("type") != TokenType.REFRESH:
            raise ValidationError("ONLY_REFRESH_TOKEN_SUPPORTED")

        access_token = generate_token(
            {"type": TokenType.ACCESS, "user_id": payload["user_id"]}, lifetime=settings.ACCESS_TOKEN_LIFETIME
        )

        return {"access": access_token}

    @override
    @property
    def response(self) -> Response:
        handler = self.renew_access_token()
        return Response(handler, status=200)


class DecodeTokenService(BaseService):
    def __init__(self, token: str, **kwargs) -> None:
        super().__init__(**kwargs)
        self.token = token

    def decode_token(self) -> dict:
        try:
            payload = jwt.decode(self.token, settings.SECRET_KEY, algorithms=[settings.AUTH_HASH_ALGORITHM])
        except JWT_ERRORS as e:
            raise ValidationError(str(e))

        if payload.get("type") != TokenType.ACCESS:
            raise ValidationError("ONLY_ACCESS_TOKEN_SUPPORTED")

        user_info = (
            User.objects.filter(pk=payload["user_id"])
            .select_related("role")
            .values("id", "first_name", "last_name", "email", "is_verified", "role__name")
            .first()
        )

        return user_info

    @override
    @property
    def response(self) -> Response:
        handler = self.decode_token()
        return Response(handler, status=200)


class SendVerificationService(BaseService):
    def send_verification(self) -> dict:
        if self.user.is_verified:
            result = {"result": "Email is already verified"}
        else:
            User.objects.send_verification_mail(self.user)
            result = {"result": True}
        return result

    @override
    @property
    def response(self) -> Response:
        handler = self.send_verification()
        return Response(handler, status=200)

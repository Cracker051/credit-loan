from datetime import datetime, timedelta
from typing import Any

import jwt
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser

from backend.authorize.const import TokenType


def generate_token(
    body: dict[str, Any],
    *,
    algorithm: str = settings.AUTH_HASH_ALGORITHM,
    lifetime: timedelta = None,
    pass_key: str = settings.SECRET_KEY,
) -> str:
    if lifetime is not None:
        body["exp"] = datetime.now() + lifetime
    return jwt.encode(body, pass_key, algorithm)


def get_jwt_credentials(user: AbstractBaseUser) -> dict:
    payload_body = {"user_id": user.pk}
    access_token = generate_token({"type": TokenType.ACCESS, **payload_body}, lifetime=settings.ACCESS_TOKEN_LIFETIME)

    refresh_token = generate_token(
        {"type": TokenType.REFRESH, **payload_body}, lifetime=settings.REFRESH_TOKEN_LIFETIME
    )

    return {"access": access_token, "refresh": refresh_token}

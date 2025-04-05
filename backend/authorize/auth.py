import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework.request import HttpRequest


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request: HttpRequest) -> None | tuple:
        token = request.headers.get("Authorization")

        if token is None or not token.startswith(settings.DEFAULT_AUTH_PREFIX):
            return None

        token = token.split(settings.DEFAULT_AUTH_PREFIX, maxsplit=1)[-1].strip()
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.AUTH_HASH_ALGORITHM])
        except (jwt.DecodeError, jwt.InvalidSignatureError, jwt.ExpiredSignatureError):
            return None

        if (user_pk := payload.get("user_id")) is not None:
            user = get_user_model().objects.filter(pk=user_pk).first()

        return (user, token)

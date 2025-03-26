from typing import Callable

import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse


class JWTAuthMiddleware:
    def __init__(self, get_response: Callable) -> None:
        self.get_response = get_response

    def __call__(self, request: HttpRequest) -> HttpResponse:
        token = request.headers.get("Authorization")

        if token is None or not token.startswith(settings.DEFAULT_AUTH_PREFIX):
            request.user = AnonymousUser()
            return self.get_response(request)

        token = token.split(settings.DEFAULT_AUTH_PREFIX, maxsplit=1)[-1]
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.AUTH_ALGORITHMS)
        except (jwt.DecodeError, jwt.InvalidSignatureError, jwt.ExpiredSignatureError):
            request.user = AnonymousUser()
            return self.get_response(request)

        if (user_pk := payload.get("user_id")) is None:
            request.user = AnonymousUser()
        else:
            request.user = get_user_model().objects.filter(pk=user_pk).first() or AnonymousUser()

        return self.get_response(request)

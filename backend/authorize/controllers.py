from backend.authorize.permissions import IsAuthenticated
from backend.authorize.serializers import BaseSerializer, LoginSerializer, RegisterSerializer, TokenSerializer
from backend.authorize.services import (
    DecodeTokenService,
    LoginService,
    RegisterUserService,
    RenewAccessTokenService,
    SendVerificationService,
)
from backend.base.controllers import BaseAPIController


class RegisterController(BaseAPIController):
    serializer_classes = {"post": RegisterSerializer}
    service_classes = {"post": RegisterUserService}


class LoginController(BaseAPIController):
    serializer_classes = {"post": LoginSerializer}
    service_classes = {"post": LoginService}


class RenewTokenController(BaseAPIController):
    serializer_classes = {"post": TokenSerializer}
    service_classes = {"post": RenewAccessTokenService}


class DecodeTokenController(BaseAPIController):
    serializer_classes = {"post": TokenSerializer}
    service_classes = {"post": DecodeTokenService}


class SendVerificationController(BaseAPIController):
    permission_classes = {"get": [IsAuthenticated]}
    serializer_classes = {"default": BaseSerializer}
    service_classes = {"get": SendVerificationService}

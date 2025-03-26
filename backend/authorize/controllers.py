from backend.authorize.serializers import LoginSerializer, RegisterSerializer, TokenSerializer
from backend.authorize.services import DecodeTokenService, LoginService, RegisterUserService, RenewAccessTokenService
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

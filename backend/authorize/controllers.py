from backend.authorize import permissions, serializers, services
from backend.base.controllers import BaseAPIController


class RegisterController(BaseAPIController):
    serializer_classes = {"post": serializers.RegisterSerializer}
    service_classes = {"post": services.RegisterUserService}


class LoginController(BaseAPIController):
    serializer_classes = {"post": serializers.LoginSerializer}
    service_classes = {"post": services.LoginService}


class RenewTokenController(BaseAPIController):
    serializer_classes = {"post": serializers.TokenSerializer}
    service_classes = {"post": services.RenewAccessTokenService}


class DecodeTokenController(BaseAPIController):
    serializer_classes = {"post": serializers.TokenSerializer}
    service_classes = {"post": services.DecodeTokenService}


class SendVerificationController(BaseAPIController):
    permission_classes = {"get": [permissions.IsAuthenticated]}
    serializer_classes = {"default": serializers.BaseSerializer}
    service_classes = {"get": services.SendVerificationService}


class VerifyEmailController(BaseAPIController):
    permission_classes = {"post": [permissions.IsAuthenticated]}
    serializer_classes = {"post": serializers.TokenSerializer}
    service_classes = {"post": services.VerifyUserEmailService}

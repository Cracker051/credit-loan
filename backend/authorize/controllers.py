from backend.authorize import permissions, serializers, services
from backend.base.controllers import BaseAPIController

from drf_yasg.utils import swagger_auto_schema


class RegisterController(BaseAPIController):
    serializer_classes = {"post": serializers.RegisterSerializer}
    service_classes = {"post": services.RegisterUserService}

    @swagger_auto_schema(request_body=serializers.RegisterSerializer)
    def post(self, request, *args, **kwargs):
        return self.dispatch(request, *args, **kwargs)


class LoginController(BaseAPIController):
    serializer_classes = {"post": serializers.LoginSerializer}
    service_classes = {"post": services.LoginService}

    @swagger_auto_schema(request_body=serializers.LoginSerializer)
    def post(self, request, *args, **kwargs):
        return self.dispatch(request, *args, **kwargs)


class RenewTokenController(BaseAPIController):
    serializer_classes = {"post": serializers.TokenSerializer}
    service_classes = {"post": services.RenewAccessTokenService}

    @swagger_auto_schema(request_body=serializers.TokenSerializer)
    def post(self, request, *args, **kwargs):
        return self.dispatch(request, *args, **kwargs)


class DecodeTokenController(BaseAPIController):
    serializer_classes = {"post": serializers.TokenSerializer}
    service_classes = {"post": services.DecodeTokenService}

    @swagger_auto_schema(request_body=serializers.TokenSerializer)
    def post(self, request, *args, **kwargs):
        return self.dispatch(request, *args, **kwargs)



class SendVerificationController(BaseAPIController):
    permission_classes = {"get": [permissions.IsAuthenticated]}
    serializer_classes = {"default": serializers.BaseSerializer}
    service_classes = {"get": services.SendVerificationService}

    def get(self, request, *args, **kwargs):
        return self.dispatch(request, *args, **kwargs)


class VerifyEmailController(BaseAPIController):
    permission_classes = {"post": [permissions.IsAuthenticated]}
    serializer_classes = {"post": serializers.TokenSerializer}
    service_classes = {"post": services.VerifyUserEmailService}

    @swagger_auto_schema(request_body=serializers.TokenSerializer)
    def post(self, request, *args, **kwargs):
        return self.dispatch(request, *args, **kwargs)

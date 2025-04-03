from django.urls import path

from backend.authorize.controllers import (
    DecodeTokenController,
    LoginController,
    RegisterController,
    RenewTokenController,
    SendVerificationController,
)


urlpatterns = [
    path("register/", RegisterController.as_view()),
    path("login/", LoginController.as_view()),
    path("token/", RenewTokenController.as_view()),
    path("decode/", DecodeTokenController.as_view()),
    path("verify/", SendVerificationController.as_view()),
]

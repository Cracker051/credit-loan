from django.urls import path

from backend.authorize import controllers


urlpatterns = [
    path("register/", controllers.RegisterController.as_view()),
    path("login/", controllers.LoginController.as_view()),
    path("token/", controllers.RenewTokenController.as_view()),
    path("decode/", controllers.DecodeTokenController.as_view()),
    path("send_verification/", controllers.SendVerificationController.as_view()),
    path("verify/", controllers.VerifyEmailController.as_view()),
]

from rest_framework import exceptions, status


class ValidationError(exceptions.ValidationError):
    pass


class UserAlreadyVerifiedException(exceptions.APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "User with this email already verified"
    default_code = "ALREADY_VERIFIED_ERROR"


class EmailDoesNotMatchException(exceptions.APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = "Token email and user email don`t mathc"
    default_code = "VERIFY_EMAIL_CONFLICT"

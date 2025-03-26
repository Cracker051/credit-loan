import jwt


class BaseTextChoices:
    @classmethod
    def choices(cls) -> dict:
        return {k.capitalize(): v for k, v in cls.__dict__.items() if not k.startswith(("__", "_"))}


class RoleChoices(BaseTextChoices):
    USER = "user"
    OPERATOR = "operator"
    CREDITOR = "creditor"


class TokenType(BaseTextChoices):
    REFRESH = "refresh"
    ACCESS = "access"


JWT_ERRORS = (
    jwt.ExpiredSignatureError,
    jwt.InvalidTokenError,
    jwt.DecodeError,
    jwt.InvalidSignatureError,
    jwt.InvalidAlgorithmError,
    jwt.MissingRequiredClaimError,
)

import jwt


class BaseTextChoices:
    @classmethod
    def choices(cls) -> dict:
        return {k.capitalize(): v for k, v in cls.__dict__.items() if not k.startswith(("__", "_"))}
    
    @classmethod
    def is_valid(_class, choice: str) -> bool:
        return (choice in BaseTextChoices.choices().values())


class RoleChoices(BaseTextChoices):
    USER = "user"
    OPERATOR = "operator"
    ADMIN = "admin"


class TokenType(BaseTextChoices):
    REFRESH = "refresh"
    ACCESS = "access"


class CreditPlanType(BaseTextChoices):
    CONSUMER = "consumer"
    PURPOSE = "purpose"


class TimePeriodType(BaseTextChoices):
    DAY = "day"
    MONTH = "month"
    QUARTER = "quarter"
    YEAR = "year"


class TransactionType(BaseTextChoices):
    INCOME = 'income'
    OUTCOME = 'outcome'


class CreditRequestStatusType(BaseTextChoices):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


JWT_ERRORS = (
    jwt.ExpiredSignatureError,
    jwt.InvalidTokenError,
    jwt.DecodeError,
    jwt.InvalidSignatureError,
    jwt.InvalidAlgorithmError,
    jwt.MissingRequiredClaimError,
)

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
    REFRESH = "Refresh"
    ACCESS = "Access"


class CreditPlanType(BaseTextChoices):
    CONSUMER = "Consumer"
    PURPOSE = "Purpose"


class TimePeriodType(BaseTextChoices):
    DAY = "Day"
    MONTH = "Month"
    QUARTER = "Quarter"
    YEAR = "Year"


class TransactionType(BaseTextChoices):
    INCOME = 'Income'
    OUTCOME = 'Outcome'


class CreditRequestStatusType(BaseTextChoices):
    PENDING = "Pending"
    ACCEPTED = "Accepted"
    REJECTED = "Rejected"


JWT_ERRORS = (
    jwt.ExpiredSignatureError,
    jwt.InvalidTokenError,
    jwt.DecodeError,
    jwt.InvalidSignatureError,
    jwt.InvalidAlgorithmError,
    jwt.MissingRequiredClaimError,
)

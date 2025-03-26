from django.contrib.auth.models import AbstractUser, BaseUserManager

from credit_loan.settings import MINIMAL_PASSWORD_LEN


class UserManager(BaseUserManager):
    def _create_user(self, email: str, first_name: str, last_name: str, password: str, **extra_fields) -> AbstractUser:
        if not email:
            raise ValueError("The Email field must be set")

        if len(password) < MINIMAL_PASSWORD_LEN:
            raise ValueError("Password is too short!")

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email: str, first_name: str, last_name: str, password: str, **extra_fields) -> AbstractUser:
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        return self._create_user(email, first_name, last_name, password, **extra_fields)

    def create_superuser(
        self, email: str, first_name: str, last_name: str, password: str, **extra_fields
    ) -> AbstractUser:
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self._create_user(email, first_name, last_name, password, **extra_fields)

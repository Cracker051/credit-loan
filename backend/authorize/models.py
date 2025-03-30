from typing import Optional, override

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

from backend.authorize.const import RoleChoices
from credit_loan.settings import MINIMAL_PASSWORD_LEN


class Role(models.Model):
    name = models.CharField(max_length=20, primary_key=True, choices=RoleChoices.choices())

    @classmethod
    def get_admin_role(cls) -> Optional["Role"]:
        return cls.objects.filter(name=RoleChoices.ADMIN).first()

    @classmethod
    def get_operator_role(cls) -> Optional["Role"]:
        return cls.objects.filter(name=RoleChoices.OPERATOR).first()

    class Meta:
        db_table = "auth_role"


class UserManager(BaseUserManager):
    def _create_user(self, email: str, first_name: str, last_name: str, password: str, **extra_fields) -> "User":
        if not email:
            raise ValueError("The Email field must be set")

        if len(password) < MINIMAL_PASSWORD_LEN:
            raise ValueError("Password is too short!")

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email: str, first_name: str, last_name: str, password: str, role: Role, **extra_fields
    ) -> "User":
        admin_role = Role.get_admin_role()
        if role == admin_role:
            raise ValueError("Cannot create user with role admin. Use `create_superuser` instead.")

        extra_fields.setdefault("is_verified", False)
        return self._create_user(email, first_name, last_name, password, role=role, **extra_fields)

    def create_superuser(self, email: str, first_name: str, last_name: str, password: str, **extra_fields) -> "User":
        admin_role = Role.get_admin_role()

        extra_fields.setdefault("is_verified", True)
        extra_fields.setdefault("role", admin_role)

        return self._create_user(email, first_name, last_name, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    is_verified = models.BooleanField(default=False)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users")

    USERNAME_FIELD = "email"

    objects = UserManager()

    @property
    def is_staff(self):
        # For correct work with Django perms
        return self.role in (Role.get_admin_role(), Role.get_operator_role())

    @override
    @property
    def is_superuser(self):
        # For correct work with Django perms
        return self.role == Role.get_admin_role()

    class Meta:
        db_table = "auth_user"

from typing import Optional, override

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.template.loader import render_to_string

from backend.authorize.utils import generate_token
from backend.base.const import RoleChoices


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
    def get_queryset(self) -> models.QuerySet:
        # Resolving N+1
        return super().get_queryset().select_related("role")

    def _create_user(self, email: str, first_name: str, last_name: str, password: str, **extra_fields) -> "User":
        if not email:
            raise ValueError("The Email field must be set")

        if len(password) < settings.MINIMAL_PASSWORD_LEN:
            raise ValueError("Password is too short!")

        email = self.normalize_email(email)
        user = self.model(email=email, first_name=first_name, last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(
        self, email: str, first_name: str, last_name: str, password: str, role: Role, **extra_fields
    ) -> "User":
        if role.name == RoleChoices.ADMIN:
            raise ValueError("Cannot create user with role admin. Use `create_superuser` instead.")

        extra_fields.setdefault("is_verified", False)
        user = self._create_user(email, first_name, last_name, password, role=role, **extra_fields)
        self.send_verification_mail(user)
        return user

    @staticmethod
    def send_verification_mail(user: "User") -> None:
        token = generate_token({"user_id": user.id}, lifetime=settings.EMAIL_VERIFICATION_LIFETIME)
        email_str = render_to_string(
            "email/confirmation.html", context={"name": user.first_name, "surname": user.last_name, "token": token}
        )
        send_mail(
            subject="Registration in credit service",
            recipient_list=[user.email],
            html_message=email_str,
            fail_silently=True,
            from_email=None,
            message="",
        )

    def create_superuser(self, email: str, first_name: str, last_name: str, password: str, **extra_fields) -> "User":
        admin_role = Role.objects.get(name=RoleChoices.ADMIN)

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
        return self.role.name in (RoleChoices.OPERATOR, RoleChoices.ADMIN)

    @override
    @property
    def is_superuser(self):
        # For correct work with Django perms
        return self.role.name == RoleChoices.ADMIN

    class Meta:
        db_table = "auth_user"

from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from backend.authorize.const import RoleChoices
from backend.authorize.managers import UserManager


class Role(models.Model):
    name = models.CharField(max_length=20, primary_key=True, choices=RoleChoices.choices())

    class Meta:
        db_table = "auth_role"


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, related_name="users")

    USERNAME_FIELD = "email"

    objects = UserManager()

    class Meta:
        db_table = "auth_user"

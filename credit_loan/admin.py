from django.contrib import admin
from django.http import HttpRequest

from backend.authorize.const import RoleChoices


class CustomAdminPage(admin.AdminSite):
    def has_permission(self, request: HttpRequest) -> bool:
        return (
            not request.user.is_anonymous
            and request.user.is_verified
            and request.user.role.name in (RoleChoices.ADMIN, RoleChoices.OPERATOR)
        )

from typing import Any

from rest_framework.permissions import IsAuthenticated
from rest_framework.request import HttpRequest


class IsVerified(IsAuthenticated):
    def has_permission(self, request: HttpRequest, view: Any) -> bool:
        return super().has_permission(request, view) and self.user.is_verified

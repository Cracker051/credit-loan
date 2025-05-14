from django.contrib.auth.decorators import login_required
from functools import wraps
from django.http import JsonResponse

from backend.base.const import RoleChoices

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsVerifiedUserContent(BasePermission):
  """
  Allows create — only verified,
  read/edit/delete — only author or admin.
  """

  def has_permission(self, request, view):
    # Для POST — перевірка на верифікацію
    if request.method == "POST":
      return request.user and request.user.is_authenticated and request.user.is_verified

    # Для GET, PUT, PATCH, DELETE — потрібно перевірити об'єкт (has_object_permission)
    return request.user and request.user.is_authenticated

  def has_object_permission(self, request, view, obj):
    if not request.user:
      return False
    
    return request.user == obj.user or request.user.is_staff
  

class IsReadOnlyContent(BasePermission):
  """
  Allows anyone to read,
  create/edit/delete — staff only.
  """
  
  def has_permission(self, request, view):
    print("request:", request)
    print("request.user:", request.user)

    # Дозволяємо будь-кому GET-запити
    if request.method in SAFE_METHODS:
      return True

    # Для POST, PUT, PATCH, DELETE — staff only
    print("staff:",request.user and request.user.is_authenticated and request.user.is_staff)
    return request.user and request.user.is_authenticated and request.user.is_staff


class IsStaffOnlyContent(BasePermission):
  """
  Restricts access to operators and admins only
  """
  def has_permission(self, request, view):
    return request.user and request.user.is_authenticated and request.user.is_staff


def non_public_content(view_func):
    @login_required
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if (not request.user) or request.user.role == RoleChoices.USER:
          JsonResponse(
              {"message": "This content is not publicly available"},
              status=403
          )
        return view_func(request, *args, **kwargs)
    return wrapper

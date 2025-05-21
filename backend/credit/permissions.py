from django.contrib.auth.decorators import login_required
from functools import wraps
from django.http import JsonResponse

from backend.base.const import RoleChoices, CreditRequestStatusType

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsVerifiedUserContent(BasePermission):
  """
  Read/edit/delete — only author or staff
  """

  def has_permission(self, request, view):
    return request.user and request.user.is_authenticated and request.user.is_verified

  def has_object_permission(self, request, view, obj):
    print("request.user == obj.user", request.user == obj.user)
    if not (request.user == obj.user or request.user.is_staff):
      return False
    
    return (obj.status == CreditRequestStatusType.PENDING
            or request.user.is_staff
            or request.method == "GET")
  

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


class IsUserListContent(BasePermission):
  """
  Allows create — only verified users
  All other operations — staff only 
  """
  def has_permission(self, request, view):
    if request.method == "POST":
      return request.user and request.user.is_authenticated and request.user.is_verified

    return request.user and request.user.is_authenticated and request.user.is_staff

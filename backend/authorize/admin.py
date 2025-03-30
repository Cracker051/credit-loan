from django.contrib import admin
from django.contrib.auth.models import Group

from backend.authorize.models import User


admin.site.unregister(Group)


@admin.register(User)
class AdminModel(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "is_verified", "role")
    exclude = ("groups", "user_permissions", "password")
    readonly_fields = ("last_login",)

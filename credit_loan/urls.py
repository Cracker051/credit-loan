from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
      title="Credit loan API",
      default_version="v1"
    ),
    public=True,
    permission_classes=(permissions.AllowAny,)
)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("credit/", include("backend.credit.urls")),
    path("auth/", include("backend.authorize.urls")),
    path("swagger.<format>/", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
]

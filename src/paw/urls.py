from __future__ import annotations

from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView

from apps.core.api import public_identity

urlpatterns = [
    path("", include("apps.core.urls")),
    path("admin/", admin.site.urls),
    path("api/v1/", public_identity, name="api-v1-root"),
    path("api/v1/health/", include("apps.health.urls")),
    path("api/v1/openapi.json", SpectacularAPIView.as_view(), name="openapi-schema"),
]

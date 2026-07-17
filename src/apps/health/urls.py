from __future__ import annotations

from django.urls import path

from apps.health.views import live, ready

app_name = "health"

urlpatterns = [
    path("live", live, name="live"),
    path("ready", ready, name="ready"),
]

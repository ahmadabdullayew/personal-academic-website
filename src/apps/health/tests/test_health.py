from __future__ import annotations

from unittest.mock import patch

import pytest
from django.db import OperationalError
from django.test import Client
from django.urls import reverse


def test_liveness_is_public_and_non_cacheable(client: Client) -> None:
    response = client.get(reverse("health:live"))

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    assert "no-cache" in response.headers["Cache-Control"]


@pytest.mark.django_db
def test_readiness_is_public_and_non_cacheable(client: Client) -> None:
    response = client.get(reverse("health:ready"))

    assert response.status_code == 200
    assert response.json() == {"status": "ready"}
    assert "no-cache" in response.headers["Cache-Control"]


def test_readiness_fails_closed_when_the_database_is_unavailable(client: Client) -> None:
    with patch(
        "apps.health.views.connection.ensure_connection",
        side_effect=OperationalError("database unavailable"),
    ):
        response = client.get(reverse("health:ready"))

    assert response.status_code == 503
    assert response.json() == {"status": "unavailable"}
    assert "no-cache" in response.headers["Cache-Control"]

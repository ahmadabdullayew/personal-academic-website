from __future__ import annotations

from django.test import Client
from django.urls import reverse


def test_public_api_root_uses_the_foundation_snapshot(client: Client) -> None:
    response = client.get(reverse("api-v1-root"))

    assert response.status_code == 200
    assert response.json() == {
        "owner": "Ahmad Abdullayev",
        "api_version": "v1",
    }

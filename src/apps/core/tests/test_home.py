from __future__ import annotations

import json
from pathlib import Path

from django.test import Client
from django.test.utils import override_settings
from django.urls import reverse


def test_home_identifies_owner_without_unapproved_academic_claims(client: Client) -> None:
    response = client.get(reverse("core:home"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "Ahmad Abdullayev" in content
    assert '<html lang="en">' in content
    assert "Verified academic details will be published only after approval." in content


def test_home_loads_the_compiled_frontend_entry(client: Client, tmp_path: Path) -> None:
    manifest_path = tmp_path / "src/static_dist/.vite/manifest.json"
    manifest_path.parent.mkdir(parents=True)
    manifest_path.write_text(
        json.dumps(
            {
                "src/static_src/main.ts": {
                    "file": "assets/main.js",
                    "css": ["assets/main.css"],
                }
            }
        ),
        encoding="utf-8",
    )

    with override_settings(BASE_DIR=tmp_path):
        response = client.get(reverse("core:home"))

    assert response.status_code == 200
    content = response.content.decode()
    assert '<link rel="stylesheet" href="/static/assets/main.css" />' in content
    assert '<script type="module" src="/static/assets/main.js"></script>' in content


def test_home_exposes_ranked_primary_audiences(client: Client) -> None:
    response = client.get(reverse("core:home"))

    assert response.status_code == 200
    content = response.content.decode()
    assert "Academic peers and prospective collaborators" in content
    assert "Academic evaluators and decision makers" in content

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from django.template import Context, Template
from django.test import override_settings

from apps.core.templatetags.vite import ViteManifestError

ENTRYPOINT = "src/static_src/main.ts"


def _render_assets() -> str:
    return Template("{% load vite %}{% vite_assets %}").render(Context())


def _write_manifest(base_dir: Path, manifest: object) -> None:
    manifest_path = base_dir / "src/static_dist/.vite/manifest.json"
    manifest_path.parent.mkdir(parents=True)
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")


def test_vite_assets_render_stylesheets_and_module_with_escaped_urls(tmp_path: Path) -> None:
    _write_manifest(
        tmp_path,
        {
            ENTRYPOINT: {
                "file": 'assets/main.js" data-injected="true',
                "css": ['assets/main.css" media="print'],
            }
        },
    )

    with override_settings(BASE_DIR=tmp_path, ENV=SimpleNamespace(app_env="test")):
        markup = _render_assets()

    assert '<link rel="stylesheet"' in markup
    assert '<script type="module"' in markup
    assert ' href="/static/assets/main.css%22%20media%3D%22print"' in markup
    assert ' src="/static/assets/main.js%22%20data-injected%3D%22true"' in markup
    assert ' data-injected="true"' not in markup
    assert ' media="print"' not in markup


def test_vite_assets_tolerate_missing_manifest_outside_production(tmp_path: Path) -> None:
    with override_settings(BASE_DIR=tmp_path, ENV=SimpleNamespace(app_env="development")):
        assert _render_assets() == ""


def test_vite_assets_require_manifest_in_production(tmp_path: Path) -> None:
    with (
        override_settings(BASE_DIR=tmp_path, ENV=SimpleNamespace(app_env="production")),
        pytest.raises(ViteManifestError, match="required in production"),
    ):
        _render_assets()


def test_vite_assets_reject_malformed_manifest(tmp_path: Path) -> None:
    manifest_path = tmp_path / "src/static_dist/.vite/manifest.json"
    manifest_path.parent.mkdir(parents=True)
    manifest_path.write_text("{not-json", encoding="utf-8")

    with (
        override_settings(BASE_DIR=tmp_path, ENV=SimpleNamespace(app_env="production")),
        pytest.raises(ViteManifestError, match="cannot be read"),
    ):
        _render_assets()


@pytest.mark.parametrize(
    "manifest, message",
    [
        ({}, "missing required entry"),
        ({ENTRYPOINT: {"css": []}}, "file must be a non-empty string"),
        ({ENTRYPOINT: {"file": "../main.js"}}, "safe relative asset path"),
        ({ENTRYPOINT: {"file": "assets/main.js", "css": "assets/main.css"}}, "must be an array"),
    ],
)
def test_vite_assets_reject_invalid_entry_contract(
    tmp_path: Path,
    manifest: object,
    message: str,
) -> None:
    _write_manifest(tmp_path, manifest)

    with (
        override_settings(BASE_DIR=tmp_path, ENV=SimpleNamespace(app_env="test")),
        pytest.raises(ViteManifestError, match=message),
    ):
        _render_assets()

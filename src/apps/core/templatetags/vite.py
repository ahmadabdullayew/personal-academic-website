from __future__ import annotations

import json
from pathlib import Path
from typing import NotRequired, Protocol, TypedDict, cast

from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.templatetags.static import static
from django.utils.html import format_html, format_html_join
from django.utils.safestring import SafeString

register = template.Library()

_ENTRYPOINT = "src/static_src/main.ts"
_MANIFEST_RELATIVE_PATH = Path("src/static_dist/.vite/manifest.json")


class ViteManifestError(ImproperlyConfigured):
    """Raised when the compiled frontend asset contract cannot be satisfied."""


class _RuntimeEnvironment(Protocol):
    app_env: str


class _ManifestEntry(TypedDict):
    file: str
    css: NotRequired[list[str]]


def _is_production() -> bool:
    environment = cast(_RuntimeEnvironment | None, getattr(settings, "ENV", None))
    return environment is not None and environment.app_env == "production"


def _asset_path(value: object, field: str) -> str:
    if not isinstance(value, str) or not value:
        raise ViteManifestError(f"Vite manifest {field} must be a non-empty string")

    parts = value.split("/")
    if value.startswith("/") or "\\" in value or any(part in {"", ".", ".."} for part in parts):
        raise ViteManifestError(f"Vite manifest {field} must be a safe relative asset path")
    return value


def _manifest_entry(manifest_path: Path) -> _ManifestEntry | None:
    try:
        with manifest_path.open(encoding="utf-8") as manifest_file:
            raw_manifest: object = json.load(manifest_file)
    except FileNotFoundError as error:
        if _is_production():
            raise ViteManifestError(
                f"Vite manifest is required in production: {manifest_path}"
            ) from error
        return None
    except (OSError, json.JSONDecodeError) as error:
        raise ViteManifestError(f"Vite manifest cannot be read: {manifest_path}") from error

    if not isinstance(raw_manifest, dict):
        raise ViteManifestError("Vite manifest root must be an object")

    raw_entry = raw_manifest.get(_ENTRYPOINT)
    if not isinstance(raw_entry, dict):
        raise ViteManifestError(f"Vite manifest is missing required entry: {_ENTRYPOINT}")

    entry_values = cast(dict[str, object], raw_entry)
    javascript = _asset_path(entry_values.get("file"), f"{_ENTRYPOINT}.file")

    raw_stylesheets = entry_values.get("css", [])
    if not isinstance(raw_stylesheets, list):
        raise ViteManifestError(f"Vite manifest {_ENTRYPOINT}.css must be an array")
    stylesheets = [
        _asset_path(value, f"{_ENTRYPOINT}.css[{index}]")
        for index, value in enumerate(raw_stylesheets)
    ]

    return {"file": javascript, "css": stylesheets}


@register.simple_tag
def vite_assets() -> SafeString:
    """Render the stylesheet and module tags declared by the Vite entry manifest."""
    manifest_path = Path(settings.BASE_DIR) / _MANIFEST_RELATIVE_PATH
    entry = _manifest_entry(manifest_path)
    if entry is None:
        return SafeString("")

    stylesheets = format_html_join(
        "\n",
        '<link rel="stylesheet" href="{}" />',
        ((static(stylesheet),) for stylesheet in entry.get("css", [])),
    )
    javascript = format_html(
        '<script type="module" src="{}"></script>',
        static(entry["file"]),
    )
    if not stylesheets:
        return javascript
    return format_html("{}\n{}", stylesheets, javascript)

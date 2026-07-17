from __future__ import annotations

from typing import Any

from django.http import HttpRequest

from apps.core.product import product_identity


def product_identity_context(_request: HttpRequest) -> dict[str, Any]:
    owner_name, language = product_identity()
    return {
        "site_owner_name": owner_name,
        "site_language": language,
    }

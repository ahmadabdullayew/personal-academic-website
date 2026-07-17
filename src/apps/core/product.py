from __future__ import annotations

import json
from functools import lru_cache
from typing import Any, cast

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


@lru_cache(maxsize=1)
def product_baseline() -> dict[str, Any]:
    """Load the versioned, deployment-immutable foundation public snapshot."""
    try:
        with settings.PRODUCT_BASELINE_PATH.open(encoding="utf-8") as baseline_file:
            baseline = cast(object, json.load(baseline_file))
    except (OSError, json.JSONDecodeError) as error:
        raise ImproperlyConfigured("the product baseline cannot be read") from error
    if not isinstance(baseline, dict):
        raise ImproperlyConfigured("the product baseline root must be an object")
    return cast(dict[str, Any], baseline)


def product_identity() -> tuple[str, str]:
    baseline = product_baseline()
    owner = baseline.get("owner")
    language = baseline.get("default_public_language")
    if not isinstance(owner, dict) or not isinstance(owner.get("full_name"), str):
        raise ImproperlyConfigured("the product baseline owner is invalid")
    if not isinstance(language, str) or not language:
        raise ImproperlyConfigured("the product baseline public language is invalid")
    return owner["full_name"], language

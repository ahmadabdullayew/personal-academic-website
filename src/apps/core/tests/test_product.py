from __future__ import annotations

import json
from collections.abc import Iterator
from pathlib import Path

import pytest
from django.core.exceptions import ImproperlyConfigured
from django.test import override_settings

from apps.core.product import product_baseline, product_identity


@pytest.fixture(autouse=True)
def clear_product_baseline_cache() -> Iterator[None]:
    product_baseline.cache_clear()
    yield
    product_baseline.cache_clear()


def _write_baseline(path: Path, value: object) -> None:
    path.write_text(json.dumps(value), encoding="utf-8")


def test_product_identity_reads_one_versioned_source(tmp_path: Path) -> None:
    baseline_path = tmp_path / "baseline.json"
    _write_baseline(
        baseline_path,
        {
            "owner": {"full_name": "Approved Owner"},
            "default_public_language": "az",
        },
    )

    with override_settings(PRODUCT_BASELINE_PATH=baseline_path):
        assert product_identity() == ("Approved Owner", "az")


@pytest.mark.parametrize(
    ("value", "message"),
    [
        ([], "root must be an object"),
        ({"owner": {}, "default_public_language": "en"}, "owner is invalid"),
        ({"owner": {"full_name": "Owner"}}, "public language is invalid"),
    ],
)
def test_product_identity_rejects_invalid_baselines(
    tmp_path: Path,
    value: object,
    message: str,
) -> None:
    baseline_path = tmp_path / "baseline.json"
    _write_baseline(baseline_path, value)

    with (
        override_settings(PRODUCT_BASELINE_PATH=baseline_path),
        pytest.raises(ImproperlyConfigured, match=message),
    ):
        product_identity()


def test_product_baseline_rejects_unreadable_json(tmp_path: Path) -> None:
    baseline_path = tmp_path / "baseline.json"
    baseline_path.write_text("{invalid", encoding="utf-8")

    with (
        override_settings(PRODUCT_BASELINE_PATH=baseline_path),
        pytest.raises(ImproperlyConfigured, match="cannot be read"),
    ):
        product_baseline()

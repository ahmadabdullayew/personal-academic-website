from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
from scripts.validate_foundation_scope import validate_foundation_scope

ROOT = Path(__file__).resolve().parents[1]


def _read(name: str) -> dict[str, Any]:
    with (ROOT / "config" / name).open(encoding="utf-8") as input_file:
        value: object = json.load(input_file)
    assert isinstance(value, dict)
    return value


@pytest.fixture
def baselines() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    return (
        _read("product-baseline.json"),
        _read("foundation-governance.json"),
        _read("requirements-matrix.json"),
    )


def test_foundation_scope_accepts_the_three_versioned_baselines(
    baselines: tuple[dict[str, Any], dict[str, Any], dict[str, Any]],
) -> None:
    validate_foundation_scope(*baselines)


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("source", "source identity"),
        ("owner", "matrix ownership"),
        ("region", "hosting regions"),
        ("locale", "default-locale"),
        ("feature", "public_search"),
        ("effective", "effective dates"),
        ("consent", "acknowledgement semantics"),
        ("search-retention", "raw search-query retention"),
        ("applicability", "FR-CONTENT-10 applicability"),
        ("approval", "product approval does not cover exactly"),
    ],
)
def test_foundation_scope_rejects_cross_artifact_drift(
    baselines: tuple[dict[str, Any], dict[str, Any], dict[str, Any]],
    mutation: str,
    message: str,
) -> None:
    product, governance, matrix = deepcopy(baselines)
    if mutation == "source":
        governance["source_documents"][0]["sha256"] = "0" * 64
    elif mutation == "owner":
        matrix["requirements"][0]["ownership"]["assigned_person"] = "Unassigned"
    elif mutation == "region":
        governance["jurisdiction"]["selected_hosting"]["region"] = "eu-west-1"
    elif mutation == "locale":
        product["default_public_language"] = "az"
    elif mutation == "feature":
        governance["jurisdiction"]["activated_processing_snapshot"]["public_search"] = "inactive"
    elif mutation == "effective":
        governance["effective_at"] = "2026-07-18T08:33:00Z"
    elif mutation == "consent":
        governance["jurisdiction"]["personal_data_controls"]["consent"][
            "privacy_acknowledgement_is_legal_consent"
        ] = True
    elif mutation == "search-retention":
        governance["jurisdiction"]["personal_data_controls"][
            "data_minimization_and_incidental_data"
        ]["raw_search_query_persistence"] = "allowed"
    elif mutation == "applicability":
        row = next(row for row in matrix["requirements"] if row["id"] == "FR-CONTENT-10")
        row["applicability"]["state"] = "not_applicable"
    elif mutation == "approval":
        governance["approval_records"][0]["scope_items"] = list(range(12, 24))
    else:  # pragma: no cover - the parametrization is closed above
        raise AssertionError(f"unhandled mutation {mutation}")

    with pytest.raises(ValueError, match=message):
        validate_foundation_scope(product, governance, matrix)

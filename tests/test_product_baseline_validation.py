from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
from scripts.validate_product_baseline import validate_baseline

BASELINE_PATH = Path(__file__).resolve().parents[1] / "config/product-baseline.json"


def valid_baseline() -> dict[str, Any]:
    with BASELINE_PATH.open(encoding="utf-8") as baseline_file:
        value: object = json.load(baseline_file)
    assert isinstance(value, dict)
    return deepcopy(value)


def test_product_baseline_accepts_the_versioned_source() -> None:
    validate_baseline(valid_baseline())


@pytest.mark.parametrize(
    ("path", "value", "message"),
    [
        (("owner", "final_decision_authority"), False, "schema error"),
        (("approvers", "security", "role"), "", "schema error"),
        (("approval_policy", "conditional_features_default_enabled"), True, "schema error"),
        (("audiences", "primary", 0, "name"), "", "schema error"),
        (("visitor_goals", 0, "statement"), "", "schema error"),
        (("source_documents", 0, "sha256"), "0" * 64, "SHA-256"),
    ],
)
def test_product_baseline_rejects_invalid_invariants(
    path: tuple[str | int, ...],
    value: object,
    message: str,
) -> None:
    baseline = valid_baseline()
    target: Any = baseline
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = value

    with pytest.raises(ValueError, match=message):
        validate_baseline(baseline)


def test_product_baseline_rejects_globally_duplicated_identifiers() -> None:
    baseline = valid_baseline()
    baseline["owner_goals"][0]["id"] = baseline["visitor_goals"][0]["id"]

    with pytest.raises(ValueError, match="globally unique"):
        validate_baseline(baseline)


def test_product_baseline_rejects_nonconsecutive_ranks() -> None:
    baseline = valid_baseline()
    baseline["visitor_goals"][1]["rank"] = 9

    with pytest.raises(ValueError, match="consecutive and ordered"):
        validate_baseline(baseline)

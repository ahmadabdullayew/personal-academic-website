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
        (("deployment", "primary_origin"), "http://ahmadabdullayev.com", "schema error"),
        (("localization", "language_selector_active"), True, "schema error"),
        (("feature_decisions", "contact", "delivery_provider"), "smtp", "schema error"),
        (("feature_decisions", "search", "query_analytics"), True, "schema error"),
        (
            ("feature_decisions", "contact", "privacy_acknowledgement_semantics"),
            "consent",
            "schema error",
        ),
        (("feature_decisions", "search", "raw_query_persistence"), "allowed", "schema error"),
        (
            ("feature_decisions", "search", "security_logging"),
            "store-the-query",
            "schema error",
        ),
        (("conditional_requirements", 0, "rationale"), "", "schema error"),
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


def test_product_baseline_rejects_an_incomplete_environment_set() -> None:
    baseline = valid_baseline()
    baseline["deployment"]["environments"].pop()

    with pytest.raises(ValueError, match="schema error"):
        validate_baseline(baseline)


def test_product_baseline_rejects_a_nonproduction_public_authority() -> None:
    baseline = valid_baseline()
    baseline["deployment"]["environments"][2]["authoritative_for_public_content"] = True

    with pytest.raises(ValueError, match="sole authority"):
        validate_baseline(baseline)


def test_product_baseline_rejects_locale_default_drift() -> None:
    baseline = valid_baseline()
    baseline["default_public_language"] = "az"

    with pytest.raises(ValueError, match="defaults must match"):
        validate_baseline(baseline)


def test_product_baseline_rejects_an_incorrect_initial_role_count() -> None:
    baseline = valid_baseline()
    baseline["administration"]["roles"][1]["initial_account_count"] = 1

    with pytest.raises(ValueError, match="exactly one owner"):
        validate_baseline(baseline)


def test_product_baseline_rejects_missing_conditional_requirement() -> None:
    baseline = valid_baseline()
    baseline["conditional_requirements"].pop()

    with pytest.raises(ValueError, match="schema error"):
        validate_baseline(baseline)


def test_product_baseline_rejects_duplicate_conditional_requirement() -> None:
    baseline = valid_baseline()
    baseline["conditional_requirements"][1] = deepcopy(baseline["conditional_requirements"][0])

    with pytest.raises(ValueError, match="all 54 P2 requirement decisions"):
        validate_baseline(baseline)


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("title", "Changed title", "metadata does not match"),
        ("priority", "P2-CONDITIONAL", "metadata does not match"),
        ("source_ref", "website-srs:FR-ABOUT-07:p49", "metadata does not match"),
        ("decision_owner", "product", "wrong accountable decision owner"),
        ("state", "active", "activation set"),
    ],
)
def test_product_baseline_rejects_conditional_requirement_drift(
    field: str,
    value: str,
    message: str,
) -> None:
    baseline = valid_baseline()
    baseline["conditional_requirements"][0][field] = value

    with pytest.raises(ValueError, match=message):
        validate_baseline(baseline)


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("deployment", "www_behavior"), "serve duplicate public content"),
        (("administration", "roles", 0, "permissions"), ["invented-permission"]),
        (
            ("feature_decisions", "search", "indexed_content_types"),
            ["drafts", "private", "secrets", "sessions", "inquiries", "audit"],
        ),
        (
            ("feature_decisions", "contact", "acceptance_point"),
            "Claim delivery before durable persistence.",
        ),
    ],
)
def test_product_baseline_rejects_unapproved_semantic_drift(
    path: tuple[str | int, ...], value: object
) -> None:
    baseline = valid_baseline()
    target: Any = baseline
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = value

    with pytest.raises(ValueError, match="approved product decision digest"):
        validate_baseline(baseline)

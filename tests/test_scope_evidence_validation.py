from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
from scripts.validate_scope_evidence import validate_scope_evidence

LEDGER_PATH = Path(__file__).resolve().parents[1] / "config" / "scope-evidence-ledger.json"


def valid_ledger() -> dict[str, Any]:
    with LEDGER_PATH.open(encoding="utf-8") as ledger_file:
        value: object = json.load(ledger_file)
    assert isinstance(value, dict)
    return deepcopy(value)


def source(ledger: dict[str, Any], source_id: str) -> dict[str, Any]:
    return next(record for record in ledger["sources"] if record["id"] == source_id)


def test_scope_evidence_accepts_the_versioned_ledger() -> None:
    validate_scope_evidence(valid_ledger())


def test_scope_evidence_rejects_an_unresolved_item_citation() -> None:
    ledger = valid_ledger()
    ledger["review_questions"][0]["citations"].append("UNKNOWN-SOURCE")

    with pytest.raises(ValueError, match="citation does not resolve"):
        validate_scope_evidence(ledger)


def test_scope_evidence_rejects_a_citation_outside_its_item_mapping() -> None:
    ledger = valid_ledger()
    source(ledger, "RFC-5646")["foundation_items"] = [13]

    with pytest.raises(ValueError, match="outside cited source"):
        validate_scope_evidence(ledger)


def test_scope_evidence_rejects_a_supplied_pdf_digest_change() -> None:
    ledger = valid_ledger()
    source(ledger, "website-srs")["identity_control"]["value"] = "0" * 64

    with pytest.raises(ValueError, match="SHA-256 drifted"):
        validate_scope_evidence(ledger)


def test_scope_evidence_rejects_changed_candidate_counts() -> None:
    ledger = valid_ledger()
    ledger["retrieval_events"][2]["candidate_count"] = 19

    with pytest.raises(ValueError, match="retrieval counts drifted"):
        validate_scope_evidence(ledger)


def test_scope_evidence_rejects_unclosed_exclusion_reasons() -> None:
    ledger = valid_ledger()
    ledger["retrieval_events"][2]["excluded_reasons"][0]["count"] = 9

    with pytest.raises(ValueError, match="exclusion-reason accounting"):
        validate_scope_evidence(ledger)


def test_scope_evidence_rejects_a_non_review_date_retrieval() -> None:
    ledger = valid_ledger()
    ledger["retrieval_events"][2]["executed_at"] = "2026-07-18T09:10:00Z"

    with pytest.raises(ValueError, match="not recorded as executed on 2026-07-17"):
        validate_scope_evidence(ledger)


def test_scope_evidence_rejects_a_false_source_retrieval_time() -> None:
    ledger = valid_ledger()
    source(ledger, "RFC-5646")["retrieved_at"] = "2026-07-17T09:11:00Z"

    with pytest.raises(ValueError, match="retrieved_at must equal"):
        validate_scope_evidence(ledger)


def test_scope_evidence_rejects_an_unknown_retrieval_event() -> None:
    ledger = valid_ledger()
    source(ledger, "RFC-5646")["retrieval_event_ids"] = ["EV-999"]

    with pytest.raises(ValueError, match="unknown retrieval event"):
        validate_scope_evidence(ledger)


def test_scope_evidence_rejects_a_false_freshness_date() -> None:
    ledger = valid_ledger()
    source(ledger, "RFC-5646")["freshness"]["next_review_on"] = "2027-07-18"

    with pytest.raises(ValueError, match="freshness date"):
        validate_scope_evidence(ledger)


def test_scope_evidence_rejects_legal_url_drift() -> None:
    ledger = valid_ledger()
    source(ledger, "LAW-AZ-PERSONAL-DATA-998-IIIQ")["locator"] = "https://example.com/replacement"

    with pytest.raises(ValueError, match="legal source drift"):
        validate_scope_evidence(ledger)


def test_scope_evidence_rejects_legal_proposition_drift() -> None:
    ledger = valid_ledger()
    source(ledger, "LAW-AZ-CABINET-237")["proposition"] = "Changed proposition."

    with pytest.raises(ValueError, match="legal source drift"):
        validate_scope_evidence(ledger)


def test_scope_evidence_rejects_a_missing_artifact_reference() -> None:
    ledger = valid_ledger()
    ledger["review_questions"][0]["artifact_refs"][0] = "docs/missing.md"

    with pytest.raises(ValueError, match="artifact reference does not exist"):
        validate_scope_evidence(ledger)


def test_scope_evidence_rejects_a_changed_source_limitation() -> None:
    ledger = valid_ledger()
    source(ledger, "POSTGRESQL-FTS")["limitation"] = "Changed without a new review."

    with pytest.raises(ValueError, match="sources drifted from the reviewed register"):
        validate_scope_evidence(ledger)


def test_scope_evidence_rejects_an_item_question_mismatch() -> None:
    ledger = valid_ledger()
    ledger["review_questions"][0]["item"] = 12

    with pytest.raises(ValueError, match="cover each item 11 through 23"):
        validate_scope_evidence(ledger)

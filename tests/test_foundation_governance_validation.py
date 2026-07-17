from __future__ import annotations

import json
from copy import deepcopy
from datetime import date
from pathlib import Path
from typing import Any

import pytest
from scripts.validate_foundation_governance import (
    _validate_approvals,
    _validate_inventory,
    _validate_jurisdiction,
    _validate_legal_sources,
    _validate_revisions,
    validate_foundation_governance,
)

BASELINE_PATH = Path(__file__).resolve().parents[1] / "config" / "foundation-governance.json"


def valid_baseline() -> dict[str, Any]:
    with BASELINE_PATH.open(encoding="utf-8") as baseline_file:
        value: object = json.load(baseline_file)
    assert isinstance(value, dict)
    return deepcopy(value)


def test_foundation_governance_accepts_the_versioned_baseline() -> None:
    validate_foundation_governance(valid_baseline())


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (("scope_items",), [19, 20, 21]),
        (
            (
                "jurisdiction",
                "selected_project_governance_baseline",
                "country_code",
            ),
            "DE",
        ),
        (("jurisdiction", "selected_hosting", "region"), "us-east-1"),
        (
            (
                "jurisdiction",
                "selected_hosting",
                "application_managed_cross_region_replication",
            ),
            "enabled",
        ),
        (("jurisdiction", "activated_processing_snapshot", "analytics"), "active"),
        (
            (
                "jurisdiction",
                "personal_data_controls",
                "purpose_and_field_inventory_before_collection",
            ),
            False,
        ),
        (("migration_plan", "dry_run_required"), False),
        (("approval_records", 0, "result"), "approved"),
    ],
)
def test_foundation_governance_rejects_schema_level_contract_changes(
    path: tuple[str | int, ...], value: object
) -> None:
    baseline = valid_baseline()
    target: Any = baseline
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = value

    with pytest.raises(ValueError, match="schema error"):
        validate_foundation_governance(baseline)


def test_foundation_governance_rejects_wrong_source_digest() -> None:
    baseline = valid_baseline()
    baseline["source_documents"][0]["sha256"] = "0" * 64

    with pytest.raises(ValueError, match="SHA-256"):
        validate_foundation_governance(baseline)


def test_foundation_governance_rejects_an_invented_stakeholder() -> None:
    baseline = valid_baseline()
    baseline["stakeholders"][0]["name"] = "Invented Maintainer"

    with pytest.raises(ValueError, match="named website owner"):
        validate_foundation_governance(baseline)


def test_foundation_governance_rejects_missing_stakeholder_role() -> None:
    baseline = valid_baseline()
    baseline["stakeholders"][0]["roles"].remove("Security Approver")

    with pytest.raises(ValueError, match="every approval role"):
        validate_foundation_governance(baseline)


def test_foundation_governance_rejects_unofficial_azerbaijan_legal_source() -> None:
    baseline = valid_baseline()
    baseline["legal_sources"][0]["url"] = "https://example.com/constitution"

    with pytest.raises(ValueError, match="official Azerbaijan host"):
        validate_foundation_governance(baseline)


def test_legal_source_validator_requires_all_material_authorities() -> None:
    baseline = valid_baseline()
    baseline["legal_sources"] = [
        source for source in baseline["legal_sources"] if source["id"] != "LAW-AZ-CABINET-161"
    ]

    with pytest.raises(ValueError, match="missing required coverage.*CABINET-161"):
        _validate_legal_sources(baseline)


def test_legal_source_validator_allows_additional_official_sources() -> None:
    baseline = valid_baseline()
    extra_source = deepcopy(baseline["legal_sources"][-1])
    extra_source["id"] = "PROVIDER-AWS-SES-ENDPOINTS"
    extra_source["url"] = "https://docs.aws.amazon.com/general/latest/gr/ses.html"
    baseline["legal_sources"].append(extra_source)

    _validate_legal_sources(baseline)


def test_legal_source_validator_pins_current_consolidated_decision_237() -> None:
    baseline = valid_baseline()
    decision_237 = next(
        source for source in baseline["legal_sources"] if source["id"] == "LAW-AZ-CABINET-237"
    )
    decision_237["url"] = (
        "https://mincom.gov.az/storage/pages/644/71b05c33324332d016b9e2347ec2ecfa.pdf"
    )

    with pytest.raises(ValueError, match="reviewed official URL"):
        _validate_legal_sources(baseline)


def test_legal_source_validator_requires_article_8_6_coverage() -> None:
    baseline = valid_baseline()
    personal_data_law = next(
        source
        for source in baseline["legal_sources"]
        if source["id"] == "LAW-AZ-PERSONAL-DATA-998-IIIQ"
    )
    personal_data_law["provisions"].remove("Article 8.6")

    with pytest.raises(ValueError, match="Article 8.6"):
        _validate_legal_sources(baseline)


def test_jurisdiction_validator_keeps_gdpr_applicability_contingent() -> None:
    baseline = valid_baseline()
    baseline["jurisdiction"]["applicability_determination"][
        "germany_hosting_alone_triggers_gdpr"
    ] = True

    with pytest.raises(ValueError, match="pending factual nexus analysis"):
        _validate_jurisdiction(baseline)


def test_jurisdiction_validator_rejects_an_asserted_court_forum() -> None:
    baseline = valid_baseline()
    baseline["jurisdiction"]["selected_project_governance_baseline"]["court_forum_established"] = (
        True
    )

    with pytest.raises(ValueError, match="court forum"):
        _validate_jurisdiction(baseline)


def test_jurisdiction_validator_requires_source_archive_gate() -> None:
    baseline = valid_baseline()
    baseline["jurisdiction"]["legal_source_provenance"]["immutable_source_verification_claimed"] = (
        True
    )

    with pytest.raises(ValueError, match="unarchived-content gate"):
        _validate_jurisdiction(baseline)


def test_jurisdiction_validator_pins_statutory_rights_deadlines() -> None:
    baseline = valid_baseline()
    rights = baseline["jurisdiction"]["personal_data_controls"]["data_subject_rights"]
    rights["reasoned_refusal_deadline_working_days"] = 7

    with pytest.raises(ValueError, match="7, 7, 5 and 3"):
        _validate_jurisdiction(baseline)


def test_jurisdiction_validator_requires_complete_collection_notice() -> None:
    baseline = valid_baseline()
    notice = baseline["jurisdiction"]["personal_data_controls"]["collection_notice"]
    notice["required_fields"].remove("conformity-certificate-and-state-expertise-status")

    with pytest.raises(ValueError, match="Article 11.2"):
        _validate_jurisdiction(baseline)


def test_jurisdiction_validator_keeps_cross_border_processing_blocked() -> None:
    baseline = valid_baseline()
    transfer = baseline["jurisdiction"]["personal_data_controls"]["cross_border_transfer"]
    transfer["status"] = "approved"

    with pytest.raises(ValueError, match="blocked pending Article 14"):
        _validate_jurisdiction(baseline)


def test_jurisdiction_validator_rejects_ses_tracking() -> None:
    baseline = valid_baseline()
    baseline["jurisdiction"]["selected_hosting"]["ses_controls"]["engagement_tracking"] = "enabled"

    with pytest.raises(ValueError, match="engagement tracking"):
        _validate_jurisdiction(baseline)


def test_jurisdiction_validator_rejects_raw_search_query_storage() -> None:
    baseline = valid_baseline()
    minimization = baseline["jurisdiction"]["personal_data_controls"][
        "data_minimization_and_incidental_data"
    ]
    minimization["raw_search_query_persistence"] = "enabled"

    with pytest.raises(ValueError, match="logging, search-query"):
        _validate_jurisdiction(baseline)


def test_foundation_governance_rejects_a_weakened_review_schedule() -> None:
    baseline = valid_baseline()
    baseline["content_governance"]["review_schedules"][0]["maximum_interval_days"] = 90

    with pytest.raises(ValueError, match="maximum intervals"):
        validate_foundation_governance(baseline)


def test_foundation_governance_rejects_unordered_event_triggers() -> None:
    baseline = valid_baseline()
    triggers = baseline["content_governance"]["event_review_triggers"]
    triggers[0], triggers[1] = triggers[1], triggers[0]

    with pytest.raises(ValueError, match="complete, consecutive and ordered"):
        validate_foundation_governance(baseline)


def test_foundation_governance_rejects_a_missing_inventory_identifier() -> None:
    baseline = valid_baseline()
    baseline["content_inventory"][9]["id"] = "CI-099"

    with pytest.raises(ValueError, match="inventory IDs"):
        validate_foundation_governance(baseline)


def test_foundation_governance_rejects_duplicate_canonical_content() -> None:
    baseline = valid_baseline()
    baseline["content_inventory"][1]["canonical_key"] = baseline["content_inventory"][0][
        "canonical_key"
    ]

    with pytest.raises(ValueError, match="canonical content keys must be unique"):
        validate_foundation_governance(baseline)


def test_foundation_governance_rejects_public_rights_unknown_content() -> None:
    baseline = valid_baseline()
    baseline["content_inventory"][0]["rights_status"] = "undetermined"

    with pytest.raises(ValueError, match="cannot publish"):
        validate_foundation_governance(baseline)


def test_foundation_governance_rejects_a_false_review_due_date() -> None:
    baseline = valid_baseline()
    baseline["content_inventory"][0]["review_due_on"] = "2026-10-16"

    with pytest.raises(ValueError, match="review due date"):
        validate_foundation_governance(baseline)


@pytest.mark.parametrize("value", [None, "2026-10-16"])
def test_foundation_governance_validates_approved_internal_review_dates(
    value: str | None,
) -> None:
    baseline = valid_baseline()
    baseline["content_inventory"][31]["review_due_on"] = value

    with pytest.raises(ValueError, match="approved content requires|review due date"):
        validate_foundation_governance(baseline)


def test_foundation_governance_rejects_a_fabricated_missing_content_source() -> None:
    baseline = valid_baseline()
    baseline["content_inventory"][5]["source_status"] = "verified"

    with pytest.raises(ValueError, match="evidence-held gap"):
        validate_foundation_governance(baseline)


def test_foundation_governance_rejects_personal_data_without_privacy_approval() -> None:
    baseline = valid_baseline()
    baseline["content_inventory"][24]["approval_domains"].remove("privacy")

    with pytest.raises(ValueError, match="requires privacy approval"):
        validate_foundation_governance(baseline)


@pytest.mark.parametrize(
    "reference",
    [
        "feature-baseline:nonexistent",
        "product-baseline:feature_decisions.missing",
        "repository:docs/does-not-exist.md",
        "repository:../outside-project.txt",
        "website-srs:page300",
        "website-srs:p317",
        "website-srs:p301-p300",
        "backend-specification:p64",
        "owner-directive:invented-directive",
        "source-gap:invented-gap",
    ],
)
def test_foundation_governance_rejects_unresolvable_inventory_sources(
    reference: str,
) -> None:
    baseline = valid_baseline()
    baseline["content_inventory"][24]["source_refs"][0] = reference

    with pytest.raises(
        ValueError,
        match=(
            "unknown prefix|does not resolve|does not exist|escapes|invalid printed-page|"
            "outside reviewed page bounds|not registered"
        ),
    ):
        validate_foundation_governance(baseline)


def test_inventory_review_is_valid_through_its_due_date() -> None:
    _validate_inventory(valid_baseline(), as_of=date(2026, 8, 16))


def test_inventory_review_is_blocked_after_its_due_date() -> None:
    with pytest.raises(ValueError, match="review is overdue"):
        _validate_inventory(valid_baseline(), as_of=date(2026, 8, 17))


def test_jurisdiction_review_is_valid_through_its_due_date() -> None:
    _validate_jurisdiction(valid_baseline(), as_of=date(2026, 10, 15))


def test_jurisdiction_review_is_blocked_after_its_due_date() -> None:
    with pytest.raises(ValueError, match="jurisdiction review is overdue"):
        _validate_jurisdiction(valid_baseline(), as_of=date(2026, 10, 16))


def test_foundation_governance_rejects_unordered_migration() -> None:
    baseline = valid_baseline()
    baseline["migration_plan"]["steps"][1]["order"] = 12

    with pytest.raises(ValueError, match="migration step order"):
        validate_foundation_governance(baseline)


def test_foundation_governance_rejects_a_false_foundation_commit() -> None:
    baseline = valid_baseline()
    baseline["revision_history"][0]["restoration_locator"] = "git commit deadbeef"

    with pytest.raises(ValueError, match="existing foundation commit"):
        validate_foundation_governance(baseline)


def test_foundation_governance_rejects_a_broken_revision_chain() -> None:
    baseline = valid_baseline()
    baseline["revision_history"][1]["previous_version"] = "invented-future-commit"

    with pytest.raises(ValueError, match="immediately preceding revision"):
        validate_foundation_governance(baseline)


def append_version_1_0_1(baseline: dict[str, Any]) -> None:
    revision = deepcopy(baseline["revision_history"][-1])
    revision.update(
        {
            "id": "REV-003",
            "logical_artifact_id": "foundation-items-11-23@1.0.1",
            "version": "1.0.1",
            "previous_version": "1.0.0",
            "recorded_at": "2026-07-17T09:00:00Z",
            "summary": "Appendability verification fixture.",
        }
    )
    baseline["revision_history"].append(revision)
    for domain in (
        "product",
        "content",
        "accessibility",
        "security",
        "privacy",
        "operations",
    ):
        previous = next(
            approval
            for approval in baseline["approval_records"]
            if approval["domain"] == domain
        )
        approval = deepcopy(previous)
        approval.update(
            {
                "id": f"APR-{domain.upper()}-002",
                "logical_artifact_id": "foundation-items-11-23@1.0.1",
                "artifact_version": "1.0.1",
                "decided_at": "2026-07-17T09:00:00Z",
                "supersedes": previous["id"],
            }
        )
        baseline["approval_records"].append(approval)
    baseline["baseline_version"] = "1.0.1"
    baseline["effective_at"] = "2026-07-17T09:00:00Z"


def test_revision_and_approval_validators_accept_append_only_successors() -> None:
    baseline = valid_baseline()
    append_version_1_0_1(baseline)

    _validate_revisions(baseline)
    _validate_approvals(baseline)


def test_approval_validator_rejects_a_broken_supersession_link() -> None:
    baseline = valid_baseline()
    append_version_1_0_1(baseline)
    baseline["approval_records"][6]["supersedes"] = "APR-PRODUCT-999"

    with pytest.raises(ValueError, match="must supersede"):
        _validate_approvals(baseline)


def test_approval_validator_rejects_a_decision_before_its_revision() -> None:
    baseline = valid_baseline()
    append_version_1_0_1(baseline)
    baseline["approval_records"][6]["decided_at"] = "2026-07-17T08:59:59Z"

    with pytest.raises(ValueError, match="predates its referenced revision"):
        _validate_approvals(baseline)


def test_foundation_governance_rejects_duplicate_approval_domains() -> None:
    baseline = valid_baseline()
    baseline["approval_records"][1]["domain"] = "product"

    with pytest.raises(ValueError, match="all six foundation approval domains"):
        validate_foundation_governance(baseline)


def test_foundation_governance_rejects_approval_without_owner_direction() -> None:
    baseline = valid_baseline()
    baseline["approval_records"][0]["evidence_refs"].remove(
        "owner-directive:2026-07-17-items-11-23"
    )

    with pytest.raises(ValueError, match="explicit owner direction"):
        validate_foundation_governance(baseline)


def test_foundation_governance_rejects_future_revision_time() -> None:
    baseline = valid_baseline()
    baseline["revision_history"][1]["recorded_at"] = "2999-01-01T00:00:00Z"

    with pytest.raises(ValueError, match="future"):
        validate_foundation_governance(baseline)


@pytest.mark.parametrize(
    ("path", "value"),
    [
        (
            ("jurisdiction", "review", "event_triggers", 0),
            "A materially substituted publication rule.",
        ),
        (
            ("content_governance", "rules", 0),
            "A materially substituted governance rule.",
        ),
        (("content_inventory", 0, "label"), "Substituted inventory label"),
        (("migration_plan", "steps", 0, "name"), "Substituted migration step"),
        (("revision_history", 1, "summary"), "Substituted revision meaning"),
        (("approval_records", 0, "decision"), "Substituted approval meaning"),
    ],
)
def test_foundation_governance_rejects_unapproved_semantic_substitution(
    path: tuple[str | int, ...], value: str
) -> None:
    baseline = valid_baseline()
    target: Any = baseline
    for part in path[:-1]:
        target = target[part]
    target[path[-1]] = value

    with pytest.raises(ValueError, match="approved governance digest"):
        validate_foundation_governance(baseline)

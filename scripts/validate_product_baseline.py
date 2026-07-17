from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = ROOT / "config" / "product-baseline.json"
SCHEMA_PATH = ROOT / "config" / "product-baseline.schema.json"
APPROVAL_DOMAINS = {
    "accessibility",
    "content",
    "operations",
    "privacy",
    "product",
    "security",
}
SOURCE_HASHES = {
    "website-srs": "976ba51a785d27d37117655a4a508eb5133edb36e988966ce31e8878a78eb9e7",
    "backend-specification": "1eca221859e9379cadd3d3e192bd35b68a7e0010ae15f8de53e539e1782c31b5",
}
UNSUPPORTED_ATTRIBUTES = {
    "academic_title",
    "biography",
    "degree",
    "discipline",
    "institutional_affiliation",
}


def _read_object(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as input_file:
        value: object = json.load(input_file)
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def _validate_schema(baseline: dict[str, Any]) -> None:
    schema = _read_object(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(baseline), key=lambda error: list(error.absolute_path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        raise ValueError(f"product baseline schema error at {location}: {error.message}")


def _assert_ranked(items: list[dict[str, Any]], label: str) -> None:
    ranks = [item["rank"] for item in items]
    expected = list(range(1, len(items) + 1))
    if ranks != expected:
        raise ValueError(f"{label} ranks must be consecutive and ordered")
    identifiers = [item["id"] for item in items]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError(f"{label} identifiers must be unique")


def validate_baseline(baseline: dict[str, Any]) -> None:
    _validate_schema(baseline)

    if date.fromisoformat(baseline["effective_date"]) > date.today():
        raise ValueError("effective_date cannot be in the future")

    owner = baseline["owner"]
    if owner["full_name"] != "Ahmad Abdullayev":
        raise ValueError("the named website owner must be Ahmad Abdullayev")
    if owner["represented_person"] != owner["full_name"]:
        raise ValueError("the owner and represented person must match")
    if not owner["final_decision_authority"]:
        raise ValueError("the named owner must retain final decision authority")
    if set(owner["unsupported_attributes_must_not_be_inferred"]) != UNSUPPORTED_ATTRIBUTES:
        raise ValueError("the unsupported academic-attribute safeguards must remain complete")

    source_documents = {document["id"]: document for document in baseline["source_documents"]}
    if set(source_documents) != set(SOURCE_HASHES):
        raise ValueError("both supplied source documents must be identified")
    for source_id, expected_hash in SOURCE_HASHES.items():
        if source_documents[source_id]["sha256"] != expected_hash:
            raise ValueError(f"{source_id} SHA-256 does not match the reviewed document")

    approvers = baseline["approvers"]
    if set(approvers) != APPROVAL_DOMAINS:
        raise ValueError("all six approval domains must be assigned")
    if any(record["name"] != owner["full_name"] for record in approvers.values()):
        raise ValueError("an approver was invented outside the available evidence")
    if len({record["role"] for record in approvers.values()}) != len(APPROVAL_DOMAINS):
        raise ValueError("each approval domain must retain a distinct role record")

    policy = baseline["approval_policy"]
    if set(policy["required_domains"]) != APPROVAL_DOMAINS:
        raise ValueError("release policy must require every approval domain")
    if policy["approval_by_silence"]:
        raise ValueError("approval by silence is prohibited")
    if policy["applicable_p0_waiver_allowed"]:
        raise ValueError("applicable P0 requirements cannot be waived")
    if policy["conditional_features_default_enabled"]:
        raise ValueError("conditional features must default to disabled")
    if not policy["separate_role_records_required"]:
        raise ValueError("separate approval role records are required")

    _assert_ranked(baseline["audiences"]["primary"], "primary audiences")
    _assert_ranked(baseline["audiences"]["secondary"], "secondary audiences")
    _assert_ranked(baseline["visitor_goals"], "visitor goals")
    _assert_ranked(baseline["owner_goals"], "owner goals")

    if len(baseline["audiences"]["primary"]) != 3:
        raise ValueError("exactly three primary audience groups are required")
    if len(baseline["audiences"]["secondary"]) != 4:
        raise ValueError("exactly four secondary audience groups are required")
    if len(baseline["visitor_goals"]) != 10 or len(baseline["owner_goals"]) != 10:
        raise ValueError("both ranked goal lists must contain ten goals")

    ranked_collections = [
        baseline["audiences"]["primary"],
        baseline["audiences"]["secondary"],
        baseline["visitor_goals"],
        baseline["owner_goals"],
    ]
    all_identifiers = [item["id"] for items in ranked_collections for item in items]
    if len(all_identifiers) != len(set(all_identifiers)):
        raise ValueError("audience and goal identifiers must be globally unique")

    valid_evidence_prefixes = {f"{source_id}:" for source_id in SOURCE_HASHES}
    evidence_records = [
        *(record["evidence_refs"] for record in approvers.values()),
        *(item["evidence_refs"] for items in ranked_collections for item in items),
    ]
    for references in evidence_records:
        if any(
            not any(reference.startswith(prefix) for prefix in valid_evidence_prefixes)
            for reference in references
        ):
            raise ValueError("an evidence reference does not identify a reviewed source document")


def main() -> None:
    baseline = _read_object(BASELINE_PATH)
    validate_baseline(baseline)
    print(
        "product baseline valid: schema, sources, owner, approvers, audiences and goals "
        "are complete"
    )


if __name__ == "__main__":
    main()

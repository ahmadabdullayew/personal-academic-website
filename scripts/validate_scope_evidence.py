from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
LEDGER_PATH = ROOT / "config" / "scope-evidence-ledger.json"
SCHEMA_PATH = ROOT / "config" / "scope-evidence-ledger.schema.json"
PRODUCT_PATH = ROOT / "config" / "product-baseline.json"
GOVERNANCE_PATH = ROOT / "config" / "foundation-governance.json"
MATRIX_PATH = ROOT / "config" / "requirements-matrix.json"

EXPECTED_SCOPE = list(range(11, 24))
EXPECTED_SOURCE_IDS = [
    "website-srs",
    "backend-specification",
    "REGISTRY-VERISIGN-RDAP-PRIMARY",
    "REGISTRY-VERISIGN-RDAP-HYPHENATED",
    "RFC-5646",
    "W3C-HTML-LANGUAGE",
    "NIST-RBAC",
    "POSTGRESQL-FTS",
    "ORCID-API-READ",
    "CROSSREF-REST-API",
    "RFC-4287",
    "OPEN-GRAPH-PROTOCOL",
    "ISO-15489-1-2016",
    "W3C-ACCESSIBILITY-STATEMENT",
    "NIST-SP-800-218",
    "LAW-AZ-CONSTITUTION-30-32",
    "LAW-AZ-PERSONAL-DATA-998-IIIQ",
    "LAW-AZ-CABINET-237",
    "LAW-AZ-CABINET-149",
    "LAW-AZ-CABINET-149-161-2022-AMENDMENT",
    "LAW-AZ-CABINET-161",
    "LAW-AZ-EHIS-DIGITAL-CONSENT",
    "AUTHORITY-AZ-PERSONAL-DATA-LICENSING",
    "AUTHORITY-AZ-PERSONAL-DATA-REGISTRY",
    "LAW-AZ-PRIVATE-INTERNATIONAL-LAW",
    "LAW-AZ-COPYRIGHT-115-IQ",
    "LAW-EU-GDPR-2016-679",
    "GUIDANCE-EU-EDPB-ARTICLE-3",
    "PROVIDER-AWS-REGIONS",
    "PROVIDER-AWS-DATA-PRIVACY",
    "PROVIDER-AWS-SES-REGIONS",
    "PROVIDER-AWS-SES-DATA-PROTECTION",
]
EXPECTED_SPEC_IDENTITIES = {
    "website-srs": (
        "personal_academic_professional_website_srs.pdf",
        "976ba51a785d27d37117655a4a508eb5133edb36e988966ce31e8878a78eb9e7",
    ),
    "backend-specification": (
        "personal_academic_website_backend_specification.pdf",
        "1eca221859e9379cadd3d3e192bd35b68a7e0010ae15f8de53e539e1782c31b5",
    ),
}
EXPECTED_EVENT_COUNTS = {
    "EV-001": (2, 2, 0),
    "EV-002": (2, 2, 0),
    "EV-003": (18, 4, 14),
    "EV-004": (18, 3, 15),
    "EV-005": (14, 3, 11),
    "EV-006": (16, 3, 13),
    "EV-007": (17, 17, 0),
}
EXPECTED_DIGESTS = {
    "review_protocol": "e170fb0e872e92e87e88ef444fa601317b866d51704939d9be936fe0a2eb7c90",
    "freshness_triggers": "d72181c7ca1b1e9184fa5b3c63164eddad40dde0b63ea0a52260f22ab991ca79",
    "retrieval_events": "0da83453c9355be8f9c37c2fbe6fbe68a7e1bd1d7df06b8d54a893e1c7dd9a56",
    "sources": "c09aa12e567bc8bcda43b6f7a7022bafb910f3f01a6e2fadf82398f994e0976c",
    "review_questions": "bee94cce6ba4c224cd595074177b539995a61563225db6da9f779e95a09e0c60",
}


def _read_object(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as input_file:
        value: object = json.load(input_file)
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def _validate_schema(ledger: dict[str, Any]) -> None:
    schema = _read_object(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(ledger), key=lambda error: list(error.absolute_path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        raise ValueError(f"scope evidence schema error at {location}: {error.message}")


def _parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("scope evidence timestamps must include a UTC offset")
    return parsed.astimezone(UTC)


def _stable_digest(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def _require_unique(values: list[str], label: str) -> None:
    if len(values) != len(set(values)):
        raise ValueError(f"{label} must be unique")


def _validate_scope_and_ids(ledger: dict[str, Any]) -> None:
    if ledger["scope_items"] != EXPECTED_SCOPE:
        raise ValueError("scope evidence must cover every ordered foundation item 11 through 23")
    if _parse_utc(ledger["effective_at"]).date() != date(2026, 7, 17):
        raise ValueError("scope evidence effective date must remain 2026-07-17")

    trigger_ids = [trigger["id"] for trigger in ledger["freshness_triggers"]]
    event_ids = [event["id"] for event in ledger["retrieval_events"]]
    source_ids = [source["id"] for source in ledger["sources"]]
    question_ids = [question["id"] for question in ledger["review_questions"]]
    question_items = [question["item"] for question in ledger["review_questions"]]

    if trigger_ids != [f"FT-{number:02d}" for number in range(1, 8)]:
        raise ValueError("freshness trigger IDs must be complete, consecutive and ordered")
    if event_ids != [f"EV-{number:03d}" for number in range(1, 8)]:
        raise ValueError("retrieval event IDs must be complete, consecutive and ordered")
    if source_ids != EXPECTED_SOURCE_IDS:
        raise ValueError("the exact 32-source identity register must remain complete and ordered")
    if question_ids != [f"RQ-{item:03d}" for item in EXPECTED_SCOPE]:
        raise ValueError("review-question IDs must map consecutively to items 11 through 23")
    if question_items != EXPECTED_SCOPE:
        raise ValueError("review questions must cover each item 11 through 23 exactly once")
    for values, label in (
        (trigger_ids, "freshness trigger IDs"),
        (event_ids, "retrieval event IDs"),
        (source_ids, "source IDs"),
        (question_ids, "review-question IDs"),
    ):
        _require_unique(values, label)


def _validate_retrieval_events(ledger: dict[str, Any]) -> None:
    sources = {source["id"]: source for source in ledger["sources"]}
    events = {event["id"]: event for event in ledger["retrieval_events"]}
    totals = Counter[str]()

    for event_id, event in events.items():
        observed = (
            event["candidate_count"],
            event["included_count"],
            event["excluded_count"],
        )
        if observed != EXPECTED_EVENT_COUNTS[event_id]:
            raise ValueError(f"{event_id} retrieval counts drifted from the executed review")
        if event["candidate_count"] != event["included_count"] + event["excluded_count"]:
            raise ValueError(f"{event_id} candidate accounting does not close")
        if event["included_count"] != len(event["included_source_ids"]):
            raise ValueError(f"{event_id} included count does not match included source IDs")
        if sum(reason["count"] for reason in event["excluded_reasons"]) != event["excluded_count"]:
            raise ValueError(f"{event_id} exclusion-reason accounting does not close")
        if _parse_utc(event["executed_at"]).date() != date(2026, 7, 17):
            raise ValueError(f"{event_id} was not recorded as executed on 2026-07-17")
        if any(source_id not in sources for source_id in event["included_source_ids"]):
            raise ValueError(f"{event_id} includes an unresolved source ID")
        for key in ("candidate_count", "included_count", "excluded_count"):
            totals[key] += event[key]

    expected_totals = Counter(candidate_count=87, included_count=34, excluded_count=53)
    if totals != expected_totals:
        raise ValueError(
            "aggregate retrieval accounting must remain 87 candidates, "
            "34 inclusions and 53 exclusions"
        )

    for source in sources.values():
        linked_times: list[datetime] = []
        for event_id in source["retrieval_event_ids"]:
            if event_id not in events:
                raise ValueError(f"{source['id']} references an unknown retrieval event")
            event = events[event_id]
            if source["id"] not in event["included_source_ids"]:
                raise ValueError(
                    f"{source['id']} is not included by its retrieval event {event_id}"
                )
            linked_times.append(_parse_utc(event["executed_at"]))
        if _parse_utc(source["retrieved_at"]) != max(linked_times):
            raise ValueError(f"{source['id']} retrieved_at must equal its latest linked event")


def _validate_sources_and_freshness(ledger: dict[str, Any]) -> None:
    trigger_ids = {trigger["id"] for trigger in ledger["freshness_triggers"]}
    cited_ids = {
        citation for question in ledger["review_questions"] for citation in question["citations"]
    }

    for source in ledger["sources"]:
        source_id = source["id"]
        if source_id not in cited_ids:
            raise ValueError(f"{source_id} is included but does not support any review question")
        if source["source_class"] != "owner-supplied-specification":
            parsed = urlparse(source["locator"])
            if parsed.scheme != "https" or not parsed.hostname:
                raise ValueError(f"{source_id} must use an exact HTTPS issuing-authority locator")

        freshness = source["freshness"]
        if any(trigger_id not in trigger_ids for trigger_id in freshness["event_trigger_ids"]):
            raise ValueError(f"{source_id} references an unresolved freshness trigger")
        maximum_age = freshness["maximum_age_days"]
        next_review = freshness["next_review_on"]
        if maximum_age is None:
            if next_review is not None:
                raise ValueError(f"{source_id} event-only freshness cannot have a review date")
        else:
            expected_review = _parse_utc(source["retrieved_at"]).date() + timedelta(
                days=maximum_age
            )
            if next_review is None or date.fromisoformat(next_review) != expected_review:
                raise ValueError(f"{source_id} freshness date does not match its maximum age")

    for source_id, (filename, digest) in EXPECTED_SPEC_IDENTITIES.items():
        source = next(source for source in ledger["sources"] if source["id"] == source_id)
        if source["locator"] != filename:
            raise ValueError(f"{source_id} filename drifted")
        if source["identity_control"] != {"kind": "sha256", "value": digest}:
            raise ValueError(f"{source_id} SHA-256 drifted")


def _validate_questions_and_artifacts(ledger: dict[str, Any]) -> None:
    sources = {source["id"]: source for source in ledger["sources"]}
    for question in ledger["review_questions"]:
        item = question["item"]
        if question["id"] != f"RQ-{item:03d}":
            raise ValueError(f"review question {question['id']} does not match item {item}")
        for citation in question["citations"]:
            if citation not in sources:
                raise ValueError(f"item {item} citation does not resolve: {citation}")
            if item not in sources[citation]["foundation_items"]:
                raise ValueError(f"item {item} is outside cited source {citation}'s mapping")
        for artifact_ref in question["artifact_refs"]:
            relative_path = artifact_ref.partition(":")[0]
            artifact_path = (ROOT / relative_path).resolve()
            try:
                artifact_path.relative_to(ROOT.resolve())
            except ValueError as error:
                raise ValueError(f"item {item} artifact reference escapes the project") from error
            if not artifact_path.is_file():
                raise ValueError(f"item {item} artifact reference does not exist: {relative_path}")


def _validate_cross_artifact_source_identity(ledger: dict[str, Any]) -> None:
    ledger_sources = {source["id"]: source for source in ledger["sources"]}
    product = _read_object(PRODUCT_PATH)
    governance = _read_object(GOVERNANCE_PATH)
    matrix = _read_object(MATRIX_PATH)

    for artifact_name, artifact in (
        (PRODUCT_PATH.name, product),
        (GOVERNANCE_PATH.name, governance),
        (MATRIX_PATH.name, matrix),
    ):
        records = {source["id"]: source for source in artifact["source_documents"]}
        if set(records) != set(EXPECTED_SPEC_IDENTITIES):
            raise ValueError(f"{artifact_name} does not retain both supplied source identities")
        for source_id, (filename, digest) in EXPECTED_SPEC_IDENTITIES.items():
            if records[source_id]["filename"] != filename or records[source_id]["sha256"] != digest:
                raise ValueError(f"{artifact_name} silently drifted {source_id} identity")

    legal_sources = {source["id"]: source for source in governance["legal_sources"]}
    expected_legal_ids = set(EXPECTED_SOURCE_IDS[-17:])
    if set(legal_sources) != expected_legal_ids:
        raise ValueError("governance legal-source register drifted from the exact 17-source review")
    for source_id, legal_source in legal_sources.items():
        ledger_source = ledger_sources[source_id]
        comparisons = (
            ("authority", "authority"),
            ("title", "title"),
            ("locator", "url"),
            ("proposition", "project_proposition"),
        )
        for ledger_key, governance_key in comparisons:
            if ledger_source[ledger_key] != legal_source[governance_key]:
                raise ValueError(
                    f"legal source drift for {source_id}: {ledger_key} no longer matches governance"
                )

    if product["owner"]["full_name"] != ledger["review_protocol"]["owner"]:
        raise ValueError("product owner and evidence-review owner must match")
    deployment = product["deployment"]
    if (
        deployment["primary_origin"],
        deployment["aws_region"],
        product["localization"]["default_locale"],
    ) != ("https://ahmadabdullayev.com", "eu-central-1", "en"):
        raise ValueError("domain, region or locale drifted from the reviewed item 11–12 decision")
    conditionals = product["conditional_requirements"]
    if len(conditionals) != 54 or Counter(row["state"] for row in conditionals) != Counter(
        active=12, inactive=42
    ):
        raise ValueError(
            "the item 14 decision must remain exactly 54 rows: 12 active and 42 inactive"
        )

    requirements = matrix["requirements"]
    priority_counts = Counter(
        (row["priority"]["level"], row["priority"]["obligation"]) for row in requirements
    )
    expected_priorities = Counter(
        {("P0", "MUST"): 148, ("P1", "SHOULD"): 62, ("P2", "CONDITIONAL"): 52, ("P2", "MAY"): 2}
    )
    applicability_counts = Counter(row["applicability"]["state"] for row in requirements)
    if len(requirements) != 264 or priority_counts != expected_priorities:
        raise ValueError("the item 23 matrix population or exact priority counts drifted")
    if applicability_counts != Counter(applicable=222, not_applicable=42):
        raise ValueError("the item 23 matrix applicability counts drifted")


def _validate_pinned_registers(ledger: dict[str, Any]) -> None:
    for key, expected_digest in EXPECTED_DIGESTS.items():
        if _stable_digest(ledger[key]) != expected_digest:
            raise ValueError(
                f"{key} drifted from the reviewed register; create a new retrieval "
                "and ledger version"
            )


def validate_scope_evidence(ledger: dict[str, Any] | None = None) -> None:
    candidate = _read_object(LEDGER_PATH) if ledger is None else ledger
    _validate_schema(candidate)
    _validate_scope_and_ids(candidate)
    _validate_retrieval_events(candidate)
    _validate_sources_and_freshness(candidate)
    _validate_questions_and_artifacts(candidate)
    _validate_cross_artifact_source_identity(candidate)
    _validate_pinned_registers(candidate)


def main() -> int:
    validate_scope_evidence()
    ledger = _read_object(LEDGER_PATH)
    candidates = sum(event["candidate_count"] for event in ledger["retrieval_events"])
    excluded = sum(event["excluded_count"] for event in ledger["retrieval_events"])
    print(
        "Scope evidence ledger is valid: "
        f"{len(ledger['review_questions'])} questions, "
        f"{len(ledger['sources'])} sources, "
        f"{candidates} screened candidates, {excluded} excluded."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

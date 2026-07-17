from __future__ import annotations

import hashlib
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
EXPECTED_BASELINE_SHA256 = "6336e99bbb961293e5d54aa0bed56439d4e90f77b505918c89f590ca7be2debb"
UNSUPPORTED_ATTRIBUTES = {
    "academic_title",
    "biography",
    "degree",
    "discipline",
    "institutional_affiliation",
}
EXPECTED_ENVIRONMENTS = ("local", "test-ci", "preview", "staging", "production")
EXPECTED_MAINTAINER_ROLES = ("owner", "administrator", "editor")
ACTIVE_P2_REQUIREMENTS = {
    "FR-ADMIN-08",
    "FR-ADMIN-11",
    "FR-ADMIN-14",
    "FR-ADMIN-16",
    "FR-CONTACT-03",
    "FR-CONTENT-10",
    "FR-OPS-03",
    "FR-SEC-02",
    "FR-SEC-04",
    "FR-SEC-05",
    "FR-SEC-06",
    "FR-SEC-09",
}
DECISION_OWNER_BY_MODULE = {
    "ABOUT": "content",
    "ACC": "accessibility",
    "ACADEMIC": "content",
    "ADMIN": "product",
    "CAREER": "content",
    "CONTACT": "product",
    "CONTENT": "content",
    "DOC": "content",
    "I18N": "content",
    "INT": "content",
    "OPS": "operations",
    "PROJ": "content",
    "PUB": "content",
    "RES": "content",
    "SEC": "security",
}
CONDITIONAL_REQUIREMENT_ROWS = (
    ("FR-ABOUT-07", "Optional pronouns and pronunciation", "P2-MAY", 48),
    ("FR-ABOUT-09", "Media and event biography kit", "P2-MAY", 51),
    ("FR-RES-09", "Funding relationship", "P2-CONDITIONAL", 62),
    ("FR-RES-10", "Ethics, limitations, and responsible use", "P2-CONDITIONAL", 63),
    ("FR-PUB-06", "Contributor role attribution", "P2-CONDITIONAL", 70),
    ("FR-PUB-07", "Equal and corresponding author indicators", "P2-CONDITIONAL", 71),
    ("FR-PUB-19", "Correction notice", "P2-CONDITIONAL", 84),
    ("FR-PUB-22", "Open-access resource", "P2-CONDITIONAL", 88),
    ("FR-PUB-23", "Local document distribution", "P2-CONDITIONAL", 89),
    ("FR-PUB-24", "Related code and software", "P2-CONDITIONAL", 90),
    ("FR-PUB-25", "Related dataset and supplement", "P2-CONDITIONAL", 91),
    ("FR-PUB-26", "Related presentations and media", "P2-CONDITIONAL", 92),
    ("FR-PUB-31", "RIS and other citation export", "P2-CONDITIONAL", 98),
    ("FR-PUB-38", "Metric provenance", "P2-CONDITIONAL", 106),
    ("FR-PROJ-05", "Team and institution attribution", "P2-CONDITIONAL", 116),
    ("FR-PROJ-09", "Repository and demonstration links", "P2-CONDITIONAL", 121),
    ("FR-PROJ-13", "Software output metadata", "P2-CONDITIONAL", 125),
    ("FR-PROJ-14", "Dataset output metadata", "P2-CONDITIONAL", 126),
    ("FR-CAREER-03", "Thesis and supervision metadata", "P2-CONDITIONAL", 129),
    ("FR-CAREER-09", "Visiting and fellowship distinction", "P2-CONDITIONAL", 136),
    ("FR-ACADEMIC-01", "Teaching profile", "P2-CONDITIONAL", 143),
    ("FR-ACADEMIC-02", "Course records", "P2-CONDITIONAL", 144),
    ("FR-ACADEMIC-04", "Mentoring and supervision", "P2-CONDITIONAL", 146),
    ("FR-ACADEMIC-05", "Award and honour records", "P2-CONDITIONAL", 147),
    ("FR-ACADEMIC-06", "Grant and funding records", "P2-CONDITIONAL", 148),
    ("FR-ACADEMIC-07", "Talk and presentation records", "P2-CONDITIONAL", 149),
    ("FR-ACADEMIC-08", "Presentation state and resources", "P2-CONDITIONAL", 150),
    ("FR-ACADEMIC-09", "Academic service records", "P2-CONDITIONAL", 151),
    ("FR-CONTENT-04", "Public scholarship articles", "P2-CONDITIONAL", 159),
    ("FR-CONTENT-07", "Technical content support", "P2-CONDITIONAL", 162),
    ("FR-CONTENT-08", "Media appearance records", "P2-CONDITIONAL", 163),
    ("FR-CONTENT-10", "Feed and social metadata", "P2-CONDITIONAL", 166),
    ("FR-DOC-07", "Multiple public variants", "P2-CONDITIONAL", 173),
    ("FR-CONTACT-03", "Optional contact form", "P2-CONDITIONAL", 178),
    ("FR-INT-02", "ORCID public-record retrieval", "P2-CONDITIONAL", 199),
    ("FR-INT-03", "Crossref DOI metadata retrieval", "P2-CONDITIONAL", 200),
    ("FR-ACC-12", "Captions and transcripts", "P2-CONDITIONAL", 237),
    ("FR-I18N-02", "Multilingual page variants", "P2-CONDITIONAL", 248),
    ("FR-I18N-03", "Equivalent language switching", "P2-CONDITIONAL", 249),
    ("FR-I18N-04", "Localized metadata and alternates", "P2-CONDITIONAL", 250),
    ("FR-I18N-06", "Directionality and mixed-language support", "P2-CONDITIONAL", 252),
    ("FR-ADMIN-08", "Media and document management", "P2-CONDITIONAL", 261),
    ("FR-ADMIN-11", "Scheduled publication and expiration", "P2-CONDITIONAL", 265),
    ("FR-ADMIN-14", "Audit trail", "P2-CONDITIONAL", 268),
    ("FR-ADMIN-16", "Build and release status", "P2-CONDITIONAL", 270),
    ("FR-SEC-02", "Administrative authentication", "P2-CONDITIONAL", 273),
    ("FR-SEC-04", "Role-based least privilege", "P2-CONDITIONAL", 275),
    ("FR-SEC-05", "Secure session lifecycle", "P2-CONDITIONAL", 276),
    ("FR-SEC-06", "Account recovery and MFA", "P2-CONDITIONAL", 277),
    ("FR-SEC-09", "Secure upload handling", "P2-CONDITIONAL", 281),
    ("FR-SEC-13", "Optional analytics activation", "P2-CONDITIONAL", 285),
    ("FR-SEC-14", "Privacy preference control", "P2-CONDITIONAL", 286),
    ("FR-SEC-16", "Third-party embed privacy", "P2-CONDITIONAL", 289),
    ("FR-OPS-03", "Loading and retry states", "P2-CONDITIONAL", 294),
)
CONDITIONAL_REQUIREMENTS = {
    requirement_id: (title, priority, page)
    for requirement_id, title, priority, page in CONDITIONAL_REQUIREMENT_ROWS
}


def _read_object(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as input_file:
        value: object = json.load(input_file)
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def _digest(value: object) -> str:
    canonical = json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()


def _validate_schema(baseline: dict[str, Any]) -> None:
    schema = _read_object(SCHEMA_PATH)
    if schema.get("$id") != "https://ahmadabdullayev.com/schemas/product-baseline.schema.json":
        raise ValueError("product schema ID must use the selected primary domain")
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


def _validate_scope_decisions(baseline: dict[str, Any]) -> None:
    if baseline["baseline_version"] != "2.0.0":
        raise ValueError("the complete foundation scope decision artifact must be version 2.0.0")

    deployment = baseline["deployment"]
    environments = deployment["environments"]
    environment_ids = tuple(environment["id"] for environment in environments)
    if environment_ids != EXPECTED_ENVIRONMENTS:
        raise ValueError("deployment environments must be complete, unique and ordered")
    expected_origins = {
        "local": "http://localhost:8000",
        "test-ci": "http://testserver",
        "preview": "https://pr-{change-id}.preview.ahmadabdullayev.com",
        "staging": "https://staging.ahmadabdullayev.com",
        "production": deployment["primary_origin"],
    }
    if any(
        environment["authoritative_origin"] != expected_origins[environment["id"]]
        for environment in environments
    ):
        raise ValueError("every deployment environment must use its selected authoritative origin")
    public_authorities = [
        environment["id"]
        for environment in environments
        if environment["authoritative_for_public_content"]
    ]
    if public_authorities != ["production"]:
        raise ValueError("production must be the sole authority for public content")
    environment_by_id = {environment["id"]: environment for environment in environments}
    if environment_by_id["preview"]["indexing"] != "deny-by-authentication-and-noindex":
        raise ValueError("preview must be authenticated and noindex")
    if environment_by_id["staging"]["indexing"] != "deny-by-authentication-and-noindex":
        raise ValueError("staging must be authenticated and noindex")
    if deployment["aws_region"] != "eu-central-1":
        raise ValueError("the selected AWS region must be eu-central-1")

    localization = baseline["localization"]
    active_locale_tags = [locale["tag"] for locale in localization["active_locales"]]
    if localization["default_locale"] != baseline["default_public_language"]:
        raise ValueError("the localization and public-language defaults must match")
    if active_locale_tags != ["en"] or localization["language_selector_active"]:
        raise ValueError("English must be the sole active locale with no empty language selector")

    administration = baseline["administration"]
    roles = administration["roles"]
    role_ids = tuple(role["id"] for role in roles)
    if role_ids != EXPECTED_MAINTAINER_ROLES:
        raise ValueError("owner, administrator and editor roles must be complete and ordered")
    initial_counts = {role["id"]: role["initial_account_count"] for role in roles}
    if initial_counts != {"owner": 1, "administrator": 0, "editor": 0}:
        raise ValueError("the initial administration assignment must be exactly one owner")
    if administration["initial_assignments"] != [
        {"principal": baseline["owner"]["full_name"], "role": "owner"}
    ]:
        raise ValueError("the initial maintainer assignment must identify the actual owner")
    if set(administration["mfa_required_roles"]) != set(EXPECTED_MAINTAINER_ROLES):
        raise ValueError("MFA must be required for every maintainer role")
    for role in roles:
        if set(role["permissions"]) & set(role["prohibitions"]):
            raise ValueError(f"{role['id']} permissions and prohibitions must not conflict")
    session_policy = administration["session_policy"]
    if session_policy["idle_timeout_minutes"] != 30:
        raise ValueError("administrative session idle timeout must be 30 minutes")
    if session_policy["absolute_timeout_hours"] != 12:
        raise ValueError("administrative session absolute timeout must be 12 hours")

    features = baseline["feature_decisions"]
    contact = features["contact"]
    if contact["delivery_region"] != deployment["aws_region"]:
        raise ValueError("contact delivery and application data must use the selected AWS region")
    if contact["public_email_address_published"] or contact["public_cookie_required"]:
        raise ValueError("the selected contact form must publish no email and require no cookie")
    if "not a legal basis" not in contact["privacy_acknowledgement_semantics"]:
        raise ValueError("privacy acknowledgement must not be represented as a legal basis")
    search = features["search"]
    if search["query_analytics"] or search["public_cookie_required"]:
        raise ValueError("public search must be cookieless and must not log behavioral analytics")
    if search["raw_query_persistence"] != "prohibited":
        raise ValueError("public search must not persist raw queries")
    if search["security_logging"] != "redacted-and-minimized-with-no-raw-query":
        raise ValueError("search security logging must exclude raw queries")

    records = baseline["conditional_requirements"]
    record_ids = tuple(record["id"] for record in records)
    expected_ids = tuple(row[0] for row in CONDITIONAL_REQUIREMENT_ROWS)
    if record_ids != expected_ids:
        raise ValueError("all 54 P2 requirement decisions must be present once and in source order")
    for record in records:
        expected_title, expected_priority, expected_page = CONDITIONAL_REQUIREMENTS[record["id"]]
        expected_source = f"website-srs:{record['id']}:p{expected_page}"
        if (
            record["title"] != expected_title
            or record["priority"] != expected_priority
            or record["source_ref"] != expected_source
        ):
            raise ValueError(f"{record['id']} metadata does not match the reviewed SRS card")
        module = record["id"].split("-")[1]
        if record["decision_owner"] != DECISION_OWNER_BY_MODULE[module]:
            raise ValueError(f"{record['id']} has the wrong accountable decision owner")
    active_ids = {record["id"] for record in records if record["state"] == "active"}
    if active_ids != ACTIVE_P2_REQUIREMENTS:
        raise ValueError("the 54-row P2 activation set does not match the approved scope")
    priority_counts = {
        priority: sum(record["priority"] == priority for record in records)
        for priority in {"P2-CONDITIONAL", "P2-MAY"}
    }
    if priority_counts != {"P2-CONDITIONAL": 52, "P2-MAY": 2}:
        raise ValueError("the P2 inventory must contain 52 conditional and two optional cards")

    synchronization = features["scholarly_synchronization"]
    if synchronization["orcid"]["state"] != "inactive" or "FR-INT-02" in active_ids:
        raise ValueError("ORCID retrieval must remain inactive until its evidence gate passes")
    if synchronization["crossref"]["state"] != "inactive" or "FR-INT-03" in active_ids:
        raise ValueError("Crossref retrieval must remain inactive until its evidence gate passes")
    privacy = features["privacy_and_discovery"]
    if privacy["analytics"] != "inactive" or "FR-SEC-13" in active_ids:
        raise ValueError("analytics must remain inactive")
    if privacy["public_nonessential_cookies"] != "inactive" or "FR-SEC-14" in active_ids:
        raise ValueError("public nonessential cookies and preference controls must remain inactive")
    if not privacy["third_party_embeds"].startswith("inactive") or "FR-SEC-16" in active_ids:
        raise ValueError("third-party embeds must remain inactive")
    if not privacy["atom_feed"].startswith("active") or "FR-CONTENT-10" not in active_ids:
        raise ValueError("the Atom feed decision must activate feed and social metadata")
    if contact["state"] != "active" or "FR-CONTACT-03" not in active_ids:
        raise ValueError("the selected contact form must activate FR-CONTACT-03")


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

    _validate_scope_decisions(baseline)

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

    if _digest(baseline) != EXPECTED_BASELINE_SHA256:
        raise ValueError("approved product decision digest does not match baseline 2.0.0")


def main() -> None:
    baseline = _read_object(BASELINE_PATH)
    validate_baseline(baseline)
    print(
        "product baseline valid: schema, sources, owner, approvers, audiences, goals, "
        "deployment, localization, administration, features and all 54 P2 decisions "
        "are complete"
    )


if __name__ == "__main__":
    main()

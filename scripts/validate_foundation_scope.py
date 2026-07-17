from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PRODUCT_PATH = ROOT / "config" / "product-baseline.json"
GOVERNANCE_PATH = ROOT / "config" / "foundation-governance.json"
MATRIX_PATH = ROOT / "config" / "requirements-matrix.json"
MANIFEST_PATH = ROOT / "config" / "foundation-scope-manifest.json"

DEPLOYMENT_TEMPLATES = {
    "preview": ROOT / ".env.preview.example",
    "staging": ROOT / ".env.staging.example",
    "production": ROOT / ".env.production.example",
}
REQUIRED_DOCUMENTS = (
    ROOT / "docs" / "product" / "foundation-scope-decisions.md",
    ROOT / "docs" / "product" / "legal-content-governance.md",
    ROOT / "docs" / "product" / "initial-content-inventory.md",
    ROOT / "docs" / "product" / "revision-and-approval.md",
    ROOT / "docs" / "research" / "scope-governance-literature-review.md",
    ROOT / "docs" / "research" / "scope-evidence-protocol.md",
    ROOT / "docs" / "traceability" / "requirements-matrix.md",
)


def _read_object(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as input_file:
        value: object = json.load(input_file)
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def _source_identity(document: dict[str, Any]) -> tuple[str, str, str]:
    return document["id"], document["filename"], document["sha256"]


def _parse_template(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line_number, raw_line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        name, separator, value = line.partition("=")
        if not separator or not name or name in values:
            raise ValueError(f"{path.name}:{line_number} is not a unique NAME=value entry")
        values[name] = value
    return values


def _validate_sources(
    product: dict[str, Any], governance: dict[str, Any], matrix: dict[str, Any]
) -> None:
    expected = [_source_identity(document) for document in product["source_documents"]]
    for name, artifact in (("governance", governance), ("matrix", matrix)):
        actual = [_source_identity(document) for document in artifact["source_documents"]]
        if actual != expected:
            raise ValueError(f"{name} source identity differs from the product baseline")


def _validate_owner_and_approvals(
    product: dict[str, Any],
    governance: dict[str, Any],
    matrix: dict[str, Any],
    manifest: dict[str, Any],
) -> None:
    owner = product["owner"]["full_name"]
    if owner != product["owner"]["represented_person"]:
        raise ValueError("the product owner and represented person must remain identical")
    if governance["content_governance"]["canonical_editorial_owner"] != owner:
        raise ValueError("governance editorial ownership differs from the product owner")
    if {row["ownership"]["assigned_person"] for row in matrix["requirements"]} != {owner}:
        raise ValueError("matrix ownership differs from the product owner")

    product_approvers = product["approvers"]
    approval_by_id = {record["id"]: record for record in governance["approval_records"]}
    if len(approval_by_id) != len(governance["approval_records"]):
        raise ValueError("governance approval IDs are not unique")
    try:
        current_approvals = [approval_by_id[approval_id] for approval_id in manifest["approval_ids"]]
    except KeyError as error:
        raise ValueError("manifest references an unknown governance approval") from error
    governance_approvals = {record["domain"]: record for record in current_approvals}
    if len(governance_approvals) != len(current_approvals):
        raise ValueError("manifest current approvals must identify one decision per domain")
    if set(governance_approvals) != set(product_approvers):
        raise ValueError("the governance and product approval domains differ")
    for domain, assignment in product_approvers.items():
        record = governance_approvals[domain]
        if assignment["name"] != owner or record["approver_role"] != assignment["role"]:
            raise ValueError(f"{domain} governance approval differs from its named assignment")
        if record["scope_items"] != list(range(11, 24)):
            raise ValueError(f"{domain} approval does not cover exactly foundation items 11-23")
        if record["artifact_version"] != manifest["artifact_version"]:
            raise ValueError(f"{domain} approval refers to the wrong manifest version")
        if record["logical_artifact_id"] != manifest["logical_artifact_id"]:
            raise ValueError(f"{domain} approval refers to the wrong manifest artifact")
        if record["result"] != "approved-for-foundation-scope":
            raise ValueError(f"{domain} current decision does not approve foundation scope")
        domain_records = [
            approval
            for approval in governance["approval_records"]
            if approval["domain"] == domain
        ]
        if domain_records[-1]["id"] != record["id"]:
            raise ValueError(f"manifest does not select the latest {domain} approval")

    revision_by_id = {revision["id"]: revision for revision in governance["revision_history"]}
    if manifest["revision_id"] not in revision_by_id:
        raise ValueError("manifest references an unknown governance revision")
    current_revision = governance["revision_history"][-1]
    if manifest["revision_id"] != current_revision["id"]:
        raise ValueError("manifest does not select the latest governance revision")
    if current_revision["logical_artifact_id"] != manifest["logical_artifact_id"]:
        raise ValueError("manifest and current revision logical artifacts differ")
    if current_revision["version"] != manifest["artifact_version"]:
        raise ValueError("manifest and current revision versions differ")


def _validate_deployment_and_features(product: dict[str, Any], governance: dict[str, Any]) -> None:
    deployment = product["deployment"]
    hosting = governance["jurisdiction"]["selected_hosting"]
    if deployment["aws_region"] != hosting["region"]:
        raise ValueError("product and governance hosting regions differ")
    if deployment["primary_origin"] != "https://" + deployment["canonical_host"]:
        raise ValueError("the primary origin does not match the canonical host")
    if product["default_public_language"] != product["localization"]["default_locale"]:
        raise ValueError("the legacy and detailed default-locale decisions differ")
    active_locale_tags = [locale["tag"] for locale in product["localization"]["active_locales"]]
    if active_locale_tags != [product["default_public_language"]]:
        raise ValueError("the selected active-locale set differs from the default language")

    features = product["feature_decisions"]
    processing = governance["jurisdiction"]["activated_processing_snapshot"]
    expected_processing = {
        "contact_form": "active-direct-submission-channel-with-aws-ses"
        if features["contact"]["state"] == "active"
        and features["contact"]["delivery_provider"] == "amazon-ses"
        else "inactive",
        "public_search": "active-public-content-only-no-raw-query-retention"
        if features["search"]["state"] == "active"
        and features["search"]["raw_query_persistence"] == "prohibited"
        else "inactive",
        "orcid_synchronization": features["scholarly_synchronization"]["orcid"]["state"],
        "crossref_synchronization": features["scholarly_synchronization"]["crossref"]["state"],
        "analytics": features["privacy_and_discovery"]["analytics"],
        "nonessential_cookies": features["privacy_and_discovery"]["public_nonessential_cookies"],
    }
    for name, expected in expected_processing.items():
        if processing[name] != expected:
            raise ValueError(f"{name} differs between feature and processing decisions")
    if processing["third_party_embeds"] != "inactive" or not features["privacy_and_discovery"][
        "third_party_embeds"
    ].startswith("inactive"):
        raise ValueError("third-party embed decisions differ")
    if processing["atom_feed"] != "active-public-content-only" or not features[
        "privacy_and_discovery"
    ]["atom_feed"].startswith("active"):
        raise ValueError("Atom feed decisions differ")
    if processing["static_social_previews"] != "active-public-content-only" or not features[
        "privacy_and_discovery"
    ]["static_social_previews"].startswith("active"):
        raise ValueError("social-preview decisions differ")
    if features["contact"]["delivery_region"] != deployment["aws_region"]:
        raise ValueError("contact delivery and application regions differ")
    controls = governance["jurisdiction"]["personal_data_controls"]
    if controls["consent"]["privacy_acknowledgement_is_legal_consent"] is not False:
        raise ValueError("privacy acknowledgement semantics differ between scope records")
    if "not a legal basis" not in features["contact"]["privacy_acknowledgement_semantics"]:
        raise ValueError("contact acknowledgement is incorrectly represented as legal consent")
    minimization = controls["data_minimization_and_incidental_data"]
    if minimization["raw_search_query_persistence"] != features["search"][
        "raw_query_persistence"
    ]:
        raise ValueError("raw search-query retention differs between scope records")


def _validate_effective_time(
    product: dict[str, Any],
    governance: dict[str, Any],
    matrix: dict[str, Any],
    manifest: dict[str, Any],
) -> None:
    product_date = product["effective_date"]
    if matrix["effective_date"] != product_date:
        raise ValueError("matrix and product effective dates differ")
    governance_instant = datetime.fromisoformat(
        governance["effective_at"].replace("Z", "+00:00")
    )
    if governance_instant.date().isoformat() != product_date:
        raise ValueError("governance, product and matrix effective dates differ")
    manifest_instant = datetime.fromisoformat(manifest["effective_at"].replace("Z", "+00:00"))
    if manifest_instant != governance_instant:
        raise ValueError("manifest and governance effective instants differ")
    revision_times = [
        datetime.fromisoformat(revision["recorded_at"].replace("Z", "+00:00"))
        for revision in governance["revision_history"]
    ]
    approval_times = [
        datetime.fromisoformat(approval["decided_at"].replace("Z", "+00:00"))
        for approval in governance["approval_records"]
    ]
    if any(recorded_at > governance_instant for recorded_at in revision_times):
        raise ValueError("a revision is later than the governance effective instant")
    if any(decided_at > governance_instant for decided_at in approval_times):
        raise ValueError("an approval is later than the governance effective instant")


def _validate_matrix_decisions(product: dict[str, Any], matrix: dict[str, Any]) -> None:
    if matrix["baseline_version"] != product["baseline_version"]:
        raise ValueError("matrix and product baseline versions differ")
    decisions = {decision["id"]: decision for decision in product["conditional_requirements"]}
    p2_rows = {row["id"]: row for row in matrix["requirements"] if row["priority"]["level"] == "P2"}
    if set(p2_rows) != set(decisions):
        raise ValueError("the matrix and product baseline do not contain the same P2 decisions")
    for requirement_id, decision in decisions.items():
        row = p2_rows[requirement_id]
        expected_state = "applicable" if decision["state"] == "active" else "not_applicable"
        if row["applicability"]["state"] != expected_state:
            raise ValueError(f"{requirement_id} applicability differs from its scope decision")
        if row["applicability"]["condition"] != decision["activation_condition"]:
            raise ValueError(
                f"{requirement_id} activation condition differs from its scope decision"
            )
        if row["applicability"]["rationale"] != decision["rationale"]:
            raise ValueError(f"{requirement_id} rationale differs from its scope decision")


def _validate_deployment_templates(product: dict[str, Any]) -> None:
    deployment = product["deployment"]
    origins = {
        environment["id"]: environment["authoritative_origin"]
        for environment in deployment["environments"]
    }
    expected_contact_modes = {"preview": "disabled", "staging": "disabled", "production": "ses"}
    for environment, path in DEPLOYMENT_TEMPLATES.items():
        values = _parse_template(path)
        expected_origin = origins[environment]
        if "{change-id}" in expected_origin:
            expected_origin = expected_origin.replace("{change-id}", "000")
        expected_host = expected_origin.removeprefix("https://")
        expected_values = {
            "APP_ENV": environment,
            "DJANGO_SETTINGS_MODULE": f"paw.settings.{environment}",
            "SITE_BASE_URL": expected_origin,
            "DJANGO_ALLOWED_HOSTS": expected_host,
            "AWS_REGION": deployment["aws_region"],
            "DEFAULT_LANGUAGE": product["localization"]["default_locale"],
            "SUPPORTED_LANGUAGES": ",".join(
                locale["tag"] for locale in product["localization"]["active_locales"]
            ),
            "CONTACT_DELIVERY_MODE": expected_contact_modes[environment],
            "ORCID_ENABLED": "false",
            "CROSSREF_ENABLED": "false",
        }
        for name, expected in expected_values.items():
            if values.get(name) != expected:
                raise ValueError(f"{path.name} {name} differs from the approved scope")


def validate_foundation_scope(
    product: dict[str, Any],
    governance: dict[str, Any],
    matrix: dict[str, Any],
    manifest: dict[str, Any] | None = None,
) -> None:
    if manifest is None:
        manifest = _read_object(MANIFEST_PATH)
    _validate_sources(product, governance, matrix)
    _validate_owner_and_approvals(product, governance, matrix, manifest)
    _validate_deployment_and_features(product, governance)
    _validate_effective_time(product, governance, matrix, manifest)
    _validate_matrix_decisions(product, matrix)
    _validate_deployment_templates(product)
    missing_documents = [path.name for path in REQUIRED_DOCUMENTS if not path.is_file()]
    if missing_documents:
        raise ValueError("foundation decision documents are missing: " + ", ".join(missing_documents))


def main() -> None:
    product = _read_object(PRODUCT_PATH)
    governance = _read_object(GOVERNANCE_PATH)
    matrix = _read_object(MATRIX_PATH)
    validate_foundation_scope(product, governance, matrix)
    print(
        "foundation scope coherent: items 11-23, 3 baselines, 3 deployment templates, "
        "6 approvals and 264 requirement rows"
    )


if __name__ == "__main__":
    main()

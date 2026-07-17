from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
BASELINE_PATH = ROOT / "config" / "foundation-governance.json"
SCHEMA_PATH = ROOT / "config" / "foundation-governance.schema.json"
PRODUCT_BASELINE_PATH = ROOT / "config" / "product-baseline.json"

SOURCE_HASHES = {
    "website-srs": "976ba51a785d27d37117655a4a508eb5133edb36e988966ce31e8878a78eb9e7",
    "backend-specification": "1eca221859e9379cadd3d3e192bd35b68a7e0010ae15f8de53e539e1782c31b5",
}
SOURCE_FILENAMES = {
    "website-srs": "personal_academic_professional_website_srs.pdf",
    "backend-specification": "personal_academic_website_backend_specification.pdf",
}
SOURCE_PRINTED_PAGE_BOUNDS = {
    "website-srs": 316,
    "backend-specification": 63,
}
OWNER_DIRECTIVE_IDS = {"2026-07-17-items-19-22"}
SOURCE_GAP_IDS = {
    "no-owner-approved-academic-content-supplied",
    "no-owner-approved-source-supplied",
}
EXPECTED_GOVERNANCE_SHA256 = "73ed13c4a97c4cab460eb454f5a7505633871761047093ecc3ef871733db440e"
REQUIRED_LEGAL_SOURCE_IDS = {
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
}
LEGAL_SOURCE_URLS = {
    "LAW-AZ-CONSTITUTION-30-32": ("https://president.az/en/pages/view/azerbaijan/constitution/"),
    "LAW-AZ-PERSONAL-DATA-998-IIIQ": "https://frameworks.e-qanun.az/19/f_19675.html",
    "LAW-AZ-CABINET-237": "https://frameworks.e-qanun.az/21/f_21060.html",
    "LAW-AZ-CABINET-149": (
        "https://mincom.gov.az/storage/pages/649/9b0e869640ba56d43615eef7906a4d08.pdf"
    ),
    "LAW-AZ-CABINET-149-161-2022-AMENDMENT": "https://e-qanun.az/framework/49396",
    "LAW-AZ-CABINET-161": (
        "https://mincom.gov.az/storage/pages/648/4b2105426aa7138d97d78c9e1cfb91c4.pdf"
    ),
    "LAW-AZ-EHIS-DIGITAL-CONSENT": "https://president.az/az/articles/view/69619",
    "AUTHORITY-AZ-PERSONAL-DATA-LICENSING": (
        "https://mincom.gov.az/az/qanunvericilik/lisenziyalasdirma/"
        "rabite-ve-informasiya-texnologiyalari-sahesinde-lisenziyalarin-verilmesi/"
        "lisenziya/ferdi-sahibkarlar-ucun"
    ),
    "AUTHORITY-AZ-PERSONAL-DATA-REGISTRY": (
        "https://mincom.gov.az/az/qanunvericilik/reyestrler/reyestrler"
    ),
    "LAW-AZ-PRIVATE-INTERNATIONAL-LAW": "https://frameworks.e-qanun.az/0/f_509.html",
    "LAW-AZ-COPYRIGHT-115-IQ": "https://frameworks.e-qanun.az/4/f_4167.html",
    "LAW-EU-GDPR-2016-679": "https://eur-lex.europa.eu/eli/reg/2016/679/oj",
    "GUIDANCE-EU-EDPB-ARTICLE-3": (
        "https://www.edpb.europa.eu/documents/guideline/"
        "guidelines-32018-on-the-territorial-scope-of-the-gdpr-article-3-version-adopted_en"
    ),
    "PROVIDER-AWS-REGIONS": (
        "https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html"
    ),
    "PROVIDER-AWS-DATA-PRIVACY": "https://aws.amazon.com/compliance/data-privacy-faq/",
    "PROVIDER-AWS-SES-REGIONS": "https://docs.aws.amazon.com/ses/latest/dg/regions.html",
    "PROVIDER-AWS-SES-DATA-PROTECTION": (
        "https://docs.aws.amazon.com/ses/latest/dg/data-protection.html"
    ),
}
REQUIRED_SOURCE_PROVISIONS = {
    "LAW-AZ-PERSONAL-DATA-998-IIIQ": {
        "Article 3.3",
        "Article 7.5",
        "Article 8.6",
        "Article 9.12",
        "Article 9.14",
        "Article 11.2",
        "Article 12.4 to 12.6",
        "Article 14.2 to 14.4",
        "Article 15",
    },
    "LAW-AZ-CABINET-237": {"Clauses 2.1 to 2.7"},
    "LAW-AZ-CABINET-161": {"Operative protection requirements, read with current amendments"},
    "LAW-AZ-COPYRIGHT-115-IQ": {"Articles 1 to 4 and Article 5.3 to 5.4"},
    "LAW-EU-GDPR-2016-679": {"Article 3"},
}
REQUIRED_SERVICE_ASSESSMENTS = {
    "application-runtime-and-relational-data",
    "object-storage-and-backups",
    "queues-and-job-payloads",
    "application-security-and-audit-logs",
    "amazon-ses-identities-suppression-feedback-and-delivery-events",
    "dns-cdn-certificates-and-edge-processing",
    "control-plane-resource-identifiers-tags-and-metadata",
    "support-access-subprocessors-and-legal-demands",
    "aws-account-billing-and-diagnostic-information",
    "recipient-mailbox-provider-and-mailbox-location",
}
REQUIRED_NOTICE_FIELDS = {
    "owner-or-operator-identity",
    "processing-purpose-and-legal-basis",
    "information-system-protection-level",
    "conformity-certificate-and-state-expertise-status",
    "intended-users-and-information-exchange-systems",
    "statutory-data-subject-rights",
}
REQUIRED_SECURITY_EVIDENCE = {
    "threat-and-protection-level-assessment",
    "approved-software-and-operating-instructions",
    "restoration-and-continuity-controls",
    "protection-and-system-project-documentation",
    "access-security-and-control-audit-registers",
    "physical-and-data-centre-controls",
    "licensed-software-evidence",
    "role-based-access-authentication-and-authorization",
    "decision-161-encryption-control-including-256-bit-key-requirement",
    "conformity-certification-and-state-expertise-evidence",
}
AZ_OFFICIAL_HOSTS = {
    "e-qanun.az",
    "frameworks.e-qanun.az",
    "mincom.gov.az",
    "president.az",
}
EU_OFFICIAL_HOSTS = {"eur-lex.europa.eu", "www.edpb.europa.eu"}
AWS_OFFICIAL_HOSTS = {"aws.amazon.com", "docs.aws.amazon.com"}
APPROVAL_ROLES = {
    "product": "Website Owner and Product Approver",
    "content": "Academic Content Approver",
    "accessibility": "Accessibility Approver",
    "security": "Security Approver",
    "privacy": "Privacy Approver",
    "operations": "Technical Operations Approver",
}
INITIAL_APPROVAL_IDS = {domain: f"APR-{domain.upper()}-001" for domain in APPROVAL_ROLES}
REVIEW_SCHEDULES = {
    "RG-030": 30,
    "RG-090": 90,
    "RG-180": 180,
    "RG-365": 365,
}
DOCUMENT_PATHS = (
    ROOT / "docs" / "product" / "legal-content-governance.md",
    ROOT / "docs" / "product" / "initial-content-inventory.md",
    ROOT / "docs" / "product" / "revision-and-approval.md",
)


def _read_object(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as input_file:
        value: object = json.load(input_file)
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def _canonical_sha256(value: object) -> str:
    canonical = json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    )
    return hashlib.sha256(canonical.encode()).hexdigest()


def _validate_schema(baseline: dict[str, Any]) -> None:
    schema = _read_object(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(baseline), key=lambda error: list(error.absolute_path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        raise ValueError(f"foundation governance schema error at {location}: {error.message}")


def _parse_utc(value: str) -> datetime:
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamps must include a UTC offset")
    return parsed.astimezone(UTC)


def _require_unique(values: list[str], label: str) -> None:
    if len(values) != len(set(values)):
        raise ValueError(f"{label} must be unique")


def _resolve_product_reference(product: dict[str, Any], dotted_path: str) -> None:
    value: object = product
    for part in dotted_path.split("."):
        if not isinstance(value, dict) or part not in value:
            raise ValueError(f"product-baseline reference does not resolve: {dotted_path}")
        value = value[part]


def _validate_inventory_reference(reference: str, product: dict[str, Any]) -> None:
    if reference in REQUIRED_LEGAL_SOURCE_IDS:
        return
    prefix, separator, target = reference.partition(":")
    if not separator or not target:
        raise ValueError(f"inventory source reference is malformed: {reference}")
    if prefix == "product-baseline":
        _resolve_product_reference(product, target)
        return
    if prefix == "repository":
        path = (ROOT / target).resolve()
        try:
            path.relative_to(ROOT.resolve())
        except ValueError as error:
            raise ValueError(f"repository reference escapes the project: {reference}") from error
        if not path.is_file():
            raise ValueError(f"repository reference does not exist: {reference}")
        return
    if prefix in SOURCE_PRINTED_PAGE_BOUNDS:
        match = re.fullmatch(r"p([1-9][0-9]*)(?:-p([1-9][0-9]*))?", target)
        if match is None:
            raise ValueError(
                f"specification reference has invalid printed-page syntax: {reference}"
            )
        start_page = int(match.group(1))
        end_page = int(match.group(2) or start_page)
        if start_page > end_page or end_page > SOURCE_PRINTED_PAGE_BOUNDS[prefix]:
            raise ValueError(
                f"specification reference is outside reviewed page bounds: {reference}"
            )
        return
    if prefix == "owner-directive":
        if target not in OWNER_DIRECTIVE_IDS:
            raise ValueError(f"owner-directive reference is not registered: {reference}")
        return
    if prefix == "source-gap":
        if target not in SOURCE_GAP_IDS:
            raise ValueError(f"source-gap reference is not registered: {reference}")
        return
    raise ValueError(f"inventory source reference uses an unknown prefix: {reference}")


def _validate_sources(baseline: dict[str, Any]) -> None:
    sources = {source["id"]: source for source in baseline["source_documents"]}
    if set(sources) != set(SOURCE_HASHES):
        raise ValueError("both reviewed specification sources must be present")
    for source_id, expected_hash in SOURCE_HASHES.items():
        source = sources[source_id]
        if source["sha256"] != expected_hash:
            raise ValueError(f"{source_id} SHA-256 does not match the reviewed document")
        if source["filename"] != SOURCE_FILENAMES[source_id]:
            raise ValueError(f"{source_id} filename does not match the reviewed document")
        if source["page_reference_model"] != "printed PDF page numbers":
            raise ValueError(f"{source_id} must use printed PDF page references")


def _validate_stakeholders(baseline: dict[str, Any]) -> None:
    stakeholders = baseline["stakeholders"]
    if len(stakeholders) != 1 or stakeholders[0]["id"] != "STK-001":
        raise ValueError("the evidence supports exactly one named stakeholder record")
    stakeholder = stakeholders[0]
    if stakeholder["name"] != "Ahmad Abdullayev":
        raise ValueError("the stakeholder must be the named website owner")
    if not set(APPROVAL_ROLES.values()).issubset(stakeholder["roles"]):
        raise ValueError("the stakeholder record must contain every approval role")

    if PRODUCT_BASELINE_PATH.exists():
        product_baseline = _read_object(PRODUCT_BASELINE_PATH)
        product_owner = product_baseline.get("owner")
        if (
            not isinstance(product_owner, dict)
            or product_owner.get("full_name") != stakeholder["name"]
        ):
            raise ValueError("governance and product baseline owners must match")


def _validate_legal_sources(baseline: dict[str, Any]) -> None:
    sources = baseline["legal_sources"]
    identifiers = [source["id"] for source in sources]
    _require_unique(identifiers, "legal source identifiers")
    missing_identifiers = REQUIRED_LEGAL_SOURCE_IDS - set(identifiers)
    if missing_identifiers:
        raise ValueError(
            "the legal and provider source register is missing required coverage: "
            + ", ".join(sorted(missing_identifiers))
        )

    effective_date = _parse_utc(baseline["effective_at"]).date()
    for source in sources:
        parsed_url = urlparse(source["url"])
        if parsed_url.scheme != "https":
            raise ValueError("legal and provider sources must use HTTPS")
        if source["jurisdiction"] == "AZ" and parsed_url.hostname not in AZ_OFFICIAL_HOSTS:
            raise ValueError("Azerbaijan legal propositions must cite an official Azerbaijan host")
        if source["jurisdiction"] == "EU" and parsed_url.hostname not in EU_OFFICIAL_HOSTS:
            raise ValueError("EU legal propositions must cite EUR-Lex or the EDPB")
        if source["jurisdiction"] == "PROVIDER" and parsed_url.hostname not in AWS_OFFICIAL_HOSTS:
            raise ValueError("provider propositions must cite official AWS documentation")
        if source["jurisdiction"] == "PROVIDER" and (
            source["source_type"] != "provider-documentation"
            or not source["id"].startswith("PROVIDER-")
        ):
            raise ValueError("AWS records must be classified as provider documentation")
        if source["jurisdiction"] != "PROVIDER" and source["id"].startswith("PROVIDER-"):
            raise ValueError("provider-prefixed sources must use the provider jurisdiction")
        if date.fromisoformat(source["reviewed_on"]) > effective_date:
            raise ValueError("a legal source cannot be reviewed after the baseline effective date")
        retrieved_on = date.fromisoformat(source["retrieved_on"])
        reviewed_on = date.fromisoformat(source["reviewed_on"])
        if retrieved_on > effective_date:
            raise ValueError("a legal source cannot be retrieved after the baseline effective date")
        if retrieved_on > reviewed_on:
            raise ValueError("a legal source cannot be reviewed before it was retrieved")

        mappings = source["proposition_mappings"]
        mapping_pairs = [
            f"{mapping['provision']}\0{mapping['proposition']}" for mapping in mappings
        ]
        _require_unique(mapping_pairs, f"{source['id']} proposition mappings")

    indexed_sources = {source["id"]: source for source in sources}
    for source_id, expected_url in LEGAL_SOURCE_URLS.items():
        if indexed_sources[source_id]["url"] != expected_url:
            raise ValueError(f"{source_id} must retain its reviewed official URL")
    for source_id, required_provisions in REQUIRED_SOURCE_PROVISIONS.items():
        actual_provisions = set(indexed_sources[source_id]["provisions"])
        missing_provisions = required_provisions - actual_provisions
        if missing_provisions:
            raise ValueError(
                f"{source_id} omits required provision coverage: "
                + ", ".join(sorted(missing_provisions))
            )


def _validate_jurisdiction(baseline: dict[str, Any], *, as_of: date | None = None) -> None:
    jurisdiction = baseline["jurisdiction"]
    selected_baseline = jurisdiction["selected_project_governance_baseline"]
    applicability = jurisdiction["applicability_determination"]
    provenance = jurisdiction["legal_source_provenance"]
    hosting = jurisdiction["selected_hosting"]
    if (selected_baseline["country_code"], hosting["region"], hosting["country_code"]) != (
        "AZ",
        "eu-central-1",
        "DE",
    ):
        raise ValueError(
            "the provisional governance baseline and hosting geography must remain AZ to DE"
        )
    if selected_baseline["status"] != (
        "provisional-pending-nexus-and-applicable-law-determination"
    ):
        raise ValueError("Azerbaijan must remain a provisional project governance baseline")
    if (
        selected_baseline["choice_of_law_enforceability_asserted"]
        or selected_baseline["court_forum_established"]
    ):
        raise ValueError("the project baseline cannot assert enforceable law choice or court forum")
    if (
        applicability["controller_establishment_and_activity_nexus_status"] != "unverified"
        or applicability["owner_residence_or_citizenship_asserted"]
        or applicability["germany_hosting_alone_triggers_gdpr"]
        or applicability["gdpr_status"] != "contingent-pending-article-3-analysis"
    ):
        raise ValueError(
            "territorial legal applicability must remain pending factual nexus analysis"
        )
    if applicability["household_or_personal_use_exception"] != (
        "not-relied-upon-without-clause-specific-determination"
    ):
        raise ValueError("the household or personal-use exception cannot be assumed")
    if (
        provenance["current_review_content_digest_status"] != "not-recorded"
        or provenance["immutable_source_verification_claimed"]
        or provenance["production_reliance_gate"]
        != "retrieve-current-official-text-and-record-content-sha256-or-stable-"
        "instrument-or-archive-identity"
    ):
        raise ValueError("legal source provenance must expose the unarchived-content gate")
    if set(provenance["required_archive_metadata"]) != {
        "source-id",
        "official-url",
        "retrieval-timestamp",
        "content-sha256-or-stable-instrument-or-archive-identity",
        "official-language-and-translation-status",
        "amendment-through-or-source-currency-status",
    }:
        raise ValueError("the production legal-source archive metadata must remain complete")

    service_assessments = hosting["service_assessment_required_for"]
    _require_unique(service_assessments, "hosting service assessments")
    if set(service_assessments) != REQUIRED_SERVICE_ASSESSMENTS:
        raise ValueError("the AWS and recipient service-by-service assessment must remain complete")
    if hosting["deployment_state"] != "selected-not-deployed-or-evidenced":
        raise ValueError("hosting selection must not be represented as deployed evidence")
    if hosting["application_managed_cross_region_replication"] != (
        "prohibited-unless-separately-approved-and-documented"
    ):
        raise ValueError("application-managed cross-region replication must remain prohibited")
    if hosting["personal_data_in_resource_names_tags_or_free_form_metadata"] != "prohibited":
        raise ValueError("personal data in AWS resource metadata must remain prohibited")
    ses_controls = hosting["ses_controls"]
    if ses_controls["engagement_tracking"] != "disabled":
        raise ValueError("SES open and click engagement tracking must remain disabled")
    if ses_controls["delivery_tls"] != (
        "require-tls-or-send-only-minimal-notification-with-secure-admin-retrieval"
    ):
        raise ValueError("SES delivery must retain its TLS or minimal-notification control")

    controls = jurisdiction["personal_data_controls"]
    registration = controls["registration"]
    if (
        registration["decision"]
        != (
            "register-before-production-unless-a-documented-clause-specific-legal-"
            "determination-establishes-an-exemption"
        )
        or registration["exemption_status"] != "none-relied-upon"
    ):
        raise ValueError("registration must remain the default absent a documented exemption")
    if not registration["evidence_required_before_collection"]:
        raise ValueError("registration or exemption evidence is mandatory before collection")

    licensing = controls["licensing"]
    if licensing["article_9_14_applicability_status"] != "undetermined" or any(
        not licensing[field]
        for field in (
            "determination_and_evidence_required_before_operation",
            "registration_does_not_resolve_licensing",
        )
    ):
        raise ValueError("Article 9.14 licensing must remain an independent operation gate")

    consent = controls["consent"]
    if consent["privacy_acknowledgement_is_legal_consent"]:
        raise ValueError("a privacy acknowledgement cannot be represented as legal consent")
    if consent["article_8_6_ehis_applicability_status"] != "undetermined" or any(
        not consent[field]
        for field in (
            "ehis_or_digital_consent_determination_required_before_collection",
            "consent_evidence_required_when_consent_is_the_basis",
            "withdrawal_mechanism_must_match_applicable_legal_channel",
        )
    ):
        raise ValueError("Article 8.6 EHIS consent and withdrawal must remain a release gate")

    certification = controls["certification_and_state_expertise"]
    if (
        certification["conformity_certificate_applicability_status"] != "undetermined"
        or certification["state_expert_examination_applicability_status"] != "undetermined"
        or not certification["determination_and_evidence_required_before_operation"]
        or not certification["status_disclosure_required_at_collection"]
    ):
        raise ValueError("certification and state-expertise determinations must remain mandatory")

    transfer = controls["cross_border_transfer"]
    if transfer["status"] != "blocked-pending-article-14-and-actual-transfer-facts":
        raise ValueError("cross-border processing must remain blocked pending Article 14 findings")
    required_article_14_findings = {
        "article_14_2_1_national_security_threat",
        "article_14_2_2_receiving_law_equivalence",
        "article_14_3_consent_or_life_health_exception",
        "article_14_4_security_safeguards",
    }
    article_14_findings = transfer["article_14_findings"]
    if set(article_14_findings) != required_article_14_findings or any(
        finding != "undetermined" for finding in article_14_findings.values()
    ):
        raise ValueError("all four Article 14 findings must be explicit and unresolved")
    if (
        transfer["aws_processing_paths_assessed"]
        or transfer["recipient_mailbox_paths_assessed"]
        or not transfer["gdpr_is_not_itself_an_article_14_equivalence_determination"]
        or not transfer["security_safeguards_evidence_required"]
    ):
        raise ValueError(
            "Article 14 cannot be satisfied by an unsupported provider or GDPR inference"
        )

    required_true_controls = {
        "provider_contract_and_processing_terms_required",
        "purpose_and_field_inventory_before_collection",
        "retention_and_deletion_rules_before_collection",
    }
    if any(not controls[field] for field in required_true_controls):
        raise ValueError("every personal-data activation gate is mandatory")

    notice = controls["collection_notice"]
    if (
        notice["status"] != "required-before-collection"
        or set(notice["required_fields"]) != REQUIRED_NOTICE_FIELDS
    ):
        raise ValueError("the Article 11.2 collection notice fields must remain complete")

    rights = controls["data_subject_rights"]
    if (
        rights["response_deadline_working_days"],
        rights["third_party_consultation_extension_working_days"],
        rights["reasoned_refusal_deadline_working_days"],
        rights["prior_recipient_notification_deadline_working_days"],
    ) != (7, 7, 5, 3):
        raise ValueError("the Article 12 working-day deadlines must remain 7, 7, 5 and 3")
    if set(rights["request_channels"]) != {
        "paper-written-application-with-identity-document",
        "electronic-request-with-enhanced-electronic-signature",
    }:
        raise ValueError("the Article 7.5 rights-request channels must remain complete")
    if (
        not rights["identity_document_minimization_and_secure_handling_required"]
        or not rights["responses_must_exclude_other_persons_personal_data"]
    ):
        raise ValueError("the statutory rights workflow must retain its privacy safeguards")

    security = controls["security"]
    if (
        not security["decision_161_clause_mapping_required"]
        or set(security["required_evidence"]) != REQUIRED_SECURITY_EVIDENCE
    ):
        raise ValueError(
            "the Decision No. 161 clause-mapped security evidence must remain complete"
        )

    minimization = controls["data_minimization_and_incidental_data"]
    if (
        minimization["only_direct_visitor_submission_channel"] != "contact-form"
        or not minimization["security_logs_and_search_queries_are_potential_personal_data"]
        or minimization["raw_search_query_persistence"] != "prohibited"
        or not minimization["query_string_and_secret_redaction_required"]
        or not minimization["access_log_field_minimization_and_fixed_retention_required"]
        or minimization["special_category_data_policy"] != "not-requested-and-prohibited-by-policy"
        or not minimization["free_text_may_receive_special_category_data"]
        or minimization["inadvertent_special_category_response"]
        != "restrict-quarantine-escalate-and-delete"
    ):
        raise ValueError("logging, search-query and inadvertent special-category controls drifted")

    feature_snapshot = jurisdiction["activated_processing_snapshot"]
    for inactive_feature in (
        "analytics",
        "nonessential_cookies",
        "third_party_embeds",
        "orcid_synchronization",
        "crossref_synchronization",
    ):
        if feature_snapshot[inactive_feature] != "inactive":
            raise ValueError(f"{inactive_feature} must remain inactive in this baseline")
    if feature_snapshot["ses_engagement_tracking"] != "inactive":
        raise ValueError("SES engagement tracking must remain inactive")

    if PRODUCT_BASELINE_PATH.exists():
        product_baseline = _read_object(PRODUCT_BASELINE_PATH)
        deployment = product_baseline.get("deployment", {})
        features = product_baseline.get("feature_decisions", {})
        contact = features.get("contact", {})
        search = features.get("search", {})
        privacy = features.get("privacy_and_discovery", {})
        if deployment.get("aws_region") != hosting["region"]:
            raise ValueError("product and governance AWS regions must match")
        if (
            contact.get("state") != "active"
            or contact.get("preferred_public_method") != "contact-form"
            or contact.get("delivery_provider") != "amazon-ses"
            or contact.get("delivery_region") != hosting["region"]
        ):
            raise ValueError("product and governance contact/SES decisions must match")
        if search.get("state") != "active" or search.get("query_analytics") is not False:
            raise ValueError("product search must remain active without query analytics")
        if any(
            privacy.get(field) != "inactive"
            for field in ("analytics", "public_nonessential_cookies")
        ) or not str(privacy.get("third_party_embeds", "")).startswith("inactive-"):
            raise ValueError("product and governance optional tracking decisions must match")

    review = jurisdiction["review"]
    effective_date = _parse_utc(baseline["effective_at"]).date()
    expected_review = effective_date + timedelta(days=review["scheduled_interval_days"])
    next_review = date.fromisoformat(review["next_scheduled_review_on"])
    if next_review != expected_review:
        raise ValueError("jurisdiction review date must equal the approved 90-day cadence")
    if next_review < (as_of or date.today()):
        raise ValueError("jurisdiction review is overdue; the approved baseline must be reviewed")


def _validate_content_governance(baseline: dict[str, Any]) -> None:
    governance = baseline["content_governance"]
    assignments = governance["role_assignments"]
    roles = [assignment["role"] for assignment in assignments]
    _require_unique(roles, "content-governance roles")
    if any(assignment["assignee"] != "Ahmad Abdullayev" for assignment in assignments):
        raise ValueError("no unsupported maintainer may be invented")

    schedules = {
        schedule["id"]: schedule["maximum_interval_days"]
        for schedule in governance["review_schedules"]
    }
    if schedules != REVIEW_SCHEDULES:
        raise ValueError("review schedule IDs and maximum intervals must remain exact")

    trigger_ids = [trigger["id"] for trigger in governance["event_review_triggers"]]
    if trigger_ids != [f"ER-{number:03d}" for number in range(1, 8)]:
        raise ValueError("event-review triggers must be complete, consecutive and ordered")


def _validate_inventory(baseline: dict[str, Any], *, as_of: date | None = None) -> None:
    inventory = baseline["content_inventory"]
    expected_ids = [f"CI-{number:03d}" for number in range(1, 33)]
    if [item["id"] for item in inventory] != expected_ids:
        raise ValueError("content inventory IDs must be complete, consecutive and ordered")
    if [item["migration_order"] for item in inventory] != list(range(1, 33)):
        raise ValueError("content migration order must be consecutive and ordered")
    _require_unique([item["canonical_key"] for item in inventory], "canonical content keys")

    effective_date = _parse_utc(baseline["effective_at"]).date()
    product = _read_object(PRODUCT_BASELINE_PATH)
    for item in inventory:
        schedule_id = item["review_schedule_id"]
        if schedule_id not in REVIEW_SCHEDULES:
            raise ValueError(f"{item['id']} references an unknown review schedule")

        public_state = item["target_state"] in {"approved-public", "temporary-public"}
        approved_reviewed_state = public_state or item["target_state"] == "approved-internal"
        if public_state and (
            item["source_status"] == "not-supplied" or item["rights_status"] == "undetermined"
        ):
            raise ValueError(f"{item['id']} cannot publish unverified or rights-unknown content")
        if approved_reviewed_state:
            if item["last_reviewed_on"] is None or item["review_due_on"] is None:
                raise ValueError(f"{item['id']} approved content requires review dates")
            last_reviewed = date.fromisoformat(item["last_reviewed_on"])
            review_due = date.fromisoformat(item["review_due_on"])
            expected_due = last_reviewed + timedelta(days=REVIEW_SCHEDULES[schedule_id])
            if review_due != expected_due:
                raise ValueError(f"{item['id']} review due date does not match its schedule")
            if last_reviewed > effective_date:
                raise ValueError(f"{item['id']} cannot be reviewed after the effective date")
            if review_due < (as_of or date.today()):
                raise ValueError(
                    f"{item['id']} review is overdue; its configured overdue action must run"
                )

        if (
            item["target_state"] == "approved-public"
            and item["migration_disposition"] != "import-verified"
        ):
            raise ValueError(f"{item['id']} approved public content must use verified import")
        if item["target_state"] == "temporary-public" and item["migration_disposition"] not in {
            "retire-temporary",
            "replace-with-approved",
        }:
            raise ValueError(f"{item['id']} temporary public content needs an exit disposition")
        if item["target_state"] == "omitted-until-approved":
            expected = (
                item["source_status"],
                item["rights_status"],
                item["migration_disposition"],
                item["last_reviewed_on"],
                item["review_due_on"],
            )
            if expected != ("not-supplied", "undetermined", "hold-unpublished", None, None):
                raise ValueError(f"{item['id']} omitted content must remain an evidence-held gap")
        if item["target_state"] == "draft-required":
            if item["migration_disposition"] != "create-after-gates":
                raise ValueError(f"{item['id']} draft content must be created only after its gates")
            if item["last_reviewed_on"] is not None or item["review_due_on"] is not None:
                raise ValueError(f"{item['id']} unapproved draft cannot claim review dates")
        if (
            item["privacy_classification"]
            in {
                "possible-third-party-data",
                "visitor-personal-data-processing",
            }
            and "privacy" not in item["approval_domains"]
        ):
            raise ValueError(f"{item['id']} personal-data content requires privacy approval")

        for reference in item["source_refs"]:
            _validate_inventory_reference(reference, product)


def _validate_migration(baseline: dict[str, Any]) -> None:
    migration = baseline["migration_plan"]
    steps = migration["steps"]
    if [step["id"] for step in steps] != [f"MP-{number:02d}" for number in range(1, 13)]:
        raise ValueError("migration step IDs must be complete, consecutive and ordered")
    if [step["order"] for step in steps] != list(range(1, 13)):
        raise ValueError("migration step order must be consecutive and ordered")
    if not all(
        migration[control]
        for control in (
            "source_freeze_required",
            "dry_run_required",
            "production_import_requires_owner_approval",
            "rollback_to_last_valid_snapshot_required",
        )
    ):
        raise ValueError("all migration safety controls are mandatory")
    if not all(migration["reconciliation"].values()):
        raise ValueError("every migration reconciliation dimension is mandatory")


def _validate_revisions(baseline: dict[str, Any]) -> None:
    revisions = baseline["revision_history"]
    expected_ids = [f"REV-{number:03d}" for number in range(1, len(revisions) + 1)]
    if [revision["id"] for revision in revisions] != expected_ids:
        raise ValueError("formal revision IDs must be complete, consecutive and ordered")
    _require_unique(
        [revision["logical_artifact_id"] for revision in revisions],
        "revision logical artifact IDs",
    )
    first = revisions[0]
    if (
        first["version"] != "62418c3"
        or "62418c3529060b2fdd27af2949cd5169e917a7a4" not in first["restoration_locator"]
    ):
        raise ValueError("REV-001 must identify the existing foundation commit exactly")
    for previous, current in zip(revisions[:-1], revisions[1:], strict=True):
        if current["previous_version"] != previous["version"]:
            raise ValueError(f"{current['id']} must link to the immediately preceding revision")

    initial_scope_revision = revisions[1]
    if (
        initial_scope_revision["version"] != "1.0.0"
        or initial_scope_revision["logical_artifact_id"] != "foundation-items-11-23@1.0.0"
        or initial_scope_revision["restoration_locator"]
        != "config/foundation-scope-manifest.json#bundle_projection_sha256"
    ):
        raise ValueError("REV-002 must identify the initial immutable items 11-23 bundle")

    current = revisions[-1]
    if current["version"] != baseline["baseline_version"]:
        raise ValueError("the current revision version must equal the governance baseline version")
    if current["logical_artifact_id"] != (f"foundation-items-11-23@{baseline['baseline_version']}"):
        raise ValueError("the current revision must use the deterministic scope artifact ID")
    if not current["restoration_locator"].strip():
        raise ValueError("the current revision requires a restoration locator")

    timestamps = [_parse_utc(revision["recorded_at"]) for revision in revisions]
    if timestamps != sorted(timestamps):
        raise ValueError("revision timestamps must be chronological")
    if any(timestamp > datetime.now(UTC) for timestamp in timestamps):
        raise ValueError("revision timestamps cannot be in the future")


def _validate_approvals(baseline: dict[str, Any]) -> None:
    approvals = baseline["approval_records"]
    if len({approval["id"] for approval in approvals}) != len(approvals):
        raise ValueError("approval record IDs must be unique")
    by_domain = {
        domain: [approval for approval in approvals if approval["domain"] == domain]
        for domain in APPROVAL_ROLES
    }
    if any(not records for records in by_domain.values()):
        raise ValueError("all six foundation approval domains require a decision record")
    if sum(len(records) for records in by_domain.values()) != len(approvals):
        raise ValueError("an approval uses an unknown domain")

    stakeholder_ids = {stakeholder["id"] for stakeholder in baseline["stakeholders"]}
    revision_by_version = {
        revision["version"]: revision for revision in baseline["revision_history"]
    }
    for domain, expected_role in APPROVAL_ROLES.items():
        records = by_domain[domain]
        expected_ids = [
            f"APR-{domain.upper()}-{number:03d}" for number in range(1, len(records) + 1)
        ]
        if [approval["id"] for approval in records] != expected_ids:
            raise ValueError(f"{domain} approval IDs must be consecutive and ordered")
        if records[0]["id"] != INITIAL_APPROVAL_IDS[domain] or records[0]["supersedes"] is not None:
            raise ValueError(
                f"{domain} initial approval must be deterministic and supersede nothing"
            )
        for previous, current in zip(records[:-1], records[1:], strict=True):
            if current["supersedes"] != previous["id"]:
                raise ValueError(f"{current['id']} must supersede the prior {domain} decision")

        record_times: list[datetime] = []
        for approval in records:
            if approval["approver_role"] != expected_role:
                raise ValueError(f"{domain} approval role does not match its assigned domain")
            if approval["stakeholder_id"] not in stakeholder_ids:
                raise ValueError(f"{domain} approval references an unknown stakeholder")
            expected_logical_id = f"foundation-items-11-23@{approval['artifact_version']}"
            if approval["logical_artifact_id"] != expected_logical_id:
                raise ValueError(f"{domain} approval references the wrong logical artifact")
            revision = revision_by_version.get(approval["artifact_version"])
            if revision is None:
                raise ValueError(f"{domain} approval references an unknown revision version")
            decided_at = _parse_utc(approval["decided_at"])
            if decided_at < _parse_utc(revision["recorded_at"]):
                raise ValueError(f"{domain} approval predates its referenced revision")
            if decided_at > datetime.now(UTC):
                raise ValueError(f"{domain} approval timestamp cannot be in the future")
            record_times.append(decided_at)
            if "foundation-scope" not in approval["scope_limit"]:
                raise ValueError(f"{domain} approval must remain limited to foundation scope")
        if record_times != sorted(record_times):
            raise ValueError(f"{domain} approval timestamps must be chronological")

        initial = records[0]
        if "owner-directive:2026-07-17-items-11-23" not in initial["evidence_refs"]:
            raise ValueError(f"{domain} approval lacks the explicit owner direction evidence")
        current = records[-1]
        if current["artifact_version"] != baseline["baseline_version"]:
            raise ValueError(f"current {domain} approval references the wrong artifact version")
        if current["result"] != "approved-for-foundation-scope":
            raise ValueError(f"current {domain} decision must approve the foundation baseline")

    effective_at = _parse_utc(baseline["effective_at"])
    current_decision_times = [
        _parse_utc(records[-1]["decided_at"]) for records in by_domain.values()
    ]
    current_revision_time = _parse_utc(baseline["revision_history"][-1]["recorded_at"])
    if effective_at != max([current_revision_time, *current_decision_times]):
        raise ValueError(
            "baseline effective_at must equal its current revision/approval completion instant"
        )


def _validate_document_trace(baseline: dict[str, Any]) -> None:
    missing_documents = [path for path in DOCUMENT_PATHS if not path.is_file()]
    if missing_documents:
        raise ValueError(
            "foundation governance documentation is missing: "
            + ", ".join(path.name for path in missing_documents)
        )
    document_text = "\n".join(path.read_text(encoding="utf-8") for path in DOCUMENT_PATHS)
    required_tokens = [
        *(source["id"] for source in baseline["legal_sources"]),
        *(schedule["id"] for schedule in baseline["content_governance"]["review_schedules"]),
        *(item["id"] for item in baseline["content_inventory"]),
        *(step["id"] for step in baseline["migration_plan"]["steps"]),
        *(revision["id"] for revision in baseline["revision_history"]),
        *(approval["id"] for approval in baseline["approval_records"]),
    ]
    missing_tokens = [token for token in required_tokens if token not in document_text]
    if missing_tokens:
        raise ValueError(
            "foundation governance documents omit machine-baseline IDs: "
            + ", ".join(missing_tokens)
        )


def validate_foundation_governance(baseline: dict[str, Any]) -> None:
    _validate_schema(baseline)
    if _parse_utc(baseline["effective_at"]) > datetime.now(UTC):
        raise ValueError("effective_at cannot be in the future")
    _validate_sources(baseline)
    _validate_stakeholders(baseline)
    _validate_legal_sources(baseline)
    _validate_jurisdiction(baseline)
    _validate_content_governance(baseline)
    _validate_inventory(baseline)
    _validate_migration(baseline)
    _validate_revisions(baseline)
    _validate_approvals(baseline)
    _validate_document_trace(baseline)
    if _canonical_sha256(baseline) != EXPECTED_GOVERNANCE_SHA256:
        raise ValueError("approved governance digest does not match baseline 1.0.0")


def main() -> None:
    baseline = _read_object(BASELINE_PATH)
    validate_foundation_governance(baseline)
    print(
        "foundation governance machine record is internally consistent; production legal, "
        "source-archive, deployment and personal-data release gates remain explicit"
    )


if __name__ == "__main__":
    main()

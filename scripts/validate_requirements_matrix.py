from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
MATRIX_PATH = ROOT / "config" / "requirements-matrix.json"
SCHEMA_PATH = ROOT / "config" / "requirements-matrix.schema.json"
PRODUCT_BASELINE_PATH = ROOT / "config" / "product-baseline.json"

SOURCE_HASHES = {
    "website-srs": "976ba51a785d27d37117655a4a508eb5133edb36e988966ce31e8878a78eb9e7",
    "backend-specification": "1eca221859e9379cadd3d3e192bd35b68a7e0010ae15f8de53e539e1782c31b5",
}

MODULES: tuple[tuple[str, str, int, tuple[str, ...]], ...] = (
    (
        "GOV",
        "Identity and Content Governance",
        8,
        ("Product Owner", "Academic Content Owner"),
    ),
    ("SHELL", "Global Shell and Navigation", 8, ("Frontend Lead", "UX Owner")),
    (
        "HOME",
        "Homepage",
        8,
        ("Product Owner", "Academic Content Owner"),
    ),
    ("ABOUT", "About and Professional Identity", 10, ("Academic Content Owner",)),
    (
        "RES",
        "Research Profile",
        10,
        ("Academic Content Owner", "Research Lead"),
    ),
    (
        "PUB",
        "Publications and Scholarly Outputs",
        42,
        ("Academic Content Owner", "Scholarly Metadata Steward"),
    ),
    (
        "PROJ",
        "Projects, Software, and Research Data",
        14,
        ("Academic Content Owner", "Technical Portfolio Owner"),
    ),
    ("CAREER", "Education, Experience, and Expertise", 14, ("Academic Content Owner",)),
    (
        "ACADEMIC",
        "Teaching, Mentoring, Recognition, Talks, and Service",
        12,
        ("Academic Content Owner",),
    ),
    (
        "CONTENT",
        "News, Public Scholarship, and Media",
        10,
        ("Academic Content Owner", "Communications Owner"),
    ),
    (
        "DOC",
        "Curriculum Vitae and Public Documents",
        8,
        ("Academic Content Owner", "Document Steward"),
    ),
    (
        "CONTACT",
        "Contact and Collaboration",
        12,
        ("Product Owner", "Privacy Owner", "Backend Lead"),
    ),
    (
        "SEARCH",
        "Search and Discovery",
        8,
        ("Frontend Lead", "Content Architecture Owner"),
    ),
    (
        "INT",
        "Scholarly Identity and External Integrations",
        10,
        ("Integration Owner", "Scholarly Metadata Steward"),
    ),
    (
        "SEO",
        "Machine-Readable Metadata and Discoverability",
        14,
        ("Technical SEO Owner", "Content Architecture Owner"),
    ),
    (
        "ACC",
        "Accessibility Functions",
        20,
        ("Accessibility Owner", "Frontend Lead"),
    ),
    (
        "I18N",
        "Internationalization and Multilingual Content",
        6,
        ("Content Localization Owner", "Frontend Lead"),
    ),
    (
        "ADMIN",
        "Content Administration and Editorial Workflow",
        16,
        ("Product Owner", "Technical Administrator"),
    ),
    (
        "SEC",
        "Authentication, Security, and Privacy",
        18,
        ("Security Owner", "Privacy Owner", "Backend Lead"),
    ),
    (
        "OPS",
        "Errors, Operations, Legal, and Data Quality",
        16,
        ("Technical Owner", "Content Owner", "Legal/Privacy Owner"),
    ),
)

EXPECTED_PRIORITY_COUNTS = {
    "P0_MUST": 148,
    "P1_SHOULD": 62,
    "P2_CONDITIONAL": 52,
    "P2_MAY": 2,
}
EXPECTED_BACKEND_CLASS_COUNTS = {
    "Direct backend": 179,
    "Shared contract": 70,
    "Frontend-led": 15,
}
EXPECTED_BACKEND_PAGE_COUNTS = {
    page: count
    for page, count in zip(
        range(38, 64),
        (
            10,
            11,
            11,
            11,
            10,
            11,
            10,
            11,
            10,
            11,
            11,
            11,
            10,
            11,
            11,
            11,
            11,
            10,
            9,
            9,
            9,
            10,
            10,
            11,
            11,
            3,
        ),
        strict=True,
    )
}

# These digests are intentionally independent of the values repeated in the JSON
# integrity block. They pin the reviewed PDF extraction and project decisions.
EXPECTED_SOURCE_LEDGER_SHA256 = "505e956ebbd194265668aa2e74d9b0856d2a14c73939ac1a7ff0c362fe824a81"
EXPECTED_DECISION_LEDGER_SHA256 = "a17de332330a6f1e379381eed3b30ad4f1e59f4e8ded324d0f38aaf9f6c2a1cc"
EXPECTED_MATRIX_SHA256 = "022d75908f45f31c5ebf07bd65705aecaee072206a8f4775209fe6e2bd492e6a"


def _read_object(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as input_file:
        value: object = json.load(input_file)
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def _validate_schema(matrix: dict[str, Any]) -> None:
    schema = _read_object(SCHEMA_PATH)
    if schema.get("$id") != ("https://ahmadabdullayev.com/schemas/requirements-matrix.schema.json"):
        raise ValueError("requirements schema ID must use the selected primary domain")
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(matrix), key=lambda error: list(error.absolute_path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        raise ValueError(f"requirements matrix schema error at {location}: {error.message}")


def _digest(value: object) -> str:
    canonical = json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    return hashlib.sha256(canonical.encode()).hexdigest()


def _source_projection(matrix: dict[str, Any]) -> dict[str, Any]:
    rows = []
    for row in matrix["requirements"]:
        rows.append(
            {
                "ordinal": row["ordinal"],
                "id": row["id"],
                "module": row["module"],
                "title": row["title"],
                "priority": row["priority"],
                "baseline_status": row["baseline_status"],
                "normative_requirement": row["normative_requirement"],
                "source": row["source"],
                "dependencies": {
                    "profile_id": row["dependencies"]["profile_id"],
                    "activation_approval_precondition": row["dependencies"][
                        "activation_approval_precondition"
                    ],
                },
                "accountable_roles": row["ownership"]["accountable_roles"],
            }
        )
    return {
        "source_documents": matrix["source_documents"],
        "dependency_profiles": matrix["dependency_profiles"],
        "requirements": rows,
    }


def _decision_projection(matrix: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "id": row["id"],
            "applicability": row["applicability"],
            "requirement_ids": row["dependencies"]["requirement_ids"],
            "assigned_person": row["ownership"]["assigned_person"],
            "assignment_ref": row["ownership"]["assignment_ref"],
        }
        for row in matrix["requirements"]
    ]


def _validate_sources(matrix: dict[str, Any]) -> None:
    documents = {document["id"]: document for document in matrix["source_documents"]}
    if set(documents) != set(SOURCE_HASHES):
        raise ValueError("both reviewed source documents must appear exactly once")
    for source_id, expected_hash in SOURCE_HASHES.items():
        if documents[source_id]["sha256"] != expected_hash:
            raise ValueError(f"{source_id} SHA-256 does not match the reviewed PDF")
    if documents["website-srs"]["pdf_page_count"] != 324:
        raise ValueError("the reviewed website SRS must retain its 324-page PDF identity")
    if documents["backend-specification"]["pdf_page_count"] != 65:
        raise ValueError("the reviewed backend specification must retain its 65-page PDF identity")


def _validate_product_baseline_alignment(matrix: dict[str, Any]) -> None:
    baseline = _read_object(PRODUCT_BASELINE_PATH)
    if matrix["baseline_version"] != baseline["baseline_version"]:
        raise ValueError("matrix and product-baseline versions must match")
    if matrix["effective_date"] != baseline["effective_date"]:
        raise ValueError("matrix and product-baseline effective dates must match")

    baseline_sources = {document["id"]: document for document in baseline["source_documents"]}
    matrix_sources = {document["id"]: document for document in matrix["source_documents"]}
    for source_id in SOURCE_HASHES:
        if matrix_sources[source_id]["sha256"] != baseline_sources[source_id]["sha256"]:
            raise ValueError(f"{source_id} identity differs from the product baseline")

    owner = baseline["owner"]["full_name"]
    if any(row["ownership"]["assigned_person"] != owner for row in matrix["requirements"]):
        raise ValueError("matrix assignees differ from the named product-baseline owner")
    if baseline["approval_policy"]["applicable_p0_waiver_allowed"]:
        raise ValueError("product baseline cannot waive applicable P0 requirements")

    decisions = {decision["id"]: decision for decision in baseline["conditional_requirements"]}
    p2_rows = [row for row in matrix["requirements"] if row["priority"]["level"] == "P2"]
    if set(decisions) != {row["id"] for row in p2_rows}:
        raise ValueError("product-baseline decisions must cover exactly the 54 P2 rows")
    for row in p2_rows:
        decision = decisions[row["id"]]
        expected_priority = f"{row['priority']['level']}-{row['priority']['obligation']}"
        expected_state = "applicable" if decision["state"] == "active" else "not_applicable"
        expected_basis = (
            "activated-capability" if decision["state"] == "active" else "dormant-capability"
        )
        applicability = row["applicability"]
        if (
            decision["title"] != row["title"]
            or decision["priority"] != expected_priority
            or applicability["state"] != expected_state
            or applicability["basis"] != expected_basis
            or applicability["condition"] != decision["activation_condition"]
            or applicability["rationale"] != decision["rationale"]
            or decision["source_ref"] not in applicability["decision_refs"]
        ):
            raise ValueError(f"{row['id']} differs from its product-baseline scope decision")


def _validate_catalogue(matrix: dict[str, Any]) -> None:
    rows = matrix["requirements"]
    expected_ids: list[str] = []
    expected_modules: dict[str, str] = {}
    expected_roles: dict[str, tuple[str, ...]] = {}
    expected_profiles: dict[str, str] = {}
    for prefix, module, count, roles in MODULES:
        profile_id = f"DEP-{prefix}"
        for number in range(1, count + 1):
            requirement_id = f"FR-{prefix}-{number:02d}"
            expected_ids.append(requirement_id)
            expected_modules[requirement_id] = module
            expected_roles[requirement_id] = roles
            expected_profiles[requirement_id] = profile_id

    ids = [row["id"] for row in rows]
    if ids != expected_ids:
        raise ValueError("requirement IDs must be complete and in canonical SRS catalogue order")
    if [row["ordinal"] for row in rows] != list(range(1, 265)):
        raise ValueError("requirement ordinals must be consecutive from 1 through 264")
    if len({row["title"] for row in rows}) != 264:
        raise ValueError("requirement titles must be unique")

    for row in rows:
        requirement_id = row["id"]
        if row["module"] != expected_modules[requirement_id]:
            raise ValueError(f"{requirement_id} is assigned to the wrong SRS module")
        if tuple(row["ownership"]["accountable_roles"]) != expected_roles[requirement_id]:
            raise ValueError(f"{requirement_id} does not preserve the SRS accountable roles")
        if row["ownership"]["assigned_person"] != "Ahmad Abdullayev":
            raise ValueError(f"{requirement_id} has an unsupported project assignee")
        if row["dependencies"]["profile_id"] != expected_profiles[requirement_id]:
            raise ValueError(f"{requirement_id} uses the wrong SRS precondition profile")
        expected_activation = (
            f'The scope decision activating "{row["title"]}" has been approved when the '
            "requirement is conditional."
        )
        if row["dependencies"]["activation_approval_precondition"] != expected_activation:
            raise ValueError(f"{requirement_id} activation precondition was not preserved exactly")


def _validate_priorities_and_applicability(matrix: dict[str, Any]) -> None:
    rows = matrix["requirements"]
    priority_keys = [f"{row['priority']['level']}_{row['priority']['obligation']}" for row in rows]
    priority_counts = dict(Counter(priority_keys))
    if priority_counts != EXPECTED_PRIORITY_COUNTS:
        raise ValueError("priority counts do not match the 264-card SRS catalogue")

    status_by_priority = {
        "P0_MUST": "Baselined - mandatory for the applicable release",
        "P1_SHOULD": (
            "Baselined - planned after mandatory scope or with the same release "
            "when capacity permits"
        ),
        "P2_CONDITIONAL": "Conditional - dormant until the activating feature or content exists",
        "P2_MAY": "Optional - approved extension candidate",
    }
    for row, priority_key in zip(rows, priority_keys, strict=True):
        if row["baseline_status"] != status_by_priority[priority_key]:
            raise ValueError(f"{row['id']} baseline status does not match its SRS priority")
        applicability = row["applicability"]
        if priority_key == "P0_MUST":
            if (
                applicability["state"] != "applicable"
                or applicability["basis"] != "srs-priority-model"
            ):
                raise ValueError(f"{row['id']} P0 applicability contradicts the release baseline")
        elif priority_key == "P1_SHOULD":
            if (
                applicability["state"] != "applicable"
                or applicability["basis"] != "full-build-profile"
            ):
                raise ValueError(f"{row['id']} P1 applicability contradicts the full-build profile")
        elif applicability["state"] == "applicable":
            if applicability["basis"] != "activated-capability":
                raise ValueError(f"{row['id']} active P2 requirement lacks an activation decision")
        elif applicability["basis"] != "dormant-capability":
            raise ValueError(f"{row['id']} dormant P2 requirement lacks a dormant decision")


def _validate_dependencies(matrix: dict[str, Any]) -> None:
    rows = matrix["requirements"]
    identifiers = {row["id"] for row in rows}
    profiles = {profile["id"]: profile for profile in matrix["dependency_profiles"]}
    if len(profiles) != 20:
        raise ValueError("the matrix must contain one unique SRS precondition profile per module")
    expected_profile_ids = {f"DEP-{prefix}" for prefix, *_ in MODULES}
    if set(profiles) != expected_profile_ids:
        raise ValueError("dependency profile identifiers do not match the twenty SRS modules")
    for prefix, module, _, _ in MODULES:
        if profiles[f"DEP-{prefix}"]["module"] != module:
            raise ValueError(f"DEP-{prefix} is assigned to the wrong module")

    edge_count = 0
    for row in rows:
        dependencies = row["dependencies"]["requirement_ids"]
        if row["id"] in dependencies:
            raise ValueError(f"{row['id']} cannot depend on itself")
        unknown = set(dependencies) - identifiers
        if unknown:
            raise ValueError(f"{row['id']} references unknown requirement dependencies")
        edge_count += len(dependencies)

    # Neither reviewed PDF declares cross-card dependencies by requirement ID.
    # Preconditions are retained through the source profiles; inferred edges are forbidden.
    if edge_count != 0:
        raise ValueError("unreferenced inter-requirement dependency edges are prohibited")
    if matrix["integrity"]["explicit_requirement_dependency_edge_count"] != edge_count:
        raise ValueError("dependency edge count does not match the matrix rows")


def _validate_trace_pages(matrix: dict[str, Any]) -> None:
    rows = matrix["requirements"]
    backend_page_counts = Counter(row["source"]["backend_trace_page"] for row in rows)
    if dict(backend_page_counts) != EXPECTED_BACKEND_PAGE_COUNTS:
        raise ValueError("backend Appendix A row-to-page mapping is incomplete or reordered")
    backend_class_counts = Counter(row["source"]["backend_class"] for row in rows)
    if dict(backend_class_counts) != EXPECTED_BACKEND_CLASS_COUNTS:
        raise ValueError("backend responsibility-class counts do not match Appendix A")
    differences = sum(
        row["source"]["srs_card_start_page"] != row["source"]["srs_toc_page"] for row in rows
    )
    if differences != 31:
        raise ValueError(
            "the 31 printed-page differences between card headings and TOC were not preserved"
        )
    if matrix["integrity"]["srs_toc_card_page_difference_count"] != differences:
        raise ValueError("printed-page difference count does not match the rows")


def _validate_integrity(matrix: dict[str, Any]) -> None:
    rows = matrix["requirements"]
    integrity = matrix["integrity"]
    applicability_counts = dict(Counter(row["applicability"]["state"] for row in rows))
    if integrity["applicability_counts"] != applicability_counts:
        raise ValueError("applicability counts do not match the matrix rows")
    if integrity["priority_counts"] != EXPECTED_PRIORITY_COUNTS:
        raise ValueError("integrity priority counts do not match the SRS")

    source_digest = _digest(_source_projection(matrix))
    decision_digest = _digest(_decision_projection(matrix))
    if integrity["source_ledger_sha256"] != source_digest:
        raise ValueError("recorded source ledger digest does not match the rows")
    if integrity["decision_ledger_sha256"] != decision_digest:
        raise ValueError("recorded decision ledger digest does not match the rows")
    if source_digest != EXPECTED_SOURCE_LEDGER_SHA256:
        raise ValueError("source ledger differs from the independently pinned PDF extraction")
    if decision_digest != EXPECTED_DECISION_LEDGER_SHA256:
        raise ValueError(
            "decision ledger differs from the independently pinned foundation decisions"
        )
    if _digest(matrix) != EXPECTED_MATRIX_SHA256:
        raise ValueError("complete requirement matrix differs from the approved 2.0.0 baseline")


def validate_requirements_matrix(matrix: dict[str, Any]) -> None:
    _validate_schema(matrix)
    _validate_sources(matrix)
    _validate_product_baseline_alignment(matrix)
    _validate_catalogue(matrix)
    _validate_priorities_and_applicability(matrix)
    _validate_dependencies(matrix)
    _validate_trace_pages(matrix)
    _validate_integrity(matrix)


def main() -> None:
    matrix = _read_object(MATRIX_PATH)
    validate_requirements_matrix(matrix)
    counts = matrix["integrity"]["applicability_counts"]
    print(
        "requirements matrix valid: 264 rows, 20 modules, "
        f"{counts['applicable']} applicable, {counts['not_applicable']} not applicable, "
        "0 invented dependency edges"
    )


if __name__ == "__main__":
    main()

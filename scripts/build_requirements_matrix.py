from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_BASELINE = ROOT / "config" / "product-baseline.json"
DEFAULT_OUTPUT = ROOT / "config" / "requirements-matrix.json"

PDFTOTEXT_MINIMUM_VERSION = (24, 2, 0)
PDFTOTEXT_MINIMUM_VERSION_LABEL = "24.02.0"
PDFTOTEXT_INSTALL_GUIDANCE = (
    "Install Poppler (Debian/Ubuntu: `sudo apt install poppler-utils`; "
    "macOS/Homebrew: `brew install poppler`), verify with `pdftotext -v`, and rerun "
    "the matrix builder."
)

SOURCE_HASHES = {
    "website-srs": "976ba51a785d27d37117655a4a508eb5133edb36e988966ce31e8878a78eb9e7",
    "backend-specification": "1eca221859e9379cadd3d3e192bd35b68a7e0010ae15f8de53e539e1782c31b5",
}

MODULES: tuple[
    tuple[str, str, int, tuple[str, ...], int],
    ...,
] = (
    (
        "GOV",
        "Identity and Content Governance",
        8,
        ("Product Owner", "Academic Content Owner"),
        15,
    ),
    ("SHELL", "Global Shell and Navigation", 8, ("Frontend Lead", "UX Owner"), 24),
    (
        "HOME",
        "Homepage",
        8,
        ("Product Owner", "Academic Content Owner"),
        33,
    ),
    ("ABOUT", "About and Professional Identity", 10, ("Academic Content Owner",), 42),
    (
        "RES",
        "Research Profile",
        10,
        ("Academic Content Owner", "Research Lead"),
        53,
    ),
    (
        "PUB",
        "Publications and Scholarly Outputs",
        42,
        ("Academic Content Owner", "Scholarly Metadata Steward"),
        64,
    ),
    (
        "PROJ",
        "Projects, Software, and Research Data",
        14,
        ("Academic Content Owner", "Technical Portfolio Owner"),
        112,
    ),
    (
        "CAREER",
        "Education, Experience, and Expertise",
        14,
        ("Academic Content Owner",),
        127,
    ),
    (
        "ACADEMIC",
        "Teaching, Mentoring, Recognition, Talks, and Service",
        12,
        ("Academic Content Owner",),
        143,
    ),
    (
        "CONTENT",
        "News, Public Scholarship, and Media",
        10,
        ("Academic Content Owner", "Communications Owner"),
        156,
    ),
    (
        "DOC",
        "Curriculum Vitae and Public Documents",
        8,
        ("Academic Content Owner", "Document Steward"),
        167,
    ),
    (
        "CONTACT",
        "Contact and Collaboration",
        12,
        ("Product Owner", "Privacy Owner", "Backend Lead"),
        175,
    ),
    (
        "SEARCH",
        "Search and Discovery",
        8,
        ("Frontend Lead", "Content Architecture Owner"),
        189,
    ),
    (
        "INT",
        "Scholarly Identity and External Integrations",
        10,
        ("Integration Owner", "Scholarly Metadata Steward"),
        198,
    ),
    (
        "SEO",
        "Machine-Readable Metadata and Discoverability",
        14,
        ("Technical SEO Owner", "Content Architecture Owner"),
        209,
    ),
    (
        "ACC",
        "Accessibility Functions",
        20,
        ("Accessibility Owner", "Frontend Lead"),
        225,
    ),
    (
        "I18N",
        "Internationalization and Multilingual Content",
        6,
        ("Content Localization Owner", "Frontend Lead"),
        247,
    ),
    (
        "ADMIN",
        "Content Administration and Editorial Workflow",
        16,
        ("Product Owner", "Technical Administrator"),
        253,
    ),
    (
        "SEC",
        "Authentication, Security, and Privacy",
        18,
        ("Security Owner", "Privacy Owner", "Backend Lead"),
        271,
    ),
    (
        "OPS",
        "Errors, Operations, Legal, and Data Quality",
        16,
        ("Technical Owner", "Content Owner", "Legal/Privacy Owner"),
        292,
    ),
)

CARD_PATTERN = re.compile(r"^[ \t]*(FR-[A-Z0-9]+-[0-9]{2}) - (.+?)[ \t]*$", re.MULTILINE)
REQUIREMENT_ID_PATTERN = re.compile(r"FR-[A-Z0-9]+-[0-9]{2}")
PRIORITY_PATTERN = re.compile(r"P[012] - (?:MUST|SHOULD|MAY|CONDITIONAL)")
ACTIVATION_TEMPLATE = (
    'The scope decision activating "{title}" has been approved when the requirement is conditional.'
)
STATUS_BY_PRIORITY = {
    "P0 - MUST": "Baselined - mandatory for the applicable release",
    "P1 - SHOULD": (
        "Baselined - planned after mandatory scope or with the same release when capacity permits"
    ),
    "P2 - CONDITIONAL": "Conditional - dormant until the activating feature or content exists",
    "P2 - MAY": "Optional - approved extension candidate",
}


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract the versioned 264-row matrix from the reviewed PDF pair."
    )
    parser.add_argument("--srs-pdf", type=Path, required=True)
    parser.add_argument("--backend-pdf", type=Path, required=True)
    parser.add_argument("--baseline", type=Path, default=DEFAULT_BASELINE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    return parser.parse_args()


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source_file:
        for chunk in iter(lambda: source_file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _pdftotext_diagnostic(completed: subprocess.CompletedProcess[str]) -> str:
    output = " ".join(f"{completed.stdout}\n{completed.stderr}".split())
    return output[:500] if output else "no version output"


def _preflight_pdftotext() -> str:
    executable = shutil.which("pdftotext")
    if executable is None:
        raise RuntimeError(
            "Matrix regeneration requires Poppler pdftotext "
            f">= {PDFTOTEXT_MINIMUM_VERSION_LABEL}, but `pdftotext` was not found on PATH. "
            f"{PDFTOTEXT_INSTALL_GUIDANCE}"
        )

    try:
        completed = subprocess.run(
            [executable, "-v"],
            check=False,
            capture_output=True,
            text=True,
        )
    except OSError as error:
        raise RuntimeError(
            f"Matrix regeneration found `pdftotext` at {executable}, but could not execute it: "
            f"{error}. {PDFTOTEXT_INSTALL_GUIDANCE}"
        ) from error

    diagnostic = _pdftotext_diagnostic(completed)
    if completed.returncode != 0:
        raise RuntimeError(
            f"Matrix regeneration could not verify `pdftotext` at {executable}: "
            f"`pdftotext -v` exited {completed.returncode} ({diagnostic}). "
            f"{PDFTOTEXT_INSTALL_GUIDANCE}"
        )

    match = re.search(r"\bpdftotext version (\d+(?:\.\d+){1,3})\b", diagnostic, re.IGNORECASE)
    if match is None:
        raise RuntimeError(
            f"Matrix regeneration could not parse the Poppler version reported by "
            f"`{executable} -v` ({diagnostic}). Required version: "
            f">= {PDFTOTEXT_MINIMUM_VERSION_LABEL}. {PDFTOTEXT_INSTALL_GUIDANCE}"
        )

    version_label = match.group(1)
    version = tuple(int(component) for component in version_label.split("."))
    comparable_version = version + (0,) * (len(PDFTOTEXT_MINIMUM_VERSION) - len(version))
    if comparable_version < PDFTOTEXT_MINIMUM_VERSION:
        raise RuntimeError(
            f"Matrix regeneration found Poppler pdftotext {version_label} at {executable}, "
            f"but requires >= {PDFTOTEXT_MINIMUM_VERSION_LABEL} for the reviewed extraction "
            f"behavior. {PDFTOTEXT_INSTALL_GUIDANCE}"
        )
    return executable


def _pdf_text(path: Path, temporary_directory: Path, pdftotext_executable: str) -> str:
    output = temporary_directory / f"{path.stem}.txt"
    subprocess.run(
        [pdftotext_executable, "-layout", str(path), str(output)],
        check=True,
        capture_output=True,
        text=True,
    )
    return output.read_text(encoding="utf-8")


def _read_object(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as source_file:
        value: object = json.load(source_file)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _normalize(value: str) -> str:
    return " ".join(value.replace("\f", " ").split())


def _clean_srs_page(page: str) -> str:
    lines = []
    for line in page.splitlines():
        stripped = line.strip()
        if (
            stripped.startswith("Personal Academic Professional Website SRS")
            and "Functional Requirements Baseline" in stripped
        ):
            continue
        if re.fullmatch(r"[0-9]+(?: of 316)?", stripped):
            continue
        lines.append(line)
    return "\n".join(lines)


def _bullets(value: str) -> list[str]:
    results: list[str] = []
    for line in value.splitlines():
        stripped = line.strip()
        if not stripped or stripped == "\f":
            continue
        if stripped.startswith("• "):
            results.append(stripped[2:])
        elif results:
            results[-1] += f" {stripped}"
        else:
            raise ValueError(f"precondition continuation has no bullet: {stripped}")
    return [_normalize(result) for result in results]


def _owner_label(roles: tuple[str, ...]) -> str:
    if len(roles) == 1:
        return roles[0]
    if len(roles) == 2:
        return f"{roles[0]} and {roles[1]}"
    return f"{', '.join(roles[:-1])}, and {roles[-1]}"


def _extract_toc_pages(srs_pages: list[str]) -> dict[str, int]:
    contents = "\n".join(srs_pages[1:7])
    matches = re.finditer(
        r"^[ \t]*(FR-[A-Z0-9]+-[0-9]{2}) - .*?[ \t]+([0-9]+)[ \t]*$",
        contents,
        re.MULTILINE,
    )
    result = {match.group(1): int(match.group(2)) for match in matches}
    if len(result) != 264:
        raise ValueError(f"expected 264 SRS TOC rows, found {len(result)}")
    return result


def _module_lookup() -> dict[str, tuple[str, int, tuple[str, ...], int]]:
    return {prefix: (module, count, roles, page) for prefix, module, count, roles, page in MODULES}


def _extract_srs_rows(srs_text: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    srs_pages = srs_text.split("\f")
    if len(srs_pages) - 1 != 324:
        raise ValueError(f"expected 324 SRS PDF pages, found {len(srs_pages) - 1}")
    toc_pages = _extract_toc_pages(srs_pages)

    # Physical PDF page 23 is printed functional page 15. Printed page 311 is
    # retained so the final requirement block has a deterministic boundary.
    detailed_pages = srs_pages[22:319]
    cleaned_pages = [_clean_srs_page(page) for page in detailed_pages]
    card_start_pages: dict[str, int] = {}
    for printed_page, page in enumerate(cleaned_pages, 15):
        for match in CARD_PATTERN.finditer(page):
            card_start_pages[match.group(1)] = printed_page

    detailed_text = "\n\f\n".join(cleaned_pages)
    matches = list(CARD_PATTERN.finditer(detailed_text))
    if len(matches) != 264 or len(card_start_pages) != 264:
        raise ValueError("the detailed SRS catalogue must contain 264 unique cards")

    modules = _module_lookup()
    rows: list[dict[str, Any]] = []
    profile_preconditions: dict[str, tuple[str, ...]] = {}
    for index, match in enumerate(matches):
        requirement_id, title = match.groups()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(detailed_text)
        block = detailed_text[match.start() : end]
        definition_index = block.find("Definition")
        if definition_index < 0:
            raise ValueError(f"{requirement_id} has no Definition field")
        priority_match = PRIORITY_PATTERN.search(block[:definition_index])
        normative_match = re.search(
            r"Normative requirement:\s*(.*?)\s*This\s+requirement\s+belongs",
            block,
            re.DOTALL,
        )
        preconditions_match = re.search(
            r"\nPreconditions\s*\n(.*?)\nMain process\s*\n",
            block,
            re.DOTALL,
        )
        if not priority_match or not normative_match or not preconditions_match:
            raise ValueError(f"{requirement_id} is missing an extracted card field")

        prefix = requirement_id.split("-")[1]
        module, _, roles, _ = modules[prefix]
        header_lines = [line.strip() for line in block[:definition_index].splitlines()]
        try:
            owner_marker = len(header_lines) - 1 - header_lines[::-1].index("Owner")
        except ValueError as error:
            raise ValueError(f"{requirement_id} has no Owner field") from error
        owner_value = next(
            (line for line in reversed(header_lines[:owner_marker]) if line),
            "",
        )
        if owner_value != _owner_label(roles):
            raise ValueError(f"{requirement_id} owner differs from the reviewed module assignment")
        preconditions = _bullets(preconditions_match.group(1))
        expected_activation = ACTIVATION_TEMPLATE.format(title=title)
        if preconditions[-1] != expected_activation:
            raise ValueError(f"{requirement_id} activation precondition changed")
        shared_preconditions = tuple(preconditions[:-1])
        previous = profile_preconditions.setdefault(prefix, shared_preconditions)
        if previous != shared_preconditions:
            raise ValueError(f"{requirement_id} does not match its module preconditions")

        priority = priority_match.group(0)
        level, obligation = priority.replace(" - ", "|").split("|")
        explicit_dependencies = sorted(
            set(REQUIREMENT_ID_PATTERN.findall(block)) - {requirement_id}
        )
        rows.append(
            {
                "ordinal": index + 1,
                "id": requirement_id,
                "module": module,
                "title": title,
                "priority": {"level": level, "obligation": obligation},
                "baseline_status": STATUS_BY_PRIORITY[priority],
                "normative_requirement": _normalize(normative_match.group(1)),
                "source": {
                    "srs_card_start_page": card_start_pages[requirement_id],
                    "srs_toc_page": toc_pages[requirement_id],
                },
                "dependencies": {
                    "profile_id": f"DEP-{prefix}",
                    "activation_approval_precondition": expected_activation,
                    "requirement_ids": explicit_dependencies,
                },
                "ownership": {
                    "accountable_roles": list(roles),
                },
            }
        )

    profiles = []
    row_by_id = {row["id"]: row for row in rows}
    for prefix, module, count, _, _ in MODULES:
        first_id = f"FR-{prefix}-01"
        last_id = f"FR-{prefix}-{count:02d}"
        profiles.append(
            {
                "id": f"DEP-{prefix}",
                "module": module,
                "source_preconditions": list(profile_preconditions[prefix]),
                "source_refs": [
                    f"website-srs:{first_id}:p{row_by_id[first_id]['source']['srs_card_start_page']}",
                    f"website-srs:{last_id}:p{row_by_id[last_id]['source']['srs_card_start_page']}",
                ],
            }
        )
    return rows, profiles


def _add_backend_trace(rows: list[dict[str, Any]], backend_text: str) -> None:
    backend_pages = backend_text.split("\f")
    if len(backend_pages) - 1 != 65:
        raise ValueError(f"expected 65 backend PDF pages, found {len(backend_pages) - 1}")
    trace_rows: list[tuple[int, str, str, str]] = []
    for printed_page in range(38, 64):
        lines = backend_pages[printed_page].splitlines()
        for line_index, line in enumerate(lines):
            priority_match = re.search(r"^.{0,25}(P[012])\s+-", line)
            if not priority_match:
                continue
            identifier_token = re.match(r"^\s*(FR-(?:[A-Z0-9]+-)?(?:[0-9]{2})?)\s+", line)
            requirement_id = identifier_token.group(1) if identifier_token else ""
            for continuation_line in lines[line_index + 1 : line_index + 13]:
                if re.fullmatch(r"FR-[A-Z0-9]+-[0-9]{2}", requirement_id):
                    break
                continuation = re.match(r"^([A-Z0-9]+-|[0-9]{2})\s+", continuation_line)
                if not continuation:
                    continue
                fragment = continuation.group(1)
                if fragment == "FR-":
                    break
                requirement_id += fragment
            if not re.fullmatch(r"FR-[A-Z0-9]+-[0-9]{2}", requirement_id):
                raise ValueError(f"backend trace row on p{printed_page} has no requirement ID")
            class_match = re.search(r"\b(Direct backend|Shared contract|Frontend-led)\b", line)
            if not class_match:
                raise ValueError(f"backend trace row on p{printed_page} has no class")
            trace_rows.append(
                (
                    printed_page,
                    requirement_id,
                    priority_match.group(1),
                    class_match.group(1),
                )
            )
    if len(trace_rows) != 264:
        raise ValueError(f"expected 264 backend Appendix A rows, found {len(trace_rows)}")

    for row, (printed_page, requirement_id, priority_level, backend_class) in zip(
        rows, trace_rows, strict=True
    ):
        if row["id"] != requirement_id:
            raise ValueError(
                f"backend Appendix A order differs at {row['id']}: found {requirement_id}"
            )
        if row["priority"]["level"] != priority_level:
            raise ValueError(f"{row['id']} priority differs between the two PDFs")
        row["source"].update(
            {
                "backend_trace_page": printed_page,
                "backend_class": backend_class,
            }
        )


def _add_project_decisions(rows: list[dict[str, Any]], baseline: dict[str, Any]) -> None:
    decisions = {decision["id"]: decision for decision in baseline["conditional_requirements"]}
    owner = baseline["owner"]["full_name"]
    for row in rows:
        priority = row["priority"]
        if priority["level"] == "P0":
            applicability = {
                "state": "applicable",
                "basis": "srs-priority-model",
                "condition": "The owner-directed website release is applicable.",
                "rationale": (
                    "The SRS makes P0 nonconformance acceptance-blocking for the "
                    "applicable release, "
                    "and the project policy permits no applicable-P0 waiver."
                ),
                "decision_refs": [
                    "website-srs:p1",
                    "config/product-baseline.json#approval_policy",
                ],
            }
        elif priority["level"] == "P1":
            applicability = {
                "state": "applicable",
                "basis": "full-build-profile",
                "condition": (
                    "The owner-directed full-build profile retains planned P1 requirements."
                ),
                "rationale": (
                    "The backend activation profile includes P1 requirements in the planned "
                    "full build; "
                    "no row-specific deferral was approved."
                ),
                "decision_refs": [
                    "website-srs:p1",
                    "backend-specification:p4",
                ],
            }
        else:
            decision = decisions.get(row["id"])
            if not decision:
                raise ValueError(f"{row['id']} has no conditional-requirement decision")
            expected_priority = f"{priority['level']}-{priority['obligation']}"
            if (
                decision["title"] != row["title"]
                or decision["priority"] != expected_priority
                or decision["source_ref"]
                != f"website-srs:{row['id']}:p{row['source']['srs_card_start_page']}"
            ):
                raise ValueError(f"{row['id']} scope decision does not match the SRS extraction")
            active = decision["state"] == "active"
            if not active and decision["state"] != "inactive":
                raise ValueError(f"{row['id']} scope decision is not binary")
            applicability = {
                "state": "applicable" if active else "not_applicable",
                "basis": "activated-capability" if active else "dormant-capability",
                "condition": decision["activation_condition"],
                "rationale": decision["rationale"],
                "decision_refs": [
                    decision["source_ref"],
                    f"config/product-baseline.json#conditional_requirements/{row['id']}",
                ],
            }
        row["applicability"] = applicability
        row["ownership"].update(
            {
                "assigned_person": owner,
                "assignment_ref": "config/product-baseline.json#owner",
            }
        )

    if set(decisions) != {row["id"] for row in rows if row["priority"]["level"] == "P2"}:
        raise ValueError("conditional-requirement decisions do not match the 54 SRS P2 rows")


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


def _build_matrix(
    srs_text: str,
    backend_text: str,
    baseline: dict[str, Any],
) -> dict[str, Any]:
    rows, profiles = _extract_srs_rows(srs_text)
    _add_backend_trace(rows, backend_text)
    _add_project_decisions(rows, baseline)
    priority_counts = Counter(
        f"{row['priority']['level']}_{row['priority']['obligation']}" for row in rows
    )
    applicability_counts = Counter(row["applicability"]["state"] for row in rows)
    differences = sum(
        row["source"]["srs_card_start_page"] != row["source"]["srs_toc_page"] for row in rows
    )
    matrix: dict[str, Any] = {
        "$schema": "./requirements-matrix.schema.json",
        "schema_version": "1.0.0",
        "baseline_version": baseline["baseline_version"],
        "effective_date": baseline["effective_date"],
        "source_documents": [
            {
                "id": "website-srs",
                "filename": "personal_academic_professional_website_srs.pdf",
                "sha256": SOURCE_HASHES["website-srs"],
                "pdf_page_count": 324,
                "printed_page_reference": (
                    "Functional pages 1-316; each row records both the detailed-card heading "
                    "page and the table-of-contents target page."
                ),
                "matrix_role": (
                    "Authoritative IDs, titles, modules, priority, status, normative statements, "
                    "preconditions, and accountable roles."
                ),
            },
            {
                "id": "backend-specification",
                "filename": "personal_academic_website_backend_specification.pdf",
                "sha256": SOURCE_HASHES["backend-specification"],
                "pdf_page_count": 65,
                "printed_page_reference": "Appendix A requirement rows on printed pages 38-63.",
                "matrix_role": (
                    "Backend responsibility class and independent 264-row "
                    "order/priority cross-check."
                ),
            },
        ],
        "page_reference_policy": {
            "model": (
                "Printed page numbers shown inside each reviewed PDF, never viewer page indices."
            ),
            "srs_card_start_page": (
                "Printed page that physically contains the detailed requirement-card heading."
            ),
            "srs_toc_page": (
                "Printed target shown in the SRS table of contents; retained separately because 31 "
                "targets differ by one page from the physical card heading."
            ),
            "backend_trace_page": (
                "Printed Appendix A page containing the corresponding backend trace row."
            ),
        },
        "dependency_policy": {
            "source_rule": (
                "Each row retains its SRS module preconditions plus its title-specific "
                "activation-approval "
                "precondition. The PDFs name no cross-card dependency by requirement ID."
            ),
            "explicit_requirement_ids_only": True,
            "unreferenced_edges_prohibited": True,
            "activation_precondition_template": ACTIVATION_TEMPLATE,
        },
        "dependency_profiles": profiles,
        "requirements": rows,
        "integrity": {
            "row_count": 264,
            "module_count": 20,
            "dependency_profile_count": 20,
            "explicit_requirement_dependency_edge_count": 0,
            "priority_counts": dict(priority_counts),
            "applicability_counts": dict(applicability_counts),
            "srs_toc_card_page_difference_count": differences,
            "source_ledger_sha256": "",
            "decision_ledger_sha256": "",
        },
    }
    matrix["integrity"]["source_ledger_sha256"] = _digest(_source_projection(matrix))
    matrix["integrity"]["decision_ledger_sha256"] = _digest(_decision_projection(matrix))
    return matrix


def main() -> None:
    arguments = _arguments()
    try:
        pdftotext_executable = _preflight_pdftotext()
    except RuntimeError as error:
        raise SystemExit(f"error: {error}") from None
    if _sha256(arguments.srs_pdf) != SOURCE_HASHES["website-srs"]:
        raise ValueError("SRS SHA-256 does not match the reviewed source")
    if _sha256(arguments.backend_pdf) != SOURCE_HASHES["backend-specification"]:
        raise ValueError("backend specification SHA-256 does not match the reviewed source")
    baseline = _read_object(arguments.baseline)
    with tempfile.TemporaryDirectory(prefix="requirements-matrix-") as temporary:
        temporary_directory = Path(temporary)
        srs_text = _pdf_text(arguments.srs_pdf, temporary_directory, pdftotext_executable)
        backend_text = _pdf_text(arguments.backend_pdf, temporary_directory, pdftotext_executable)
    matrix = _build_matrix(srs_text, backend_text, baseline)
    arguments.output.write_text(
        json.dumps(matrix, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(
        f"wrote {len(matrix['requirements'])} rows to {arguments.output}; "
        f"source digest {matrix['integrity']['source_ledger_sha256']}"
    )


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path
from typing import Any

import pytest
from scripts.build_requirements_matrix import _add_backend_trace
from scripts.validate_requirements_matrix import validate_requirements_matrix

MATRIX_PATH = Path(__file__).resolve().parents[1] / "config" / "requirements-matrix.json"


def valid_matrix() -> dict[str, Any]:
    with MATRIX_PATH.open(encoding="utf-8") as matrix_file:
        value: object = json.load(matrix_file)
    assert isinstance(value, dict)
    return deepcopy(value)


def test_requirements_matrix_accepts_the_versioned_source() -> None:
    validate_requirements_matrix(valid_matrix())


def test_requirements_matrix_contains_exactly_264_canonical_rows() -> None:
    matrix = valid_matrix()

    assert len(matrix["requirements"]) == 264
    assert matrix["requirements"][0]["id"] == "FR-GOV-01"
    assert matrix["requirements"][-1]["id"] == "FR-OPS-16"
    assert len({row["id"] for row in matrix["requirements"]}) == 264


@pytest.mark.parametrize(
    ("mutation", "message"),
    [
        ("duplicate-id", "canonical SRS catalogue order"),
        ("changed-title", "source ledger"),
        ("invented-dependency", "dependency edges"),
        ("wrong-owner", "accountable roles"),
        ("wrong-applicability-basis", "P0 applicability"),
        ("p2-decision-drift", "product-baseline scope decision"),
        ("wrong-page-difference-count", "printed-page difference count"),
    ],
)
def test_requirements_matrix_rejects_noncanonical_changes(
    mutation: str,
    message: str,
) -> None:
    matrix = valid_matrix()
    if mutation == "duplicate-id":
        matrix["requirements"][1]["id"] = matrix["requirements"][0]["id"]
    elif mutation == "changed-title":
        matrix["requirements"][0]["title"] = "Invented title"
        matrix["requirements"][0]["dependencies"]["activation_approval_precondition"] = (
            'The scope decision activating "Invented title" has been approved when the '
            "requirement is conditional."
        )
    elif mutation == "invented-dependency":
        matrix["requirements"][0]["dependencies"]["requirement_ids"] = ["FR-GOV-02"]
    elif mutation == "wrong-owner":
        matrix["requirements"][0]["ownership"]["accountable_roles"] = ["Invented Owner"]
    elif mutation == "wrong-applicability-basis":
        matrix["requirements"][0]["applicability"]["basis"] = "full-build-profile"
    elif mutation == "p2-decision-drift":
        p2_row = next(row for row in matrix["requirements"] if row["priority"]["level"] == "P2")
        p2_row["applicability"]["condition"] = "Invented activation condition."
    elif mutation == "wrong-page-difference-count":
        matrix["integrity"]["srs_toc_card_page_difference_count"] = 0
    else:  # pragma: no cover - the parametrization is closed above
        raise AssertionError(f"unhandled mutation {mutation}")

    with pytest.raises(ValueError, match=message):
        validate_requirements_matrix(matrix)


def test_all_p2_rows_have_an_explicit_binary_scope_decision() -> None:
    matrix = valid_matrix()
    p2_rows = [row for row in matrix["requirements"] if row["priority"]["level"] == "P2"]

    assert len(p2_rows) == 54
    assert {row["applicability"]["state"] for row in p2_rows} <= {
        "applicable",
        "not_applicable",
    }
    assert all(row["applicability"]["decision_refs"] for row in p2_rows)


def test_dependency_rows_preserve_preconditions_without_inventing_edges() -> None:
    matrix = valid_matrix()
    profiles = {profile["id"]: profile for profile in matrix["dependency_profiles"]}

    assert len(profiles) == 20
    for row in matrix["requirements"]:
        assert row["dependencies"]["profile_id"] in profiles
        assert profiles[row["dependencies"]["profile_id"]]["source_preconditions"]
        assert row["dependencies"]["activation_approval_precondition"]
        assert row["dependencies"]["requirement_ids"] == []


def test_backend_trace_rejects_a_same_priority_requirement_id_reorder() -> None:
    matrix = valid_matrix()
    rows = [
        {"id": row["id"], "priority": {"level": row["priority"]["level"]}, "source": {}}
        for row in matrix["requirements"]
    ]
    pages = [""] * 66
    for row in matrix["requirements"]:
        page = row["source"]["backend_trace_page"]
        pages[page] += (
            f"{row['id']}   {row['priority']['level']} - "
            f"{row['source']['backend_class']}   {row['title']}\n"
        )
    first_page_lines = pages[38].splitlines()
    first_id = rows[0]["id"]
    second_id = rows[1]["id"]
    first_page_lines[0] = first_page_lines[0].replace(first_id, second_id, 1)
    first_page_lines[1] = first_page_lines[1].replace(second_id, first_id, 1)
    pages[38] = "\n".join(first_page_lines)

    with pytest.raises(ValueError, match="backend Appendix A order differs"):
        _add_backend_trace(rows, "\f".join(pages))


def test_backend_trace_reconstructs_a_wrapped_requirement_id() -> None:
    matrix = valid_matrix()
    rows = [
        {"id": row["id"], "priority": {"level": row["priority"]["level"]}, "source": {}}
        for row in matrix["requirements"]
    ]
    pages = [""] * 66
    for row in matrix["requirements"]:
        page = row["source"]["backend_trace_page"]
        identifier = row["id"]
        if identifier == "FR-ABOUT-01":
            identifier = "FR-ABOUT-"
        elif identifier == "FR-ACADEMIC-01":
            identifier = "FR-"
        pages[page] += (
            f"{identifier}   {row['priority']['level']} - "
            f"{row['source']['backend_class']}   {row['title']}\n"
        )
        if row["id"] == "FR-ABOUT-01":
            pages[page] += "01   MUST\n"
        elif row["id"] == "FR-ACADEMIC-01":
            pages[page] += "ACADEMIC-   CONDITIONAL\n01   CONDITIONAL\n"

    _add_backend_trace(rows, "\f".join(pages))

    about_row = next(row for row in rows if row["id"] == "FR-ABOUT-01")
    assert about_row["source"]["backend_trace_page"] == 40
    academic_row = next(row for row in rows if row["id"] == "FR-ACADEMIC-01")
    assert academic_row["source"]["backend_trace_page"] == 48

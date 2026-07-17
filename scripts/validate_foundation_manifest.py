from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "config" / "foundation-scope-manifest.json"
SCHEMA_PATH = ROOT / "config" / "foundation-scope-manifest.schema.json"

GOVERNANCE_CORE_PROJECTION = "exclude:revision_history,approval_records"
EXPECTED_COMPONENTS = (
    (
        "product-baseline",
        "config/product-baseline.json",
        "2.0.0",
        "canonical-json-sha256",
        None,
    ),
    (
        "product-baseline-schema",
        "config/product-baseline.schema.json",
        "1.0.0",
        "raw-file-sha256",
        None,
    ),
    (
        "foundation-governance-core",
        "config/foundation-governance.json",
        "1.0.0",
        "canonical-json-projection-sha256",
        GOVERNANCE_CORE_PROJECTION,
    ),
    (
        "foundation-governance-schema",
        "config/foundation-governance.schema.json",
        "1.0.0",
        "raw-file-sha256",
        None,
    ),
    (
        "requirements-matrix",
        "config/requirements-matrix.json",
        "2.0.0",
        "canonical-json-sha256",
        None,
    ),
    (
        "requirements-matrix-schema",
        "config/requirements-matrix.schema.json",
        "1.0.0",
        "raw-file-sha256",
        None,
    ),
    (
        "scope-evidence-ledger",
        "config/scope-evidence-ledger.json",
        "1.0.0",
        "canonical-json-sha256",
        None,
    ),
    (
        "scope-evidence-ledger-schema",
        "config/scope-evidence-ledger.schema.json",
        "1.0.0",
        "raw-file-sha256",
        None,
    ),
    (
        "env-preview-template",
        ".env.preview.example",
        "2.0.0",
        "raw-file-sha256",
        None,
    ),
    (
        "env-staging-template",
        ".env.staging.example",
        "2.0.0",
        "raw-file-sha256",
        None,
    ),
    (
        "env-production-template",
        ".env.production.example",
        "2.0.0",
        "raw-file-sha256",
        None,
    ),
    (
        "runtime-environment-contract",
        "src/paw/environment.py",
        "2.0.0",
        "raw-file-sha256",
        None,
    ),
    (
        "preview-settings",
        "src/paw/settings/preview.py",
        "2.0.0",
        "raw-file-sha256",
        None,
    ),
    (
        "staging-settings",
        "src/paw/settings/staging.py",
        "2.0.0",
        "raw-file-sha256",
        None,
    ),
    (
        "production-settings",
        "src/paw/settings/production.py",
        "2.0.0",
        "raw-file-sha256",
        None,
    ),
)

# Independent pin for the canonical manifest projection with
# bundle_projection_sha256 omitted. It is populated only after every component
# digest and the approval/revision linkage have been reviewed together.
EXPECTED_BUNDLE_PROJECTION_SHA256 = (
    "1c536eb256a436a838c4870fb23f3ad11ad50425dab2fa64e7d64dee528edc34"
)


def _read_object(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as input_file:
        value: object = json.load(input_file)
    if not isinstance(value, dict):
        raise ValueError(f"{path.name} must contain a JSON object")
    return value


def _canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()


def _canonical_sha256(value: object) -> str:
    return hashlib.sha256(_canonical_bytes(value)).hexdigest()


def _raw_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _validate_schema(manifest: dict[str, Any]) -> None:
    schema = _read_object(SCHEMA_PATH)
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    errors = sorted(validator.iter_errors(manifest), key=lambda error: list(error.absolute_path))
    if errors:
        error = errors[0]
        location = ".".join(str(part) for part in error.absolute_path) or "<root>"
        raise ValueError(f"foundation manifest schema error at {location}: {error.message}")


def _resolve_component_path(relative_path: str) -> Path:
    candidate = Path(relative_path)
    if candidate.is_absolute() or ".." in candidate.parts:
        raise ValueError(f"manifest component path escapes the repository: {relative_path}")
    resolved = (ROOT / candidate).resolve(strict=True)
    try:
        resolved.relative_to(ROOT.resolve())
    except ValueError as error:
        raise ValueError(
            f"manifest component path escapes the repository: {relative_path}"
        ) from error
    if not resolved.is_file():
        raise ValueError(f"manifest component is not a regular file: {relative_path}")
    return resolved


def _component_digest(component: dict[str, Any], path: Path) -> str:
    digest_kind = component["digest_kind"]
    if digest_kind == "raw-file-sha256":
        return _raw_sha256(path)

    value = _read_object(path)
    if digest_kind == "canonical-json-sha256":
        return _canonical_sha256(value)
    if digest_kind == "canonical-json-projection-sha256":
        if component["projection"] != GOVERNANCE_CORE_PROJECTION:
            raise ValueError("the governance component uses an unknown projection")
        projected = {
            key: item
            for key, item in value.items()
            if key not in {"revision_history", "approval_records"}
        }
        return _canonical_sha256(projected)
    raise ValueError(f"unsupported component digest kind: {digest_kind}")


def manifest_projection_sha256(manifest: dict[str, Any]) -> str:
    projection = {
        key: value for key, value in manifest.items() if key != "bundle_projection_sha256"
    }
    return _canonical_sha256(projection)


def validate_foundation_manifest(manifest: dict[str, Any]) -> None:
    _validate_schema(manifest)

    components = manifest["components"]
    identifiers = [component["id"] for component in components]
    paths = [component["path"] for component in components]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("foundation manifest component IDs must be unique")
    if len(paths) != len(set(paths)):
        raise ValueError("foundation manifest component paths must be unique")

    actual_contract = tuple(
        (
            component["id"],
            component["path"],
            component["version"],
            component["digest_kind"],
            component["projection"],
        )
        for component in components
    )
    if actual_contract != EXPECTED_COMPONENTS:
        raise ValueError("foundation manifest components differ from the exact ordered contract")

    for component in components:
        path = _resolve_component_path(component["path"])
        actual_digest = _component_digest(component, path)
        if component["sha256"] != actual_digest:
            raise ValueError(f"{component['id']} digest does not match its repository component")

    product = _read_object(ROOT / "config" / "product-baseline.json")
    governance = _read_object(ROOT / "config" / "foundation-governance.json")
    expected_sources = [
        {
            "id": source["id"],
            "filename": source["filename"],
            "sha256": source["sha256"],
        }
        for source in product["source_documents"]
    ]
    if manifest["source_documents"] != expected_sources:
        raise ValueError("foundation manifest source identity differs from the product baseline")

    revision_ids = {revision["id"] for revision in governance["revision_history"]}
    approval_ids = {approval["id"] for approval in governance["approval_records"]}
    if manifest["revision_id"] not in revision_ids:
        raise ValueError("foundation manifest revision ID is absent from governance")
    if set(manifest["approval_ids"]) - approval_ids:
        raise ValueError("foundation manifest approval IDs are absent from governance")
    if governance["revision_history"][-1]["logical_artifact_id"] != manifest["logical_artifact_id"]:
        raise ValueError("current governance revision and manifest logical IDs differ")

    actual_projection_digest = manifest_projection_sha256(manifest)
    if manifest["bundle_projection_sha256"] != actual_projection_digest:
        raise ValueError("foundation manifest bundle projection digest is internally incorrect")
    if actual_projection_digest != EXPECTED_BUNDLE_PROJECTION_SHA256:
        raise ValueError(
            "foundation manifest bundle projection differs from approved version 1.0.0"
        )


def main() -> None:
    manifest = _read_object(MANIFEST_PATH)
    validate_foundation_manifest(manifest)
    print(
        "foundation scope manifest valid: 15 exact repository components, revision, "
        "approvals, sources and independently pinned bundle projection agree"
    )


if __name__ == "__main__":
    main()

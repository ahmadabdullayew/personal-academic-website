# Formal revision history and stakeholder approvals

## 1. Record authority and scope

This record resolves foundation item 22. The machine-readable authority is
`config/foundation-governance.json` version 1.0.0. Revision and approval entries
are append-only. A correction creates a new entry that identifies the earlier
record; it does not silently alter the historical decision.

The named stakeholder is `STK-001`, Ahmad Abdullayev, the website owner and
represented person. The six approval records below reflect the explicit owner
direction dated 17 July 2026 to make and complete the project-foundation
selections for items 11 through 23. They approve those selections for foundation
scope. They do not claim feature-release conformance, production deployment,
accessibility conformance, a security assessment, completed personal-data
registration, a restoration drill or conformity with all 264 SRS requirements.

## 2. Revision-record contract

Every revision records:

| Field                   | Required meaning                                                               |
| ----------------------- | ------------------------------------------------------------------------------ |
| Revision ID             | Immutable consecutive identifier; never recycled.                              |
| Logical artifact ID     | Stable artifact identity independent of a future Git commit.                   |
| Version                 | Existing commit abbreviation or semantic artifact version.                     |
| Previous version        | Explicit predecessor; null only for the first recorded revision.               |
| Recorded time           | UTC RFC 3339 timestamp.                                                        |
| Actor role              | The role that prepared or recorded the change.                                 |
| Change type and summary | Bounded description of what changed and why.                                   |
| Changed sections        | Exact affected governance areas.                                               |
| Migration impact        | Source, schema, mapping, import, reconciliation and rollback effect.           |
| Security/privacy impact | Processing, visibility, authorization, provider, retention and rights effect.  |
| Accessibility impact    | Content, asset, language, interaction or verification effect.                  |
| Test impact             | Schema, validator, negative test and evidence changes.                         |
| Restoration locator     | Existing Git object or logical artifact path/version; no invented future hash. |

In addition, a requirement change records previous text, new text, reason,
affected modules, migration impact, test impact, security/privacy impact,
accessibility impact, owner decision and effective baseline version, matching
SRS Chapter 8. Retired IDs remain traceable and are never reused.

## 3. Revision ledger

### `REV-001` — existing repository foundation

- Logical artifact: `repository-foundation@62418c3`
- Version: `62418c3`
- Full restoration object: `62418c3529060b2fdd27af2949cd5169e917a7a4`
- Recorded: `2026-07-17T08:18:51Z`
- Actor role: Repository Owner
- Change: initial source repository, product baseline, architecture, development
  contract and executable foundation checks.
- Migration impact: no legacy academic content was migrated.
- Security/privacy impact: public/private boundaries and the prohibition on
  unsupported public attributes were established.
- Accessibility impact: WCAG 2.2 Level AA was selected as the target.
- Test impact: executable foundation checks were established.

### `REV-002` — complete foundation items 11–23 bundle

- Logical artifact: `foundation-items-11-23@1.0.0`
- Version: `1.0.0`
- Previous version: `62418c3`
- Recorded: `2026-07-17T08:33:00Z`
- Actor role: implementation agent acting under owner instruction
- Change: deployment, language, administration and feature decisions;
  provisional legal baseline and selected region; official evidence register;
  ownership/workflow/review controls; 32-record inventory; 12-step migration;
  formal revision and six approval records; exact 264-row matrix and immutable
  bundle manifest.
- Migration impact: an approved plan and explicit dispositions were created; no
  production content mutation is claimed.
- Security/privacy impact: registration, Article 14 transfer, minimization,
  rights, provider, notice, retention and publication controls were made
  mandatory.
- Accessibility impact: asset/document migration requires accessibility evidence
  before approval.
- Test impact: schema, semantic, cross-artifact, source-regeneration and bundle
  integrity negative tests were added.
- Restoration locator:
  `config/foundation-scope-manifest.json#bundle_projection_sha256`. The manifest
  is outside its own component set, so this locator does not create a circular
  digest or assert a future Git hash.

## 4. Approval-record contract

Every approval contains a deterministic decision ID, one domain, the exact
scope-item list, decision text, result, stakeholder, approver role, logical
artifact/version, UTC decision time, evidence references and an express scope
limit. It also contains `supersedes`: null for a domain's first decision and the
immediately preceding same-domain approval ID for every later decision. Approval
by silence is prohibited. Foundation results are either
`approved-for-foundation-scope` or `rejected-for-foundation-scope`; the current
record in every required domain must approve the current baseline. A
production/release workflow uses its own evidence and result.

All six records identify logical artifact `foundation-items-11-23@1.0.0`,
version 1.0.0, stakeholder `STK-001`, scope items 11–23 and the explicit owner
direction `owner-directive:2026-07-17-items-11-23`.

| Decision ID             | Domain and role                              | Approved foundation decision                                                                                                                                                                                     | Express limit                                                                                          |
| ----------------------- | -------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| `APR-PRODUCT-001`       | Product — Website Owner and Product Approver | Selected scope, jurisdiction, content governance, inventory, migration, revisions and traceability foundation                                                                                                    | Not feature-release, production-deployment or whole-SRS conformance approval.                          |
| `APR-CONTENT-001`       | Content — Academic Content Approver          | Canonical ownership, evidence rule, four cadences, seven event triggers, 32-record inventory and hold rules                                                                                                      | Each future public content revision still needs its own evidence and approval.                         |
| `APR-ACCESSIBILITY-001` | Accessibility — Accessibility Approver       | Accessibility evidence gate for migrated documents, media, language metadata and complete workflows                                                                                                              | Does not represent any page, document or process as accessibility-conformant.                          |
| `APR-SECURITY-001`      | Security — Security Approver                 | Public/private boundary, quarantine, minimized processing, immutable evidence and provider-control gates                                                                                                         | Not a threat model, penetration test or security-release approval.                                     |
| `APR-PRIVACY-001`       | Privacy — Privacy Approver                   | Provisional Azerbaijan baseline pending nexus/applicable-law review; selected-not-deployed `eu-central-1`; registration, licensing, consent-channel, certification, transfer, notice, rights and retention gates | Does not determine applicable law, waive mandatory law or approve production personal-data collection. |
| `APR-OPERATIONS-001`    | Operations — Technical Operations Approver   | Migration, reconciliation, atomic publication, rollback, archive and append-only revision controls                                                                                                               | Not deployment, restoration-drill or production-release approval.                                      |

Each result is `approved-for-foundation-scope`, recorded at
`2026-07-17T08:33:00Z`.

## 5. Change and supersession procedure

1. Allocate the next consecutive `REV-NNN` identifier.
2. Preserve the complete previous record and identify its version.
3. Record previous and new values, rationale and affected items/modules.
4. Evaluate migration, security/privacy, accessibility and test effects.
5. Update official-source review evidence when law, provider or region is
   affected.
6. Update inventory dispositions, review dates and migration mappings when
   content is affected.
7. Run schema and semantic validation plus targeted negative tests.
8. Allocate the next consecutive `APR-DOMAIN-NNN` in every affected domain,
   point `supersedes` to the previous same-domain decision, and decide one
   immutable logical artifact/version.
9. Publish or activate only after all applicable gates pass.
10. Preserve the prior public snapshot and demonstrate the restoration path.

A superseded approval remains visible with its original result and scope. The
new decision points to it and states whether it replaces, narrows, rejects or
extends the earlier decision. Dates, IDs, evidence and result are never
rewritten to make a later state appear to have existed earlier.

## 6. Verification

`scripts/validate_foundation_governance.py` validates the JSON Schema, exact
source hashes, official-source host boundaries, Azerbaijan/Germany selection,
activation gates, schedules, calculated due dates and overdue blocking,
inventory states and exact evidence references, migration order and safety
controls, consecutive append-only revision and per-domain approval chains,
temporal consistency, and presence of every machine ID in these documents. The
separate manifest validator recomputes all 15 component digests and an
independently pinned bundle projection. Negative tests mutate one invariant at a
time and require rejection.

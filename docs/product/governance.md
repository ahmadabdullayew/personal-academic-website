# Product governance and named approvers

## Owner

**Website owner and represented person: Ahmad Abdullayev.**

Ahmad Abdullayev is the final decision authority for public identity, factual
claims, visibility, content approval, feature activation and release acceptance.
No academic title, institutional affiliation, degree, discipline or biography is
inferred until it is supported by an owner-approved source record.

The name is supported by the owner-directed implementation request, local Git
identity, operating-system account and project path. The supplied documents
support the one-owner authority model; they do not independently identify the
owner by name. This distinction prevents the product model from being
misrepresented as identity evidence.

The two reviewed inputs are identified by immutable digest:

| Input                                                 | SHA-256                                                            |
| ----------------------------------------------------- | ------------------------------------------------------------------ |
| `personal_academic_professional_website_srs.pdf`      | `976ba51a785d27d37117655a4a508eb5133edb36e988966ce31e8878a78eb9e7` |
| `personal_academic_website_backend_specification.pdf` | `1eca221859e9379cadd3d3e192bd35b68a7e0010ae15f8de53e539e1782c31b5` |

## Approval assignments

| Domain        | Named approver   | Authority                                                                            |
| ------------- | ---------------- | ------------------------------------------------------------------------------------ |
| Product       | Ahmad Abdullayev | Scope, priority, feature activation, P1 deferral and product acceptance              |
| Content       | Ahmad Abdullayev | Identity, claims, dates, outputs, relationships, evidence, rights and wording        |
| Accessibility | Ahmad Abdullayev | Accessibility trace, manual/automated results, complete processes and documents      |
| Security      | Ahmad Abdullayev | Threats, authorization, authentication, uploads, secrets, dependencies and incidents |
| Privacy       | Ahmad Abdullayev | Processing, notices, consent, providers, retention, deletion and visibility boundary |
| Operations    | Ahmad Abdullayev | Builds, deployment, migration, monitoring, backups, restoration and rollback         |

These are separate approval decisions even though one real person presently
occupies all roles. No additional person is invented.

Assignment names an accountable decision maker; it does not silently create a
release decision. Each domain still records its own result against a defined
artifact and evidence set.

## Approval rules

1. Every recorded decision includes approver, role, scope, artifact/version,
   evidence, result, timestamp and rationale.
2. Approval by silence is prohibited.
3. Applicable P0 failure cannot be waived.
4. P1 deferral requires an individual rationale, impact assessment and owner
   approval.
5. A conditional feature remains disabled until all affected approval domains
   approve its activation.
6. Content approval cannot override accessibility, security, privacy or
   operations failure.
7. Security, privacy, accessibility and recoverability failures block release.
8. Emergency operations authority permits rollback, unpublication, credential
   revocation and temporary shutdown; it does not permit unreviewed public
   content.
9. Later maintainers may prepare or review work, but delegation of final
   authority requires a versioned governance decision.

The machine-validated form is `config/product-baseline.json`.

## Decision-record contract

Each product, content, accessibility, security, privacy and operations decision
uses all of these fields:

| Field             | Contract                                                          |
| ----------------- | ----------------------------------------------------------------- |
| Decision ID       | Unique, immutable identifier                                      |
| Domain            | Exactly one assigned approval domain                              |
| Approver and role | Must match the versioned assignment                               |
| Scope             | Exact features, routes and data covered                           |
| Artifact/version  | Commit, release candidate or immutable artifact digest            |
| Evidence          | Test reports, review records and requirement references           |
| Result            | `approved`, `rejected` or `deferred`; silence is never a result   |
| Timestamp         | UTC RFC 3339 timestamp                                            |
| Rationale         | Non-empty reasoning, including residual risk                      |
| Deferral detail   | Impact, owner approval and follow-up, required for every deferral |

The foundation baseline records role assignments. Release-decision records are
created only when the corresponding review evidence exists.

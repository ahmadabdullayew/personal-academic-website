# Foundation items 1–23 traceability

| Item | Required outcome                      | Primary implementation evidence                                  | Executable evidence                              |
| ---: | ------------------------------------- | ---------------------------------------------------------------- | ------------------------------------------------ |
|    1 | Functioning source repository         | Git `main`, intentional initial commit, source tree              | fresh-clone `make check`                         |
|    2 | README and local development          | `README.md`, `docs/development/local-development.md`             | `make bootstrap`, live-stack probe               |
|    3 | Seven architecture selections         | ADR 0001 and foundation literature review                        | Django/Compose/build checks                      |
|    4 | Manifests and locks                   | `pyproject.toml`, `uv.lock`, `package.json`, `package-lock.json` | `make lock-check`                                |
|    5 | Format/lint/type/test commands        | Makefile and package scripts                                     | format, lint, type and test targets              |
|    6 | Environment documentation/examples    | examples and environment contract                                | environment/deployment checks and negative tests |
|    7 | Actual owner                          | product baseline owner record and governance provenance          | schema/cross-field validation                    |
|    8 | Named approvers                       | six domain assignments and decision-record contract              | schema/cross-field validation                    |
|    9 | Primary/secondary audiences           | audience document and machine baseline                           | schema/cross-field validation                    |
|   10 | Ranked visitor/owner goals            | ranked-goal document, method and evidence references             | schema/cross-field validation                    |
|   11 | Domain and deployment environments    | product baseline, environment contract and deployment templates  | product, environment and coherence validation    |
|   12 | Active languages and default locale   | product-baseline localization decision                           | schema, cross-field and deployment checks        |
|   13 | Administration model and roles        | owner/administrator/editor authorization decision                | schema and product validation                    |
|   14 | Optional/conditional capabilities     | all 54 P2 decisions with rationale and activation condition      | exact-set, count and matrix reconciliation       |
|   15 | Contact method and provider           | contact form and Amazon SES decision                             | product/governance/template reconciliation       |
|   16 | Site-wide search                      | active PostgreSQL public-snapshot-only search decision           | product/governance reconciliation                |
|   17 | ORCID and Crossref synchronization    | two inactive decisions and exact activation gates                | product/governance/template reconciliation       |
|   18 | Analytics/cookies/embeds/feeds/social | privacy-and-discovery decision record                            | product/governance reconciliation                |
|   19 | Applicable legal jurisdiction         | jurisdiction and official-source ledger                          | governance schema and legal cross-field checks   |
|   20 | Content ownership/review schedules    | workflow, assignments, four cadences and seven event triggers    | governance schedule and ownership checks         |
|   21 | Content inventory/migration plan      | 32 inventory rows and 12 ordered migration steps                 | governance state, rights, dates and gate checks  |
|   22 | Revision history/approval records     | two linked revisions and six domain decisions                    | chronology, version, scope and role checks       |
|   23 | 264-row requirements matrix           | versioned applicability/dependency/ownership ledger              | PDF regeneration, hashes and matrix validator    |

The supplied PDFs are external evidence inputs, not repository dependencies.
Their filenames, printed-page reference convention and SHA-256 digests are
recorded in all three machine baselines so a reviewer can verify that references
point to the same documents. `scripts/validate_foundation_scope.py` additionally
rejects drift among the product, governance, matrix and deployment-template
decisions.

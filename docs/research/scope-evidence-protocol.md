# Reproducible evidence protocol for foundation items 11–23

- Review date: 2026-07-17
- Decision and review owner: Ahmad Abdullayev
- Machine ledger: `config/scope-evidence-ledger.json` version 1.0.0
- Contract: `config/scope-evidence-ledger.schema.json`
- Semantic and drift validator: `scripts/validate_scope_evidence.py`
- Closed scope: foundation items 11 through 23, exactly once each

## 1. Review question

The review asked:

> Which finite deployment, language, administration, capability, legal,
> content, migration, approval and traceability decisions resolve
> project-foundation items 11 through 23 while preserving every supplied
> requirement and every unresolved activation gate?

The question is deliberately narrower than implementation acceptance. A scope
decision can be complete while its implementation, production activation or
release evidence is still a later gate. Likewise, an inactive conditional
capability is a resolved dormant state when its activation condition and owner
are recorded.

## 2. Evidence precedence and admission rules

Evidence was considered in this order:

1. the two owner-supplied specifications, identified by exact SHA-256;
2. primary legislation and official government publications;
3. standards and protocols from their controlling organizations;
4. official provider and registry documentation; and
5. explicit owner policy for values external literature cannot choose, such as
   the preferred domain or launch language.

A source was included only if its issuing authority and a narrow proposition
directly constrain at least one item 11–23 decision. Every source record states
its authority, exact locator, retrieval time, proposition, limitation, identity
control, supporting retrieval event, item mapping and freshness rule.

The review excluded duplicate formats, unnecessary translations, superseded or
draft material when a final source governs, secondary commentary, marketing
comparisons and results that did not constrain a reviewed decision. Provider
documentation is evidence of provider behavior, not independent proof of legal
compliance. A standard describes a control model; it is not evidence that the
site already implements that model.

## 3. Source-file identity

The supplied specifications are pinned by bytes, not merely by file name:

| Source ID | File | SHA-256 | Use |
| --- | --- | --- | --- |
| `website-srs` | `personal_academic_professional_website_srs.pdf` | `976ba51a785d27d37117655a4a508eb5133edb36e988966ce31e8878a78eb9e7` | Complete product scope, priority, preconditions, roles and 264 detailed cards |
| `backend-specification` | `personal_academic_website_backend_specification.pdf` | `1eca221859e9379cadd3d3e192bd35b68a7e0010ae15f8de53e539e1782c31b5` | Backend responsibility and independent 264-row Appendix A reconciliation |

Any changed byte content, name, page-reference model, extraction count or hash
is a new source edition. It cannot replace the reviewed file under the existing
ledger version.

## 4. Executed retrieval and screening ledger

Candidate counts are raw results or direct targets screened in the recorded
event. The same official source can appear in more than one event, so 34
included event instances resolve to 32 unique source records.

| Event | UTC execution | Method and exact sites | Candidate queries | Included | Excluded | Selection result |
| --- | --- | --- | ---: | ---: | ---: | --- |
| `EV-001` | 2026-07-17 08:40 | Local direct retrieval; owner-supplied filesystem | 2 | 2 | 0 | Both supplied PDFs retained and hashed |
| `EV-002` | 2026-07-17 08:50 | Direct RDAP retrieval; `rdap.verisign.com` | 2 | 2 | 0 | Exact unhyphenated and hyphenated `.com` paths both retained; HTTP 404 was observed for each |
| `EV-003` | 2026-07-17 09:10 | Web search; AWS Docs, RFC Editor, W3C, NIST | 18 | 4 | 14 | AWS region, RFC 5646, W3C HTML-language and NIST RBAC sources selected |
| `EV-004` | 2026-07-17 09:12 | Web search; AWS Docs, PostgreSQL, ORCID, Crossref | 18 | 3 | 15 | SES data protection, PostgreSQL search and Crossref REST sources selected |
| `EV-005` | 2026-07-17 09:14 | Web search; ORCID, RFC Editor, OGP, ISO | 14 | 3 | 11 | ORCID read API, RFC 4287 and ISO 15489-1 selected; OGP resolved in `EV-006` |
| `EV-006` | 2026-07-17 09:16 | Web search; OGP, W3C, NIST, Verisign RDAP | 16 | 3 | 13 | OGP, W3C statement maintenance and final NIST SSDF 1.1 selected |
| `EV-007` | 2026-07-17 09:18 | Direct official retrieval; Azerbaijan, EU and AWS authority sites | 17 | 17 | 0 | Exact 17-source legal/provider register retained without subsetting |
| **Total** | | | **87** | **34** | **53** | **32 unique sources** |

The exact query strings, sites, included source IDs and exclusion-reason counts
are data fields in `retrieval_events`. The validator requires each event to
satisfy all three equalities:

```text
candidate_count = included_count + excluded_count
included_count = number of included_source_ids
excluded_count = sum of categorized exclusion-reason counts
```

For the four web-search events, 53 results were excluded as duplicates,
alternate formats or translations, adjacent documentation, historical or draft
material, older version documentation, or sources without a distinct
decision-controlling proposition. The reason categories and their exact counts
are retained per event rather than replaced with a general narrative.

## 5. Standards, protocols and provider sources

The selected non-legal literature is finite and authority-led:

| Source ID | Stable identity or retrieval snapshot | Decision proposition |
| --- | --- | --- |
| `RFC-5646` | RFC 5646, BCP 47, September 2009 | Language-tag syntax and semantics |
| `W3C-HTML-LANGUAGE` | English W3C guidance retrieved 2026-07-17 | Default and nested HTML language declarations |
| `NIST-RBAC` | NIST FAQ updated 2026-03-04, retrieved 2026-07-17 | Users, roles, permissions, sessions and transaction authorization |
| `POSTGRESQL-FTS` | `current` resolved to PostgreSQL 18 Chapter 12 on 2026-07-17 | Parsing, queries, ranking, highlighting, dictionaries and indexing |
| `ORCID-API-READ` | Official tutorial retrieved 2026-07-17 | Read data for a specified ORCID record and use sandbox testing |
| `CROSSREF-REST-API` | Official page with 2020-04-08 update marker, retrieved 2026-07-17 | Retrieve deposited scholarly metadata, including by DOI |
| `RFC-4287` | RFC 4287, December 2005, updated by RFC 5988 | Atom feed and entry syntax and processing |
| `OPEN-GRAPH-PROTOCOL` | Basic-metadata page retrieved 2026-07-17 | Static page-head metadata for link previews |
| `ISO-15489-1-2016` | Edition 2, 2016, confirmed 2021 | Records, metadata, responsibilities, monitoring and records controls |
| `W3C-ACCESSIBILITY-STATEMENT` | Page updated 2025-05-20, retrieved 2026-07-17 | Target/version, evaluation evidence, approval and maintenance date |
| `NIST-SP-800-218` | Final SSDF 1.1, February 2022 | Roles, protected artifacts, provenance and repeatable verification |
| `PROVIDER-AWS-REGIONS` | Frankfurt/Germany/three-AZ snapshot retrieved 2026-07-17 | Identity of `eu-central-1`, not end-to-end residency |
| `PROVIDER-AWS-DATA-PRIVACY` | Official FAQ retrieved 2026-07-17 | Region choice for customer content and separate service/account paths |
| `PROVIDER-AWS-SES-REGIONS` | Official page retrieved 2026-07-17 | Region-specific SES resources and non-regional recipient delivery |
| `PROVIDER-AWS-SES-DATA-PROTECTION` | Official page retrieved 2026-07-17 | Sensitive metadata boundaries and opportunistic-TLS default |

The final NIST SSDF 1.1 source was selected. The surfaced SSDF 1.2 material was
still draft and was therefore not substituted for the final publication. The
PostgreSQL `current` URL is explicitly recorded as a retrieval snapshot because
it can resolve to a later major version.

## 6. Official legal and jurisdiction register

The ledger mirrors the governance baseline's 17 official legal/provider
records by exact ID, authority, title, URL and project proposition. Validation
fails if either side changes independently.

| Source ID | Exact official URL |
| --- | --- |
| `LAW-AZ-CONSTITUTION-30-32` | <https://president.az/en/pages/view/azerbaijan/constitution/> |
| `LAW-AZ-PERSONAL-DATA-998-IIIQ` | <https://frameworks.e-qanun.az/19/f_19675.html> |
| `LAW-AZ-CABINET-237` | <https://frameworks.e-qanun.az/21/f_21060.html> |
| `LAW-AZ-CABINET-149` | <https://mincom.gov.az/storage/pages/649/9b0e869640ba56d43615eef7906a4d08.pdf> |
| `LAW-AZ-CABINET-149-161-2022-AMENDMENT` | <https://e-qanun.az/framework/49396> |
| `LAW-AZ-CABINET-161` | <https://mincom.gov.az/storage/pages/648/4b2105426aa7138d97d78c9e1cfb91c4.pdf> |
| `LAW-AZ-EHIS-DIGITAL-CONSENT` | <https://president.az/az/articles/view/69619> |
| `AUTHORITY-AZ-PERSONAL-DATA-LICENSING` | <https://mincom.gov.az/az/qanunvericilik/lisenziyalasdirma/rabite-ve-informasiya-texnologiyalari-sahesinde-lisenziyalarin-verilmesi/lisenziya/ferdi-sahibkarlar-ucun> |
| `AUTHORITY-AZ-PERSONAL-DATA-REGISTRY` | <https://mincom.gov.az/az/qanunvericilik/reyestrler/reyestrler> |
| `LAW-AZ-PRIVATE-INTERNATIONAL-LAW` | <https://frameworks.e-qanun.az/0/f_509.html> |
| `LAW-AZ-COPYRIGHT-115-IQ` | <https://frameworks.e-qanun.az/4/f_4167.html> |
| `LAW-EU-GDPR-2016-679` | <https://eur-lex.europa.eu/eli/reg/2016/679/oj> |
| `GUIDANCE-EU-EDPB-ARTICLE-3` | <https://www.edpb.europa.eu/documents/guideline/guidelines-32018-on-the-territorial-scope-of-the-gdpr-article-3-version-adopted_en> |
| `PROVIDER-AWS-REGIONS` | <https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html> |
| `PROVIDER-AWS-DATA-PRIVACY` | <https://aws.amazon.com/compliance/data-privacy-faq/> |
| `PROVIDER-AWS-SES-REGIONS` | <https://docs.aws.amazon.com/ses/latest/dg/regions.html> |
| `PROVIDER-AWS-SES-DATA-PROTECTION` | <https://docs.aws.amazon.com/ses/latest/dg/data-protection.html> |

The Republic of Azerbaijan remains a provisional internal engineering and
governance baseline. The ledger does not turn that choice into a claim about
residence, citizenship, exclusive court competence or the absence of another
mandatory law. The GDPR source and EDPB guidance are retained conditionally;
German hosting alone is not recorded as satisfying the Article 3 test. Every
Azerbaijani-language legal proposition is identified as a project English
paraphrase in the governance source record and requires provision-level review
when a gate is reached.

## 7. One question and result for every item

| Item | Exact review subject | Closed result |
| ---: | --- | --- |
| 11 | Domain and environments | `https://ahmadabdullayev.com`; `www` redirect; local, test/CI, preview, staging, production; `eu-central-1` |
| 12 | Active languages and default locale | English `en` only and default; explicit gate for another locale |
| 13 | Administration and maintainers | Named-account single-owner administration; owner, administrator, editor; MFA and bounded sessions |
| 14 | Optional and conditional capabilities | All 54 P2 rows decided: 12 active, 42 inactive |
| 15 | Contact and delivery | `/contact/` active; Amazon SES in `eu-central-1`; truthful multi-stage delivery states |
| 16 | Search | Active PostgreSQL full-text search over approved public snapshots only |
| 17 | ORCID and Crossref | Both inactive behind separate verified-identifier and approved-DOI gates |
| 18 | Analytics, storage, embeds, feeds, previews | Analytics, nonessential public storage and embeds inactive; admin security cookies, Atom and static previews active |
| 19 | Jurisdiction | Azerbaijan provisional internal baseline; Germany selected hosting location; mandatory-law and production gates preserved |
| 20 | Ownership and review | Ahmad Abdullayev; six approval domains; 30/90/180/365-day maximum intervals and immediate event review |
| 21 | Inventory and migration | 32 inventory records and a reversible 12-step migration plan |
| 22 | Revisions and approvals | Linked `REV-001`/`REV-002` and six separately scoped approvals |
| 23 | Applicability matrix | 264 rows; 148 P0, 62 P1, 52 conditional P2, 2 may-P2; 222 applicable, 42 dormant |

The machine ledger contains the full question, answer, citations, artifact
references, decision owner and evidence boundary for every row. Citations are
foreign keys: each must resolve to a source that explicitly maps to the same
foundation item.

## 8. Freshness and event-driven review

The ledger defines seven mandatory triggers:

1. source URL, redirect, authority or material-content change;
2. standard, protocol, guidance or provider version/status change;
3. legal amendment, repeal, replacement or consolidation change;
4. provider region, service, contract, subprocessor, endpoint or delivery change;
5. project domain, environment, locale, role, feature, jurisdiction, content or
   applicability change;
6. scheduled review due date or affected release, whichever comes first; and
7. supplied-file identity, page model, population or digest change.

Owner-supplied specifications are event-reviewed. RDAP and the mutable Ministry
registry page use 30-day review periods. Other mutable provider, integration and
legal sources use 90-day periods. Stable standards and protocols use 365-day
periods unless an earlier event occurs. Every dated source computes
`next_review_on` as its retrieval date plus `maximum_age_days`; the validator
rejects hand-entered date drift.

## 9. Machine enforcement and reproduction

Run the focused ledger validation and tests with the locked environment:

```shell
uv run --frozen --env-file .env.test.example \
  python scripts/validate_scope_evidence.py
uv run --frozen --env-file .env.test.example \
  pytest tests/test_scope_evidence_validation.py -q --no-cov
```

The validator enforces:

- one ordered question for each integer 11 through 23;
- exactly 32 ordered, unique source identities;
- exactly seven retrieval events and seven freshness triggers;
- exact per-event and aggregate candidate accounting: 87 screened, 34 included
  event instances and 53 excluded;
- both PDF names and SHA-256 values across product, governance, matrix and
  evidence artifacts;
- exact legal-source ID, authority, title, URL and proposition equality with
  `foundation-governance.json`;
- citation and retrieval-event referential integrity;
- HTTPS issuing-authority locators for every external source;
- source-to-item applicability and repository artifact existence;
- calculated freshness dates;
- product decisions for owner, domain, AWS region, locale and all 54 P2 rows;
- matrix totals, priority totals and 222/42 applicability totals; and
- cryptographic digests of the reviewed protocol, triggers, retrieval events,
  sources and review questions.

Those final register digests make a changed proposition, limitation, query,
count, timestamp, citation or identity fail closed. A legitimate change requires
a new retrieval event, updated decision evidence, a new ledger version and an
intentional validator update; it cannot pass as unnoticed source drift.

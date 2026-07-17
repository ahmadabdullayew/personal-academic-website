# Scope and governance evidence review for foundation items 11–23

- Review date: 2026-07-17
- Decision owner: Ahmad Abdullayev
- Product baseline: `config/product-baseline.json` version 2.0.0
- Governance baseline: `config/foundation-governance.json` version 1.0.0
- Requirement matrix: `config/requirements-matrix.json` baseline version 2.0.0,
  schema version 1.0.0

## 1. Review question and method

The review asked which finite scope, deployment, administration, feature,
jurisdiction, content-governance, migration and traceability decisions satisfy
foundation items 11–23 without inventing owner attributes or silently activating
conditional requirements.

Evidence was evaluated in this order:

1. the two owner-supplied specifications at their recorded SHA-256 identities;
2. legislation and government publications from official repositories;
3. standards and protocol specifications from their issuing organizations;
4. selected-service behavior from official provider documentation; and
5. explicit owner-directed project policy where external evidence cannot decide
   a value such as the preferred domain or default language.

The SRS extraction covers every detailed functional-requirement card and the
table of contents. The backend cross-check covers every Appendix A row. Official
sources were included only when they constrain a selected decision. Secondary
legal summaries, vendor-comparison articles, marketing listicles and sources
that could not be tied to a decision were excluded. Provider documentation is
evidence of provider behavior, not independent proof of legal compliance.

Legal/provider URLs are mutable. The register records retrieval date, official
language, translation status, currency note and proposition mapping, but this
review did not record source-content digests and does not claim immutable
capture. Production reliance requires fresh official retrieval plus a SHA-256 or
stable instrument/archive identity and amendment status.

## 2. Source identity and extraction controls

| Source                                                | Role                                                                                      | Integrity control                                                                                             |
| ----------------------------------------------------- | ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| `personal_academic_professional_website_srs.pdf`      | IDs, titles, priorities, requirements, preconditions, accountable roles and project scope | SHA-256 `976ba51a785d27d37117655a4a508eb5133edb36e988966ce31e8878a78eb9e7`; 324 PDF pages; 264 detailed cards |
| `personal_academic_website_backend_specification.pdf` | backend responsibility, activation profile and independent order/priority reconciliation  | SHA-256 `1eca221859e9379cadd3d3e192bd35b68a7e0010ae15f8de53e539e1782c31b5`; 65 PDF pages; 264 Appendix A rows |

All citations to these documents use printed page numbers. The extractor keeps
both the SRS table-of-contents target and the physical detailed-card heading
because 31 targets differ by one printed page. It rejects a different file hash,
page count, ID order, card count, priority sequence or backend trace count.

## 3. Decision synthesis by foundation item

| Item | Resolved decision                                                                                                                                                                                                                  | Controlling evidence                                                                                                                  | Auditable result                                                                                                                                          |
| ---: | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
|   11 | `https://ahmadabdullayev.com`; `www` redirects; local, test/CI, preview, staging and production; regional AWS resources in `eu-central-1`                                                                                          | SRS deployment/SEO requirements; backend deployment profile; AWS Regions documentation                                                | product baseline, three deployment templates, settings checks                                                                                             |
|   12 | English `en` is the sole active and default locale                                                                                                                                                                                 | SRS internationalization cards; RFC 5646; W3C language-declaration guidance                                                           | locale set, route policy and exact activation gate for another language                                                                                   |
|   13 | named-account online administration with owner, administrator and editor roles; MFA for all                                                                                                                                        | SRS administration/security cards; backend auth profile; NIST role-based access-control model                                         | deny-by-default operations, role prohibitions, session and recovery policy                                                                                |
|   14 | all 54 P2 cards decided: 12 active and 42 inactive                                                                                                                                                                                 | SRS P2 semantics and all 54 card bodies; backend activation profile                                                                   | one machine row per P2 ID with rationale, activation condition and decision owner                                                                         |
|   15 | contact form active; Amazon SES in `eu-central-1`; public email not exposed                                                                                                                                                        | SRS contact/security/operations cards; backend contact flow; SES security and region guidance                                         | exact intake fields, durable acceptance point, failure semantics and production gates                                                                     |
|   16 | site-wide search active over approved public snapshots using PostgreSQL full-text search                                                                                                                                           | SRS search/privacy cards; backend public-index boundary; PostgreSQL search documentation                                              | included types, excluded states and no query analytics                                                                                                    |
|   17 | ORCID and Crossref synchronization inactive                                                                                                                                                                                        | SRS integration cards; backend candidate-import model; official provider API guidance                                                 | separate verified-identifier and approved-DOI activation gates                                                                                            |
|   18 | analytics, optional public storage and third-party embeds inactive; admin security cookies, Atom and static social previews active                                                                                                 | SRS security/content cards; RFC 4287; Open Graph protocol                                                                             | exact state for every named capability and public-data boundary                                                                                           |
|   19 | Azerbaijan is the provisional internal governance baseline pending controller-nexus and applicable-law determination; no governing law or court forum is conclusively asserted; Germany is the selected regional-resource location | Constitution, Personal Data and Private International Law, Decisions 237/149/161, EHIS, GDPR/EDPB scope guidance and AWS/SES evidence | nexus, registration/exemption, licensing, consent channel, certification/expertise, notice, rights deadlines, security, transfer and source-archive gates |
|   20 | Ahmad Abdullayev owns editorial decisions; six approval domains; four maximum review intervals and seven event triggers                                                                                                            | SRS governance/operations cards; backend revision/publication model; ISO 15489 records principles; W3C maintenance guidance           | workflow, owners, due-date calculations, overdue actions and event responses                                                                              |
|   21 | 32-row initial inventory and 12-step migration plan                                                                                                                                                                                | both specifications; ISO 15489; NIST secure-development evidence practices                                                            | source/right/privacy/state disposition for every content family, reconciliation and rollback                                                              |
|   22 | linked `REV-001` and `REV-002`; six separate scope-limited approval records                                                                                                                                                        | SRS change-control requirements; ISO 15489; NIST SSDF                                                                                 | append-only fields, predecessor, impacts, restoration locator, exact domain and artifact version                                                          |
|   23 | exact 264-row applicability/dependency/ownership matrix                                                                                                                                                                            | all 264 SRS cards and all 264 backend Appendix A rows                                                                                 | 148 P0, 62 P1, 52 P2-CONDITIONAL, 2 P2-MAY; 222 applicable and 42 not applicable                                                                          |

## 4. Deployment, language and administration evidence

AWS identifies `eu-central-1` as Europe (Frankfurt), Germany and documents its
Availability Zones. The scope decision requires selected regional resources to
use that region and prohibits application-managed cross-region replication
unless separately approved; it does not claim deployment or an absolute region
lock. Runtime/data, backups, queues, logs, SES state, edge/control-plane paths,
support/subprocessors, account metadata, legal demands and recipient mail
systems require separate evidence and disclosure:
<https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html>.

RFC 5646 defines the language-tag syntax and registry model. W3C guidance says
the language of HTML content should be declared on the `html` element and that
language changes should be marked on the relevant element. That supports `en`
and element-level tags, while the choice of English as the only active language
remains the owner's explicit launch-scope decision:

- <https://www.rfc-editor.org/info/rfc5646/>
- <https://www.w3.org/International/questions/qa-html-language-declarations.html>

NIST's role-based access-control material separates users, roles, permissions
and constraints. The selected owner/administrator/editor model applies that
separation to a one-owner site without creating fictitious initial accounts.
Authentication does not confer product, content, accessibility, security,
privacy or operations approval authority:
<https://csrc.nist.gov/Projects/role-based-access-control/faqs>.

## 5. Contact, search, synchronization and discovery evidence

SES documentation requires protection of credentials and sensitive data, and
describes encryption behavior and shared-responsibility boundaries. Because SES
uses opportunistic TLS by default, the project requires TLS or sends only a
minimal notification whose substantive content remains in the secured
administrative system. Personal data is prohibited in resource names, tags and
free-form metadata; open/click tracking is disabled. Form acceptance, durable
queuing and provider delivery remain different states:
<https://docs.aws.amazon.com/ses/latest/dg/data-protection.html>.

PostgreSQL documents parsing, query construction, ranking, highlighting,
dictionaries and index acceleration for full-text search. The expected corpus
does not supply evidence for a second search datastore, while the existing
database can update the approved public search projection in the publication
transaction: <https://www.postgresql.org/docs/current/textsearch.html>.

ORCID's API retrieves data for a specified ORCID iD, while Crossref retrieves
provider metadata. Neither provider identifies this website owner without an
owner-verified identifier or proves that a retrieved record should overwrite a
local record. Both integrations are therefore dormant candidate-import paths,
not unresolved choices:

- <https://info.orcid.org/documentation/api-tutorials/api-tutorial-read-data-on-a-record/>
- <https://www.crossref.org/documentation/retrieve-metadata/rest-api/>

RFC 4287 supplies the Atom document and entry model. Open Graph supplies static
page metadata for link previews. Both can be generated from approved public
snapshots without analytics, optional visitor storage, embedded scripts or a new
private-data flow:

- <https://www.rfc-editor.org/info/rfc4287/>
- <https://ogp.me/>

## 6. Jurisdiction and privacy evidence

The sources do not establish the owner/controller's establishment, activity
location, residence, citizenship, visitor targeting or monitoring. Azerbaijan is
therefore a provisional internal engineering baseline, not a conclusive
applicable-law or court-forum claim. Mandatory law and any contractual
law-choice effect remain subject to the actual nexus and agreement facts:
<https://frameworks.e-qanun.az/0/f_509.html>.

The current consolidated Personal Data Law supplies the project gates. Article
3.3 is a fact-specific personal/household exception and is not assumed. Article
7.5 supplies the paper-plus-identity-document and enhanced-electronic-signature
rights channels. Article 8.6 requires an EHIS consent/withdrawal determination;
Article 9.14 creates a separate licensing issue. Article 11.2 supplies the
collection-notice fields, and Article 12 sets working-day limits of seven,
possible additional seven, five for reasoned refusal and three for prior-
recipient notification. Articles 14 and 15 control cross-border transfer and
registration:

- <https://frameworks.e-qanun.az/19/f_19675.html>
- <https://president.az/az/articles/view/69619>
- <https://mincom.gov.az/az/qanunvericilik/lisenziyalasdirma/rabite-ve-informasiya-texnologiyalari-sahesinde-lisenziyalarin-verilmesi/lisenziya/ferdi-sahibkarlar-ucun>

Decision 237 is cited from its current consolidated text, including the 29
December 2024 clause 2.3 amendment. Exemptions require a clause-and-facts match;
no authority-issued exemption certificate is invented. Decision 149 controls the
registration package and is read with the 2022 authority-name amendment and
current Ministry registry. Decision 161 requires a current, amendment-aware
security mapping covering threats/protection level, software and instructions,
restoration, protection/project documentation, access and audit registers,
physical controls, licensed software, authentication/authorization, applicable
encryption/key requirements, certification and state expertise:

- <https://frameworks.e-qanun.az/21/f_21060.html>
- <https://mincom.gov.az/storage/pages/649/9b0e869640ba56d43615eef7906a4d08.pdf>
- <https://e-qanun.az/framework/49396>
- <https://mincom.gov.az/az/qanunvericilik/reyestrler/reyestrler>
- <https://mincom.gov.az/storage/pages/648/4b2105426aa7138d97d78c9e1cfb91c4.pdf>

Cross-border processing remains blocked pending the actual state-border fact and
separate Article 14.2.1 national-security, 14.2.2 receiving-law equivalence,
14.3 consent/life-health and 14.4 security findings for AWS and recipient-mail
paths. GDPR is EU-wide, not a Germany-only jurisdiction label. Its applicability
to the owner/controller remains contingent on Article 3 establishment, targeting
or monitoring facts; German hosting alone is not the trigger, and GDPR evidence
is not itself the Azerbaijan Article 14 equivalence determination:

- <https://eur-lex.europa.eu/eli/reg/2016/679/oj>
- <https://www.edpb.europa.eu/documents/guideline/guidelines-32018-on-the-territorial-scope-of-the-gdpr-article-3-version-adopted_en>

Constitution Articles 30/32 and Copyright Law Article 5(3)–(4) support the
privacy, intellectual-property, expression and copy-ownership distinctions:

- <https://president.az/en/pages/view/azerbaijan/constitution/>
- <https://frameworks.e-qanun.az/4/f_4167.html>

Logs and search queries are potential personal data. Raw-query persistence and
query analytics are disabled, query strings and secrets are redacted, and log
fields/retention are minimized. Special-category data is not requested and is
prohibited by policy, but free text can contain it; inadvertent receipt follows
restricted-access, quarantine, escalation and deletion controls.

## 7. Ownership, review, inventory, migration and records evidence

ISO 15489-1 describes records, record metadata, policies, assigned
responsibilities, monitoring, recurrent context analysis, records controls and
processes for creating, capturing and managing records. That evidence supports
attributable versioned decisions and migration evidence packs; it does not
dictate this project's numeric review intervals:
<https://www.iso.org/standard/62542.html>.

W3C's accessibility-statement guidance recommends identifying the evaluated
version, evidence, assessment method, approval/complaint route and publication
date, and notes that an accessibility-statement date older than one year may be
considered unmaintained. The project uses the shorter applicable interval when a
record is more volatile:
<https://www.w3.org/WAI/planning/statements/generator/>.

NIST SP 800-218 connects secure development to documented roles, provenance,
review, protected artifacts and repeatable verification. It supports a frozen
source manifest, quarantined unknowns, tested mappings, immutable approvals,
reconciliation and a demonstrated restoration path:
<https://csrc.nist.gov/pubs/sp/800/218/final>.

The 30/90/180/365-day schedules are explicit risk-based project maxima: current
contact and opportunity content changes fastest; active identity/legal content
needs quarterly review; assets/licences are reviewed semiannually; historical
records annually. Every inaccuracy, role change, correction/retraction,
rights/privacy concern, legal/provider change, security incident or broken
destination triggers immediate review regardless of the calendar.

## 8. Matrix result and reproducibility

The PDF builder extracts every SRS card's ID, title, priority, normative text,
printed page, preconditions and accountable roles, then reconciles the complete
priority sequence with backend Appendix A. No reviewed card names another `FR-*`
ID as a dependency; the matrix consequently preserves the 20 exact module-level
precondition profiles and prohibits invented inter-card edges.

The closed totals are:

- 264 unique ordered rows in 20 modules;
- 148 P0-MUST, 62 P1-SHOULD, 52 P2-CONDITIONAL and 2 P2-MAY;
- 222 applicable rows and 42 dormant rows;
- 179 direct-backend, 70 shared-contract and 15 frontend-led rows; and
- 31 explicitly retained SRS TOC/card-heading page differences.

Reproduction and consistency checks are:

```shell
python3 scripts/build_requirements_matrix.py \
  --srs-pdf /path/to/personal_academic_professional_website_srs.pdf \
  --backend-pdf /path/to/personal_academic_website_backend_specification.pdf \
  --output /tmp/requirements-matrix.json
cmp config/requirements-matrix.json /tmp/requirements-matrix.json
make scope-check
```

`make scope-check` validates the three schemas and semantic ledgers, then
rejects cross-artifact drift in source identity, owner, approvals, domain,
region, locale, feature states, all P2 applicability records and deployment
templates.

## 9. Decision boundaries and update triggers

The primary-domain selection does not claim that DNS registration or production
deployment has occurred. Feature activation in scope does not claim feature
implementation or release acceptance. Foundation approval does not claim WCAG
conformance, legal registration, a security assessment, a restoration exercise
or whole-site conformance.

A new version and affected-domain approvals are required when the owner changes
a domain, environment, language, maintainer role, feature state, jurisdiction,
provider, region, processing purpose, data field, retention period, content
disposition, review cadence or requirement applicability decision. The previous
record remains addressable and the last approved public snapshot remains the
rollback target.

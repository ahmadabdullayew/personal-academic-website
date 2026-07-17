# Foundation scope decisions 11–18

## 1. Decision authority and interpretation

This document records the finite project decisions for foundation items 11–18.
The normative machine-readable authority is `config/product-baseline.json`,
version `2.0.0`; its schema and validator reject missing, duplicated,
contradictory or silently changed decisions.

`Active` means that the capability is in the approved product scope and all of
its dependencies apply. It does not bypass implementation, evidence or release
gates. `Inactive` means that the capability, control, route and empty public
presentation are suppressed. An inactive P2 card can change state only through a
versioned decision after its recorded activation condition is satisfied.

The review used both supplied specifications at their recorded SHA-256 digests,
the existing architecture and environment contracts, and the official sources
listed in section 10. The SRS defines 52 P2-CONDITIONAL cards and two P2-MAY
cards. All 54 are decided individually in section 5 and in the machine baseline.

## 2. Item 11 — primary domain and deployment environments

The one public authority is `https://ahmadabdullayev.com`. The shorter
unhyphenated owner-name domain is the canonical origin.
`https://www.ahmadabdullayev.com` is only a path-and-query-preserving HTTP 308
redirect, never a second origin. HTTP redirects to HTTPS. Preview and staging
hosts never redirect into a state that makes their unpublished content
canonical.

The selected AWS application and durable-data region is `eu-central-1`, Europe
(Frankfurt), Germany. Before deployment, regional production, staging and
preview resources plus relational data, objects, queues, logs, backups and SES
delivery-event state must be configured there; application-managed cross-region
replication is prohibited unless separately approved. This is a binding target
configuration, not evidence that infrastructure has already been provisioned.
Outbound email necessarily traverses recipient mail systems, while CloudFront,
DNS, certificate-management and any other global, edge or out-of-region path
must be separately inventoried and disclosed. Germany is therefore a disclosed
prospective processing location, not a claim that every network hop remains
there or that the selected region alone establishes applicable law. The actual
controller/data-subject nexus, processor terms and any applicable transfer
mechanism must be determined before release.

| Environment | Authoritative origin                                 | Access and indexing                                           | Permitted data                                                                       |
| ----------- | ---------------------------------------------------- | ------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| local       | `http://localhost:8000`                              | developer machine only; not indexable                         | synthetic or explicitly sanitized development data                                   |
| test/CI     | `http://testserver`                                  | isolated automation only; disposable                          | deterministic synthetic fixtures                                                     |
| preview     | `https://pr-{change-id}.preview.ahmadabdullayev.com` | authenticated reviewers; authentication plus `noindex`        | ephemeral sanitized review data; delivery and integrations off                       |
| staging     | `https://staging.ahmadabdullayev.com`                | authenticated maintainers; authentication plus `noindex`      | production-shaped synthetic or irreversibly sanitized data; provider sinks/sandboxes |
| production  | `https://ahmadabdullayev.com`                        | public reads only for approved routes; private administration | public snapshots only at the public boundary; all other states access-controlled     |

Authentication is the confidentiality control for preview and staging;
`robots.txt` and `X-Robots-Tag: noindex, nofollow, noarchive` are defense in
depth, not access control. Production is the only environment authoritative for
public content.

## 3. Item 12 — active languages and default locale

English (`en`) is the sole active language and the default locale. It uses
unprefixed canonical routes, left-to-right direction and page-level `lang="en"`.
Text in another language retains the shortest correct element-level BCP 47 tag.
There is no language selector while only one locale is active, and no silent
machine-translated public variant is presented as approved content.

A further locale requires a complete owner-approved translation inventory,
independent draft/review/publication state, equivalent-route map, localized
titles/descriptions/social metadata, reciprocal alternates, staleness ownership,
and bidirectional-text testing when relevant. This is why FR-I18N-02, 03, 04 and
06 are inactive rather than partially displayed.

## 4. Item 13 — administration model and maintainer roles

The model is online single-owner administration with named, non-shared accounts,
deny-by-default operation authorization and no public registration. The initial
assignment is exactly one owner account for Ahmad Abdullayev; no administrator
or editor is invented.

| Role          | Initial accounts | Allowed operations                                                                                                                               | Explicit boundary                                                                                    |
| ------------- | ---------------: | ------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| owner         |                1 | all content operations; publish/unpublish/rollback; maintainer and role management; capability activation; approved sync; quality/release review | cannot bypass validation or required approvals; cannot expose secrets or non-public records          |
| administrator |                0 | all content operations; publish/unpublish/rollback; editor-account management; approved sync; quality/release review                             | cannot transfer ownership, alter the owner role, activate conditional scope or bypass validation     |
| editor        |                0 | create/edit drafts; quarantine uploads; relationships/order; preview; publication request                                                        | cannot publish, roll back, manage accounts/roles, activate integrations or approve quarantined files |

MFA is required for all three maintainer roles. Sessions expire after 30 minutes
of inactivity and after 12 hours absolutely, require reauthentication for
sensitive operations, and are invalidated after material credential or role
changes. Recovery is single-use, expiring, owner-channel verified and audited;
it invalidates existing sessions. Approval roles remain separate from account
roles: possessing an admin permission does not manufacture content, privacy,
security, accessibility or operations approval.

## 5. Item 14 — every optional and conditional card

The complete result is 12 active and 42 inactive cards. The table below follows
the SRS source order and uses the detailed card's printed start page, not a
physical PDF page or an approximate module range.

| ID             | Page | State    | Decision and exact activation condition                                                                                                                           | Accountable decision role |
| -------------- | ---: | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------- |
| FR-ABOUT-07    |   48 | inactive | No approved pronouns/pronunciation may be inferred; activate only from the owner's approved exact value or accessible asset.                                      | content                   |
| FR-ABOUT-09    |   51 | inactive | No approved media kit; activate with a rights-cleared accessible biography/headshot/topic inventory and usage policy.                                             | content                   |
| FR-RES-09      |   62 | inactive | No approved funding relationship; activate for an evidence-backed public funder, sponsor or grant relation.                                                       | content                   |
| FR-RES-10      |   63 | inactive | No research record triggers the statement; activate when approved ethics, limitation, access or responsible-use context is required.                              | content                   |
| FR-PUB-06      |   70 | inactive | No controlled contributor-role data; activate when evidence-backed roles preserve authorship and order.                                                           | content                   |
| FR-PUB-07      |   71 | inactive | No equal/corresponding-author assertion; activate only from publisher- or author-approved evidence.                                                               | content                   |
| FR-PUB-19      |   84 | inactive | No correction event; activate for a verified correction, erratum or material update with a dated notice.                                                          | content                   |
| FR-PUB-22      |   88 | inactive | No lawful open-access destination inventoried; activate with verified URL and accurate access-state label.                                                        | content                   |
| FR-PUB-23      |   89 | inactive | No distributable local file; activate after rights, version, accessibility and owner approval are recorded.                                                       | content                   |
| FR-PUB-24      |   90 | inactive | No publication/software relation; activate for an approved versioned software record or release.                                                                  | content                   |
| FR-PUB-25      |   91 | inactive | No publication/dataset relation; activate with approved identifier, access and licence state.                                                                     | content                   |
| FR-PUB-26      |   92 | inactive | No publication/presentation/media relation; activate when both canonical records and rights are approved.                                                         | content                   |
| FR-PUB-31      |   98 | inactive | No launch need for another citation format; activate a named format only after a tested lossless field mapping and media type exist.                              | content                   |
| FR-PUB-38      |  106 | inactive | No approved external metrics and analytics are off; activate only with provider, date, scope, limits, cache and failure policy approved.                          | content                   |
| FR-PROJ-05     |  116 | inactive | No team/institution attribution; activate with evidence-backed public relationships and approved wording.                                                         | content                   |
| FR-PROJ-09     |  121 | inactive | No repository/demo destination; activate with a verified public URL and accurate maintenance/status state.                                                        | content                   |
| FR-PROJ-13     |  125 | inactive | No software output; activate with canonical version, licence, repository, contribution and release metadata.                                                      | content                   |
| FR-PROJ-14     |  126 | inactive | No dataset output; activate with identifier, version, licence, access, documentation and stewardship metadata.                                                    | content                   |
| FR-CAREER-03   |  129 | inactive | No thesis/supervision record; activate from verified title, institution, degree state and approved public supervision data.                                       | content                   |
| FR-CAREER-09   |  136 | inactive | No visiting/fellowship record; activate when verified appointment type, institution and dates are public.                                                         | content                   |
| FR-ACADEMIC-01 |  143 | inactive | No teaching profile; activate from verified scope, role, institution, dates and audience.                                                                         | content                   |
| FR-ACADEMIC-02 |  144 | inactive | No course record; activate with verified course/role while excluding student and restricted material.                                                             | content                   |
| FR-ACADEMIC-04 |  146 | inactive | No mentoring/supervision record; activate with relationship evidence, privacy basis and any named person's consent.                                               | content                   |
| FR-ACADEMIC-05 |  147 | inactive | No award/honour record; activate with granting body, date, scope and evidence.                                                                                    | content                   |
| FR-ACADEMIC-06 |  148 | inactive | No grant record; activate with funder, identifier, role, dates, disclosure decision and research links.                                                           | content                   |
| FR-ACADEMIC-07 |  149 | inactive | No talk record; activate with title, event, role, date, status and approved destination/resources.                                                                | content                   |
| FR-ACADEMIC-08 |  150 | inactive | No presentation state/resource; activate with an approved talk plus rights-cleared slides/video/transcript/output.                                                | content                   |
| FR-ACADEMIC-09 |  151 | inactive | No public service record; activate when verified disclosure excludes confidential review, committee and personal data.                                            | content                   |
| FR-CONTENT-04  |  159 | inactive | No long-form article; activate with an owner-authored, reviewed, rights-cleared article under correction/revision policy.                                         | content                   |
| FR-CONTENT-07  |  162 | inactive | No special technical construct; activate a named code/math/citation/table/figure renderer only after semantic, accessibility and security tests.                  | content                   |
| FR-CONTENT-08  |  163 | inactive | No media appearance; activate with verified outlet, title, date, role, link and rights/privacy review.                                                            | content                   |
| FR-CONTENT-10  |  166 | active   | Atom and static social metadata are selected; generate both only from approved public snapshots.                                                                  | content                   |
| FR-DOC-07      |  173 | inactive | No multiple document variants; activate with two approved accessible variants and explicit audience/language/version/current labels.                              | content                   |
| FR-CONTACT-03  |  178 | active   | The form is the selected public method; production opens after SES identity, privacy, retention, abuse, idempotency, accessibility and failure tests pass.        | product                   |
| FR-INT-02      |  199 | inactive | No verified ORCID iD/import scope; activate only after identifier, field, credential, provenance, cache, retry, duplicate and conflict approval/tests.            | content                   |
| FR-INT-03      |  200 | inactive | No approved DOI record; activate only after DOI plus mapping, etiquette, cache, retry, provenance, duplicate and conflict approval/tests.                         | content                   |
| FR-ACC-12      |  237 | inactive | No time-based media; activation is mandatory before any applicable media release and requires captions, transcript and alternatives.                              | accessibility             |
| FR-I18N-02     |  248 | inactive | English only; activate after a second locale has independent complete workflow and ownership.                                                                     | content                   |
| FR-I18N-03     |  249 | inactive | One locale makes a selector misleading; activate with a second locale and explicit equivalent-route map.                                                          | content                   |
| FR-I18N-04     |  250 | inactive | No alternate route exists; activate with localized metadata, canonicals and reciprocal alternates.                                                                | content                   |
| FR-I18N-06     |  252 | inactive | No mixed-direction/RTL content; activate after bidi isolation, direction, font and assistive-technology tests.                                                    | content                   |
| FR-ADMIN-08    |  261 | active   | Full editorial media/document management is selected; every file stays quarantined until type, malware, rights, metadata, accessibility and approval checks pass. | product                   |
| FR-ADMIN-11    |  265 | active   | Scheduled publication/expiry is selected with UTC storage, explicit editorial timezone, idempotent jobs and last-public-snapshot preservation.                    | product                   |
| FR-ADMIN-14    |  268 | active   | Privileged administration, delivery, configuration and publication need attributable security/integrity evidence even with one initial account.                   | product                   |
| FR-ADMIN-16    |  270 | active   | Preview/staging/production promotion requires immutable validation, deployment, health and rollback status.                                                       | product                   |
| FR-SEC-02      |  273 | active   | Online administration is selected; every admin route/API authenticates before protected reads or mutations.                                                       | security                  |
| FR-SEC-04      |  275 | active   | The exact owner/admin/editor role set is selected with deny-by-default operations and no shared accounts.                                                         | security                  |
| FR-SEC-05      |  276 | active   | Online sessions use Secure, HttpOnly, SameSite cookies, CSRF protection, both expiries, logout and invalidation.                                                  | security                  |
| FR-SEC-06      |  277 | active   | Password-based privileged administration makes MFA and safe recovery mandatory before production access.                                                          | security                  |
| FR-SEC-09      |  281 | active   | Active uploads require size/type allow-lists, quarantine, inspection, non-executable storage, immutable identity and approval.                                    | security                  |
| FR-SEC-13      |  285 | inactive | No launch measurement purpose; activate only after a minimal event model, legal basis, notice, retention, access, deletion and provider review.                   | security                  |
| FR-SEC-14      |  286 | inactive | No public optional storage/embed requires preference UI; activate only with a separately approved purpose, equal reject and later withdrawal.                     | security                  |
| FR-SEC-16      |  289 | inactive | Embeds are prohibited; activate a specific provider only after four-domain review, click-to-activate and complete non-embed alternative.                          | security                  |
| FR-OPS-03      |  294 | active   | Contact, search, uploads, schedules and releases require accessible truthful progress, bounded idempotent retries and isolated failure.                           | operations                |

The two P2-MAY cards are FR-ABOUT-07 and FR-ABOUT-09. The other 52 rows are
P2-CONDITIONAL. This count is enforced independently of the row titles and
states.

## 6. Item 15 — contact method and delivery provider

The preferred route is a cookie-free form at `/contact/`; the owner's email
address is not published. Amazon SES in `eu-central-1` is the selected
production delivery provider; activation requires the recorded identity,
privacy, retention, security and operational gates. An outbound message then
necessarily traverses recipient mail infrastructure and is not represented as
region-confined. Inquiry type, sender name, reply email, subject, message and a
privacy acknowledgement are required. That acknowledgement records presentation
and acknowledgement of the collection notice only: it is not a legal basis and
does not replace a separately required consent channel. Marketing consent is
inactive and no newsletter/subscription purpose is combined with an inquiry.

The exact visitor acceptance point is durable normalized inquiry storage with a
retention deadline plus one durably queued idempotent delivery job. The response
says only “accepted for processing”; it never says delivered. Field errors
preserve valid input. Honeypot/timing, rate/reputation and duplicate controls do
not make an inaccessible challenge the sole defense. SES failure creates a
delivery event and bounded retry, not false success. SES sending-domain
verification, DKIM, bounce/complaint handling, production access and the secret
recipient destination are deployment gates, not reasons to publish placeholders.

## 7. Item 16 — site-wide search

Public search is active at `/search/` and uses PostgreSQL full-text search. The
index source is the approved published snapshot, never mutable draft tables.
Indexed types are profile; research; publications; projects/software/datasets;
career/academic activities; and news/articles/talks/media/documents. Draft,
private, restricted, embargoed, revoked, deleted and administrative states are
excluded from the index, suggestions, counts, facets, caches and logs.

Ranking follows the backend baseline: exact title/identifier, title/name,
keyword/theme/author, summary/body, verified recency/featured state, then
canonical date and stable-ID tie-break. Queries require no public cookie and are
not behavioral analytics. A search failure leaves canonical pages and navigation
available. Raw search queries are never persisted; security logging is redacted
and minimized without retaining the raw query.

## 8. Item 17 — ORCID and Crossref synchronization

Both synchronization capabilities are inactive. ORCID lacks an owner-verified iD
and approved public-field scope. Crossref lacks an owner-approved DOI-bearing
publication inventory. No identifier, record or credential is invented.

When separately activated, synchronization is an explicit maintainer-triggered
candidate import. Provider data carries source, retrieval time and
raw/normalized provenance; it never silently overwrites approved local truth.
Activation requires normalization, mapping, cache/conditional request,
rate-limit, retry, duplicate, conflict, stale-data, audit and mock-provider
tests. ORCID requires the verified iD and appropriate credentials; Crossref
requires at least one approved normalized DOI and responsible API
identification.

## 9. Item 18 — analytics, cookies, embeds, feeds and social previews

| Capability                               | Decision               | Consequence                                                                                                                                             |
| ---------------------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| visitor analytics                        | inactive               | no analytics script, pixel, event stream, query analytics or analytics identifier                                                                       |
| public nonessential cookies/storage      | inactive               | no public consent banner because there is nothing optional to accept or reject                                                                          |
| authenticated admin session/CSRF cookies | active                 | scoped to the protected administration purpose with secure lifecycle controls                                                                           |
| third-party embeds                       | inactive               | use an approved local thumbnail/description, transcript where applicable and direct link                                                                |
| Atom feed                                | active at `/feed.atom` | RFC 4287 output from current approved public news/articles only; stable IDs and canonical links                                                         |
| social previews                          | active                 | server-rendered page-specific Open Graph title, description, canonical URL and approved image/alternative; no client script, cookie or tracking request |

A future analytics, optional storage or embed decision cannot be smuggled in as
a template change. It requires a new purpose-specific scope record and the
applicable content, accessibility, privacy, security, legal and operations
evidence.

## 10. Evidence synthesis and decision limits

1. The SRS establishes the P2 activation semantics on printed page 1, the
   public/truth/continuity invariants on pages 6–7, the 54 detailed P2 cards at
   the pages in section 5, and the relevant search, integration, accessibility,
   internationalization, administration, security and operations cards through
   page 294.
2. The backend specification selects the full backend profile on printed pages
   4–5, deployment boundaries on pages 6–7, authentication/security/privacy on
   pages 22–24, contact on page 25, search on pages 26–27, ORCID/Crossref on
   page 28 and deployment/acceptance on pages 32–36.
3. [BCP 47 language tags and HTML language declarations](https://www.w3.org/International/articles/language-tags/)
   support the `en` and element-level tagging contract. They do not establish
   that untranslated content exists.
4. [AWS's region catalogue](https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html)
   identifies `eu-central-1` as Europe (Frankfurt), Germany with three
   Availability Zones.
   [RDS regional documentation](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.RegionsAndAvailabilityZones.html)
   states that regions are isolated and data is not automatically replicated
   across them.
   [AWS data-residency documentation](https://aws.amazon.com/compliance/data-protection/)
   explains customer region choice; it does not replace the project's legal
   transfer and processor assessment.
5. [Amazon SES region documentation](https://docs.aws.amazon.com/ses/latest/dg/regions.html)
   makes credentials, verified identities, quotas and suppression state
   regional. This supports using the same selected region and treating identity,
   DKIM and production sending access as explicit gates.
6. [PostgreSQL full-text-search documentation](https://www.postgresql.org/docs/current/textsearch.html)
   covers parsing, queries, ranking, highlighting and indexes. The expected
   single-owner corpus does not justify a second search data store; corpus and
   query benchmarks remain implementation acceptance evidence.
7. [ORCID Public API registration guidance](https://info.orcid.org/documentation/integration-guide/registering-a-public-api-client/)
   requires credentials tied to an ORCID record and recommends sandbox testing.
   [Crossref REST API guidance](https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/)
   permits public access. Neither provider makes retrieved metadata locally
   authoritative or proves that it belongs to this owner.
8. [RFC 4287](https://www.rfc-editor.org/info/rfc4287/) defines Atom feed and
   entry metadata, stable IDs, timestamps and link semantics. The feed decision
   uses this open format without enabling tracking.
9. [The Open Graph protocol](https://ogp.me/) defines the static metadata used
   for link previews. Static metadata is a published representation; it does not
   require an embedded third-party script.

The literature and standards constrain interoperability, privacy, security and
truthfulness. They do not mathematically prove that one domain, language or
feature set is universally best. Those values are explicit owner-controlled
project decisions, made auditable instead of being disguised as external facts.

## 11. Consistency proof

1. Cardinality is closed: 264 SRS cards exist; the P2 subset is exactly 54,
   partitioned into 52 conditional and two optional cards, then partitioned
   again into 12 active and 42 inactive decisions.
2. Identity is closed: every P2 ID, title, priority and printed start page is
   checked against a fixed reviewed-source tuple; omission, duplication,
   reordering or page drift fails validation.
3. Accountability is closed: every row has one decision owner from the six
   approved domains, a non-empty rationale and a non-empty activation condition.
4. Dependency closure holds: contact activates its form decision; uploads
   activate secure upload handling; online administration activates
   authentication, RBAC, session, MFA, audit and release status; asynchronous
   operations activate loading/retry; Atom/social output activates
   FR-CONTENT-10.
5. Negative closure holds: inactive ORCID maps to inactive FR-INT-02; inactive
   Crossref maps to inactive FR-INT-03; inactive analytics, optional public
   storage and embeds map to inactive FR-SEC-13, 14 and 16; one locale maps to
   inactive multilingual cards.
6. Boundary closure holds: production alone is public authority; preview and
   staging require authentication and noindex; search/feed/social outputs derive
   only from public snapshots; private states never become derivatives.
7. Runtime drift is detectable: the schema fixes the primary origin, region,
   locale, provider and feature states, while cross-field validation enforces
   their relationships. Focused negative tests mutate each class of invariant
   and require rejection.

Accordingly, items 11–18 contain no unrecorded choice. A later change is a new
versioned decision with evidence; it is not an ambiguity in this baseline.

# Initial content inventory and migration plan

## 1. Inventory result

This record resolves foundation item 21. The inventory is complete for the
content families defined by the supplied SRS, backend specification and current
repository state. It distinguishes content that actually exists from target
content types; a target slot is not represented as existing source material.

At baseline version 1.0.0:

- 3 records are approved public foundation data: owner name, current canonical
  routes and the English locale baseline;
- 4 records are temporary public foundation copy with an explicit retirement or
  replacement disposition;
- 19 target families have no owner-approved source and are held unpublished;
- 5 records require new drafts and all named activation/publication gates; and
- 1 record is an approved internal governance record.

No academic title, role, affiliation, biography, research claim, publication,
project, degree, experience, activity, CV or personal asset is inferred from a
filename, user account, repository path or the generic website specifications.

## 2. Ordered 32-record inventory

| ID       | Canonical content                                            | Current evidence state                                             | Migration disposition      | Target state and exact release gate                                                                                     |
| -------- | ------------------------------------------------------------ | ------------------------------------------------------------------ | -------------------------- | ----------------------------------------------------------------------------------------------------------------------- |
| `CI-001` | Canonical owner name                                         | Verified as Ahmad Abdullayev in the product baseline               | Import verified            | Approved public; every human- and machine-readable identity uses the exact canonical value.                             |
| `CI-002` | Temporary verified-details notice                            | Observed in `src/templates/home.html`                              | Retire temporary           | Temporary public; remove when approved biography and positioning content launch.                                        |
| `CI-003` | Temporary primary-audience list                              | Observed in product baseline/home template                         | Retire temporary           | Temporary public; remove before content-complete launch.                                                                |
| `CI-004` | Temporary visitor-goal list                                  | Observed in product baseline/home template                         | Retire temporary           | Temporary public; remove before content-complete launch.                                                                |
| `CI-005` | Generic foundation description/footer                        | Observed in `src/templates/base.html`                              | Replace with approved copy | Temporary public; accurate positioning and policy navigation replace it before launch.                                  |
| `CI-006` | Preferred names and disambiguation                           | No owner-approved source supplied                                  | Hold unpublished           | Omitted until approved non-sensitive disambiguation evidence exists.                                                    |
| `CI-007` | Titles, roles and affiliations                               | No owner-approved source supplied                                  | Hold unpublished           | Omitted until organization, title, dates, state and evidence are approved.                                              |
| `CI-008` | Short biography                                              | No owner-approved source supplied                                  | Hold unpublished           | Omitted until the source and material claim evidence are approved.                                                      |
| `CI-009` | Medium, extended and media biographies                       | No owner-approved source supplied                                  | Hold unpublished           | Omitted until all variants derive from one approved fact set.                                                           |
| `CI-010` | Portrait and pronunciation assets                            | No approved asset supplied                                         | Hold unpublished           | Omitted until consent, copyright, licence, attribution and accessibility treatment are recorded.                        |
| `CI-011` | Expertise                                                    | No owner-approved source supplied                                  | Hold unpublished           | Omitted until every material expertise claim has evidence.                                                              |
| `CI-012` | Research overview, areas, questions and methods              | No owner-approved source supplied                                  | Hold unpublished           | Omitted until specialist and public explanations are approved.                                                          |
| `CI-013` | Research activities, collaborators, institutions and funding | No owner-approved source supplied                                  | Hold unpublished           | Omitted until dates, contribution, third-party basis and funding terms pass review.                                     |
| `CI-014` | Publication core metadata and identifiers                    | No owner-approved source supplied                                  | Hold unpublished           | Omitted until titles, venues, status, dates and identifiers are approved and deduplicated.                              |
| `CI-015` | Publication authors, contributions, versions and resources   | No owner-approved source supplied                                  | Hold unpublished           | Omitted until author order, roles, version/resource rights and correction state are verified.                           |
| `CI-016` | Projects, memberships, outcomes and evidence                 | No owner-approved source supplied                                  | Hold unpublished           | Omitted until contribution, confidentiality, attribution and evidence pass review.                                      |
| `CI-017` | Software and datasets                                        | No owner-approved source supplied                                  | Hold unpublished           | Omitted until licence, release, repository, access, security and ethical limits pass.                                   |
| `CI-018` | Education and theses                                         | No owner-approved source supplied                                  | Hold unpublished           | Omitted until institution, program, state, dates, thesis and third-party basis are approved.                            |
| `CI-019` | Experience and appointments                                  | No owner-approved source supplied                                  | Hold unpublished           | Omitted until position, organization, dates, current state and outcomes are approved.                                   |
| `CI-020` | Teaching, courses and mentoring                              | No owner-approved source supplied                                  | Hold unpublished           | Omitted; restricted material and learner identities remain excluded absent a publication basis.                         |
| `CI-021` | Awards, grants, talks and service                            | No owner-approved source supplied                                  | Hold unpublished           | Omitted until title, organization, role, date, state and evidence are approved.                                         |
| `CI-022` | News, articles and media                                     | No owner-approved source supplied                                  | Hold unpublished           | Omitted until authorship, source, dates, external rights, embed status and corrections pass.                            |
| `CI-023` | Current CV and accessible equivalent                         | No owner-approved document supplied                                | Hold unpublished           | Omitted until the current approved version is privacy-safe and has an accessible equivalent.                            |
| `CI-024` | Documents, images, audio, video and supplements              | No owner-approved assets supplied                                  | Hold unpublished           | Omitted until checksum, type, malware, rights, privacy and accessibility checks pass.                                   |
| `CI-025` | Contact form and collaboration copy                          | Contact/SES feature decision exists; final public copy does not    | Create after gates         | Draft required; registration/exemption, transfer, provider, notice, consent, retention and delivery evidence must pass. |
| `CI-026` | Privacy and storage notice                                   | Official legal sources exist; processing-specific draft does not   | Create after gates         | Draft required; it must exactly match fields, purposes, recipients, region, retention, rights and route.                |
| `CI-027` | Rights, licence and attribution notice                       | Official legal sources exist; site-specific draft does not         | Create after gates         | Draft required; no ownership or licence claim may exceed item-level evidence.                                           |
| `CI-028` | Rights/privacy/impersonation/inaccuracy/takedown route       | SRS/legal sources exist; tested public workflow does not           | Create after gates         | Draft required; report, protect, acknowledge, triage, contain, decide and escalate paths must pass.                     |
| `CI-029` | Routes, redirects and navigation labels                      | Root route and shell observed in repository                        | Import verified            | Approved public; active paths are unique, canonical, public-authorized and loop-free.                                   |
| `CI-030` | Structured metadata, Atom and static social previews         | Feature decision exists; approved academic source content does not | Create after gates         | Draft required; derive only from the exact approved public snapshot and assets.                                         |
| `CI-031` | English source-locale content and metadata                   | English baseline verified                                          | Import verified            | Approved public; every public route and metadata representation declares English consistently.                          |
| `CI-032` | Legal sources, governance, revisions and approvals           | This versioned machine baseline and owner direction                | Create reference           | Approved internal; validation passes and decisions remain append-only and attributable.                                 |

The detailed owner, approval-domain, review-class, rights, privacy, date and
source-reference fields remain in the machine baseline. These table summaries do
not replace them.

## 3. Disposition semantics

1. **Import verified** means transform an identified source value into a
   versioned draft, verify the transformed value, and separately approve it. It
   never means bypassing the publication workflow.
2. **Retire temporary** means the current narrow foundation copy may remain only
   until its stated replacement gate. It is not migrated into canonical academic
   content.
3. **Replace with approved** means the observed generic copy is a known
   placeholder and cannot survive content-complete launch unchanged.
4. **Hold unpublished** means there is no sufficient owner-approved source. The
   route, control, metadata, feed entry and empty section are omitted.
5. **Create after gates** means the source requirements exist but the
   site-specific content must be written from the final enabled processing and
   then reviewed.
6. **Create reference** means the internal governance record is versioned and
   auditable; it is not automatically public policy text.

## 4. Ordered migration plan

The plan status is `approved-plan-not-executed`. Execution begins only when a
real source is supplied. Every step has an explicit rollback path; production
import requires owner approval and a dry run.

### `MP-01` — Freeze and identify sources

Create a read-only export and manifest containing source owner, extraction time,
format, record/relationship/asset counts and cryptographic checksums. Exit only
when each source is immutable and identifiable. Roll back by discarding the
working copy and recreating it from the frozen export.

### `MP-02` — Discover and enumerate

Map every discovered record and asset to one of `CI-001` through `CI-032` or to
a reasoned exclusion record. Unmapped material is a failed inventory. Roll back
to the prior inventory revision and rerun discovery.

### `MP-03` — Classify rights, privacy and visibility

Assign rights status, privacy class, intended visibility,
consent/confidentiality evidence and disposition. Unknowns go to
quarantine/hold, never the candidate public set. Roll back by removing the
affected batch from every public candidate.

### `MP-04` — Normalize and deduplicate canonical facts

Normalize dates, identifiers, names and relationships; identify conflicts; and
select one canonical key per fact. Display text cannot become a second source of
truth. Roll back by discarding normalized candidates while retaining the frozen
source.

### `MP-05` — Transform into versioned drafts

Use a versioned field mapping to create schema-valid drafts with source IDs,
field provenance and migration batch ID. No draft is public. Roll back by
deleting the unapproved batch, not by modifying the source.

### `MP-06` — Verify facts and relationships

Audit claims, dates, lifecycle state, authorship order, contributions,
identifiers and relationships against evidence. Conflicts remain explicit and
unpublished. Roll back by rejecting the draft revision; the active public
snapshot is unchanged.

### `MP-07` — Validate assets and accessibility

Verify checksum, detected type, malware result, licence, attribution, alt text,
caption, transcript, accessible document equivalent and public filename. Failed
assets remain quarantined and dependent public actions are removed.

### `MP-08` — Complete legal, privacy and rights review

Review the candidate public set, processing inventory, registration/exemption,
Article 14 transfer evidence, provider terms, notices, retention, consent,
licences, attribution and takedown route. Roll back by keeping affected content
or processing inactive.

### `MP-09` — Approve one immutable release candidate

Product, content, accessibility, security, privacy and operations decisions must
identify one immutable revision and checksum set. A rejection preserves the last
approved release.

### `MP-10` — Publish atomically

Activate the approved snapshot through one transaction or an equivalent atomic
workflow after verifying the rollback target. Any failure restores/reactivates
the last verified snapshot.

### `MP-11` — Rebuild derivatives and reconcile

Search, canonical routes, redirects, sitemap, Atom, structured data, social
previews, caches and public assets must use the same published revision.
Reconcile source/target record counts, relationship counts, asset checksums,
route uniqueness, public/private boundary and derivative snapshot identity.
Unexplained variance fails the migration. Roll back by serving the last coherent
derivative set.

### `MP-12` — Archive evidence and close

Archive the immutable source manifest, mappings, validation reports, approvals,
release identifier, reconciliation and restoration demonstration. Every source
item must have a final disposition. A later correction opens a new revision; it
never rewrites the closed evidence pack.

## 5. Migration acceptance equations

For each source family, the reconciliation invariant is:

`source count = imported + merged-as-duplicate + held + excluded-with-reason`

For every imported asset:

`source checksum = staged checksum = approved-object checksum`

For every public derivative:

`derivative.source_revision_id = active_published_revision_id`

A migration is rejected if a count has unexplained variance, an identifier or
route is duplicated, a relationship is orphaned, a checksum changes without a
recorded transformation, an unapproved/private field is public, a required right
or alternative is absent, or restoration is not demonstrated.

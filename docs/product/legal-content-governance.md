# Legal jurisdiction and content-governance baseline

## 1. Selected baseline and unresolved applicability

This record resolves foundation items 19 and 20 as project-governance
decisions. The machine-readable authority is
`config/foundation-governance.json` version 1.0.0.

1. The Republic of Azerbaijan (`AZ`) is the **provisional internal engineering
   and governance baseline**. It is not represented as a conclusive statement
   of legally applicable law.
2. The controller's establishment, activity location, residence or citizenship,
   visitor targeting, monitoring and other legally relevant nexus facts are not
   established by the supplied specifications. Those facts and the resulting
   applicable-law analysis are production personal-data gates.
3. No enforceable choice of law or court forum is asserted. Mandatory law is
   preserved. Any contractual choice-of-law effect, procedural competence and
   forum require their own facts and legal determination.
4. Amazon Web Services `eu-central-1`, Europe (Frankfurt), Germany (`DE`) is the
   selected regional-resource location. Selection is not deployment evidence.
   Regional services must be configured there, and application-managed
   cross-region replication is prohibited unless separately approved and
   documented.
5. Region evidence is service-specific. Runtime and relational data, objects and
   backups, queues, logs, SES state, DNS/CDN/certificates, control-plane metadata,
   support and subprocessors, account/billing information, legal demands and the
   recipient mailbox path each require an individual location and transfer
   record. No absolute “region lock” is claimed.
6. The contact form is the only selected **direct visitor-submission channel**.
   Security logs and search queries can also be personal data. Public search,
   Atom and static social previews use approved public content only. Raw search
   queries are not retained.
7. Analytics, nonessential public cookies, third-party embeds, SES open/click
   tracking, ORCID synchronization and Crossref synchronization are inactive.
   Administrative session cookies and server-side processing remain disclosed
   and independently assessed.
8. GDPR applicability is `contingent-pending-article-3-analysis`. German hosting
   is a processing-location fact; it does not by itself place the owner or
   controller within GDPR Article 3.

## 2. Evidence synthesis and source register

The supplied SRS and backend specification establish the functional and records
baseline: canonical identity, evidence-backed claims, provenance, lifecycle,
review accountability, immutable revisions, audit, rights records, policy
publication, takedown, migration reconciliation and atomic publication. The
following official sources support legal propositions and release gates; they do
not invent missing nexus facts or activate a feature.

| Source ID | Proposition used | Project consequence |
| --- | --- | --- |
| [`LAW-AZ-CONSTITUTION-30-32`](https://president.az/en/pages/view/azerbaijan/constitution/) | Articles 30 and 32 protect intellectual property, private life and personal information, including correction or elimination remedies. | Claims, rights, privacy and correction remain governed records. |
| [`LAW-AZ-PERSONAL-DATA-998-IIIQ`](https://frameworks.e-qanun.az/19/f_19675.html) | Articles 3.3, 7.5, 8.6, 9.12, 9.14, 11.2, 12, 14 and 15 establish fact-specific scope, channels, audit, licensing, notice, rights, transfer and registration requirements. | Every corresponding determination and evidence item is a production gate. |
| [`LAW-AZ-CABINET-237`](https://frameworks.e-qanun.az/21/f_21060.html) | Current consolidated clauses 2.1–2.7 define fact-specific registration exemptions; the current text includes the 29 December 2024 amendment to clause 2.3. | No exemption is inferred from a small site or owner status; clause and facts must match. |
| [`LAW-AZ-CABINET-149`](https://mincom.gov.az/storage/pages/649/9b0e869640ba56d43615eef7906a4d08.pdf) | Decision 149 defines the registration process and evidence package. | Prepare the owner, basis, purpose, categories, safeguards, users, transfer, audit and rights evidence. |
| [`LAW-AZ-CABINET-149-161-2022-AMENDMENT`](https://e-qanun.az/framework/49396) | Decision 137 of 2022 updates the competent-ministry name in Decisions 149 and 161. | Historical PDFs are read with the current authority-name amendment. |
| [`LAW-AZ-CABINET-161`](https://mincom.gov.az/storage/pages/648/4b2105426aa7138d97d78c9e1cfb91c4.pdf) | Decision 161 supplies specific, amendment-sensitive protection requirements. | Produce a clause-level implementation and evidence mapping; generic “secure” language is insufficient. |
| [`LAW-AZ-EHIS-DIGITAL-CONSENT`](https://president.az/az/articles/view/69619) | The EHIS regulation includes the Digital Consent subsystem used with Personal Data Law Article 8.6. | Determine the required consent and withdrawal channel before consent-dependent collection. |
| [`AUTHORITY-AZ-PERSONAL-DATA-LICENSING`](https://mincom.gov.az/az/qanunvericilik/lisenziyalasdirma/rabite-ve-informasiya-texnologiyalari-sahesinde-lisenziyalarin-verilmesi/lisenziya/ferdi-sahibkarlar-ucun) | The Ministry publishes the licensing route for forming personal-data resources and creating or servicing systems. | Resolve Article 9.14 licensing separately from registration. |
| [`AUTHORITY-AZ-PERSONAL-DATA-REGISTRY`](https://mincom.gov.az/az/qanunvericilik/reyestrler/reyestrler) | The Ministry publishes the current personal-data information-system registry route. | Recheck and archive the current authority route at release. |
| [`LAW-AZ-PRIVATE-INTERNATIONAL-LAW`](https://frameworks.e-qanun.az/0/f_509.html) | Articles 1 and 24–27 distinguish internal policy from agreement-based contractual choice and preserve mandatory-law analysis. | Do not label the provisional baseline as conclusively governing law or forum. |
| [`LAW-AZ-COPYRIGHT-115-IQ`](https://frameworks.e-qanun.az/4/f_4167.html) | Article 5(3)–(4) distinguishes protected expression and copyright from ideas and ownership or possession of a copy. | Require item-level authorship, licence and attribution evidence. |
| [`LAW-EU-GDPR-2016-679`](https://eur-lex.europa.eu/eli/reg/2016/679/oj) | Article 3 supplies establishment, offering-of-goods-or-services and monitoring tests. | Record GDPR as contingent; hosting location alone is not the test. |
| [`GUIDANCE-EU-EDPB-ARTICLE-3`](https://www.edpb.europa.eu/documents/guideline/guidelines-32018-on-the-territorial-scope-of-the-gdpr-article-3-version-adopted_en) | EDPB Guidelines 3/2018 explain the Article 3 territorial-scope tests. | Complete a factual establishment/targeting/monitoring analysis if EU-facing processing is contemplated. |
| [`PROVIDER-AWS-REGIONS`](https://docs.aws.amazon.com/global-infrastructure/latest/regions/aws-regions.html) | AWS identifies `eu-central-1` as Europe (Frankfurt), Germany, with three Availability Zones. | This proves region identity, not every processing path or deployment. |
| [`PROVIDER-AWS-DATA-PRIVACY`](https://aws.amazon.com/compliance/data-privacy-faq/) | AWS describes customer-content region choice while distinguishing account data, resource metadata, service behavior and legal demands. | Archive terms and actual service configuration; do not claim an absolute content lock. |
| [`PROVIDER-AWS-SES-REGIONS`](https://docs.aws.amazon.com/ses/latest/dg/regions.html) | SES identities, credentials, suppression and feedback settings are region-specific. | Configure and evidence the selected SES region, while separately recording recipient delivery paths. |
| [`PROVIDER-AWS-SES-DATA-PROTECTION`](https://docs.aws.amazon.com/ses/latest/dg/data-protection.html) | AWS warns against sensitive data in tags/names and documents opportunistic TLS as the SES default. | Prohibit personal data in resource metadata; require TLS or send only a minimal notification with secure administrative retrieval. |

The entries record official URL, language, translation status, reviewed/retrieved
date, currency note and proposition-to-provision mapping. They do **not** claim
immutable capture: no source-content digest was recorded for this review. Before
production reliance, every mutable source is re-retrieved and archived with its
source ID, official URL, timestamp, SHA-256 or stable instrument/archive
identity, official language and translation status, and amendment-through or
currency status. Provider documentation is evidence of provider statements, not
legislation. The register is reviewed every 90 days and on every legal, nexus,
provider, region, subprocessor, purpose, field, recipient, retention or feature
change.

## 3. Exact legal and privacy controls

1. **Applicable-law gate.** Before production personal-data processing, record
   the controller establishment/activity nexus, relevant visitor populations,
   targeting or monitoring, actual processing locations and the resulting
   applicable-law analysis. The Article 3.3 household/personal-use exception is
   not relied upon without a clause-specific determination.
2. **System owner.** Ahmad Abdullayev is the project-recorded information-system
   owner. Provider/operator status and contract terms are evidenced separately.
3. **Registration.** Registration is the conservative default before production
   collection. An exemption requires a documented match to the exact operative
   Decision 237 clause and facts, with competent-authority guidance where needed;
   no unsupported authority-issued “exemption record” is assumed.
4. **Licensing.** Personal Data Law Article 9.14 licensing applicability remains
   undetermined. Resolve and evidence it before operation. Registration does not
   answer the licensing question.
5. **Consent channel.** A privacy acknowledgment records notice acknowledgment;
   it is not represented as legal consent. Determine Article 8.6 and EHIS/Digital
   Consent applicability before collection. When consent is the basis, retain
   the legally required consent and withdrawal evidence through the applicable
   channel.
6. **Collection notice.** Before collection, disclose owner/operator identity,
   processing purpose and legal basis, protection level, conformity-certificate
   and state-expertise status, intended users and exchange systems, and statutory
   data-subject rights, as required by Article 11.2.
7. **Rights channels and deadlines.** Implement the Article 7.5 paper application
   with identity document and enhanced-electronic-signature request channels.
   Respond within seven working days; extend by no more than seven working days
   when third-party consultation is necessary; give a reasoned refusal within
   five working days; and notify prior recipients of required measures within
   three working days. Minimize and protect identity evidence and exclude other
   people's personal data from responses.
8. **Certification and state expertise.** Resolve conformity-certificate,
   system/project-documentation and state-expert-examination applicability,
   obtain required evidence before operation, and disclose status at collection.
9. **Decision 161 security.** Maintain a current clause mapping and evidence for
   threat/protection-level assessment, approved software and instructions,
   restoration, protection and project documentation, access/security/audit
   registers, physical and data-centre controls, licensed software, role-based
   authentication/authorization, the applicable encryption/key requirement,
   certification and state expertise. Exclude repealed clauses and incorporate
   amendments.
10. **Audit and minimization.** Map every contact field, log field, query,
    recipient, operation and retention period to a declared purpose. Apply the
    Article 9.12 audit requirement without logging message bodies, credentials,
    secrets or unnecessary query strings.
11. **Article 14 transfer gate.** Processing remains blocked until the actual
    crossing-of-Azerbaijan-border fact and separate findings for Article 14.2.1
    national security, 14.2.2 receiving-law equivalence, 14.3 consent or
    life/health exception, and 14.4 security are recorded. Assess AWS and
    recipient-mailbox paths. GDPR status alone is not an Article 14 equivalence
    determination.
12. **AWS and SES controls.** Archive service terms/DPA and configuration
    evidence. Prohibit personal data in resource IDs, names, tags and free-form
    metadata. Disable SES open/click tracking. Require delivery TLS or send only
    a minimal notification and keep substantive inquiry content in the secured
    administrative system.
13. **Search and logs.** Search indexes approved public content only, query
    analytics and raw query persistence are disabled, secrets/query strings are
    redacted, and access/security log fields and retention are minimized and
    fixed.
14. **Inadvertent special-category data.** Special-category data is not requested
    and submission is prohibited by policy, but free text can still contain it.
    Inadvertent receipt triggers restricted access, quarantine, escalation and
    deletion. Automated decision-making and personal-data sale or brokerage
    remain prohibited.
15. **Policy and storage notice.** Publish the privacy notice before contact
    collection. No public consent interface is active while nonessential public
    storage is inactive; administrative-session cookies and server processing
    are still disclosed and assessed. Publish the site-use/rights and reporting
    routes at launch.
16. **Change gate.** Analytics, optional storage, embeds, ORCID or Crossref cannot
    activate through configuration alone. The scope record, processing
    inventory, applicable-law/privacy review, policy delta, source archive and
    tests must identify the same release candidate.

## 4. Content ownership and approval

Ahmad Abdullayev is the canonical editorial owner. One person currently fills
four distinct operational functions; the decisions remain distinct even when the
assignee is the same:

| Function                      | Assignee         | Accountable result                                                                        |
| ----------------------------- | ---------------- | ----------------------------------------------------------------------------------------- |
| Content Maintainer            | Ahmad Abdullayev | Canonical draft, evidence and provenance are complete.                                    |
| Academic Content Approver     | Ahmad Abdullayev | Meaning, facts, dates, currency and public claims are approved.                           |
| Privacy Approver              | Ahmad Abdullayev | Personal data, rights, consent, retention, policies and third-party effects are approved. |
| Technical Operations Approver | Ahmad Abdullayev | Only the approved immutable revision is published and rollback remains possible.          |

The canonical lifecycle is:

`draft → fact-review → rights-privacy-review → approved → published → superseded-or-archived`

Approval by silence is not a transition. Publication is a second decision after
content approval. A failed derivative or deployment leaves the last valid public
snapshot intact.

Every governed record contains its canonical key, editorial owner, source and
provenance, rights status, privacy classification, lifecycle and visibility,
review class, last reviewer/time, approval record and revision identifier.
Missing evidence produces omission or an explicit draft; it never produces a
substitute claim.

## 5. Review schedules

The intervals are maximum periods, not targets that override an event trigger.
The due date is the last substantive review date plus the exact interval.

| ID       |  Maximum | Content class                                                                                               | Overdue action                                                   |
| -------- | -------: | ----------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| `RG-030` |  30 days | Contact routes, opportunities, temporary launch copy, active calls to action and incident-sensitive notices | Remove or unpublish time-sensitive claims until reviewed.        |
| `RG-090` |  90 days | Identity, current roles, active research/publications/CV, legal, privacy and policy controls                | Block a new release and require owner review.                    |
| `RG-180` | 180 days | Assets, licences, attribution, localized variants and stable supporting material                            | Block replacement publication and review continued availability. |
| `RG-365` | 365 days | Completed education, historical roles and other archival dated records                                      | Queue a content audit before the next release.                   |

Seven events override the calendar immediately:

1. `ER-001`: reported inaccuracy—contain misleading publication immediately;
   triage within two business days.
2. `ER-002`: role, affiliation, contact, availability or opportunity change—
   review every dependent representation at the effective time.
3. `ER-003`: correction, withdrawal, retraction or identifier conflict—freeze
   automatic propagation until owner review.
4. `ER-004`: rights, privacy, withdrawal, impersonation or takedown concern—
   acknowledge within two business days, preserve evidence and restrict where
   risk warrants.
5. `ER-005`: law, provider, region, purpose, field or subprocessor change—
   complete impact review before activation.
6. `ER-006`: incident or unauthorized exposure—contain immediately and start the
   incident record.
7. `ER-007`: broken route, destination or asset—restore, redirect or remove the
   broken claim while preserving history.

## 6. Publication acceptance rule

A content item is publishable only when its schema is valid; source and
provenance are traceable; factual, rights, privacy and accessibility gates
applicable to that item pass; the review date is current; an approval identifies
the exact revision; and public-boundary tests prove that no private, draft,
restricted, embargoed, revoked or unapproved field reaches HTML, APIs, search,
feeds, sitemaps, social previews, caches, logs or files.

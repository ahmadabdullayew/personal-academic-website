# Foundation literature and standards review

- Review date: 2026-07-17
- Decision scope: repository foundation, architecture, ownership, audiences and
  goals
- Accountable decision owner: Ahmad Abdullayev
- Evidence classes: standards, official specifications, official product
  documentation and peer-reviewed empirical research

This synthesis is supported by the exact
[search/screening and extraction record](foundation-review-protocol.md) and the
[weighted component matrices, sensitivity and cost record](architecture-options-matrix.md).

## 1. Review questions

1. Which architecture best protects truthful public state while supporting
   administration, accessibility, discovery, APIs, integrations and recovery?
2. Which persistence, search, queue and object-storage boundaries minimize
   leakage and maintenance risk for a personal academic corpus?
3. Which audience groups and tasks are supported by the supplied requirements
   and research on scholarly identity?
4. Which controls must be fixed at the repository foundation rather than
   postponed?

## 2. Search and selection method

Searches were conducted on 2026-07-17 against official standards bodies,
official project documentation, government technical publications, Crossref DOI
records and the supplied SRS/backend specification. The protocol records exact
requests, bounded counts, deduplication, screening criteria, source hashes, page
mapping and retained-study extraction. Query concepts were:

- personal academic website, academic homepage, scholarly identity, online
  visibility;
- requirements engineering, product quality, accessibility, secure development;
- server rendering, Django security/admin/templates, API schema;
- PostgreSQL full-text search, trigram, GIN and accent handling;
- SQS delivery, dead-letter queues, S3 encryption/versioning, ECS/RDS
  availability; and
- package locks, reproducible installation and deployment checks.

Sources were included when they were authoritative for a selected technology,
normative for a required quality attribute, or empirical research directly
concerning scholarly online identity. Marketing comparisons, unsourced tutorials
and generic listicles were excluded. The review prefers maintained
version-specific documentation. Vendor documentation is used for the behavior of
that vendor's service, not as independent proof that the service should be
selected.

The bounded scholarly search screened 60 Crossref records, retained seven and
added four unique SRS/current-review seeds, producing an 11-record evidence set.
This is a reproducible bounded review, not an exhaustive systematic review of
all bibliographic databases.

## 3. Requirements and quality evidence

ISO/IEC/IEEE 29148:2018 remains the relevant requirements-engineering reference
after its 2024 confirmation. Its focus on lifecycle requirements and
traceability supports a machine-validated product baseline rather than
undocumented assumptions: <https://www.iso.org/standard/72089.html>.

ISO/IEC 25010:2023 supplies a product-quality model. The foundation uses
functional suitability, reliability, security, maintainability, compatibility
and portability as decision criteria rather than selecting a stack from
popularity alone: <https://www.iso.org/standard/78176.html>.

ISO/IEC 25012:2008, confirmed in 2025, contributes a structured-data quality
model. Identity, dates, identifiers and visibility can be functionally present
while inaccurate or inconsistent: <https://www.iso.org/standard/35736.html>.

RFC 2119 as clarified by RFC 8174 defines the special interpretation of
uppercase BCP 14 requirement terms; those RFCs do not define this project's
priority levels:

- <https://www.rfc-editor.org/info/rfc2119>
- <https://www.rfc-editor.org/info/rfc8174>

WCAG 2.2 defines testable accessibility criteria and full-page/complete-process
conformance. This supports server-rendered semantic HTML, progressive
enhancement and accessibility as a release-blocking approval domain:
<https://www.w3.org/TR/WCAG22/>.

OWASP ASVS 5.0.0 provides versioned application-security verification
requirements. Its control-level use is a later security milestone, while this
foundation already separates secrets, validates environment configuration and
fixes the public/private storage boundary:
<https://owasp.org/www-project-application-security-verification-standard/>.

NIST SP 800-218 recommends integrating secure development practices throughout
the software lifecycle. That supports locked dependencies, automated checks,
reviewable changes and environment separation from the first commit:
<https://csrc.nist.gov/pubs/sp/800/218/final>.

## 4. Scholarly identity and audience evidence

The supplied SRS identifies academic visitors, professional visitors, public
visitors and machine actors. It prioritizes owner identification, current focus,
research, publications, projects, CV/resources, contact and trustworthy state.

Research on online scholarly identity reports that researchers use digital
profiles to support visibility, dissemination, trust and reputation while also
experiencing platform, ethical and reputational risks. These findings support an
owner-controlled hub with evidence, provenance and restrained claims rather than
automated self-promotional text:

- Kjellberg and Haider, “Researchers’ online visibility: tensions of visibility,
  trust and reputation,” <https://doi.org/10.1108/OIR-07-2017-0211>.
- Radford et al., “People are reading your work,” scholarly identity and social
  networking sites, <https://doi.org/10.1108/JD-04-2019-0074>.

The extraction table also covers Döring, Papacharissi, Thoms and Thelwall, two
Hyland studies, Dumont and Frindte, Bar-Ilan et al., a second Radford record and
Yan and Zhang. Their methods, samples and limits are recorded in the protocol.
Together they support owner control, research/output prominence, provenance and
discovery; they do not prove the exact audience or goal ranks.

Google Scholar's inclusion guidance conditionally calls for crawlable per-work
URLs, simple links, visible complete abstracts or full text and bibliographic
metadata. It also expects an included collection to consist primarily of
scholarly articles. This supports compatible publication pages but does not
guarantee that a general personal site will be included:
<https://scholar.google.com/intl/en/scholar/inclusion.html>.

ORCID, Crossref and DataCite imports remain provenance-labelled candidates for
owner review. DataCite Metadata Schema 4.7 is the current reviewed vocabulary.
CRediT roles do not determine authorship, and FAIR principles apply to assessed
research objects/metadata rather than automatically to an entire website. The
exact official sources and interpretation limits are in the protocol.

The primary audiences therefore rank academic peers/collaborators, academic
evaluators and students/early-career researchers. Professional evaluators,
event/media intermediaries, the general public and machine discovery systems are
secondary. The ranked goals in `docs/product/audiences-and-goals.md` follow the
SRS's stated purpose sequence and preserve non-negotiable truth, accessibility,
privacy and security constraints.

## 5. Frontend/backend architecture evidence

Django 5.2 is the selected long-term-support branch. Official documentation
covers ORM and migrations, authentication, permissions, CSRF, sessions,
templates, forms, international support, sitemaps, feeds, redirects, static
files and a trusted internal admin. Its admin documentation states that
process-centric interfaces should use custom views, matching the need for
special preview, publication, rollback and conflict workflows:

- <https://www.djangoproject.com/download/>
- <https://docs.djangoproject.com/en/5.2/ref/contrib/admin/>
- <https://docs.djangoproject.com/en/5.2/topics/security/>
- <https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/>

Django templates escape variables by default when used correctly. A
server-rendered public page also avoids requiring hydration before identity,
navigation, metadata or error content is available:
<https://docs.djangoproject.com/en/5.2/ref/templates/language/>.

Django REST Framework provides the versioned API boundary. Its documentation
recommends third-party OpenAPI generation rather than the deprecated built-in
generator, supporting drf-spectacular:
<https://www.django-rest-framework.org/topics/documenting-your-api/>.

Vite is selected only for strict TypeScript progressive enhancements and
content-hashed assets; it is not a second application runtime:
<https://vite.dev/guide/build>.

### Architectural comparison

The companion matrix scores alternatives separately for frontend, backend,
database, search, queue, object storage and hosting with disclosed criteria and
weights. Sensitivity testing leaves the first five categories stable but shows
that queue and hosting change under strong cost/exit weights; SQS and AWS
therefore retain explicit cost and operations approval triggers.

| Option                    |            Truth/public boundary | Accessibility/HTML |                     Editorial fit |                 Operations | Initial decision    |
| ------------------------- | -------------------------------: | -----------------: | --------------------------------: | -------------------------: | ------------------- |
| Django modular monolith   |                             High |               High |                              High |           One web boundary | Selected            |
| Static-only generation    |          High for simple content |               High | Insufficient for selected backend | Low until dynamic features | Rejected as primary |
| Next.js plus separate API | Requires cache/auth coordination |   Potentially high |             Custom implementation |     Two runtime boundaries | Rejected initially  |
| Headless content system   |        Remote authority boundary |  Depends on client |         Generic workflow mismatch |        Provider dependency | Rejected            |
| Microservices             |   Distributed consistency burden |            Neutral |           Excessive for one owner | Highest operational burden | Rejected            |

The decision is not a claim that one framework is universally superior. It is
the strongest fit for this evidence set: one editorial authority, modest scale,
public HTML, complex state/security rules and low operational burden.

## 6. Database and search evidence

PostgreSQL 18 provides maintained full-text parsing, query processing, ranking,
highlighting and index support. GIN is designed for inverted indexes used by
full-text search, while `pg_trgm` supports similarity matching and `unaccent`
can support accent-insensitive processing:

- <https://www.postgresql.org/docs/current/textsearch.html>
- <https://www.postgresql.org/docs/current/gin.html>
- <https://www.postgresql.org/docs/current/pgtrgm.html>
- <https://www.postgresql.org/docs/current/unaccent.html>

The expected corpus does not justify a second search database. A public search
projection updated in the publication transaction is safer than asynchronously
copying draft-capable records into a separate cluster. A dedicated engine
remains possible if measured corpus, language or latency requirements exceed
PostgreSQL behavior.

Amazon RDS Multi-AZ supplies managed failover, backup and point-in-time-recovery
mechanisms:

- <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.Failover.html>
- <https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_WorkingWithAutomatedBackups.html>

These mechanisms do not replace application-level restoration tests.

## 7. Queue and asynchronous evidence

Celery integrates with Django and supports Amazon SQS. SQS Standard queues use
at-least-once delivery and can redeliver or reorder messages. Therefore the
architecture requires a transactional outbox, message identifiers, idempotency
effect records, stale-revision rejection and a dead-letter queue:

- <https://docs.celeryq.dev/en/stable/django/first-steps-with-django.html>
- <https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/sqs.html>
- <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html>
- <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html>
- <https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html>

SQS is selected because production hosting already uses AWS and because it
removes broker host administration. Its missing Celery remote-control/events
features are accepted only with database job state and CloudWatch metrics as the
operational evidence source.

## 8. Object storage and hosting evidence

S3 supports server-side encryption and versioning. CloudFront Origin Access
Control can restrict direct S3 access. The requirements need stronger isolation
than changing an ACL on one object; therefore quarantine, private and public
derivatives occupy separate buckets:

- <https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingEncryption.html>
- <https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html>
- <https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html>

ECS services and Application Load Balancers support container task replacement
and multi-zone routing. Managed compute is selected to avoid owner-managed
hosts:

- <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-load-balancing.html>
- <https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-rebalancing.html>

The scope baseline selects AWS `eu-central-1` (Europe/Frankfurt, Germany) for
preview, staging, production and their durable regional application data. AWS
documents three Availability Zones for this region and availability for the
selected RDS, S3 and SES regional resources. Cross-region replication is
disabled. Outbound email still traverses recipient mail infrastructure, and
global or edge service paths require separate inventory and disclosure. The
legal record must consequently govern processing in Germany, provider paths,
processor terms and any applicable international-transfer mechanism; region
selection does not itself establish legal compliance.

## 9. Reproducibility evidence

`uv.lock` and `package-lock.json` record complete resolved dependency graphs. CI
and local setup use frozen/clean installation modes. npm documents
workspaces/clean installation, and uv documents universal lock and frozen
synchronization:

- <https://docs.npmjs.com/cli/commands/npm-ci/>
- <https://docs.astral.sh/uv/concepts/projects/sync/>

Formatting, linting, strict type checks, coverage tests, policy validation,
Django system checks, Compose validation and the asset build are one
`make check` gate.

## 10. Limitations and update triggers

1. Audience ordering is evidence-led and should later be tested with approved
   user research. Analytics remains inactive unless a separate minimal-purpose
   privacy decision activates it.
2. AWS `eu-central-1` is selected; jurisdiction, processor, transfer, workload,
   cost-envelope and recovery evidence remain release inputs rather than
   unspecified region choices.
3. PostgreSQL search must be benchmarked against the real corpus and supported
   languages.
4. The queue selection must be revisited if task latency, ordering or
   workflow-control needs exceed SQS transport behavior.
5. Django 5.2, Python 3.13, Node 22 and all direct dependencies require
   maintained security updates and reviewed lock changes.
6. Every architecture extraction or new data store requires a new decision
   record and proof that the public/private boundary remains intact.
7. SQS and AWS hosting require measured workload, cost-envelope and owner-labor
   inputs before deployment approval; the review does not invent a monthly cost.

The review is refreshed when a selected dependency loses support, a new legal
jurisdiction applies, measured scale violates an assumption, or a requirement
introduces an unsupported quality attribute.

# ADR 0001: Platform architecture

- Status: accepted for foundation implementation
- Date: 2026-07-17
- Decision owner: Ahmad Abdullayev
- Evidence: `docs/research/foundation-literature-review.md`

## Context

The product is a one-owner, public, content-heavy academic and professional
website with strong requirements for evidence integrity, accessible HTML, search
discoverability, metadata, editorial review, secure administration, revision
history, privacy boundaries, uploads, background integrations and
recoverability.

The expected corpus is modest. Operational burden and the probability of stale
or contradictory public output matter more than independent service scaling.

## Decision

Use a server-rendered modular monolith with separately scalable worker
processes.

### Frontend

- Django templates produce the complete semantic HTML response.
- Plain CSS is the primary presentation layer.
- Strict TypeScript provides progressive enhancements only where interaction
  requires it.
- Vite builds content-hashed JavaScript and CSS.
- Public tasks remain understandable when enhancement JavaScript is unavailable.

### Backend

- Python 3.13.
- Django 5.2 LTS.
- Django REST Framework for `/api/v1`.
- drf-spectacular for a generated and validated OpenAPI description.
- Django administration for trusted model-oriented maintenance.
- Custom views for process-oriented preview, approval, conflict, rollback,
  import and takedown workflows.

### Database and search

- PostgreSQL 18.4.
- PostgreSQL full-text search using weighted stored `tsvector`, GIN, `pg_trgm`
  and `unaccent` where language requirements justify them.
- Search documents are public projections, not queries across draft tables.
- Snapshot and search-projection updates occur in the same database transaction.
- A separate search service requires later measured evidence before adoption.

### Queue

- Celery 5.6 over Amazon SQS Standard queues.
- The database transaction writes a durable outbox event.
- A relay publishes committed outbox records to SQS.
- Delivery is treated as at-least-once and potentially out of order.
- Every message carries an event ID, aggregate ID, revision ID and idempotency
  key.
- Workers persist effect records and reject obsolete revisions.
- A dead-letter queue and alarm isolate repeated failures.

### Object storage

- Production uses Amazon S3 with Block Public Access, versioning, SSE-KMS and
  lifecycle rules.
- Quarantine, approved-private and public-derivative objects use separate
  buckets.
- Public derivatives are served through CloudFront Origin Access Control.
- User uploads never become public directly.

### Hosting

- Route 53 and ACM for domain and certificates.
- CloudFront and AWS WAF at the public edge.
- Application Load Balancer to two or more ECS Fargate Django tasks across
  availability zones.
- Separate no-ingress Fargate services for outbox relay and Celery workers.
- RDS PostgreSQL Multi-AZ in private subnets.
- SQS, S3, ECR, Secrets Manager, KMS, CloudWatch and AWS Backup.
- The AWS region is selected later through the jurisdiction and residency
  decision.

### Public caching boundary

- Initially, CloudFront does not cache public HTML.
- Only content-hashed static assets and approved immutable media receive long
  cache lifetimes.
- HTML caching may be activated only after purge, correction, withdrawal and
  retraction tests prove complete invalidation.

## Alternatives evaluated

### Static-only generator

Rejected as the primary architecture because the selected full backend profile
requires authenticated administration, preview, publication state, revisions,
schedules, contact processing, imports, audit and background work. Static
generation remains a possible public derivative later.

### Next.js frontend plus separate TypeScript API

Rejected for the initial implementation. It adds a second rendering, cache,
authentication and deployment boundary. Multi-instance response/cache
coordination would need additional invalidation proof. It can be reconsidered
only if a measured interaction requirement outgrows progressively enhanced
server rendering.

### Headless content system

Rejected because truth, lifecycle, revision, relationship, privacy and
public-snapshot rules are product-specific. Delegating them to a generic remote
content API would add a second authority and provider dependency.

### Microservices

Rejected because current scale and ownership do not justify distributed
transactions, independent schemas, cross-service authorization or additional
failure modes.

### Dedicated search cluster

Rejected initially because the expected corpus fits PostgreSQL search and
because a second index creates an avoidable stale-private-data boundary.

## Consequences

1. One codebase owns public rendering, administration, API schemas and security
   policy.
2. Web and worker processes scale independently without splitting domain
   ownership.
3. Database transaction design is critical for publication and outbox behavior.
4. SQS handlers must be idempotent.
5. The architecture can later extract a service only when measurements and an
   ADR justify the additional boundary.

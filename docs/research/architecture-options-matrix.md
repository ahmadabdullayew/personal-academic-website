# Architecture options, sensitivity and cost record

## Method

Options receive an ordinal rating from 0 to 5:

- 5: direct fit with minimal added boundary/operations;
- 4: strong fit with modest added work;
- 3: viable with meaningful compensating work or risk;
- 2: weak fit/substantial controls;
- 1: severe mismatch; and
- 0: cannot satisfy an applicable requirement.

The score is `sum(weight × rating / 5)`. Ratings are transparent reviewer
judgments based on the linked capabilities and project requirements, not
laboratory measurements.

| Code | Criterion                                    | Weight |
| ---- | -------------------------------------------- | -----: |
| F    | functional/editorial fit                     |     25 |
| I    | integrity and public/private boundary        |     20 |
| S    | security and maintenance support             |     15 |
| O    | operations, availability and recovery burden |     15 |
| U    | user quality, discovery and latency fit      |     10 |
| P    | portability and exit feasibility             |     10 |
| C    | low-traffic cost predictability              |      5 |

## Frontend

| Option                                          |   F |   I |   S |   O |   U |   P |   C | Total | Disposition                               |
| ----------------------------------------------- | --: | --: | --: | --: | --: | --: | --: | ----: | ----------------------------------------- |
| Django templates + Vite TypeScript enhancements |   5 |   5 |   4 |   5 |   5 |   4 |   5 |    95 | selected                                  |
| Astro + separate backend API                    |   4 |   3 |   4 |   3 |   5 |   4 |   4 |    75 | viable, adds rendering/build boundary     |
| Static-only generator                           |   2 |   4 |   4 |   4 |   5 |   5 |   5 |    75 | cannot implement selected backend profile |
| Next.js + separate backend API                  |   4 |   3 |   4 |   2 |   4 |   3 |   3 |    67 | adds runtime/cache/version coordination   |
| Browser SPA + API                               |   3 |   3 |   3 |   3 |   3 |   4 |   3 |    62 | unnecessary client dependency             |

Primary sources:
[Django templates](https://docs.djangoproject.com/en/5.2/topics/templates/),
[Django security](https://docs.djangoproject.com/en/5.2/topics/security/),
[Vite build](https://vite.dev/guide/build/),
[Astro islands](https://docs.astro.build/en/concepts/islands/) and
[Next.js server/client components](https://nextjs.org/docs/app/getting-started/server-and-client-components).

## Backend

| Option                          |   F |   I |   S |   O |   U |   P |   C | Total | Disposition                                            |
| ------------------------------- | --: | --: | --: | --: | --: | --: | --: | ----: | ------------------------------------------------------ |
| Django modular monolith         |   5 |   5 |   4 |   5 |   4 |   4 |   5 |    93 | selected                                               |
| FastAPI modular application     |   4 |   4 |   4 |   4 |   4 |   5 |   5 |    83 | strong API base; more custom editorial/admin/auth work |
| NestJS modular application      |   4 |   4 |   4 |   3 |   4 |   4 |   4 |    77 | viable; more implementation/tooling boundaries         |
| Generic headless content system |   3 |   3 |   3 |   4 |   4 |   2 |   4 |    64 | generic workflow/remote authority mismatch             |

Primary sources:
[Django admin](https://docs.djangoproject.com/en/5.2/ref/contrib/admin/),
[Django authentication](https://docs.djangoproject.com/en/5.2/topics/auth/),
[DRF API documentation](https://www.django-rest-framework.org/topics/documenting-your-api/),
[FastAPI features](https://fastapi.tiangolo.com/features/) and
[NestJS documentation](https://docs.nestjs.com/).

## Database

| Option     |   F |   I |   S |   O |   U |   P |   C | Total | Disposition                                    |
| ---------- | --: | --: | --: | --: | --: | --: | --: | ----: | ---------------------------------------------- |
| PostgreSQL |   5 |   5 |   5 |   5 |   4 |   5 |   4 |    97 | selected                                       |
| MySQL      |   4 |   4 |   5 |   5 |   3 |   5 |   4 |    86 | viable; weaker selected-search fit             |
| SQLite     |   3 |   4 |   5 |   2 |   3 |   5 |   5 |    73 | tests only for selected concurrent workflow    |
| DynamoDB   |   2 |   3 |   5 |   4 |   2 |   2 |   3 |    60 | poor relational revision/ordering/conflict fit |

Primary sources: [PostgreSQL 18](https://www.postgresql.org/docs/18/),
[MySQL full-text search](https://dev.mysql.com/doc/refman/8.4/en/fulltext-search.html),
[SQLite FTS5](https://www.sqlite.org/fts5.html) and
[DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html).

## Search

| Option                                        |   F |   I |   S |   O |   U |   P |   C | Total | Disposition                               |
| --------------------------------------------- | --: | --: | --: | --: | --: | --: | --: | ----: | ----------------------------------------- |
| PostgreSQL FTS + GIN + `pg_trgm` + `unaccent` |   5 |   5 |   4 |   5 |   4 |   5 |   5 |    95 | selected initially                        |
| Amazon OpenSearch                             |   5 |   3 |   4 |   2 |   5 |   3 |   2 |    73 | reconsider after measured need            |
| Algolia                                       |   4 |   3 |   4 |   5 |   5 |   1 |   2 |    73 | managed, but external copy/exit/cost risk |
| Meilisearch                                   |   4 |   3 |   3 |   3 |   4 |   4 |   4 |    70 | adds synchronization/service operation    |

Primary sources:
[PostgreSQL text search](https://www.postgresql.org/docs/18/textsearch.html),
[GIN](https://www.postgresql.org/docs/18/gin.html),
[`pg_trgm`](https://www.postgresql.org/docs/18/pgtrgm.html),
[`unaccent`](https://www.postgresql.org/docs/18/unaccent.html),
[OpenSearch Service](https://docs.aws.amazon.com/opensearch-service/),
[Meilisearch](https://www.meilisearch.com/docs/learn/getting_started/what_is_meilisearch)
and
[Algolia](https://www.algolia.com/doc/guides/getting-started/what-is-algolia/).

## Queue

| Option                              |   F |   I |   S |   O |   U |   P |   C | Total | Disposition                               |
| ----------------------------------- | --: | --: | --: | --: | --: | --: | --: | ----: | ----------------------------------------- |
| SQS Standard + transactional outbox |   4 |   4 |   5 |   5 |   4 |   2 |   4 |    82 | selected conditionally                    |
| RabbitMQ quorum queues              |   5 |   4 |   4 |   2 |   4 |   4 |   3 |    78 | stronger broker semantics, more operation |
| PostgreSQL outbox polling only      |   3 |   5 |   4 |   3 |   3 |   5 |   5 |    77 | cost/exit alternative at low volume       |
| Redis Streams                       |   4 |   3 |   4 |   3 |   4 |   3 |   2 |    69 | durability/replication must be operated   |

SQS's at-least-once delivery requires idempotency, stale-revision rejection,
visibility-timeout control and a dead-letter queue. Sources:
[delivery semantics](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues-at-least-once-delivery.html),
[visibility timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html),
[dead-letter queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html),
[Celery SQS](https://docs.celeryq.dev/en/stable/getting-started/backends-and-brokers/sqs.html),
[RabbitMQ quorum queues](https://www.rabbitmq.com/docs/quorum-queues) and
[Redis Streams](https://redis.io/docs/latest/develop/data-types/streams/).

## Object storage

| Option                                 |   F |   I |   S |   O |   U |   P |   C | Total | Disposition                                    |
| -------------------------------------- | --: | --: | --: | --: | --: | --: | --: | ----: | ---------------------------------------------- |
| Amazon S3                              |   5 |   5 |   5 |   5 |   5 |   3 |   4 |    95 | selected                                       |
| Cloudflare R2                          |   4 |   4 |   4 |   4 |   5 |   3 |   5 |    81 | cost alternative; verify required API features |
| Self-managed MinIO                     |   4 |   5 |   4 |   2 |   4 |   5 |   2 |    78 | durability becomes owner-operated              |
| Application filesystem/attached volume |   2 |   3 |   3 |   2 |   3 |   5 |   5 |    58 | inadequate isolation/recovery                  |

Sources:
[S3 encryption](https://docs.aws.amazon.com/AmazonS3/latest/userguide/UsingEncryption.html),
[S3 versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html),
[CloudFront OAC](https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/private-content-restricting-access-to-s3.html),
[R2 S3 compatibility](https://developers.cloudflare.com/r2/api/s3/api/),
[R2 consistency](https://developers.cloudflare.com/r2/reference/consistency/)
and
[MinIO erasure coding](https://min.io/docs/minio/linux/operations/concepts/erasure-coding.html).

## Hosting

| Option                             |   F |   I |   S |   O |   U |   P |   C | Total | Disposition                                      |
| ---------------------------------- | --: | --: | --: | --: | --: | --: | --: | ----: | ------------------------------------------------ |
| AWS managed stack                  |   5 |   5 |   5 |   4 |   5 |   3 |   2 |    90 | selected pending region/cost approval            |
| Self-managed Kubernetes            |   5 |   5 |   4 |   1 |   5 |   5 |   1 |    81 | disproportionate one-owner burden                |
| Render managed services            |   4 |   4 |   4 |   5 |   4 |   2 |   4 |    79 | lower-burden alternative/different exit boundary |
| Fly.io Machines/managed PostgreSQL |   4 |   4 |   4 |   4 |   4 |   3 |   4 |    78 | viable PaaS alternative                          |
| Self-managed VPS                   |   4 |   4 |   3 |   1 |   3 |   5 |   5 |    69 | low fee transfers patch/recovery/on-call labor   |

Sources:
[ECS load balancing](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-load-balancing.html),
[ECS zone rebalancing](https://docs.aws.amazon.com/AmazonECS/latest/developerguide/service-rebalancing.html),
[RDS Multi-AZ](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Concepts.MultiAZ.Failover.html),
[RDS recovery](https://docs.aws.amazon.com/prescriptive-guidance/latest/backup-recovery/rds.html),
[Render Django](https://render.com/docs/deploy-django),
[Render service types](https://render.com/docs/service-types) and
[Fly pricing/model](https://fly.io/docs/about/pricing/).

## Sensitivity analysis

The same ratings were recalculated under four weight profiles:

| Scenario         |   F |   I |   S |   O |   U |   P |   C |
| ---------------- | --: | --: | --: | --: | --: | --: | --: |
| Baseline         |  25 |  20 |  15 |  15 |  10 |  10 |   5 |
| Cost-first       |  15 |  15 |  10 |  10 |  10 |  15 |  25 |
| Operations-first |  20 |  15 |  15 |  30 |   5 |   5 |  10 |
| Exit-first       |  20 |  20 |  10 |  10 |  10 |  25 |   5 |

| Category       | Baseline       | Cost-first           | Operations-first | Exit-first           |
| -------------- | -------------- | -------------------- | ---------------- | -------------------- |
| Frontend       | Django/Vite 95 | Django/Vite 95       | Django/Vite 96   | Django/Vite 93       |
| Backend        | Django 93      | Django 93            | Django 95        | Django 91            |
| Database       | PostgreSQL 97  | PostgreSQL 93        | PostgreSQL 97    | PostgreSQL 97        |
| Search         | PostgreSQL 95  | PostgreSQL 96        | PostgreSQL 96    | PostgreSQL 96        |
| Queue          | SQS 82         | PostgreSQL outbox 84 | SQS 87           | PostgreSQL outbox 82 |
| Object storage | S3 95          | S3 89                | S3 96            | S3 89                |
| Hosting        | AWS 90         | VPS 78               | AWS 86           | Kubernetes 86        |

Frontend, backend, database, search and object storage remain first under all
tested profiles. Queue and hosting are sensitive: SQS wins with meaningful
operations weight; PostgreSQL polling wins cost/exit cases. AWS wins the
requirements/security/operations cases, while cost-first and exit-first weights
promote options that transfer substantially more labor to the owner. Therefore
region, cost envelope and owner-operations capacity remain hosting/queue
approval gates.

## Cost record and missing inputs

A defensible monthly total requires region, request/peak load, web/worker sizes,
database size/IOPS/retention/availability, storage/requests/egress, queue retry
volume, observability retention, deployment frequency, recovery objectives and a
value for owner maintenance time.

An AWS estimate must include ALB hours/capacity, Fargate runtime, RDS
primary/standby/storage/backups, S3 storage/requests/egress, SQS, CloudFront,
WAF, KMS, Secrets Manager, CloudWatch, ECR, networking, Route 53 and backup
copies. Use the [AWS Pricing Calculator](https://calculator.aws/#/) only after
those inputs and region are recorded.

PaaS headline compute can omit highly available databases, workers, private
networking, backup retention, egress, logs and support. Self-hosted software can
lower service fees while transferring upgrades, monitoring, incident response,
durability and restoration testing to the owner.

## Binding selection and reassessment

The selected foundation is semantic Django templates, Vite-built progressive
TypeScript, Django 5.2 LTS/DRF/drf-spectacular, PostgreSQL 18 for relational
data and initial public search, Celery/SQS with
outbox/idempotency/stale-event/DLQ controls, separate S3
quarantine/private/public-derivative buckets, and the CloudFront/WAF → ALB →
ECS/RDS/SQS/S3 managed AWS shape.

Reassess on measured PostgreSQL search failure, strict queue ordering/workflow
needs, an approved cost ceiling the selection exceeds, a jurisdiction change, or
an owner-operations constraint that changes the weights.

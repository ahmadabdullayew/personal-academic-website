# Personal Academic Website

This repository is the implementation foundation for Ahmad Abdullayev's personal
academic and professional website. It begins with a deliberately narrow public
page: the owner is identified, but no academic title, degree, discipline,
affiliation or biography is inferred before an approved source record exists.

## Foundation status

The project-and-scope foundation establishes:

1. a functioning Git repository on `main`;
2. a reproducible Python and Node toolchain;
3. an evidence-led architecture decision;
4. safe local environment examples;
5. executable formatting, linting, typing, testing and build commands;
6. named ownership and release-approval roles;
7. primary and secondary audiences;
8. ranked visitor and owner goals;
9. the primary domain, five deployment environments and one active locale;
10. the administration model and named maintainer roles;
11. binary decisions for all 54 optional or conditional requirement cards;
12. contact, search, synchronization, privacy and discovery feature decisions;
13. jurisdiction, content ownership, approval and review controls;
14. a 32-record initial content inventory and 12-step migration plan;
15. formal revision history and six domain-specific approval records; and
16. the exact 264-row applicability, dependency and ownership matrix.

This milestone resolves foundation items 1–23. Applicable website capabilities
remain connected to their own implementation and release evidence; unsupported
personal or academic claims remain unpublished.

## Owner and accountability

- Website owner and represented person: **Ahmad Abdullayev**.
- Final accountable approver for product, content, accessibility, security,
  privacy and operations: **Ahmad Abdullayev**.
- Each approval domain requires a separate recorded decision even when one
  person fills every role.
- Applicable P0 failures are not waivable.

See [governance](docs/product/governance.md),
[scope decisions 11–18](docs/product/foundation-scope-decisions.md),
[legal and content governance](docs/product/legal-content-governance.md) and
[audiences and goals](docs/product/audiences-and-goals.md).

## Architecture

```text
Route 53 + ACM
       |
CloudFront + WAF -------- approved immutable S3 derivatives
       |
      ALB
       |
ECS Fargate Django web tasks
       |
       +---- RDS PostgreSQL 18.4 Multi-AZ
       |       data + revisions + public snapshots + search + audit + outbox
       |
       +---- private S3 quarantine/private/public boundaries
       |
outbox relay -> SQS -> idempotent Celery workers -> S3/providers/database
```

The public frontend is semantic server-rendered Django HTML with progressively
enhanced strict TypeScript built by Vite. Django REST Framework supplies
`/api/v1`. PostgreSQL supplies persistence and full-text/trigram search. Celery
consumes at-least-once SQS messages through idempotent handlers. Production
storage uses separate private S3 buckets. Production hosting uses AWS managed
services across multiple availability zones in `eu-central-1`
(Europe/Frankfurt). The primary public origin is `https://ahmadabdullayev.com`.

The binding rationale and alternatives are recorded in
[ADR 0001](docs/architecture/0001-platform.md) and the source review in
[the foundation literature review](docs/research/foundation-literature-review.md).
The selections for items 11–23 have a separate
[scope and governance evidence review](docs/research/scope-governance-literature-review.md).

## Prerequisites

- Git 2.43 or later.
- `uv` 0.11.29 or later.
- Node.js 22.23.0 and npm 10.9.8.
- Docker with Compose support for PostgreSQL and local S3/SQS emulation.
- Poppler `pdftotext` 24.02.0 or later when regenerating the 264-row matrix;
  verify it with `pdftotext -v`. It is not required to validate the committed
  matrix.

The repository pins Python 3.13.14 in `.python-version` and Node 22.23.0 in
`.nvmrc`.

## Local setup

```bash
cp .env.example .env.local
uv sync --frozen
npm ci
make services-up
make migrate
make check
make dev
```

The site is then available at <http://localhost:8000>. Run `npm run dev` in a
second terminal while editing TypeScript or CSS assets.

Stop local infrastructure with:

```bash
make services-down
```

Detailed clean-clone, migration and troubleshooting instructions are in
[docs/development/local-development.md](docs/development/local-development.md).

## Command contract

| Command                 | Result                                                                |
| ----------------------- | --------------------------------------------------------------------- |
| `make bootstrap`        | Create `.env.local` if absent and install frozen Python/Node locks    |
| `make services-up`      | Start PostgreSQL and local S3/SQS emulation and wait for health       |
| `make services-down`    | Stop local services without deleting named data volumes               |
| `make migrate`          | Apply Django migrations to the selected environment                   |
| `make dev`              | Start Django's local development server                               |
| `npm run dev`           | Rebuild TypeScript/CSS assets on changes                              |
| `make format`           | Format and safely auto-fix Python, TypeScript, JSON, CSS and Markdown |
| `make format-check`     | Verify formatting without modifying files                             |
| `make lint`             | Run Ruff, ESLint and Stylelint with warnings treated as failures      |
| `make typecheck`        | Run strict mypy and TypeScript checks                                 |
| `make test`             | Run Python and TypeScript tests with coverage thresholds              |
| `make env-check`        | Validate the environment contract                                     |
| `make scope-check`      | Validate all three baselines and their cross-artifact consistency     |
| `make production-check` | Run deployment checks against generated safe validation config        |
| `make migration-check`  | Reject model changes that lack migrations                             |
| `make openapi-check`    | Generate and validate the versioned OpenAPI document                  |
| `make build`            | Build content-hashed frontend assets and collect static files         |
| `make check`            | Execute every foundation release check                                |

## Repository map

```text
config/                 machine-readable product, governance and requirement baselines
docs/architecture/      binding architecture decisions
docs/development/       local setup, environment and testing contracts
docs/product/           owner, approval, audience and goal baseline
docs/research/          reproducible evidence review
frontend/               TypeScript unit tests
infra/aws/              production deployment boundary and future IaC home
scripts/                environment, product and local-service validation
src/apps/               implemented Django applications
src/paw/                settings, URL and runtime configuration
src/static_src/         authored TypeScript and CSS
src/static_dist/        generated content-hashed assets
src/templates/          server-rendered semantic HTML
tests/                  cross-application Python tests
```

## Configuration and secrets

`.env.example` contains safe local values; `.env.test.example` contains isolated
test values. Preview, staging and production have non-secret deployment
templates. Real `.env` files are ignored. Deployed secrets must be supplied
through AWS Secrets Manager or Systems Manager Parameter Store and IAM task
roles. No AWS access key is stored in a deployment template.

See [the environment contract](docs/development/environment.md).

## Security and content integrity

- Public pages must read only approved public snapshots.
- Separate S3 buckets enforce quarantine, approved-private and public-derivative
  boundaries.
- SQS delivery is treated as at-least-once; worker effects require idempotency
  records.
- Unapproved academic attributes are prohibited from public content.
- Security reports follow [SECURITY.md](SECURITY.md).

## Further development

All new behavior must be connected to an SRS requirement, measurable acceptance
criteria and executable or inspectable evidence. See
[CONTRIBUTING.md](CONTRIBUTING.md) and the
[foundation traceability matrix](docs/traceability/foundation.md) and the
[264-row requirement matrix](docs/traceability/requirements-matrix.md).

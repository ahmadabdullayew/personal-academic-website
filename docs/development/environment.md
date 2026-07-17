# Environment contract

Real local values belong in `.env.local`, which Git ignores. Production values
come from managed configuration and IAM roles, not a deployed environment file.

| Variable                      | Classification          |        Required | Contract                                                                 |
| ----------------------------- | ----------------------- | --------------: | ------------------------------------------------------------------------ |
| `APP_ENV`                     | public runtime          |             yes | `development`, `test`, `preview`, `staging` or `production`               |
| `DJANGO_SETTINGS_MODULE`      | public runtime          |             yes | selected settings module                                                 |
| `DJANGO_DEBUG`                | public runtime          |             yes | exact `true`/`false`; false in preview, staging and production           |
| `DJANGO_SECRET_KEY`           | secret                  |             yes | long random production value; placeholders rejected                      |
| `DJANGO_ALLOWED_HOSTS`        | public runtime          |             yes | comma-separated trusted hosts                                            |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | security configuration  |             yes | explicit origins with schemes                                            |
| `SITE_BASE_URL`               | public runtime          |             yes | absolute URL; HTTPS in every deployed environment                        |
| `POSTGRES_DB`                 | local infrastructure    |           local | Compose database name                                                    |
| `POSTGRES_USER`               | sensitive configuration |           local | Compose database role                                                    |
| `POSTGRES_PASSWORD`           | secret                  |           local | local example only; managed secret in production                         |
| `DATABASE_URL`                | secret                  |             yes | PostgreSQL URL; in-memory SQLite only for tests; deployments require TLS |
| `DATABASE_POOL_MAX`           | public runtime          |             yes | positive integer applied to the psycopg connection pool                  |
| `AWS_REGION`                  | public runtime          |             yes | `eu-central-1` in every deployed environment                              |
| `AWS_ACCESS_KEY_ID`           | secret                  | local/test only | required as an emulator pair; rejected in deployed environments          |
| `AWS_SECRET_ACCESS_KEY`       | secret                  | local/test only | required as an emulator pair; rejected in deployed environments          |
| `S3_ENDPOINT_URL`             | public runtime          |             yes | LocalStack locally; AWS endpoint in production                           |
| `S3_BUCKET_QUARANTINE`        | security boundary       |             yes | distinct private quarantine bucket                                       |
| `S3_BUCKET_PRIVATE`           | security boundary       |             yes | distinct approved-private bucket                                         |
| `S3_BUCKET_PUBLIC`            | security boundary       |             yes | distinct public-derivative bucket                                        |
| `SQS_ENDPOINT_URL`            | public runtime          |             yes | LocalStack locally; AWS endpoint in production                           |
| `SQS_QUEUE_URL`               | sensitive configuration |             yes | jobs queue URL; credentials never embedded                               |
| `DEFAULT_LANGUAGE`            | public content          |             yes | must appear in supported languages                                       |
| `SUPPORTED_LANGUAGES`         | public content          |             yes | unique comma-separated BCP 47 language tags                              |
| `CONTACT_DELIVERY_MODE`       | feature control         |             yes | preview/staging `disabled`; production `ses`                              |
| `ORCID_ENABLED`               | feature control         |             yes | exact boolean; defaults false                                            |
| `CROSSREF_ENABLED`            | feature control         |             yes | exact boolean; defaults false                                            |
| `LOG_LEVEL`                   | public runtime          |             yes | `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`                        |

## Rules

1. `APP_ENV` is exactly `development`, `test`, `preview`, `staging` or
   `production`, and its Django settings module must match.
2. Example secrets, debug mode, wildcard/site-mismatched hosts, non-HTTPS
   origins, static AWS keys, non-PostgreSQL databases and PostgreSQL connections
   without a TLS `sslmode` are rejected in preview, staging and production.
3. In-memory SQLite is accepted only for tests. Development and production use
   PostgreSQL.
4. The selected deployed origins are exact: a `pr-<id>` preview host, the
   staging host, and the production primary host. Allowed hosts and trusted
   origins contain only the corresponding selected value.
5. Deployed AWS region and S3/SQS endpoints are pinned to `eu-central-1`; the
   three syntactically valid storage buckets remain distinct and the queue URL
   includes a queue path.
6. English is the only deployed default/supported language. ORCID and Crossref
   remain false. Contact delivery is disabled outside production and is `ses`
   in production.
7. No secret is exposed through browser-prefixed variables.
8. Every deployed startup fails closed when required configuration is missing
   or unsafe.
9. Secret rotation must preserve a documented overlap or invalidation procedure.

The S3, SQS, contact, ORCID and Crossref variables define the selected adapter
boundary. Production configuration selects SES, while provider calls still
remain blocked until the contact implementation and every privacy, security and
operations release gate pass. Parsing configuration does not claim that a
feature has passed release acceptance.

Run `make env-check` after every configuration change.

## Selected environment catalogue

| Environment | Authoritative origin                                      | Data and access boundary                                                                 |
| ----------- | --------------------------------------------------------- | ---------------------------------------------------------------------------------------- |
| local       | `http://localhost:8000`                                   | developer machine; LocalStack/PostgreSQL; synthetic or explicitly approved fixture data  |
| test/CI     | `http://testserver`                                       | isolated in-memory test state; no external provider calls                                |
| preview     | `https://pr-<id>.preview.ahmadabdullayev.com`             | ephemeral, authenticated, `noindex`; synthetic data only; contact and integrations off   |
| staging     | `https://staging.ahmadabdullayev.com`                     | persistent preproduction, authenticated, `noindex`; sanitized data only                  |
| production  | `https://ahmadabdullayev.com`                             | public approved snapshots; AWS `eu-central-1`; contact delivery through SES              |

`https://www.ahmadabdullayev.com` is a redirect-only alias to the production
origin, never a second content origin. Preview hosts replace `<id>` with the
exact deployment identifier; wildcard application hosts are prohibited.

The committed deployment templates are `.env.preview.example`,
`.env.staging.example`, and `.env.production.example`. They document public
configuration and managed-secret references; they are intentionally not
runnable secret files. Deployment values are resolved from AWS Secrets Manager,
Systems Manager Parameter Store, service discovery, and IAM task roles.

# Local development

## Clean-clone setup

1. Check out the repository on branch `main`.
2. Install `uv`, Node 22.23.0, npm 10.9.8 and Docker Compose.
3. Run `cp .env.example .env.local`.
4. Run `uv sync --frozen`.
5. Run `npm ci`.
6. Run `make services-up`.
7. Run `make migrate`.
8. Run `make check`.
9. Run `make dev`.
10. In a second terminal, run `npm run dev` while editing assets.

`uv` provisions the Python version named in `.python-version` when it is not
already available. `npm ci` installs exactly the dependency graph in
`package-lock.json`.

## Requirement-matrix source regeneration

Ordinary development and validation use the committed 264-row matrix and do not
need the source PDFs or a PDF extractor. Regenerating that matrix from the two
reviewed PDFs additionally requires Poppler `pdftotext` 24.02.0 or later.

Install the `poppler-utils` package on Debian/Ubuntu or the `poppler` formula
with Homebrew on macOS, then verify the executable and version before running
the builder:

```shell
pdftotext -v
python3 scripts/build_requirements_matrix.py \
  --srs-pdf /path/to/personal_academic_professional_website_srs.pdf \
  --backend-pdf /path/to/personal_academic_website_backend_specification.pdf \
  --output /tmp/requirements-matrix.json
cmp config/requirements-matrix.json /tmp/requirements-matrix.json
```

The first command must report `pdftotext version 24.02.0` or a later version.
The builder performs the same preflight and gives platform-specific installation
and verification guidance when the executable is missing, cannot run, reports an
unrecognized version, or is too old.

## Local services

Docker Compose starts:

- PostgreSQL 18.4 on `127.0.0.1:5432`;
- LocalStack S3/SQS emulation on `127.0.0.1:4566`;
- three separate local buckets; and
- the configured jobs queue and its dead-letter queue.

Compose reads the same `.env.local` file as Django. Bucket and queue names in
that file are passed into the initialization script, preventing service/runtime
configuration drift.

Container images are pinned to immutable platform digests. Local services bind
to the loopback interface only.

## Migration workflow

1. Change Django models.
2. Run
   `uv run --env-file .env.local python manage.py makemigrations --check --dry-run`
   first to inspect whether a migration is required.
3. Generate and review the migration.
4. Apply it with `make migrate`.
5. Add migration and constraint tests.
6. Never edit a migration that has reached a shared environment.

## Verification

Run `make check` before review. It verifies lockfiles, environment and product
policy, Django configuration, Compose syntax, formatting, lint, strict typing,
coverage tests and the production asset build.

## Shutdown

`make services-down` preserves named volumes. Deliberate data-volume deletion is
a separate destructive operation and is not part of the ordinary command
surface.

## Common failures

- **Python unavailable:** run `uv python install 3.13.14` and repeat
  `uv sync --frozen`.
- **Node version rejected:** activate the `.nvmrc` version.
- **Port already used:** stop the conflicting local process; do not silently
  change shared example ports.
- **Environment error:** compare `.env.local` with
  `docs/development/environment.md` and rerun `make env-check`.
- **Container unhealthy:** inspect `docker compose ps` and service logs before
  migrating.
- **Lock drift:** regenerate the relevant lock deliberately and review its full
  diff.
- **Matrix extractor unavailable:** install Poppler `pdftotext` 24.02.0 or
  later, confirm `pdftotext -v`, and rerun the matrix builder.

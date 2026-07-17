export PYTHONPATH := $(CURDIR)/src

UV_RUN = uv run --frozen
UV_DEV = uv run --frozen --env-file .env.local
UV_TEST = uv run --frozen --env-file .env.test.example
COMPOSE_DEV = docker compose --env-file .env.local
COMPOSE_CHECK = docker compose --env-file .env.example

.PHONY: bootstrap build check clean compose-check dev django-check env-check format format-check lint lock-check migration-check migrate openapi-check production-check scope-check services-down services-up shell-check test test-python test-typescript typecheck

.env.local:
	cp .env.example .env.local

bootstrap: .env.local
	uv sync --frozen
	npm ci

services-up: .env.local
	$(COMPOSE_DEV) up --detach --wait

services-down: .env.local
	$(COMPOSE_DEV) down --remove-orphans

migrate: .env.local
	$(UV_DEV) python manage.py migrate

dev: .env.local
	$(UV_DEV) python manage.py runserver 0.0.0.0:8000

build:
	npm run build
	$(UV_TEST) python manage.py collectstatic --noinput --clear

format:
	$(UV_RUN) ruff format src scripts tests
	$(UV_RUN) ruff check --fix src scripts tests
	npm run format

format-check:
	$(UV_RUN) ruff format --check src scripts tests
	npm run format:check

lint:
	$(UV_RUN) ruff check src scripts tests
	npm run lint

typecheck:
	$(UV_TEST) mypy
	npm run typecheck

test-python:
	$(UV_TEST) pytest

test-typescript:
	npm run test:coverage

test: test-python test-typescript

env-check:
	$(UV_TEST) python scripts/validate_environment.py

scope-check:
	$(UV_RUN) python scripts/validate_product_baseline.py
	$(UV_RUN) python scripts/validate_foundation_governance.py
	$(UV_RUN) python scripts/validate_requirements_matrix.py
	$(UV_RUN) python scripts/validate_foundation_manifest.py
	$(UV_RUN) python scripts/validate_foundation_scope.py

django-check:
	$(UV_TEST) python manage.py check

production-check:
	$(UV_RUN) python scripts/check_production_settings.py

migration-check:
	$(UV_TEST) python manage.py makemigrations --check --dry-run

openapi-check:
	$(UV_TEST) python manage.py spectacular --file /tmp/paw-openapi.yaml --validate

shell-check:
	sh -n scripts/localstack-init.sh

compose-check:
	$(COMPOSE_CHECK) config --quiet

lock-check:
	uv lock --check
	npm ci --ignore-scripts --dry-run
	git diff --exit-code -- uv.lock package-lock.json

check: lock-check env-check scope-check django-check production-check migration-check openapi-check compose-check shell-check format-check lint typecheck test build

clean:
	rm -rf .coverage coverage.xml coverage-js htmlcov src/static_dist/.vite src/static_dist/assets staticfiles
	touch src/static_dist/.gitkeep

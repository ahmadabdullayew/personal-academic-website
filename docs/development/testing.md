# Testing and quality contract

## Foundation gates

1. `make format-check` verifies Python and repository formatting.
2. `make lint` runs Ruff, ESLint and Stylelint with no warnings accepted.
3. `make typecheck` runs strict mypy and TypeScript.
4. `make test` runs Python and TypeScript suites with branch coverage.
5. Python and TypeScript coverage thresholds are 90% for the implemented
   foundation.
6. `make django-check` validates test/runtime Django configuration.
7. `make production-check` runs Django's deployment checks with an ephemeral
   generated secret and production-shaped, non-routable configuration.
8. `make migration-check` rejects model changes without migrations.
9. `make openapi-check` generates and validates the API description.
10. `make env-check` validates runtime configuration.
11. `make scope-check` validates the complete JSON schema plus owner, source,
    approval, audience and goal cross-field invariants.
12. `make compose-check` and `make shell-check` validate local infrastructure.
13. `make build` proves asset-manifest integration and static-file assembly.

## Test principles

- A missing test command is not a pass.
- Test names state observable behavior.
- Failure paths are tested with success paths.
- Tests use the test environment contract and no production data.
- Public tests assert the absence of unsupported personal claims.
- Later requirement tests use the requirement ID in test metadata or evidence
  records.

Browser, accessibility, integration, security, migration and restoration suites
are added with the corresponding implemented capabilities. They must not be
represented as passed before their environments and assertions exist.

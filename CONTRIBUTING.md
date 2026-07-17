# Contributing

## Required workflow

1. Link the change to one or more requirement IDs or to an approved foundation
   decision.
2. Record affected data, privacy, security, accessibility and operational
   boundaries.
3. Add or update measurable tests.
4. Run `make check`.
5. Request the applicable approval-domain decisions described in
   `docs/product/governance.md`.

## Change rules

- Do not infer academic titles, affiliations, degrees, disciplines or
  biographical facts.
- Do not expose draft, private, restricted, embargoed, expired, revoked or
  deleted data.
- Do not weaken an applicable P0 requirement through an ordinary code review.
- Do not commit secrets or production personal data.
- Add dependencies only to satisfy a recorded requirement or architecture
  decision.
- Commit regenerated `uv.lock` and `package-lock.json` with every dependency
  change.
- Migrations are append-only after release; repair them with later migrations.

## Quality gate

`make check` is the minimum local gate. A missing check is not interpreted as a
pass.

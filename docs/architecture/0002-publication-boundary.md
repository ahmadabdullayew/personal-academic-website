# ADR 0002: Approved public-snapshot boundary

- Status: accepted as a binding invariant
- Date: 2026-07-17
- Decision owner: Ahmad Abdullayev

## Decision

Public templates, public APIs, search documents, feeds, sitemaps, structured
metadata, social previews, caches and exported files may read only an approved
public snapshot or a derivative generated exclusively from that snapshot.

## Foundation implementation status

At this milestone, `config/product-baseline.json` is a versioned,
deployment-immutable foundation public snapshot. It contains only the verified
owner name, role assignments, audiences and ranked goals; the page deliberately
withholds academic attributes. Django loads owner identity and the homepage from
that one file, so the base template does not keep a second copy.

The database-backed revision, approval and publication transaction described
below is the binding design for later content modules; it is not represented as
already implemented by the static foundation snapshot.

## Required transaction

A publication transaction must:

1. lock the record and validate the proposed revision;
2. confirm actor authorization and publication preconditions;
3. create an immutable approved snapshot;
4. switch the active public-snapshot reference;
5. update the public search projection;
6. record the audit event; and
7. insert an outbox event.

If any step fails, none of the steps becomes visible.

## Asynchronous derivatives

Each derivative message includes the approved snapshot/revision identifier.
Workers reject events older than the record's current approved revision, persist
idempotency effects and never query draft values while generating public output.

## Cache rule

Public HTML is uncached at the edge until correction, withdrawal, retraction and
purge tests prove complete multi-instance invalidation. Content-hashed approved
assets may be cached immutably.

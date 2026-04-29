# Production Depth: Court Workpaper Persistence

## Summary

CivicCourt now supports optional SQLAlchemy-backed court form and hearing-prep workpaper records through `CIVICCOURT_WORKPAPER_DB_URL`.

## Shipped

- `CourtWorkpaperRepository` with schema-aware SQLAlchemy tables.
- Persisted court form draft records with `form_id`.
- Persisted hearing-prep records with `prep_id`.
- Retrieval endpoints:
  - `GET /api/v1/civiccourt/form-draft/{form_id}`
  - `GET /api/v1/civiccourt/hearing-prep/{prep_id}`
- Actionable `503` guidance when persistence is not configured.
- Regression tests for repository reload, API round trip, missing-record `404`, no-config `503`, and stateless fallback behavior.

## Still Not Shipped

- Court case-management replacement.
- E-filing.
- Warrant issuance.
- Judicial decisions.
- Legal advice.
- Live LLM calls.
- Court CMS connectors.

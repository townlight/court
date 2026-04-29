# CivicCourt

CivicCourt is the CivicSuite municipal court clerk support module. Version 0.1.2 helps clerks prepare cited procedure answers, draft review-required court forms, build hearing prep checklists, search sample public records while hiding restricted matters, and optionally persist local workpaper records.

It is intentionally not a court case-management system, e-filing system, warrant issuance workflow, judicial decision tool, legal advice engine, live LLM runtime, or court CMS connector.

## Shipping in v0.1.2

- Cited procedure Q&A for clerk-reviewed court workflow support.
- Court form draft assembly with a not-filed boundary.
- Hearing preparation checklist support for clerk use before scheduling or filing.
- Restricted-record-aware sample search that keeps sealed and juvenile matters out of public results.
- Optional database-backed court form and hearing-prep workpaper records via `CIVICCOURT_WORKPAPER_DB_URL`.
- Bearer-token protection for persisted form and hearing-prep retrieval via `CIVICCOURT_AUTH_TOKEN_ROLES`.
- FastAPI runtime with health, public landing page, deterministic endpoints, docs, tests, browser QA, and release gates.

## Not shipped yet

- Court CMS write-back, e-filing, warrants, judicial decisions, legal advice, live LLM calls, or live court CMS connector runtime.
- Staff SSO, clerk approval queues, and official filing workflows. v0.1.2 protects persisted retrieval only; later releases will expand workflow auth.

## Install

```bash
python -m pip install -e ".[dev]"
python -m uvicorn civiccourt.main:app --host 127.0.0.1 --port 8143
```

CivicCourt v0.1.2 is pinned to `civiccore==0.4.0`.

## API Surface

- `GET /` returns honest current-state metadata and roadmap boundary.
- `GET /health` returns runtime and CivicCore version status.
- `GET /civiccourt` renders the public module overview.
- `POST /api/v1/civiccourt/procedure-answer` returns a cited procedure answer draft.
- `POST /api/v1/civiccourt/form-draft` returns a clerk-reviewed form draft and a `form_id` when persistence is configured.
- `GET /api/v1/civiccourt/form-draft/{form_id}` retrieves a persisted form draft when both `CIVICCOURT_WORKPAPER_DB_URL` and `CIVICCOURT_AUTH_TOKEN_ROLES` are configured.
- `POST /api/v1/civiccourt/search` returns restricted-record-aware sample search results.
- `POST /api/v1/civiccourt/hearing-prep` returns a hearing prep checklist and a `prep_id` when persistence is configured.
- `GET /api/v1/civiccourt/hearing-prep/{prep_id}` retrieves a persisted hearing prep record when both `CIVICCOURT_WORKPAPER_DB_URL` and `CIVICCOURT_AUTH_TOKEN_ROLES` are configured.

## Optional Persistence And Retrieval Auth

Set `CIVICCOURT_WORKPAPER_DB_URL` to enable local SQLAlchemy-backed court form and hearing-prep workpaper records:

```bash
export CIVICCOURT_WORKPAPER_DB_URL="sqlite+pysqlite:///./civiccourt.db"
```

Set `CIVICCOURT_AUTH_TOKEN_ROLES` to a JSON object that maps bearer tokens to roles before exposing persisted retrieval:

```json
{
  "reader-token": ["workpaper_reader"],
  "clerk-admin-token": "workpaper_reader,court_clerk_admin"
}
```

Without the database variable, CivicCourt remains deterministic and stateless. Without the auth variable, persisted retrieval endpoints return actionable `503` responses that name the missing auth configuration. With auth configured, anonymous callers receive `401` and callers without an allowed role receive `403`.

## Documentation

- [User Manual](USER-MANUAL.md)
- [Architecture](docs/architecture.md)
- [Landing Page](docs/index.html)
- [Release Notes](CHANGELOG.md)

Apache 2.0 code. CC BY 4.0 docs.

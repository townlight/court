<a id="civiccourt-user-manual"></a>

# Townlight Courts User Manual

## Non-Technical Staff

Townlight Courts helps municipal court clerks prepare cited procedural answers, draft court forms for review, search public sample court records while hiding restricted records, assemble hearing preparation checklists, and optionally retrieve saved workpaper records when IT enables persistence and retrieval auth.

Published version `0.1.2` is a foundation label under suite-wide release-recovery review. Do not promote it as production court software until the recovery gates and a future v1.0.0 definition of done are complete.

Court clerks remain responsible for every form, citation, procedure answer, and hearing checklist. Townlight Courts does not decide cases, issue warrants, file documents, provide legal advice, expose sealed or juvenile records, or replace the court case-management system.

## IT / Technical

Install with:

```bash
python -m pip install -e ".[dev]"
python -m uvicorn civiccourt.main:app --host 127.0.0.1 --port 8143
```

Runtime dependency: published Townlight Core v0.4.0 release wheel.

Primary endpoints:

- `GET /health` - service and Townlight Core version.
- `GET /civiccourt` - public sample UI.
- `POST /api/v1/civiccourt/procedure-answer` - cited procedure answer draft.
- `POST /api/v1/civiccourt/form-draft` - clerk-reviewed form draft.
- `GET /api/v1/civiccourt/form-draft/{form_id}` - persisted form draft retrieval when `CIVICCOURT_WORKPAPER_DB_URL` and `CIVICCOURT_AUTH_TOKEN_ROLES` are set.
- `POST /api/v1/civiccourt/search` - restricted-record-aware sample search.
- `POST /api/v1/civiccourt/hearing-prep` - hearing preparation checklist.
- `GET /api/v1/civiccourt/hearing-prep/{prep_id}` - persisted hearing prep retrieval when `CIVICCOURT_WORKPAPER_DB_URL` and `CIVICCOURT_AUTH_TOKEN_ROLES` are set.

Persisted retrieval requires a bearer token configured through `CIVICCOURT_AUTH_TOKEN_ROLES`. Without the database variable, retrieval endpoints return actionable persistence guidance. Without the auth variable, retrieval endpoints return actionable auth guidance.

## Architecture

![Townlight Courts architecture](docs/architecture-civiccourt.svg)

Townlight Courts is a module on top of Townlight Core. v0.1.2 is deterministic and local: no court CMS connector, live LLM call, warrant issuance, e-filing, judicial decision, or legal advice is shipped.

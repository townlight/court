# CivicCourt User Manual

## Non-Technical Staff

CivicCourt helps municipal court clerks prepare cited procedural answers, draft court forms for review, search public sample court records while hiding restricted records, and assemble hearing preparation checklists.

Court clerks remain responsible for every form, citation, procedure answer, and hearing checklist. CivicCourt does not decide cases, issue warrants, file documents, provide legal advice, expose sealed or juvenile records, or replace the court case-management system.

## IT / Technical

Install with:

```bash
python -m pip install -e ".[dev]"
python -m uvicorn civiccourt.main:app --host 127.0.0.1 --port 8143
```

Runtime dependency: `civiccore==0.2.0`.

Primary endpoints:

- `GET /health` - service and CivicCore version.
- `GET /civiccourt` - public sample UI.
- `POST /api/v1/civiccourt/procedure-answer` - cited procedure answer draft.
- `POST /api/v1/civiccourt/form-draft` - clerk-reviewed form draft.
- `POST /api/v1/civiccourt/search` - restricted-record-aware sample search.
- `POST /api/v1/civiccourt/hearing-prep` - hearing preparation checklist.

## Architecture

![CivicCourt architecture](docs/architecture-civiccourt.svg)

CivicCourt is a module on top of CivicCore. v0.1.0 is deterministic and local: no court CMS connector, live LLM call, warrant issuance, e-filing, judicial decision, or legal advice is shipped.

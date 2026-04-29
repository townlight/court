# CivicCourt

CivicCourt v0.1.1 ships the municipal court clerk support foundation plus optional workpaper persistence for CivicSuite: cited procedure Q&A, court form drafts, hearing preparation checklists, optional database-backed court form and hearing-prep workpapers, restricted-record-aware search, FastAPI runtime, public sample UI, docs, tests, browser QA, and release gates.

It is not a court case-management system, e-filing system, warrant issuance workflow, judicial decision tool, legal advice engine, live LLM runtime, or court CMS connector.

Install:

```bash
python -m pip install -e ".[dev]"
python -m uvicorn civiccourt.main:app --host 127.0.0.1 --port 8143
```

CivicCourt v0.1.1 is pinned to `civiccore==0.3.0`.

Set `CIVICCOURT_WORKPAPER_DB_URL` to enable local SQLAlchemy-backed court form and hearing-prep workpaper records. Without it, CivicCourt remains deterministic and stateless.

Apache 2.0 code. CC BY 4.0 docs.

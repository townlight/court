CivicCourt

CivicCourt published v0.1.2 is a foundation label under suite-wide release-recovery review. It provides municipal court clerk support foundations: cited procedure Q&A, review-required court form drafts, hearing preparation checklists, restricted-record-aware search, optional database-backed court form and hearing-prep workpaper records, bearer-token protection for persisted retrieval, FastAPI runtime, public sample UI, docs, tests, browser QA, and release gates. Do not promote it as production court software until the recovery gates and a future v1.0.0 definition of done are complete.

It is not a court case-management system, e-filing system, warrant issuance workflow, judicial decision tool, legal advice engine, live LLM runtime, or court CMS connector.

Install:
python -m pip install -e ".[dev]"
python -m uvicorn civiccourt.main:app --host 127.0.0.1 --port 8143

CivicCourt v0.1.2 is pinned to the published CivicCore v0.4.0 release wheel.

Set CIVICCOURT_WORKPAPER_DB_URL to enable local SQLAlchemy-backed court form and hearing-prep workpaper records.
Set CIVICCOURT_AUTH_TOKEN_ROLES to a JSON token-to-role map before exposing persisted retrieval.
Without the database variable, CivicCourt remains deterministic and stateless. Without the auth variable, persisted retrieval endpoints return actionable 503 guidance. With auth configured, anonymous callers receive 401 and unauthorized roles receive 403.

Apache 2.0 code. CC BY 4.0 docs.

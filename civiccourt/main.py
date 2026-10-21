"""FastAPI runtime foundation for Townlight Courts."""

import os

from civiccore import __version__ as CIVICCORE_VERSION
from civiccore.auth import AuthenticatedPrincipal, authorize_bearer_roles
from fastapi import Depends, FastAPI, HTTPException, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civiccourt import __version__
from civiccourt.case_search import CourtRecord, search_court_records
from civiccourt.forms import draft_court_form
from civiccourt.hearings import build_hearing_prep_checklist
from civiccourt.persistence import CourtWorkpaperRepository, StoredCourtForm, StoredHearingPrep
from civiccourt.procedure import CourtProcedureSource, answer_procedure_question
from civiccourt.public_ui import render_public_lookup_page

app = FastAPI(
    title='Townlight Courts',
    version=__version__,
    description='Municipal court clerk document and procedure support foundation for Townlight.',
)

_workpaper_repository: CourtWorkpaperRepository | None = None
_workpaper_db_url: str | None = None
_workpaper_bearer = HTTPBearer(auto_error=False)


@app.get("/favicon.ico", include_in_schema=False)
def favicon() -> Response:
    """Return an empty favicon response so browser QA has a clean console."""

    return Response(status_code=204)

PROCEDURE_SOURCES = [
    CourtProcedureSource(
        "c1",
        "Municipal court local rules",
        "Court clerk procedure, forms, hearings, and docket preparation rules",
        "Municipal Court Local Rule 1",
    )
]

SAMPLE_RECORDS = [
    CourtRecord("MC-100", "Public parking citation", "Citation hearing continued.", "Docket 100"),
    CourtRecord("MC-SEALED", "Sealed juvenile matter", "Restricted.", "Docket sealed", sealed=True),
]


class ProcedureQuestionRequest(BaseModel):
    question: str


class FormDraftRequest(BaseModel):
    case_id: str
    form_type: str
    fields: list[str]


class CourtSearchRequest(BaseModel):
    query: str


class HearingPrepRequest(BaseModel):
    case_id: str
    docket_items: list[str]


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "CivicCourt",
        "version": __version__,
        "status": "court clerk support foundation plus workpaper persistence",
        "message": (
            "Townlight Courts procedure Q&A, form drafts, restricted-record-aware search, hearing "
            "prep checklists, optional database-backed form and hearing-prep workpapers, and public UI "
            "foundation are online; court case management, e-filing, warrant issuance, judicial decisions, "
            "legal advice, live LLM calls, and court CMS connectors are not implemented yet."
        ),
        "next_step": (
            "Post-v0.1.2 roadmap: isolated deployment profile, SSO-aligned clerk access, "
            "and read-only court CMS adapters"
        ),
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "civiccourt",
        "version": __version__,
        "civiccore_version": CIVICCORE_VERSION,
    }


@app.get("/civiccourt", response_class=HTMLResponse)
def public_page() -> str:
    return render_public_lookup_page()


@app.post("/api/v1/civiccourt/procedure-answer")
def procedure_answer(request: ProcedureQuestionRequest) -> dict[str, object]:
    return answer_procedure_question(request.question, PROCEDURE_SOURCES).__dict__


@app.post("/api/v1/civiccourt/form-draft")
def form_draft(request: FormDraftRequest) -> dict[str, object]:
    if _workpaper_database_url() is not None:
        stored = _get_workpaper_repository().create_form(
            case_id=request.case_id,
            form_type=request.form_type,
            fields=request.fields,
        )
        return _stored_form_response(stored)

    draft = draft_court_form(request.case_id, request.form_type, request.fields)
    payload = draft.__dict__
    payload["form_id"] = None
    return payload


def _require_workpaper_reader(
    credentials: HTTPAuthorizationCredentials | None = Depends(_workpaper_bearer),
) -> AuthenticatedPrincipal:
    return authorize_bearer_roles(
        credentials,
        service_name='Townlight Courts',
        feature_name="persisted workpaper retrieval",
        token_roles_env_var="CIVICCOURT_AUTH_TOKEN_ROLES",
        allowed_roles={"workpaper_reader", "court_clerk_admin"},
    )


@app.get("/api/v1/civiccourt/form-draft/{form_id}")
def get_form_draft(
    form_id: str,
    _principal: AuthenticatedPrincipal = Depends(_require_workpaper_reader),
) -> dict[str, object]:
    if _workpaper_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "Townlight Courts persisted workpaper retrieval auth is not configured.",
                "fix": (
                    "Set CIVICCOURT_AUTH_TOKEN_ROLES before exposing persisted court form draft retrieval."
                ),
            },
        )
    stored = _get_workpaper_repository().get_form(form_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Court form draft record not found.",
                "fix": "Use a form_id returned by POST /api/v1/civiccourt/form-draft.",
            },
        )
    return _stored_form_response(stored)


@app.post("/api/v1/civiccourt/search")
def record_search(request: CourtSearchRequest) -> dict[str, object]:
    return search_court_records(request.query, SAMPLE_RECORDS).__dict__


@app.post("/api/v1/civiccourt/hearing-prep")
def hearing_prep(request: HearingPrepRequest) -> dict[str, object]:
    if _workpaper_database_url() is not None:
        stored = _get_workpaper_repository().create_hearing_prep(
            case_id=request.case_id,
            docket_items=request.docket_items,
        )
        return _stored_hearing_prep_response(stored)

    prep = build_hearing_prep_checklist(request.case_id, request.docket_items)
    payload = prep.__dict__
    payload["prep_id"] = None
    return payload


@app.get("/api/v1/civiccourt/hearing-prep/{prep_id}")
def get_hearing_prep(
    prep_id: str,
    _principal: AuthenticatedPrincipal = Depends(_require_workpaper_reader),
) -> dict[str, object]:
    if _workpaper_database_url() is None:
        raise HTTPException(
            status_code=503,
            detail={
                "message": "Townlight Courts workpaper persistence is not configured.",
                "fix": "Set CIVICCOURT_WORKPAPER_DB_URL to retrieve persisted hearing prep records.",
            },
        )
    stored = _get_workpaper_repository().get_hearing_prep(prep_id)
    if stored is None:
        raise HTTPException(
            status_code=404,
            detail={
                "message": "Hearing prep record not found.",
                "fix": "Use a prep_id returned by POST /api/v1/civiccourt/hearing-prep.",
            },
        )
    return _stored_hearing_prep_response(stored)


def _workpaper_database_url() -> str | None:
    return os.environ.get("CIVICCOURT_WORKPAPER_DB_URL")


def _get_workpaper_repository() -> CourtWorkpaperRepository:
    global _workpaper_db_url, _workpaper_repository
    db_url = _workpaper_database_url()
    if db_url is None:
        raise RuntimeError("CIVICCOURT_WORKPAPER_DB_URL is not configured.")
    if _workpaper_repository is None or db_url != _workpaper_db_url:
        _dispose_workpaper_repository()
        _workpaper_db_url = db_url
        _workpaper_repository = CourtWorkpaperRepository(db_url=db_url)
    return _workpaper_repository


def _dispose_workpaper_repository() -> None:
    global _workpaper_repository
    if _workpaper_repository is not None:
        _workpaper_repository.engine.dispose()
        _workpaper_repository = None


def _stored_form_response(stored: StoredCourtForm) -> dict[str, object]:
    return {
        "form_id": stored.form_id,
        "case_id": stored.case_id,
        "form_type": stored.form_type,
        "fields": list(stored.fields),
        "clerk_review_required": stored.clerk_review_required,
        "not_filed": stored.not_filed,
        "boundary": stored.boundary,
        "created_at": stored.created_at.isoformat(),
    }


def _stored_hearing_prep_response(stored: StoredHearingPrep) -> dict[str, object]:
    return {
        "prep_id": stored.prep_id,
        "case_id": stored.case_id,
        "checklist": list(stored.checklist),
        "clerk_review_required": stored.clerk_review_required,
        "not_scheduling": stored.not_scheduling,
        "created_at": stored.created_at.isoformat(),
    }

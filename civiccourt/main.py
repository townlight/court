"""FastAPI runtime foundation for CivicCourt."""

from civiccore import __version__ as CIVICCORE_VERSION
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from civiccourt import __version__
from civiccourt.case_search import CourtRecord, search_court_records
from civiccourt.forms import draft_court_form
from civiccourt.hearings import build_hearing_prep_checklist
from civiccourt.procedure import CourtProcedureSource, answer_procedure_question
from civiccourt.public_ui import render_public_lookup_page

app = FastAPI(
    title="CivicCourt",
    version=__version__,
    description="Municipal court clerk document and procedure support foundation for CivicSuite.",
)

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
        "status": "court clerk support foundation",
        "message": (
            "CivicCourt procedure Q&A, form drafts, restricted-record-aware search, hearing "
            "prep checklists, and public UI foundation are online; court case management, "
            "e-filing, warrant issuance, judicial decisions, legal advice, live LLM calls, "
            "and court CMS connectors are not implemented yet."
        ),
        "next_step": "Post-v0.1.0 roadmap: isolated deployment profile and read-only court CMS adapters",
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
    return draft_court_form(request.case_id, request.form_type, request.fields).__dict__


@app.post("/api/v1/civiccourt/search")
def record_search(request: CourtSearchRequest) -> dict[str, object]:
    return search_court_records(request.query, SAMPLE_RECORDS).__dict__


@app.post("/api/v1/civiccourt/hearing-prep")
def hearing_prep(request: HearingPrepRequest) -> dict[str, object]:
    return build_hearing_prep_checklist(request.case_id, request.docket_items).__dict__

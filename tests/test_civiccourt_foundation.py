from civiccourt import __version__
from civiccourt.case_search import CourtRecord, search_court_records
from civiccourt.forms import draft_court_form
from civiccourt.hearings import build_hearing_prep_checklist
from civiccourt.procedure import CourtProcedureSource, answer_procedure_question


def test_version_is_release_version():
    assert __version__ == "0.1.0"


def test_procedure_answer_is_cited_and_not_legal_advice():
    result = answer_procedure_question(
        "how do I prepare a continuance form",
        [CourtProcedureSource("c1", "Local rules", "continuance form", "Local Rule 3")],
    )
    assert result.citations == ("Local Rule 3",)
    assert result.clerk_review_required is True
    assert "does not provide legal advice" in result.boundary


def test_form_draft_requires_clerk_review_and_is_not_filed():
    draft = draft_court_form("MC-100", "summons", ["defendant", "hearing date"])
    assert draft.clerk_review_required is True
    assert draft.not_filed is True
    assert "does not issue warrants" in draft.boundary


def test_search_hides_sealed_and_juvenile_records():
    result = search_court_records(
        "hearing",
        [
            CourtRecord("MC-100", "Public case", "Hearing continued.", "Docket 100"),
            CourtRecord("MC-200", "Sealed case", "Restricted", "Docket 200", sealed=True),
            CourtRecord("MC-300", "Juvenile case", "Restricted", "Docket 300", juvenile=True),
        ],
    )
    assert len(result.results) == 1
    assert result.results[0].case_id == "MC-100"
    assert result.restricted_records_hidden is True


def test_hearing_prep_is_not_scheduling():
    checklist = build_hearing_prep_checklist("MC-100", ["Confirm interpreter", "Print docket"])
    assert checklist.clerk_review_required is True
    assert checklist.not_scheduling is True

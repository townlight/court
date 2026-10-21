"""Court form preparation helpers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CourtFormDraft:
    case_id: str
    form_type: str
    fields: tuple[str, ...]
    clerk_review_required: bool
    not_filed: bool
    boundary: str


def draft_court_form(case_id: str, form_type: str, fields: list[str]) -> CourtFormDraft:
    return CourtFormDraft(
        case_id=case_id,
        form_type=form_type,
        fields=tuple(fields),
        clerk_review_required=True,
        not_filed=True,
        boundary=(
            "Draft only: Townlight Courts does not issue warrants, file documents, schedule hearings, "
            "or replace the court case-management system."
        ),
    )

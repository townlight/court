"""Hearing preparation checklist helpers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class HearingPrepChecklist:
    case_id: str
    checklist: tuple[str, ...]
    clerk_review_required: bool
    not_scheduling: bool


def build_hearing_prep_checklist(case_id: str, docket_items: list[str]) -> HearingPrepChecklist:
    checklist = tuple(docket_items) if docket_items else ("Confirm local rule checklist.",)
    return HearingPrepChecklist(
        case_id=case_id,
        checklist=checklist,
        clerk_review_required=True,
        not_scheduling=True,
    )

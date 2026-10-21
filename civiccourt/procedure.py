"""Municipal court procedure Q&A helpers."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CourtProcedureSource:
    source_id: str
    title: str
    text: str
    citation: str


@dataclass(frozen=True)
class CourtProcedureAnswer:
    answer: str
    citations: tuple[str, ...]
    clerk_review_required: bool
    boundary: str


def answer_procedure_question(
    question: str, sources: list[CourtProcedureSource]
) -> CourtProcedureAnswer:
    citations = tuple(source.citation for source in sources if source.text)
    return CourtProcedureAnswer(
        answer=(
            f"Draft municipal court procedure answer for: {question}. "
            "Verify against the cited local rule before use."
        ),
        citations=citations,
        clerk_review_required=True,
        boundary=(
            "Townlight Courts provides clerk support over court procedures and forms; it does not "
            "provide legal advice, decide cases, or replace the court CMS."
        ),
    )

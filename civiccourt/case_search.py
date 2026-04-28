"""Court record search helpers with sealed-record boundaries."""

from dataclasses import dataclass


@dataclass(frozen=True)
class CourtRecord:
    case_id: str
    title: str
    summary: str
    citation: str
    sealed: bool = False
    juvenile: bool = False


@dataclass(frozen=True)
class CourtSearchResult:
    query: str
    results: tuple[CourtRecord, ...]
    restricted_records_hidden: bool
    boundary: str


def search_court_records(query: str, records: list[CourtRecord]) -> CourtSearchResult:
    visible = tuple(record for record in records if not record.sealed and not record.juvenile)
    return CourtSearchResult(
        query=query,
        results=visible,
        restricted_records_hidden=len(visible) != len(records),
        boundary=(
            "CivicCourt search excludes sealed and juvenile records in v0.1.1 and is not a "
            "court case-management system."
        ),
    )

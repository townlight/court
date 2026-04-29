from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import Engine, create_engine

from civiccourt.forms import draft_court_form
from civiccourt.hearings import build_hearing_prep_checklist


metadata = sa.MetaData()

court_form_records = sa.Table(
    "court_form_records",
    metadata,
    sa.Column("form_id", sa.String(36), primary_key=True),
    sa.Column("case_id", sa.String(160), nullable=False),
    sa.Column("form_type", sa.String(255), nullable=False),
    sa.Column("fields", sa.JSON(), nullable=False),
    sa.Column("clerk_review_required", sa.Boolean(), nullable=False),
    sa.Column("not_filed", sa.Boolean(), nullable=False),
    sa.Column("boundary", sa.Text(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civiccourt",
)

hearing_prep_records = sa.Table(
    "hearing_prep_records",
    metadata,
    sa.Column("prep_id", sa.String(36), primary_key=True),
    sa.Column("case_id", sa.String(160), nullable=False),
    sa.Column("checklist", sa.JSON(), nullable=False),
    sa.Column("clerk_review_required", sa.Boolean(), nullable=False),
    sa.Column("not_scheduling", sa.Boolean(), nullable=False),
    sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
    schema="civiccourt",
)


@dataclass(frozen=True)
class StoredCourtForm:
    form_id: str
    case_id: str
    form_type: str
    fields: tuple[str, ...]
    clerk_review_required: bool
    not_filed: bool
    boundary: str
    created_at: datetime


@dataclass(frozen=True)
class StoredHearingPrep:
    prep_id: str
    case_id: str
    checklist: tuple[str, ...]
    clerk_review_required: bool
    not_scheduling: bool
    created_at: datetime


class CourtWorkpaperRepository:
    """SQLAlchemy-backed court form and hearing-prep workpaper records."""

    def __init__(self, *, db_url: str | None = None, engine: Engine | None = None) -> None:
        base_engine = engine or create_engine(db_url or "sqlite+pysqlite:///:memory:", future=True)
        if base_engine.dialect.name == "sqlite":
            self.engine = base_engine.execution_options(schema_translate_map={"civiccourt": None})
        else:
            self.engine = base_engine
            with self.engine.begin() as connection:
                connection.execute(sa.text("CREATE SCHEMA IF NOT EXISTS civiccourt"))
        metadata.create_all(self.engine)

    def create_form(self, *, case_id: str, form_type: str, fields: list[str]) -> StoredCourtForm:
        draft = draft_court_form(case_id, form_type, fields)
        stored = StoredCourtForm(
            form_id=str(uuid4()),
            case_id=draft.case_id,
            form_type=draft.form_type,
            fields=draft.fields,
            clerk_review_required=draft.clerk_review_required,
            not_filed=draft.not_filed,
            boundary=draft.boundary,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(
                court_form_records.insert().values(
                    form_id=stored.form_id,
                    case_id=stored.case_id,
                    form_type=stored.form_type,
                    fields=list(stored.fields),
                    clerk_review_required=stored.clerk_review_required,
                    not_filed=stored.not_filed,
                    boundary=stored.boundary,
                    created_at=stored.created_at,
                )
            )
        return stored

    def get_form(self, form_id: str) -> StoredCourtForm | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(court_form_records).where(court_form_records.c.form_id == form_id)
            ).mappings().first()
        if row is None:
            return None
        return _row_to_form(row)

    def create_hearing_prep(self, *, case_id: str, docket_items: list[str]) -> StoredHearingPrep:
        prep = build_hearing_prep_checklist(case_id, docket_items)
        stored = StoredHearingPrep(
            prep_id=str(uuid4()),
            case_id=prep.case_id,
            checklist=prep.checklist,
            clerk_review_required=prep.clerk_review_required,
            not_scheduling=prep.not_scheduling,
            created_at=datetime.now(UTC),
        )
        with self.engine.begin() as connection:
            connection.execute(
                hearing_prep_records.insert().values(
                    prep_id=stored.prep_id,
                    case_id=stored.case_id,
                    checklist=list(stored.checklist),
                    clerk_review_required=stored.clerk_review_required,
                    not_scheduling=stored.not_scheduling,
                    created_at=stored.created_at,
                )
            )
        return stored

    def get_hearing_prep(self, prep_id: str) -> StoredHearingPrep | None:
        with self.engine.begin() as connection:
            row = connection.execute(
                sa.select(hearing_prep_records).where(hearing_prep_records.c.prep_id == prep_id)
            ).mappings().first()
        if row is None:
            return None
        return _row_to_hearing_prep(row)


def _row_to_form(row: object) -> StoredCourtForm:
    data = dict(row)
    return StoredCourtForm(
        form_id=data["form_id"],
        case_id=data["case_id"],
        form_type=data["form_type"],
        fields=tuple(data["fields"]),
        clerk_review_required=data["clerk_review_required"],
        not_filed=data["not_filed"],
        boundary=data["boundary"],
        created_at=data["created_at"],
    )


def _row_to_hearing_prep(row: object) -> StoredHearingPrep:
    data = dict(row)
    return StoredHearingPrep(
        prep_id=data["prep_id"],
        case_id=data["case_id"],
        checklist=tuple(data["checklist"]),
        clerk_review_required=data["clerk_review_required"],
        not_scheduling=data["not_scheduling"],
        created_at=data["created_at"],
    )

from __future__ import annotations

from pathlib import Path

from fastapi.testclient import TestClient

from civiccourt.main import app, _dispose_workpaper_repository
from civiccourt.persistence import CourtWorkpaperRepository


client = TestClient(app)


def test_repository_persists_form_and_hearing_prep(tmp_path: Path) -> None:
    db_path = tmp_path / "civiccourt.db"
    db_url = f"sqlite+pysqlite:///{db_path.as_posix()}"

    repository = CourtWorkpaperRepository(db_url=db_url)
    form = repository.create_form(case_id="MC-100", form_type="summons", fields=["name"])
    prep = repository.create_hearing_prep(case_id="MC-100", docket_items=["Confirm interpreter"])
    repository.engine.dispose()

    reloaded = CourtWorkpaperRepository(db_url=db_url)
    stored_form = reloaded.get_form(form.form_id)
    stored_prep = reloaded.get_hearing_prep(prep.prep_id)
    reloaded.engine.dispose()

    assert stored_form is not None
    assert stored_form.case_id == "MC-100"
    assert stored_form.not_filed is True
    assert stored_prep is not None
    assert stored_prep.not_scheduling is True
    assert stored_prep.checklist == ("Confirm interpreter",)
    db_path.unlink()


def test_workpaper_persistence_api_round_trip(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civiccourt-api.db"
    monkeypatch.setenv("CIVICCOURT_WORKPAPER_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    _dispose_workpaper_repository()

    created_form = client.post(
        "/api/v1/civiccourt/form-draft",
        json={"case_id": "MC-100", "form_type": "summons", "fields": ["name"]},
    )
    form_id = created_form.json()["form_id"]
    fetched_form = client.get(f"/api/v1/civiccourt/form-draft/{form_id}")
    created_prep = client.post(
        "/api/v1/civiccourt/hearing-prep",
        json={"case_id": "MC-100", "docket_items": ["Confirm interpreter"]},
    )
    prep_id = created_prep.json()["prep_id"]
    fetched_prep = client.get(f"/api/v1/civiccourt/hearing-prep/{prep_id}")

    _dispose_workpaper_repository()
    monkeypatch.delenv("CIVICCOURT_WORKPAPER_DB_URL")

    assert created_form.status_code == 200
    assert form_id
    assert fetched_form.status_code == 200
    assert fetched_form.json()["not_filed"] is True
    assert created_prep.status_code == 200
    assert prep_id
    assert fetched_prep.status_code == 200
    assert fetched_prep.json()["not_scheduling"] is True
    db_path.unlink()


def test_get_form_without_persistence_returns_actionable_503(monkeypatch) -> None:
    monkeypatch.delenv("CIVICCOURT_WORKPAPER_DB_URL", raising=False)
    _dispose_workpaper_repository()

    response = client.get("/api/v1/civiccourt/form-draft/example")

    assert response.status_code == 503
    detail = response.json()["detail"]
    assert detail["message"] == "CivicCourt workpaper persistence is not configured."
    assert "Set CIVICCOURT_WORKPAPER_DB_URL" in detail["fix"]


def test_get_hearing_prep_missing_id_returns_actionable_404(monkeypatch, tmp_path: Path) -> None:
    db_path = tmp_path / "civiccourt-missing.db"
    monkeypatch.setenv("CIVICCOURT_WORKPAPER_DB_URL", f"sqlite+pysqlite:///{db_path.as_posix()}")
    _dispose_workpaper_repository()

    response = client.get("/api/v1/civiccourt/hearing-prep/missing")

    _dispose_workpaper_repository()
    monkeypatch.delenv("CIVICCOURT_WORKPAPER_DB_URL")

    assert response.status_code == 404
    detail = response.json()["detail"]
    assert detail["message"] == "Hearing prep record not found."
    assert "POST /api/v1/civiccourt/hearing-prep" in detail["fix"]
    db_path.unlink()

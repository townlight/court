from fastapi.testclient import TestClient

from civiccourt import __version__
from civiccourt.main import app

client = TestClient(app)


def test_root_reports_honest_current_state():
    payload = client.get("/").json()
    assert payload["name"] == "CivicCourt"
    assert payload["version"] == __version__
    assert "court case management" in payload["message"]
    assert "not implemented yet" in payload["message"]


def test_health_reports_civiccore_pin():
    assert client.get("/health").json() == {
        "status": "ok",
        "service": "civiccourt",
        "version": "0.1.1",
        "civiccore_version": "0.3.0",
    }


def test_public_ui_contains_version_boundaries_and_dependency():
    text = client.get("/civiccourt").text
    assert "CivicCourt v0.1.1" in text
    assert "No court CMS replacement" in text
    assert "civiccore==0.3.0" in text


def test_api_endpoints_return_deterministic_payloads():
    assert (
        client.post(
            "/api/v1/civiccourt/procedure-answer",
            json={"question": "continuance process"},
        ).status_code
        == 200
    )
    assert (
        client.post(
            "/api/v1/civiccourt/form-draft",
            json={"case_id": "MC-100", "form_type": "summons", "fields": ["name"]},
        ).json()["not_filed"]
        is True
    )
    assert (
        client.post("/api/v1/civiccourt/search", json={"query": "hearing"}).json()[
            "restricted_records_hidden"
        ]
        is True
    )
    assert (
        client.post(
            "/api/v1/civiccourt/hearing-prep",
            json={"case_id": "MC-100", "docket_items": ["Confirm interpreter"]},
        ).json()["not_scheduling"]
        is True
    )

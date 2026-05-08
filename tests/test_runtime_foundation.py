from pathlib import Path
import re
import tomllib

from fastapi.testclient import TestClient

from civiccourt import __version__
from civiccourt.main import app

client = TestClient(app)
ROOT = Path(__file__).resolve().parents[1]


def test_root_reports_honest_current_state():
    payload = client.get("/").json()
    assert payload["name"] == "CivicCourt"
    assert payload["version"] == __version__
    assert payload["status"] == "court clerk support foundation plus workpaper persistence"
    assert "database-backed form and hearing-prep workpapers" in payload["message"]
    assert "court case management" in payload["message"]
    assert "not implemented yet" in payload["message"]


def test_health_reports_civiccore_pin():
    payload = client.get("/health").json()

    assert payload["status"] == "ok"
    assert payload["service"] == "civiccourt"
    assert payload["version"] == "0.1.2"
    assert re.fullmatch(r"\d+\.\d+\.\d+", payload["civiccore_version"])


def test_public_ui_contains_version_boundaries_and_dependency():
    text = client.get("/civiccourt").text
    assert "CivicCourt v0.1.2" in text
    assert "No court CMS replacement" in text
    assert "published foundation label under suite-wide release-recovery review" in text
    assert "CivicCore v0.4.0 release wheel" in text


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
        ).json()["form_id"]
        is None
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
        ).json()["prep_id"]
        is None
    )


def test_release_script_prefers_python3_and_avoids_windowsapps_fallback() -> None:
    lines = (ROOT / "scripts" / "verify-release.sh").read_text(encoding="utf-8").splitlines()
    candidate_line = next(line for line in lines if line.startswith("PYTHON_CANDIDATES+="))

    assert "python3 python py" in candidate_line
    assert "WindowsApps" not in candidate_line


def test_pyproject_uses_published_civiccore_release_wheel() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))

    dependencies = pyproject["project"]["dependencies"]
    assert any(
        dependency
        == "civiccore @ https://github.com/CivicSuite/civiccore/releases/download/v0.4.0/civiccore-0.4.0-py3-none-any.whl"
        for dependency in dependencies
    )
    assert pyproject["tool"]["hatch"]["metadata"]["allow-direct-references"] is True


def test_docs_gate_rejects_stale_shipping_product_ready_and_mojibake_markers() -> None:
    text = (ROOT / "scripts" / "verify-docs.sh").read_text(encoding="utf-8")

    assert '"Shipping v0.1.2"' in text
    assert '"product-ready"' in text
    assert '"production-ready"' in text
    assert '"Ã¢"' in text or '"â"' in text


def test_docs_index_marks_foundation_label_provisional() -> None:
    text = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")

    assert "published foundation label under suite-wide release-recovery review" in text
    assert "v0.1.2 foundation under recovery review" in text
    assert "release-recovery-status.md" in text
    assert "Shipping v0.1.2" not in text


def test_recovery_status_blocks_product_promotion() -> None:
    text = (ROOT / "docs" / "release-recovery-status.md").read_text(encoding="utf-8")

    assert "not product-ready" in text
    assert "must not be promoted as production municipal court software" in text

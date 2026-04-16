import os
from importlib import reload

from fastapi.testclient import TestClient


def test_create_and_list_leads(tmp_path):
    db_path = tmp_path / "test.db"
    os.environ["DB_PATH"] = str(db_path)

    import app.main as main_module

    reload(main_module)
    client = TestClient(main_module.app)

    payload = {
        "full_name": "Mario Torres",
        "phone": "+34 699123123",
        "email": "mario@example.com",
        "postal_code": "46001",
        "city": "Valencia",
        "region": "Comunidad Valenciana",
        "lead_type": "portabilidad",
        "budget_eur": 39,
        "wants_portability": True,
        "preferred_channel": "email",
        "best_time_slot": "manana",
        "has_confirmed_coverage": True,
        "gdpr_consent": True,
        "source": "meta_ads",
    }

    response = client.post("/leads", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] >= 1
    assert data["priority"] in {"alta", "media", "baja"}

    listed = client.get("/leads?limit=10")
    assert listed.status_code == 200
    assert len(listed.json()) >= 1


def test_preview_route(tmp_path):
    db_path = tmp_path / "test.db"
    os.environ["DB_PATH"] = str(db_path)

    import app.main as main_module

    reload(main_module)
    client = TestClient(main_module.app)

    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")

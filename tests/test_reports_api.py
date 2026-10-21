VALID_CSV = b"""date,category,amount,description
2026-07-01,Servicios,450000,Internet
2026-07-05,Nomina,2000000,Pago quincenal
"""


def upload(client, content=VALID_CSV, filename="gastos.csv"):
    return client.post("/reports", files={"file": (filename, content, "text/csv")})


def test_create_report_happy_path(client):
    response = upload(client)
    assert response.status_code == 200
    body = response.json()
    assert body["summary_text"] == "Fake summary."
    assert body["total_amount"] == 2450000
    assert len(body["expenses"]) == 2


def test_create_report_with_malformed_csv_returns_400(client):
    response = upload(client, content=b"date,category,amount\n2026-07-01,Servicios,450000\n")
    assert response.status_code == 400


def test_list_reports(client):
    upload(client)
    response = client.get("/reports")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_report_by_id(client):
    created = upload(client).json()
    response = client.get(f"/reports/{created['id']}")
    assert response.status_code == 200
    assert response.json()["id"] == created["id"]


def test_get_report_not_found(client):
    response = client.get("/reports/999")
    assert response.status_code == 404


def test_requires_api_key(client):
    for key in ("", "wrong"):
        assert client.get("/reports", headers={"X-API-Key": key}).status_code == 401


def test_csv_over_1mb_returns_413(client):
    response = upload(client, content=VALID_CSV + b"x" * 1_000_000)
    assert response.status_code == 413


def test_summary_language_is_passed_through(client, monkeypatch):
    seen = {}
    monkeypatch.setattr("app.reports.generate_summary", lambda **kwargs: seen.update(kwargs) or "Resumen.")
    response = client.post("/reports", files={"file": ("g.csv", VALID_CSV, "text/csv")}, data={"language": "es"})
    assert response.status_code == 200
    assert seen["language"] == "es"


def test_unsupported_language_returns_422(client):
    response = client.post("/reports", files={"file": ("g.csv", VALID_CSV, "text/csv")}, data={"language": "fr"})
    assert response.status_code == 422

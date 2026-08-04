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

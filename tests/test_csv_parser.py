import pytest

from app.csv_parser import parse_expenses_csv

VALID_CSV = b"""date,category,amount,description
2026-07-01,Servicios,450000,Internet
2026-07-05,Nomina,2000000,Pago quincenal
"""


def test_parses_valid_csv():
    rows = parse_expenses_csv(VALID_CSV)
    assert len(rows) == 2
    assert rows[0]["category"] == "Servicios"
    assert rows[0]["amount"] == 450000.0


def test_missing_column_raises():
    csv_bytes = b"date,category,amount\n2026-07-01,Servicios,450000\n"
    with pytest.raises(ValueError, match="Missing required columns"):
        parse_expenses_csv(csv_bytes)


def test_non_numeric_amount_raises():
    csv_bytes = b"date,category,amount,description\n2026-07-01,Servicios,notanumber,Internet\n"
    with pytest.raises(ValueError, match="Row 2"):
        parse_expenses_csv(csv_bytes)


def test_empty_csv_raises():
    csv_bytes = b"date,category,amount,description\n"
    with pytest.raises(ValueError, match="no data rows"):
        parse_expenses_csv(csv_bytes)

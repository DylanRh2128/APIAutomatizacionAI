from datetime import date

from app.aggregation import aggregate_expenses


def expense(amount, category="Servicios"):
    return {"date": date(2026, 7, 1), "category": category, "amount": amount, "description": ""}


def test_totals_by_category_and_overall():
    rows = [expense(100, "A"), expense(200, "A"), expense(50, "B")]
    result = aggregate_expenses(rows)
    assert result["total_amount"] == 350
    assert result["totals_by_category"] == {"A": 300, "B": 50}


def test_detects_outlier():
    # 9 normal expenses around 100, one clear outlier at 10000
    rows = [expense(100, "A") for _ in range(9)] + [expense(10000, "A")]
    result = aggregate_expenses(rows)
    assert len(result["outliers"]) == 1
    assert result["outliers"][0]["amount"] == 10000


def test_no_outliers_when_category_has_one_expense():
    rows = [expense(100, "A")]
    result = aggregate_expenses(rows)
    assert result["outliers"] == []

import statistics
from collections import defaultdict


def aggregate_expenses(expenses: list[dict]) -> dict:
    total_amount = sum(e["amount"] for e in expenses)

    by_category: dict[str, list[dict]] = defaultdict(list)
    for e in expenses:
        by_category[e["category"]].append(e)

    totals_by_category = {
        category: sum(e["amount"] for e in rows) for category, rows in by_category.items()
    }

    outliers = []
    for category, rows in by_category.items():
        amounts = [e["amount"] for e in rows]
        if len(amounts) < 2:
            continue
        mean = statistics.mean(amounts)
        stdev = statistics.stdev(amounts)
        if stdev == 0:
            continue
        for e in rows:
            if abs(e["amount"] - mean) > 2 * stdev:
                outliers.append(e)

    return {
        "total_amount": total_amount,
        "totals_by_category": totals_by_category,
        "outliers": outliers,
    }

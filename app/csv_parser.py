import csv
import io
from datetime import date, datetime

REQUIRED_COLUMNS = {"date", "category", "amount", "description"}


class InvalidCSVError(ValueError):
    pass


def parse_expenses_csv(raw: bytes) -> list[dict]:
    text = raw.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))

    if reader.fieldnames is None or not REQUIRED_COLUMNS.issubset(reader.fieldnames):
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        raise InvalidCSVError(f"Missing required columns: {sorted(missing)}")

    rows = []
    for i, row in enumerate(reader, start=2):  # row 1 is the header
        try:
            rows.append(
                {
                    "date": datetime.strptime(row["date"].strip(), "%Y-%m-%d").date(),
                    "category": row["category"].strip(),
                    "amount": float(row["amount"]),
                    "description": row["description"].strip(),
                }
            )
        except (ValueError, AttributeError) as e:
            raise InvalidCSVError(f"Row {i}: {e}") from e

    if not rows:
        raise InvalidCSVError("CSV has no data rows")

    return rows

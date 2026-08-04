# Testing

Run with: `pytest` (needs `DATABASE_URL` and `ANTHROPIC_API_KEY` set to any dummy value — the
API tests use an in-memory SQLite database and a mocked Claude call, never the real ones).

- `tests/test_csv_parser.py` — valid CSV, missing column, non-numeric amount, empty file.
- `tests/test_aggregation.py` — totals by category, outlier detection, no false outliers when a
  category has a single expense.
- `tests/test_reports_api.py` — `POST /reports` happy path and malformed CSV, `GET /reports`,
  `GET /reports/{id}` including the 404 case. `app.reports.generate_summary` is monkey-patched
  (see `tests/conftest.py`) so tests never call the real Claude API.

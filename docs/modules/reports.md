# `app/reports.py`

The API layer: the three `/reports` endpoints. `create_report` is the only non-trivial one —
it chains `csv_parser` → `aggregation` → `llm_client`, and only builds/commits the `Report` +
`Expense` rows after the LLM call succeeds, so a failed summary never leaves a half-written
report in the database. `list_reports` and `get_report` are plain SQLAlchemy queries.

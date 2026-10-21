# Architecture

## Flow

`POST /reports` → parse CSV (`app/csv_parser.py`) → aggregate in Python
(`app/aggregation.py`) → ask the LLM to write the summary from those numbers
(`app/llm_client.py`) → persist `Report` + `Expense` rows (`app/models.py`) → return the
full report.

The DB write only happens after the LLM call succeeds, so a failed summary never leaves a
half-written report in the database.

## Key decision: The LLM never does arithmetic

Totals, per-category sums, and outlier detection (amount more than 2 standard deviations from
its category's mean) are all plain Python (`statistics` module). The LLM only receives the
already-computed numbers and writes the narrative. LLMs are not reliable at exact arithmetic —
handing the LLM a CSV and asking it to "summarize the totals" would risk a wrong number in the
report.

## Junior-acceptable vs. what a senior would do differently

- **Schema management**: tables are created with `Base.metadata.create_all()` on startup.
  Junior-acceptable for a portfolio project; a senior would use Alembic migrations from day one
  so schema changes in production are versioned and reversible.
- **No authentication**: the API has no login/API key yet (documented as a known gap, not an
  oversight). A senior would not ship even an MVP publicly reachable without at least an API key.
- **Synchronous DB access**: uses the sync SQLAlchemy API instead of async SQLAlchemy + an async
  driver. Fine at this scale; a senior optimizing for throughput would go async end-to-end.
- **No retry on OpenAI API failures**: a transient failure just returns a 502 to the caller. A
  senior would add a bounded retry with backoff before giving up.

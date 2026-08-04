# Expense Report Summary API

## Problem

Small business owners track expenses in a spreadsheet but rarely have time to turn that into
an actual executive summary — what did we spend, on what, and did anything look off this month.

## Solution

Upload a CSV of expenses and get back a report: totals, a breakdown by category, statistical
outliers (unusually large expenses within their category), and a plain-English executive
summary written by Claude. Reports are saved, so you can list and revisit past ones.

All math (totals, category breakdowns, outlier detection) is computed in plain Python — Claude
is only used to write the narrative summary from numbers it's given, never to do the arithmetic
itself. See [docs/architecture.md](docs/architecture.md) for why.

## Stack

Python + FastAPI + PostgreSQL (SQLAlchemy) + Claude API (Anthropic).

## How to run it

```bash
python -m venv .venv
.venv/Scripts/activate        # or source .venv/bin/activate on Linux/Mac
pip install -r requirements.txt

cp .env.example .env          # then fill in DATABASE_URL and ANTHROPIC_API_KEY
uvicorn app.main:app --reload
```

Open `http://localhost:8000/docs` for the interactive API docs.

## Run it with Docker

No local Python/PostgreSQL install needed — just Docker:

```bash
ANTHROPIC_API_KEY=your-real-key docker compose up --build
```

The API is on `http://localhost:8001` (mapped from the container's port 8000, to avoid clashing
with a locally-running Postgres/instance on 8000/5432). See
[docs/deployment.md](docs/deployment.md).

## Try it

```bash
curl -F "file=@sample_expenses.csv" http://localhost:8000/reports
```

CSV must have columns: `date` (YYYY-MM-DD), `category`, `amount`, `description`.

## Documentation

- [docs/architecture.md](docs/architecture.md) — key decisions, junior-acceptable vs. what a senior would do differently
- [docs/api-reference.md](docs/api-reference.md) — endpoints
- [docs/data-model.md](docs/data-model.md) — database schema
- [docs/security.md](docs/security.md) — secrets handling
- [docs/testing.md](docs/testing.md) — what's tested and why
- [docs/deployment.md](docs/deployment.md) — Docker

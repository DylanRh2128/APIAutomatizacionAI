# API Reference

Every endpoint below requires header `X-API-Key` matching the server's `API_KEY` (`401` if
missing or wrong) — each report costs a OpenAI API call, so the upload can't be left open.

## `POST /reports`

Upload a CSV file (`multipart/form-data`, field name `file`) and get back the generated report.

CSV columns required: `date` (`YYYY-MM-DD`), `category`, `amount` (number), `description`.

Response `200`:
```json
{
  "id": 1,
  "created_at": "2026-08-03T12:00:00",
  "period_start": "2026-07-01",
  "period_end": "2026-07-31",
  "total_amount": 2450000.0,
  "source_filename": "gastos.csv",
  "summary_text": "...",
  "expenses": [
    {"date": "2026-07-01", "category": "Servicios", "amount": 450000.0, "description": "Internet"}
  ]
}
```

Errors: `400` if the CSV is missing a required column, has a non-numeric amount, or has no data
rows. `413` if the file is over 1 MB. `502` if the OpenAI API call fails.

## `GET /reports`

Lists past reports (no expense detail), most recent first.

## `GET /reports/{id}`

Same shape as the `POST /reports` response. `404` if the report doesn't exist.

### Optional `language` form field

`POST /reports` accepts `language` = `en` (default) or `es` alongside the file; it only changes the
language the summary is written in (`422` for anything else). The numbers are unaffected.

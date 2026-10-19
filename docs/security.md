# Security

- `DATABASE_URL` and `ANTHROPIC_API_KEY` are read from environment variables (`.env`, loaded via
  `python-dotenv`). `.env` is git-ignored; only `.env.example` (with placeholder values) is
  committed.
- Uploaded CSVs are parsed with Python's stdlib `csv` module (no `eval`/dynamic code execution).
  Malformed rows are rejected with a `400` before anything is written to the database.
- Every endpoint requires `X-API-Key` (compared with `secrets.compare_digest`), since each upload
  spends Claude API credits. Uploads are capped at 1 MB and rejected with `413` before parsing.

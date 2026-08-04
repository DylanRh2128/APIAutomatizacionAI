# Security

- `DATABASE_URL` and `ANTHROPIC_API_KEY` are read from environment variables (`.env`, loaded via
  `python-dotenv`). `.env` is git-ignored; only `.env.example` (with placeholder values) is
  committed.
- Uploaded CSVs are parsed with Python's stdlib `csv` module (no `eval`/dynamic code execution).
  Malformed rows are rejected with a `400` before anything is written to the database.
- **Known gap**: there is no authentication yet — anyone who can reach the API can upload a CSV
  or read past reports. Acceptable for a portfolio demo; before any real use, add at minimum an
  API key check on every endpoint.

# `app/llm_client.py`

Wraps the OpenAI SDK (Chat Completions). `generate_summary()` receives already-computed
totals/outliers and builds a prompt that explicitly tells the model not to recalculate anything —
only to write the narrative. Returns plain text. The model comes from `OPENAI_MODEL` (default
`gpt-5.4-nano`). The client is created once at module import time (`OPENAI_API_KEY` must be set
before this module is imported, same as `DATABASE_URL` in `app/db.py`) — same pattern used
everywhere else in this app, no lazy-singleton machinery.

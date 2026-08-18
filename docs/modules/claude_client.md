# `app/claude_client.py`

Wraps the Anthropic SDK. `generate_summary()` receives already-computed totals/outliers and
builds a prompt that explicitly tells Claude not to recalculate anything — only to write the
narrative. Returns plain text. The Anthropic client is created once at module import time
(`ANTHROPIC_API_KEY` must be set before this module is imported, same as `DATABASE_URL` in
`app/db.py`) — same pattern used everywhere else in this app, no lazy-singleton machinery.

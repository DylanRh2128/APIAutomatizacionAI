# `app/claude_client.py`

Wraps the Anthropic SDK. `generate_summary()` receives already-computed totals/outliers and
builds a prompt that explicitly tells Claude not to recalculate anything — only to write the
narrative. Returns plain text. The Anthropic client is created lazily (module-level singleton)
so importing this module never requires `ANTHROPIC_API_KEY` to be set — only calling
`generate_summary()` does.

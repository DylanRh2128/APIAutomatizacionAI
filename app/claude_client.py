import os

from anthropic import Anthropic

_client = None


def _get_client() -> Anthropic:
    global _client
    if _client is None:
        _client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    return _client


def generate_summary(totals_by_category: dict, total_amount: float, outliers: list[dict]) -> str:
    outliers_text = (
        "\n".join(
            f"- {o['date']}: {o['category']} — {o['amount']} ({o['description']})"
            for o in outliers
        )
        or "None"
    )
    categories_text = "\n".join(
        f"- {category}: {amount}" for category, amount in totals_by_category.items()
    )

    prompt = f"""You are writing a short executive summary of a small business's expenses for
this period. Use only the numbers given below — do not recalculate or invent any numbers.

Total expenses: {total_amount}

Totals by category:
{categories_text}

Unusual expenses (statistical outliers within their category):
{outliers_text}

Write a 2-4 paragraph executive summary in plain English: overall spending, the top
categories, and whether the unusual expenses deserve attention. No headings, no bullet points."""

    message = _get_client().messages.create(
        model="claude-3-5-haiku-latest",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text

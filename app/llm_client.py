import os

from openai import OpenAI

_client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = os.environ.get("OPENAI_MODEL", "gpt-5.4-nano")
LANGUAGES = {"en": "English", "es": "Spanish"}


def generate_summary(
    totals_by_category: dict, total_amount: float, outliers: list[dict], language: str = "en"
) -> str:
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

Write a 2-4 paragraph executive summary in plain {LANGUAGES[language]}: overall spending, the top
categories, and whether the unusual expenses deserve attention. No headings, no bullet points."""

    response = _client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

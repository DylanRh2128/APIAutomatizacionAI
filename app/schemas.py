from datetime import date, datetime

from pydantic import BaseModel


class ExpenseOut(BaseModel):
    date: date
    category: str
    amount: float
    description: str

    model_config = {"from_attributes": True}


class ReportListItem(BaseModel):
    id: int
    created_at: datetime
    period_start: date
    period_end: date
    total_amount: float
    source_filename: str

    model_config = {"from_attributes": True}


class ReportOut(ReportListItem):
    summary_text: str
    expenses: list[ExpenseOut]

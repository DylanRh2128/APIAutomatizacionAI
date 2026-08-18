from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.aggregation import aggregate_expenses
from app.claude_client import generate_summary
from app.csv_parser import parse_expenses_csv
from app.db import get_db
from app.models import Expense, Report
from app.schemas import ReportListItem, ReportOut

router = APIRouter()


@router.post("/reports", response_model=ReportOut)
async def create_report(file: UploadFile, db: Session = Depends(get_db)):
    raw = await file.read()
    try:
        rows = parse_expenses_csv(raw)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    aggregates = aggregate_expenses(rows)

    try:
        summary_text = generate_summary(
            totals_by_category=aggregates["totals_by_category"],
            total_amount=aggregates["total_amount"],
            outliers=aggregates["outliers"],
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Failed to generate summary: {e}")

    dates = [r["date"] for r in rows]
    report = Report(
        period_start=min(dates),
        period_end=max(dates),
        total_amount=aggregates["total_amount"],
        summary_text=summary_text,
        source_filename=file.filename or "unknown.csv",
    )
    report.expenses = [Expense(**row) for row in rows]

    db.add(report)
    db.commit()
    db.refresh(report)
    return report


@router.get("/reports", response_model=list[ReportListItem])
def list_reports(db: Session = Depends(get_db)):
    return db.query(Report).order_by(Report.created_at.desc()).all()


@router.get("/reports/{report_id}", response_model=ReportOut)
def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.get(Report, report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

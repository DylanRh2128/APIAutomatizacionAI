from fastapi import FastAPI

from app.db import Base, engine
from app import models  # noqa: F401 — registers models on Base before create_all
from app.reports import router as reports_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expense Report Summary API")
app.include_router(reports_router)


@app.get("/health")
def health():
    return {"status": "ok"}

import os
import threading
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, database
from backend.database import get_db
from backend.worker import run_osint_task
from backend.agents import run_agent_workflow
from pydantic import BaseModel

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Agentic Threat Intel API")

HF_MODE = os.getenv("HF_MODE", "").lower() == "true"

# ─── AUTO-CREATE DEMO USER ON STARTUP ───
def ensure_demo_user():
    from backend.database import SessionLocal
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.username == "demo").first()
        if not user:
            user = models.User(username="demo", hashed_password="demo")
            db.add(user)
            db.commit()
    finally:
        db.close()

ensure_demo_user()

class QueryRequest(BaseModel):
    query: str

def run_osint_sync(report_id: int, query: str):
    from backend.database import SessionLocal
    db = SessionLocal()
    try:
        report = db.query(models.OSINTReport).filter(models.OSINTReport.id == report_id).first()
        if not report:
            return
        report.status = "processing"
        report.phase = "parsing"
        db.commit()

        findings = run_agent_workflow(report_id, query, db)

        report.findings = findings
        report.status = "completed"
        report.phase = "completed"
        from datetime import datetime
        report.completed_at = datetime.utcnow()
        db.commit()
    except Exception as e:
        db.rollback()
        report = db.query(models.OSINTReport).filter(models.OSINTReport.id == report_id).first()
        if report:
            report.status = "failed"
            report.phase = "failed"
            report.findings = f"Error: {str(e)}"
            db.commit()
    finally:
        db.close()

@app.post("/api/v1/run_osint")
def run_osint(req: QueryRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == "demo").first()
    if not user:
        raise HTTPException(status_code=500, detail="Demo user not found")

    new_report = models.OSINTReport(user_id=user.id, query=req.query)
    db.add(new_report)
    db.commit()
    db.refresh(new_report)

    if HF_MODE:
        threading.Thread(target=run_osint_sync, args=(new_report.id, req.query), daemon=True).start()
    else:
        task = run_osint_task.delay(new_report.id, req.query)
        new_report.task_id = task.id
        db.commit()

    return {"id": new_report.id, "query": new_report.query, "status": new_report.status, "findings": new_report.findings}

@app.get("/api/v1/reports")
def get_reports(db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == "demo").first()
    if not user:
        raise HTTPException(status_code=500, detail="Demo user not found")
    reports = db.query(models.OSINTReport).filter(models.OSINTReport.user_id == user.id).order_by(models.OSINTReport.created_at.desc()).all()
    return reports

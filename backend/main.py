import os
import threading
from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend import models, database
from backend.database import get_db
from backend.worker import run_osint_task
from backend.agents import run_agent_workflow
from pydantic import BaseModel
from passlib.context import CryptContext

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Agentic Threat Intel API")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

HF_MODE = os.getenv("HF_MODE", "").lower() == "true"

class UserCreate(BaseModel):
    username: str
    password: str

class QueryRequest(BaseModel):
    username: str
    query: str

class ReportResponse(BaseModel):
    id: int
    query: str
    status: str
    findings: str | None

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

@app.post("/api/v1/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = pwd_context.hash(user.password)
    new_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created successfully"}

@app.post("/api/v1/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()
    if not db_user or not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful", "username": db_user.username}

@app.post("/api/v1/run_osint", response_model=ReportResponse)
def run_osint(req: QueryRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == req.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

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

    return new_report

@app.get("/api/v1/reports/{username}")
def get_reports(username: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    reports = db.query(models.OSINTReport).filter(models.OSINTReport.user_id == user.id).order_by(models.OSINTReport.created_at.desc()).all()
    return reports

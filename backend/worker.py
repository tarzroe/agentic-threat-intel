import os
from celery import Celery
from backend.agents import run_agent_workflow
from backend.database import SessionLocal
from backend.models import OSINTReport
from datetime import datetime

REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

celery_app = Celery("tasks", broker=REDIS_URL, backend=REDIS_URL)

@celery_app.task(bind=True, name="run_osint_task")
def run_osint_task(self, report_id: int, query: str):
    db = SessionLocal()
    try:
        report = db.query(OSINTReport).filter(OSINTReport.id == report_id).first()
        if not report:
            return

        report.status = "processing"
        report.phase = "parsing"
        db.commit()

        findings = run_agent_workflow(report_id, query, db_session=db)

        report.findings = findings
        report.status = "completed"
        report.phase = "completed"
        report.completed_at = datetime.utcnow()
        db.commit()
    except Exception as e:
        db.rollback()
        report = db.query(OSINTReport).filter(OSINTReport.id == report_id).first()
        if report:
            report.status = "failed"
            report.phase = "failed"
            report.findings = f"Error: {str(e)}"
            db.commit()
    finally:
        db.close()

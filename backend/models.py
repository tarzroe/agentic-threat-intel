import os
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.database import Base

is_sqlite = os.getenv("DATABASE_URL", "").startswith("sqlite")

datetime_kw = {"timezone": True} if not is_sqlite else {}

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(**datetime_kw), server_default=func.now())

class OSINTReport(Base):
    __tablename__ = "osint_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    query = Column(String, nullable=False)
    task_id = Column(String, index=True, nullable=True)
    status = Column(String, default="pending")
    phase = Column(String, default="pending")
    findings = Column(Text, nullable=True)
    created_at = Column(DateTime(**datetime_kw), server_default=func.now())
    completed_at = Column(DateTime(**datetime_kw), nullable=True)

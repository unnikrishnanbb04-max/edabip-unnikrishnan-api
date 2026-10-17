from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey, Boolean, Index
)
from sqlalchemy.sql import func

from app.database import Base


class ReportSchedule(Base):
    __tablename__ = "report_schedules"
    __table_args__ = (
        Index("ix_report_schedules_active_next_run", "is_active", "next_run"),
    )

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(
        Integer, ForeignKey("reports.id"), nullable=False, index=True
    )
    frequency = Column(String(30), nullable=False)
    next_run = Column(DateTime, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
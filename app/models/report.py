
from sqlalchemy import (
    Column, Integer, String, DateTime, Float, ForeignKey
)
from sqlalchemy.sql import func

from app.database import Base
from sqlalchemy import Index

class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (
    Index("ix_reports_status_created_at", "status", "created_at"),
    Index("ix_reports_type_created_at", "report_type", "created_at"),
    Index("ix_reports_owner", "owner"),)
    id = Column(Integer, primary_key=True, index=True)
    report_name = Column(String(150), nullable=False, index=True)
    module = Column(String(100), nullable=False)
    report_type = Column(String(30), nullable=False)
    template_id = Column(
        Integer,
        ForeignKey("report_templates.id"),
        nullable=True
    )
    owner = Column(String(100), nullable=False)
    status = Column(String(30), default="Scheduled", nullable=False)
    last_run = Column(DateTime, nullable=True)
    run_time = Column(Float, default=0.0)
    created_at = Column(DateTime, server_default=func.now())

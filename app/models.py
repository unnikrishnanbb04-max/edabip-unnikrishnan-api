from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import relationship

from .database import Base


class ReportTemplate(Base):
    __tablename__ = "report_templates"

    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String(150), nullable=False)
    module = Column(String(100), nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime, default=datetime.utcnow)

    reports = relationship(
        "Report",
        back_populates="template"
    )


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    report_name = Column(String(200), nullable=False)
    module = Column(String(100), nullable=False)
    report_type = Column(String(30), nullable=False)
    template_id = Column(
        Integer,
        ForeignKey("report_templates.id"),
        nullable=True
    )
    owner = Column(String(100), nullable=False)
    status = Column(String(30), nullable=False)
    last_run = Column(DateTime, nullable=True)
    run_time_seconds = Column(Numeric(10, 2), default=0)
    created_at = Column(DateTime, default=datetime.utcnow)

    template = relationship(
        "ReportTemplate",
        back_populates="reports"
    )

    activities = relationship(
        "ReportActivity",
        back_populates="report",
        cascade="all, delete-orphan"
    )


class ReportActivity(Base):
    __tablename__ = "report_activity"

    id = Column(Integer, primary_key=True, index=True)

    report_id = Column(
        Integer,
        ForeignKey("reports.id"),
        nullable=False
    )

    action = Column(String(100), nullable=False)

    status = Column(String(30), nullable=False)

    message = Column(String(500))

    started_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    completed_at = Column(DateTime, nullable=True)

    run_time_seconds = Column(
        Numeric(10, 2),
        default=0
    )

    report = relationship(
        "Report",
        back_populates="activities"
    )
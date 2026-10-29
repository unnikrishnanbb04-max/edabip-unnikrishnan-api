from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Index, Integer, String, Text, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

def utcnow():
    return datetime.now(timezone.utc)

class ReportTemplate(Base):
    __tablename__ = "report_templates"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    template_name: Mapped[str] = mapped_column(String(150), nullable=False, index=True)
    module: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    reports: Mapped[list["Report"]] = relationship(back_populates="template")

class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (
        Index("ix_reports_status_type", "status", "report_type"),
        Index("ix_reports_created_at", "created_at"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    module: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    report_type: Mapped[str] = mapped_column(String(20), nullable=False, index=True)  # Scheduled / On Demand
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="Scheduled", index=True)
    owner: Mapped[str] = mapped_column(String(120), nullable=False)
    last_run: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    run_duration_seconds: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    template_id: Mapped[int | None] = mapped_column(ForeignKey("report_templates.id", ondelete="SET NULL"), index=True)
    template: Mapped[ReportTemplate | None] = relationship(back_populates="reports")
    activities: Mapped[list["ReportActivity"]] = relationship(back_populates="report", cascade="all, delete-orphan")
    schedules: Mapped[list["ReportSchedule"]] = relationship(back_populates="report", cascade="all, delete-orphan")

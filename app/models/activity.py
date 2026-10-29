from datetime import datetime, timezone
from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, Float, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

def utcnow():
    return datetime.now(timezone.utc)

class ReportActivity(Base):
    __tablename__ = "report_activity"
    __table_args__ = (
        UniqueConstraint("schedule_id", "scheduled_for", name="uq_activity_schedule_time"),
        Index("ix_activity_status_created", "status", "created_at"),
    )
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id", ondelete="CASCADE"), nullable=False, index=True)
    schedule_id: Mapped[int | None] = mapped_column(ForeignKey("report_schedules.id", ondelete="SET NULL"), nullable=True, index=True)
    scheduled_for: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    action: Mapped[str] = mapped_column(String(30), nullable=False, default="run")
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    message: Mapped[str | None] = mapped_column(Text)
    duration_seconds: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False, index=True)
    report: Mapped["Report"] = relationship(back_populates="activities")
    schedule: Mapped["ReportSchedule | None"] = relationship(back_populates="runs")

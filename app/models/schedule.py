from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

def utcnow():
    return datetime.now(timezone.utc)

class ReportSchedule(Base):
    __tablename__ = "report_schedules"
    __table_args__ = (Index("ix_schedules_active_next_run", "is_active", "next_run"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id", ondelete="CASCADE"), nullable=False, index=True)
    frequency: Mapped[str] = mapped_column(String(20), nullable=False)
    next_run: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow, nullable=False)
    report: Mapped["Report"] = relationship(back_populates="schedules")
    runs: Mapped[list["ReportActivity"]] = relationship(back_populates="schedule")

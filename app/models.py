from sqlalchemy import String, DateTime, Boolean, ForeignKey, Integer, Text, UniqueConstraint, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120))
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="Viewer", index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    reports = relationship("Report", back_populates="owner")

class ReportTemplate(Base):
    __tablename__ = "report_templates"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(160), unique=True)
    module: Mapped[str] = mapped_column(String(80), index=True)
    description: Mapped[str | None] = mapped_column(Text)
    reports = relationship("Report", back_populates="template")

class Report(Base):
    __tablename__ = "reports"
    __table_args__ = (Index("ix_reports_status_created", "status", "created_at"), Index("ix_reports_type_module", "report_type", "module"))
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(180), index=True)
    module: Mapped[str] = mapped_column(String(80), index=True)
    report_type: Mapped[str] = mapped_column(String(20), default="On Demand", index=True)
    status: Mapped[str] = mapped_column(String(20), default="Scheduled", index=True)
    owner_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), index=True)
    template_id: Mapped[int | None] = mapped_column(ForeignKey("report_templates.id", ondelete="SET NULL"), index=True)
    last_run_at: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
    run_duration_ms: Mapped[int | None] = mapped_column(Integer)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    owner = relationship("User", back_populates="reports")
    template = relationship("ReportTemplate", back_populates="reports")
    activities = relationship("ReportActivity", back_populates="report", cascade="all, delete-orphan")
    schedules = relationship("ReportSchedule", back_populates="report", cascade="all, delete-orphan")

class ReportSchedule(Base):
    __tablename__ = "report_schedules"
    __table_args__ = (UniqueConstraint("report_id", "frequency", name="uq_schedule_report_frequency"), Index("ix_schedule_active_due", "is_active", "next_run_at"))
    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int] = mapped_column(ForeignKey("reports.id", ondelete="CASCADE"), index=True)
    frequency: Mapped[str] = mapped_column(String(20))
    next_run_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, index=True)
    last_claimed_for: Mapped[DateTime | None] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    report = relationship("Report", back_populates="schedules")

class ReportActivity(Base):
    __tablename__ = "report_activity"
    __table_args__ = (Index("ix_activity_status_created", "status", "created_at"), Index("ix_activity_action_created", "action", "created_at"))
    id: Mapped[int] = mapped_column(primary_key=True)
    report_id: Mapped[int | None] = mapped_column(ForeignKey("reports.id", ondelete="SET NULL"), index=True)
    action: Mapped[str] = mapped_column(String(40))
    status: Mapped[str] = mapped_column(String(20), index=True)
    message: Mapped[str | None] = mapped_column(Text)
    run_duration_ms: Mapped[int | None] = mapped_column(Integer)
    request_id: Mapped[str | None] = mapped_column(String(64), index=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)
    report = relationship("Report", back_populates="activities")

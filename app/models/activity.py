
from sqlalchemy import Column, Index, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.sql import func

from app.database import Base


class ReportActivity(Base):
    __tablename__ = "report_activity"

    __table_args__ = (
        Index("ix_activity_status_created_at", "status", "created_at"),
        Index("ix_activity_username", "username"),
    )

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(
        Integer,
        ForeignKey("reports.id"),
        nullable=True
    )
    username = Column(String(100), nullable=False)
    action = Column(String(100), nullable=False)
    status = Column(String(30), nullable=False)
    details = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now())

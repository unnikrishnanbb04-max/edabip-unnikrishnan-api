
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models import ReportSchedule, Report, User
from app.exceptions import not_found
from app.services.report_service import record_activity


def create_schedule(db: Session, data, user: User):
    report = db.query(Report).filter(
        Report.id == data.report_id
    ).first()

    if not report:
        raise not_found("Report not found")

    if data.next_run <= datetime.now(timezone.utc).replace(tzinfo=None):
        raise ValueError("next_run must be in the future")

    schedule = ReportSchedule(
        report_id=data.report_id,
        frequency=data.frequency,
        next_run=data.next_run,
        is_active=True
    )

    db.add(schedule)

    record_activity(
        db, report.id, user.username,
        "Schedule created", "Completed",
        f"{data.frequency} schedule created"
    )

    db.commit()
    db.refresh(schedule)
    return schedule

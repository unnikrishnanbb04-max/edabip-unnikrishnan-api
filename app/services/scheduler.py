import logging
from datetime import datetime, timezone
from dateutil.relativedelta import relativedelta
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.report import Report
from app.models.schedule import ReportSchedule
from app.models.activity import ReportActivity

logger = logging.getLogger("reports_api")

def next_occurrence(current: datetime, frequency: str) -> datetime:
    if frequency == "Daily":
        from datetime import timedelta
        return current + timedelta(days=1)
    if frequency == "Weekly":
        from datetime import timedelta
        return current + timedelta(weeks=1)
    if frequency == "Monthly":
        return current + relativedelta(months=1)
    raise ValueError("Unsupported schedule frequency")

def run_due_schedules(db: Session, now: datetime | None = None) -> int:
    now = now or datetime.now(timezone.utc)
    # PostgreSQL row locks avoid two workers claiming the same due schedule simultaneously.
    stmt = select(ReportSchedule).where(
        ReportSchedule.is_active.is_(True), ReportSchedule.next_run <= now
    ).order_by(ReportSchedule.id).with_for_update(skip_locked=True)
    schedules = db.scalars(stmt).all()
    ran = 0
    for schedule in schedules:
        scheduled_for = schedule.next_run
        # Unique (schedule_id, scheduled_for) is the final guard against duplicate runs.
        existing = db.scalar(select(ReportActivity.id).where(
            ReportActivity.schedule_id == schedule.id,
            ReportActivity.scheduled_for == scheduled_for
        ))
        if existing:
            schedule.next_run = next_occurrence(scheduled_for, schedule.frequency)
            continue
        report = db.get(Report, schedule.report_id)
        if report is None:
            schedule.is_active = False
            continue
        # Deterministic dummy work: report IDs divisible by 7 simulate failure.
        status = "Failed" if report.id % 7 == 0 else "Completed"
        duration = float((report.id % 5) + 1)
        activity = ReportActivity(
            report_id=report.id, schedule_id=schedule.id, scheduled_for=scheduled_for,
            action="scheduled_run", status=status,
            message="Simulated scheduled execution", duration_seconds=duration
        )
        db.add(activity)
        report.status = status
        report.last_run = now
        report.run_duration_seconds = duration
        schedule.next_run = next_occurrence(scheduled_for, schedule.frequency)
        ran += 1
        logger.info("schedule_id=%s report_id=%s status=%s scheduled_for=%s", schedule.id, report.id, status, scheduled_for.isoformat())
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        logger.warning("Duplicate scheduled activity prevented by unique constraint")
        return 0
    return ran

def scheduler_tick():
    db = SessionLocal()
    try:
        return run_due_schedules(db)
    except Exception:
        db.rollback()
        logger.exception("Scheduler tick failed")
        return 0
    finally:
        db.close()

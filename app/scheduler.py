import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from app.database import SessionLocal
from app.models import ReportSchedule, Report, ReportActivity
log = logging.getLogger("reports.scheduler")
def add_frequency(dt, frequency):
    if frequency == "Daily": return dt + timedelta(days=1)
    if frequency == "Weekly": return dt + timedelta(days=7)
    if frequency == "Monthly": return dt + timedelta(days=30)  # Demo approximation; use calendar arithmetic for production.
    raise ValueError("Invalid frequency")
def run_due_schedules(db=None):
    own = db is None
    session = db or SessionLocal()
    count = 0
    try:
        now = datetime.now(timezone.utc)
        stmt = select(ReportSchedule).where(ReportSchedule.is_active.is_(True), ReportSchedule.next_run_at <= now).with_for_update(skip_locked=True)
        for s in session.scalars(stmt).all():
            scheduled_for = s.next_run_at
            s.last_claimed_for = scheduled_for
            s.next_run_at = add_frequency(s.frequency, scheduled_for)
            r = session.get(Report, s.report_id)
            if r:
                failed = "fail" in r.name.lower()
                r.status = "Failed" if failed else "Completed"
                r.last_run_at = now
                r.run_duration_ms = 1250 if failed else 820
                session.add(ReportActivity(report_id=r.id, action="scheduled_run", status=r.status, message=f"Scheduled run for {scheduled_for.isoformat()}", run_duration_ms=r.run_duration_ms))
            log.info("schedule_id=%s scheduled_for=%s", s.id, scheduled_for)
            count += 1
        session.commit()
        return count
    except Exception:
        session.rollback()
        log.exception("scheduler batch failed")
        raise
    finally:
        if own: session.close()

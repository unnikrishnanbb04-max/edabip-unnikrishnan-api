from datetime import datetime, timedelta, timezone
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base
from app.models import Report, ReportSchedule, ReportActivity
from app.services.scheduler import run_due_schedules

def make_db():
    engine = create_engine("sqlite://", connect_args={"check_same_thread":False}, poolclass=StaticPool)
    Base.metadata.create_all(engine)
    return engine, sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)

def test_due_schedule_runs_once():
    engine, Session = make_db()
    now = datetime.now(timezone.utc)
    with Session() as db:
        report = Report(report_name="Due", module="Finance", report_type="Scheduled", status="Scheduled", owner="A")
        db.add(report); db.flush()
        schedule = ReportSchedule(report_id=report.id, frequency="Daily", next_run=now-timedelta(minutes=2), is_active=True)
        db.add(schedule); db.commit()
        assert run_due_schedules(db, now) == 1
        assert run_due_schedules(db, now) == 0
        assert db.scalar(select(ReportActivity.id).where(ReportActivity.schedule_id == schedule.id)) is not None
    engine.dispose()

def test_paused_schedule_does_not_run():
    engine, Session = make_db()
    now = datetime.now(timezone.utc)
    with Session() as db:
        report = Report(report_name="Paused", module="Finance", report_type="Scheduled", status="Scheduled", owner="A")
        db.add(report); db.flush()
        schedule = ReportSchedule(report_id=report.id, frequency="Daily", next_run=now-timedelta(minutes=2), is_active=False)
        db.add(schedule); db.commit()
        assert run_due_schedules(db, now) == 0
        assert db.scalar(select(ReportActivity.id)) is None
    engine.dispose()

from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ReportSchedule


def list_schedules(
    db: Session,
    active: bool | None = None,
):
    statement = select(ReportSchedule)

    if active is not None:
        statement = statement.where(
            ReportSchedule.is_active == active
        )

    statement = statement.order_by(
        ReportSchedule.id.desc()
    )

    return db.scalars(statement).all()


def create_schedule(
    db: Session,
    schedule: ReportSchedule,
):
    try:
        db.add(schedule)
        db.commit()
        db.refresh(schedule)
        return schedule
    except Exception:
        db.rollback()
        raise


def get_schedule(
    db: Session,
    schedule_id: int,
):
    return db.get(ReportSchedule, schedule_id)


def update_schedule(
    db: Session,
    schedule: ReportSchedule,
):
    try:
        db.commit()
        db.refresh(schedule)
        return schedule
    except Exception:
        db.rollback()
        raise


def delete_schedule(
    db: Session,
    schedule: ReportSchedule,
):
    try:
        db.delete(schedule)
        db.commit()
    except Exception:
        db.rollback()
        raise


def get_due_schedules(
    db: Session,
    current_time: datetime,
):
    statement = (
        select(ReportSchedule)
        .where(
            ReportSchedule.is_active.is_(True),
            ReportSchedule.next_run <= current_time,
        )
        .order_by(ReportSchedule.next_run.asc())
    )

    return db.scalars(statement).all()

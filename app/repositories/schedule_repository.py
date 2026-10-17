
from sqlalchemy.orm import Session

from app.models import ReportSchedule


def list_schedules(db: Session):
    return db.query(ReportSchedule).order_by(
        ReportSchedule.id.desc()
    ).all()


def create_schedule(db: Session, schedule: ReportSchedule):
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule


def get_schedule(db: Session, schedule_id: int):
    return db.query(ReportSchedule).filter(
        ReportSchedule.id == schedule_id
    ).first()

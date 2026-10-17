
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, ReportSchedule, Report
from app.schemas.schedule import (
    ScheduleCreate, ScheduleUpdate, ScheduleResponse
)
from app.services.auth_service import require_admin
from app.exceptions import not_found

router = APIRouter(prefix="/schedules", tags=["Schedules"])


@router.post("/", response_model=ScheduleResponse, status_code=201)
def create_schedule(
    data: ScheduleCreate,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    if data.next_run.replace(tzinfo=None) <= datetime.utcnow():
        raise HTTPException(422, "next_run must be in the future")

    report = db.query(Report).filter(
        Report.id == data.report_id
    ).first()

    if not report:
        raise not_found("Report not found")

    schedule = ReportSchedule(**data.model_dump(), is_active=True)
    db.add(schedule)
    db.commit()
    db.refresh(schedule)
    return schedule


@router.get("/", response_model=list[ScheduleResponse])
def list_schedules(
    active: bool | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    query = db.query(ReportSchedule)

    if active is not None:
        query = query.filter(ReportSchedule.is_active == active)

    return query.order_by(ReportSchedule.id.desc()).all()


@router.patch("/{schedule_id}", response_model=ScheduleResponse)
def update_schedule(
    schedule_id: int,
    data: ScheduleUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    schedule = db.query(ReportSchedule).filter(
        ReportSchedule.id == schedule_id
    ).first()

    if not schedule:
        raise not_found("Schedule not found")

    changes = data.model_dump(exclude_unset=True)

    if "next_run" in changes and changes["next_run"] is not None:
        if changes["next_run"].replace(tzinfo=None) <= datetime.utcnow():
            raise HTTPException(422, "next_run must be in the future")

    for field, value in changes.items():
        setattr(schedule, field, value)

    db.commit()
    db.refresh(schedule)
    return schedule


@router.patch("/{schedule_id}/pause", response_model=ScheduleResponse)
def pause_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    schedule = db.query(ReportSchedule).filter(
        ReportSchedule.id == schedule_id
    ).first()

    if not schedule:
        raise not_found("Schedule not found")

    schedule.is_active = False
    db.commit()
    db.refresh(schedule)
    return schedule


@router.patch("/{schedule_id}/resume", response_model=ScheduleResponse)
def resume_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    schedule = db.query(ReportSchedule).filter(
        ReportSchedule.id == schedule_id
    ).first()

    if not schedule:
        raise not_found("Schedule not found")

    if schedule.next_run.replace(tzinfo=None) <= datetime.utcnow():
        raise HTTPException(
            422, "Update next_run to a future time before resuming"
        )

    schedule.is_active = True
    db.commit()
    db.refresh(schedule)
    return schedule

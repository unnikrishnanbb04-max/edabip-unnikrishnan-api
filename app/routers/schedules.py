from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models.user import User
from app.models.report import Report
from app.models.schedule import ReportSchedule
from app.models.activity import ReportActivity
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate, ScheduleResponse

router = APIRouter(prefix="/schedules", tags=["Schedules"])

@router.post("", response_model=ScheduleResponse, status_code=201, summary="Create a report schedule")
def create_schedule(payload: ScheduleCreate, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    if db.get(Report, payload.report_id) is None:
        raise HTTPException(status_code=404, detail="Report not found")
    item = ReportSchedule(**payload.model_dump())
    db.add(item); db.commit(); db.refresh(item)
    return item

@router.get("", summary="List schedules with pagination")
def list_schedules(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100),
                   active: bool | None = None, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    stmt = select(ReportSchedule)
    if active is not None:
        stmt = stmt.where(ReportSchedule.is_active == active)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.scalars(stmt.order_by(ReportSchedule.id.desc()).offset((page-1)*size).limit(size)).all()
    return {"items": [ScheduleResponse.model_validate(x).model_dump(mode="json") for x in items], "total": total, "page": page, "size": size}

@router.get("/{schedule_id}", response_model=ScheduleResponse, summary="Get a schedule")
def get_schedule(schedule_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    item = db.get(ReportSchedule, schedule_id)
    if not item: raise HTTPException(status_code=404, detail="Schedule not found")
    return item

@router.patch("/{schedule_id}", response_model=ScheduleResponse, summary="Update a schedule")
def update_schedule(schedule_id: int, payload: ScheduleUpdate, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    item = db.get(ReportSchedule, schedule_id)
    if not item: raise HTTPException(status_code=404, detail="Schedule not found")
    for key, value in payload.model_dump(exclude_unset=True).items(): setattr(item, key, value)
    db.commit(); db.refresh(item)
    return item

@router.post("/{schedule_id}/pause", response_model=ScheduleResponse, summary="Pause a schedule")
def pause_schedule(schedule_id: int, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    item = db.get(ReportSchedule, schedule_id)
    if not item: raise HTTPException(status_code=404, detail="Schedule not found")
    item.is_active = False; db.commit(); db.refresh(item)
    return item

@router.post("/{schedule_id}/resume", response_model=ScheduleResponse, summary="Resume a schedule")
def resume_schedule(schedule_id: int, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    item = db.get(ReportSchedule, schedule_id)
    if not item: raise HTTPException(status_code=404, detail="Schedule not found")
    item.is_active = True; db.commit(); db.refresh(item)
    return item

@router.get("/{schedule_id}/runs", summary="Get execution history for a schedule")
def schedule_runs(schedule_id: int, page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100),
                  db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if db.get(ReportSchedule, schedule_id) is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    stmt = select(ReportActivity).where(ReportActivity.schedule_id == schedule_id)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    items = db.scalars(stmt.order_by(ReportActivity.created_at.desc()).offset((page-1)*size).limit(size)).all()
    return {"items": [{"id":x.id,"report_id":x.report_id,"schedule_id":x.schedule_id,"status":x.status,"action":x.action,"scheduled_for":x.scheduled_for,"created_at":x.created_at,"message":x.message} for x in items], "total":total,"page":page,"size":size}

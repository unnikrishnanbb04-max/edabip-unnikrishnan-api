import csv, io
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.report import Report
from app.schemas.report import ReportCreate, ReportResponse, SummaryResponse
from app.repositories.reports import list_reports, get_summary, get_status_percentages, get_type_distribution, recent_reports, top_templates, list_activity
from app.services.reports import get_report_or_404, run_report
from sqlalchemy import select
from app.dependencies import get_current_user, require_admin


router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/summary", response_model=SummaryResponse, summary="Get report summary")
def summary(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return get_summary(db)

@router.get("/type-distribution", summary="Count reports by type")
def type_distribution(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return {"items": get_type_distribution(db)}

@router.get("/status-percentages", summary="Get report status percentages")
def status_percentages(db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return {"items": get_status_percentages(db)}

@router.get("/recent", summary="Get recent reports")
def recent(db: Session = Depends(get_db), limit: int = Query(10, ge=1, le=100), user: User = Depends(get_current_user)):
    items = db.scalars(
    select(Report)
    .order_by(Report.created_at.desc())
    .limit(limit)
).all()
    return {"items": [ReportResponse.model_validate(r).model_dump(mode="json") for r in items], "total": len(items), "page": 1, "size": len(items)}

@router.get("/top-templates", summary="Get most-used report templates")
def templates(db: Session = Depends(get_db), limit: int = Query(5, ge=1, le=50), user: User = Depends(get_current_user)):
    from app.repositories.reports import top_templates
    items = top_templates(db, limit)
    return {"items": items, "total": len(items), "page": 1, "size": len(items)}

@router.get("", response_model=None, summary="List reports with filtering and pagination")
def reports_list(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100),
                 search: str | None = None, status: str | None = None,
                 report_type: str | None = None, sort_by: str = "created_at",
                 order: str = Query("desc", pattern="^(asc|desc)$"),
                 date_from: datetime | None = None, date_to: datetime | None = None,
                 db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if sort_by not in {"id","report_name","module","report_type","status","owner","created_at","last_run"}:
        raise HTTPException(status_code=422, detail="Unsupported sort_by column")
    items, total = list_reports(db, page, size, search, status, report_type, sort_by, order, date_from, date_to)
    return {"items": [ReportResponse.model_validate(r).model_dump(mode="json") for r in items], "total": total, "page": page, "size": size}

@router.post("", response_model=ReportResponse, status_code=201, summary="Create a report")
def create_report(payload: ReportCreate, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    report = Report(**payload.model_dump(), status="Scheduled")
    db.add(report); db.commit(); db.refresh(report)
    return report

@router.get("/activity/list", summary="List recent activity")
def activity_list(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100),
                  search: str | None = None, status: str | None = None,
                  sort_by: str = "created_at", order: str = Query("desc", pattern="^(asc|desc)$"),
                  date_from: datetime | None = None, date_to: datetime | None = None,
                  db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    if sort_by not in {"id","status","created_at","report_id"}:
        raise HTTPException(status_code=422, detail="Unsupported sort_by column")
    items, total = list_activity(db, page, size, search, status, date_from, date_to, sort_by, order)
    return {"items": [{"id": x.id, "report_id": x.report_id, "schedule_id": x.schedule_id, "action": x.action, "status": x.status, "message": x.message, "duration_seconds": x.duration_seconds, "created_at": x.created_at.isoformat()} for x in items], "total": total, "page": page, "size": size}

@router.get("/activity/export.csv", summary="Export filtered recent activity as CSV")
def activity_csv(search: str | None = None, status: str | None = None,
                 date_from: datetime | None = None, date_to: datetime | None = None,
                 db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    items, _ = list_activity(db, 1, 10000, search, status, date_from, date_to)
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerow(["id","report_id","schedule_id","action","status","message","duration_seconds","created_at"])
    for x in items:
        writer.writerow([x.id,x.report_id,x.schedule_id,x.action,x.status,x.message,x.duration_seconds,x.created_at.isoformat()])
    buffer.seek(0)
    return StreamingResponse(iter([buffer.getvalue()]), media_type="text/csv", headers={"Content-Disposition": 'attachment; filename="recent_activity.csv"'})



@router.get("/{report_id}", response_model=ReportResponse, summary="Get a report")
def get_report(report_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    return get_report_or_404(db, report_id)

@router.post("/{report_id}/rerun", response_model=ReportResponse, summary="Re-run a report (Admin only)")
def rerun(report_id: int, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    return run_report(db, get_report_or_404(db, report_id), "rerun")

@router.delete("/{report_id}", status_code=204, summary="Delete a report (Admin only)")
def delete_report(report_id: int, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    report = get_report_or_404(db, report_id)
    db.delete(report); db.commit()
    return None


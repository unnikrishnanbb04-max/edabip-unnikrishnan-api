
import csv
from datetime import datetime
from io import StringIO

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Report
from app.schemas.report import (
    ReportCreate, ReportUpdate, ReportResponse
)
from app.services.auth_service import get_current_user, require_admin
from app.services import report_service
from app.repositories import report_repository as repo
from app.exceptions import not_found

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.post("/", response_model=ReportResponse, status_code=201)
def create_report(
    data: ReportCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return report_service.create_report(db, data, user)


@router.get("/")
def list_reports(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: str | None = None,
    report_type: str | None = None,
    sort_by: str = Query("id", pattern="^(id|report_name|module|report_type|owner|status|last_run|run_time|created_at)$"),
    order: str = Query("desc", pattern="^(asc|desc)$"),
    start_date: datetime | None = None,
    end_date: datetime | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    if status and status not in {"Completed", "Failed", "Scheduled"}:
        raise HTTPException(422, "Invalid status")

    if report_type and report_type not in {"Scheduled", "On Demand"}:
        raise HTTPException(422, "Invalid report_type")

    if start_date and end_date and start_date > end_date:
        raise HTTPException(422, "start_date must be before end_date")

    items, total = repo.list_reports(
        db, page, limit, status, report_type,
        sort_by, order, start_date, end_date
    )

    return {
        "items": items,
        "total": total,
        "page": page,
        "limit": limit,
        "total_pages": (total + limit - 1) // limit,
    }


@router.get("/export/csv")
def export_reports(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    rows = db.query(Report).order_by(Report.id).all()

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "id", "report_name", "module", "report_type",
        "owner", "status", "last_run", "run_time"
    ])

    for row in rows:
        writer.writerow([
            row.id, row.report_name, row.module, row.report_type,
            row.owner, row.status, row.last_run, row.run_time
        ])

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=reports.csv"
        },
    )


@router.get("/{report_id}", response_model=ReportResponse)
def get_report(
    report_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    report = repo.get_report(db, report_id)

    if not report:
        raise not_found("Report not found")

    return report


@router.patch("/{report_id}", response_model=ReportResponse)
def update_report(
    report_id: int,
    data: ReportUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    return report_service.update_report(db, report_id, data, user)


@router.delete("/{report_id}")
def delete_report(
    report_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    return report_service.delete_report(db, report_id, user)


@router.post("/{report_id}/run", response_model=ReportResponse)
def run_report(
    report_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    return report_service.run_report(db, report_id, user)

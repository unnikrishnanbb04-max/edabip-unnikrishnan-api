from datetime import datetime
from io import StringIO

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Report, ReportActivity
from ..schemas import ReportListResponse

router = APIRouter(
    prefix="/reports",
    tags=["Reports"]
)


@router.get(
    "/",
    response_model=ReportListResponse
)
def get_reports(
    page: int = 1,
    limit: int = 10,
    status: str | None = None,
    report_type: str | None = None,
    db: Session = Depends(get_db)
):
    if page < 1:
        raise HTTPException(
            status_code=422,
            detail="page must be greater than 0"
        )

    if limit < 1 or limit > 100:
        raise HTTPException(
            status_code=422,
            detail="limit must be between 1 and 100"
        )

    query = db.query(Report)

    if status:
        allowed_statuses = {
            "Completed",
            "Failed",
            "Scheduled"
        }

        if status not in allowed_statuses:
            raise HTTPException(
                status_code=422,
                detail="Invalid status"
            )

        query = query.filter(
            Report.status == status
        )

    if report_type:
        allowed_types = {
            "Scheduled",
            "On Demand"
        }

        if report_type not in allowed_types:
            raise HTTPException(
                status_code=422,
                detail="Invalid report type"
            )

        query = query.filter(
            Report.report_type == report_type
        )

    total = query.count()

    reports = (
        query
        .order_by(Report.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    total_pages = (
        (total + limit - 1) // limit
        if total
        else 0
    )

    return {
        "success": True,
        "data": reports,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages
        },
        "message": "Reports fetched successfully"
    }


@router.get("/{report_id}")
def get_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    report = (
        db.query(Report)
        .filter(Report.id == report_id)
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    return {
        "success": True,
        "data": report,
        "message": "Report fetched successfully"
    }


@router.post("/{report_id}/rerun")
def rerun_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    report = (
        db.query(Report)
        .filter(Report.id == report_id)
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    report.status = "Scheduled"

    activity = ReportActivity(
        report_id=report.id,
        action="Re-run",
        status="Scheduled",
        message="Report scheduled for re-run",
        started_at=datetime.utcnow()
    )

    db.add(activity)
    db.commit()
    db.refresh(report)

    return {
        "success": True,
        "data": report,
        "message": "Report scheduled for re-run"
    }


@router.get("/{report_id}/download")
def download_report(
    report_id: int,
    db: Session = Depends(get_db)
):
    report = (
        db.query(Report)
        .filter(Report.id == report_id)
        .first()
    )

    if not report:
        raise HTTPException(
            status_code=404,
            detail="Report not found"
        )

    if report.status != "Completed":
        raise HTTPException(
            status_code=400,
            detail="Only completed reports can be downloaded"
        )

    report.status = "Completed"

    activity = ReportActivity(
        report_id=report.id,
        action="Download",
        status="Completed",
        message="Report downloaded successfully",
        started_at=datetime.utcnow(),
        completed_at=datetime.utcnow()
    )

    db.add(activity)
    db.commit()

    csv_data = StringIO()

    csv_data.write(
        "id,report_name,module,report_type,owner,status,run_time_seconds\n"
    )

    csv_data.write(
        f"{report.id},"
        f"{report.report_name},"
        f"{report.module},"
        f"{report.report_type},"
        f"{report.owner},"
        f"{report.status},"
        f"{report.run_time_seconds}\n"
    )

    csv_data.seek(0)

    return StreamingResponse(
        iter([csv_data.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition":
                f"attachment; filename=report_{report.id}.csv"
        }
    )
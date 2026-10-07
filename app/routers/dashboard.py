from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Report

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)


@router.get("/summary")
def get_summary(
    db: Session = Depends(get_db)
):
    total = db.query(Report).count()

    completed = (
        db.query(Report)
        .filter(Report.status == "Completed")
        .count()
    )

    failed = (
        db.query(Report)
        .filter(Report.status == "Failed")
        .count()
    )

    scheduled = (
        db.query(Report)
        .filter(Report.status == "Scheduled")
        .count()
    )

    average = (
        db.query(
            func.avg(Report.run_time_seconds)
        )
        .filter(Report.run_time_seconds > 0)
        .scalar()
    )

    return {
        "success": True,
        "data": {
            "total_reports": total,
            "completed": completed,
            "failed": failed,
            "scheduled": scheduled,
            "average_run_time": round(float(average or 0), 2)
        },
        "message": "Summary fetched successfully"
    }


@router.get("/type-distribution")
def get_type_distribution(
    db: Session = Depends(get_db)
):
    results = (
        db.query(
            Report.report_type,
            func.count(Report.id)
        )
        .group_by(Report.report_type)
        .all()
    )

    data = [
        {
            "report_type": report_type,
            "count": count
        }
        for report_type, count in results
    ]

    return {
        "success": True,
        "data": data,
        "message": "Report type distribution fetched successfully"
    }


@router.get("/status-distribution")
def get_status_distribution(
    db: Session = Depends(get_db)
):
    total = db.query(Report).count()

    results = (
        db.query(
            Report.status,
            func.count(Report.id)
        )
        .group_by(Report.status)
        .all()
    )

    data = []

    for status, count in results:
        percentage = (
            (count / total) * 100
            if total
            else 0
        )

        data.append({
            "status": status,
            "count": count,
            "percentage": round(percentage, 2)
        })

    return {
        "success": True,
        "data": data,
        "message": "Status distribution fetched successfully"
    }


@router.get("/recent-reports")
def get_recent_reports(
    limit: int = 10,
    db: Session = Depends(get_db)
):
    if limit < 1 or limit > 100:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=422,
            detail="limit must be between 1 and 100"
        )

    reports = (
        db.query(Report)
        .order_by(
            Report.last_run.desc()
        )
        .limit(limit)
        .all()
    )

    return {
        "success": True,
        "data": reports,
        "message": "Recent reports fetched successfully"
    }
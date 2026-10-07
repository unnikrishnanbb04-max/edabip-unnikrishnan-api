from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import ReportActivity

router = APIRouter(
    prefix="/activity",
    tags=["Activity"]
)


@router.get("/")
def get_activity(
    page: int = 1,
    limit: int = 10,
    search: str | None = None,
    status: str | None = None,
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

    query = db.query(ReportActivity)

    if search:
        query = query.filter(
            ReportActivity.message.ilike(
                f"%{search}%"
            )
        )

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
            ReportActivity.status == status
        )

    total = query.count()

    activities = (
        query
        .order_by(
            ReportActivity.started_at.desc()
        )
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
        "data": activities,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages
        },
        "message": "Activity fetched successfully"
    }
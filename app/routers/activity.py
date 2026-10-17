
import csv
from io import StringIO

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.schemas.activity import ActivityResponse
from app.repositories.activity_repository import (
    list_activities, filtered_activities
)
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/activity", tags=["Activity"])


def validate_status(status: str | None):
    if status and status not in {"Completed", "Failed", "Scheduled"}:
        raise HTTPException(422, "Invalid activity status")


@router.get("/")
def get_activity(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    status: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    validate_status(status)

    items, total = list_activities(
        db, page, limit, status, search
    )

    return {
        "items": [
            ActivityResponse.model_validate(item).model_dump(mode="json")
            for item in items
        ],
        "total": total,
        "page": page,
        "limit": limit,
    }


@router.get("/export/csv")
def export_activity_csv(
    status: str | None = None,
    search: str | None = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    validate_status(status)

    activities = filtered_activities(db, status, search)

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "id", "report_id", "username", "action",
        "status", "details", "created_at"
    ])

    for activity in activities:
        writer.writerow([
            activity.id,
            activity.report_id,
            activity.username,
            activity.action,
            activity.status,
            activity.details,
            activity.created_at,
        ])

    output.seek(0)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=recent_activity.csv"
        },
    )

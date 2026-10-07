from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Report, ReportTemplate

router = APIRouter(
    prefix="/templates",
    tags=["Templates"]
)


@router.get("/top")
def get_top_templates(
    limit: int = 5,
    db: Session = Depends(get_db)
):
    if limit < 1 or limit > 20:
        from fastapi import HTTPException

        raise HTTPException(
            status_code=422,
            detail="limit must be between 1 and 20"
        )

    results = (
        db.query(
            ReportTemplate.id,
            ReportTemplate.template_name,
            func.count(Report.id).label(
                "report_count"
            )
        )
        .outerjoin(
            Report,
            Report.template_id == ReportTemplate.id
        )
        .group_by(
            ReportTemplate.id,
            ReportTemplate.template_name
        )
        .order_by(
            func.count(Report.id).desc()
        )
        .limit(limit)
        .all()
    )

    data = [
        {
            "template_id": template_id,
            "template_name": template_name,
            "report_count": report_count
        }
        for (
            template_id,
            template_name,
            report_count
        ) in results
    ]

    return {
        "success": True,
        "data": data,
        "message": "Top report templates fetched successfully"
    }
from sqlalchemy.orm import Session

from app.models import ReportActivity


def list_activities(
    db: Session,
    page: int = 1,
    limit: int = 10,
    status: str | None = None,
    search: str | None = None,
):
    query = db.query(ReportActivity)

    if status:
        query = query.filter(ReportActivity.status == status)

    if search:
        term = f"%{search}%"
        query = query.filter(
            ReportActivity.action.ilike(term)
            | ReportActivity.username.ilike(term)
            | ReportActivity.details.ilike(term)
        )

    total = query.count()

    items = (
        query.order_by(ReportActivity.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
        .all()
    )

    return items, total


def filtered_activities(
    db: Session,
    status: str | None = None,
    search: str | None = None,
):
    query = db.query(ReportActivity)

    if status:
        query = query.filter(ReportActivity.status == status)

    if search:
        term = f"%{search}%"
        query = query.filter(
            ReportActivity.action.ilike(term)
            | ReportActivity.username.ilike(term)
            | ReportActivity.details.ilike(term)
        )

    return query.order_by(ReportActivity.created_at.desc()).all()

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.models import ReportActivity


def filtered_activities(
    db: Session,
    status: str | None = None,
    search: str | None = None,
):
    statement = select(ReportActivity)

    if status:
        statement = statement.where(ReportActivity.status == status)

    if search:
        term = f"%{search}%"
        statement = statement.where(
            or_(
                ReportActivity.username.ilike(term),
                ReportActivity.action.ilike(term),
                ReportActivity.details.ilike(term),
            )
        )

    statement = statement.order_by(ReportActivity.created_at.desc())

    return db.scalars(statement).all()


def list_activities(
    db: Session,
    page: int,
    limit: int,
    status: str | None = None,
    search: str | None = None,
):
    statement = select(ReportActivity)
    count_statement = select(func.count()).select_from(ReportActivity)

    if status:
        statement = statement.where(ReportActivity.status == status)
        count_statement = count_statement.where(
            ReportActivity.status == status
        )

    if search:
        term = f"%{search}%"
        search_filter = or_(
            ReportActivity.username.ilike(term),
            ReportActivity.action.ilike(term),
            ReportActivity.details.ilike(term),
        )
        statement = statement.where(search_filter)
        count_statement = count_statement.where(search_filter)

    statement = (
        statement
        .order_by(ReportActivity.created_at.desc())
        .offset((page - 1) * limit)
        .limit(limit)
    )

    items = db.scalars(statement).all()
    total = db.scalar(count_statement) or 0

    return items, total


from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models import Report


def get_report(db: Session, report_id: int):
    statement = select(Report).where(Report.id == report_id)
    return db.scalar(statement)


def list_reports(
    db: Session,
    page: int,
    limit: int,
    status: str | None = None,
    report_type: str | None = None,
    sort_by: str = "id",
    order: str = "desc",
    start_date: datetime | None = None,
    end_date: datetime | None = None,
):
    statement = select(Report)
    count_statement = select(func.count()).select_from(Report)

    if status:
        statement = statement.where(Report.status == status)
        count_statement = count_statement.where(Report.status == status)

    if report_type:
        statement = statement.where(Report.report_type == report_type)
        count_statement = count_statement.where(
            Report.report_type == report_type
        )

    if start_date:
        statement = statement.where(Report.created_at >= start_date)
        count_statement = count_statement.where(
            Report.created_at >= start_date
        )

    if end_date:
        statement = statement.where(Report.created_at <= end_date)
        count_statement = count_statement.where(
            Report.created_at <= end_date
        )

    allowed_columns = {
        "id": Report.id,
        "report_name": Report.report_name,
        "module": Report.module,
        "report_type": Report.report_type,
        "owner": Report.owner,
        "status": Report.status,
        "last_run": Report.last_run,
        "run_time": Report.run_time,
        "created_at": Report.created_at,
    }

    column = allowed_columns[sort_by]
    statement = statement.order_by(
        column.asc() if order == "asc" else column.desc()
    )

    statement = statement.offset((page - 1) * limit).limit(limit)

    items = db.scalars(statement).all()
    total = db.scalar(count_statement) or 0

    return items, total

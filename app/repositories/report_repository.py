
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Report


SORT_COLUMNS = {
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


def get_report(db: Session, report_id: int):
    return db.query(Report).filter(
        Report.id == report_id
    ).first()


def list_reports(
    db: Session,
    page: int = 1,
    limit: int = 10,
    status: str | None = None,
    report_type: str | None = None,
    sort_by: str = "id",
    order: str = "desc",
    start_date: datetime | None = None,
    end_date: datetime | None = None,
):
    query = db.query(Report)

    if status:
        query = query.filter(Report.status == status)

    if report_type:
        query = query.filter(Report.report_type == report_type)

    if start_date:
        query = query.filter(Report.created_at >= start_date)

    if end_date:
        query = query.filter(Report.created_at <= end_date)

    column = SORT_COLUMNS[sort_by]

    if order == "desc":
        query = query.order_by(column.desc())
    else:
        query = query.order_by(column.asc())

    total = query.count()
    items = query.offset((page - 1) * limit).limit(limit).all()

    return items, total

from sqlalchemy import select, func, text
from sqlalchemy.orm import Session
from app.models.report import Report, ReportTemplate
from app.models.activity import ReportActivity
from app.models.schedule import ReportSchedule

SORT_COLUMNS = {
    "id": Report.id, "report_name": Report.report_name, "module": Report.module,
    "report_type": Report.report_type, "status": Report.status, "owner": Report.owner,
    "created_at": Report.created_at, "last_run": Report.last_run,
}

def list_reports(db: Session, page: int, size: int, search: str | None = None,
                 status_filter: str | None = None, report_type: str | None = None,
                 sort_by: str = "created_at", order: str = "desc",
                 date_from=None, date_to=None):
    stmt = select(Report)
    if search:
        stmt = stmt.where(Report.report_name.ilike(f"%{search}%"))
    if status_filter:
        stmt = stmt.where(Report.status == status_filter)
    if report_type:
        stmt = stmt.where(Report.report_type == report_type)
    if date_from:
        stmt = stmt.where(Report.created_at >= date_from)
    if date_to:
        stmt = stmt.where(Report.created_at <= date_to)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    col = SORT_COLUMNS.get(sort_by, Report.created_at)
    stmt = stmt.order_by(col.asc() if order == "asc" else col.desc()).offset((page-1)*size).limit(size)
    return db.scalars(stmt).all(), total

def get_summary(db: Session):
    total = db.scalar(select(func.count(Report.id))) or 0
    completed = db.scalar(select(func.count(Report.id)).where(Report.status == "Completed")) or 0
    failed = db.scalar(select(func.count(Report.id)).where(Report.status == "Failed")) or 0
    scheduled = db.scalar(select(func.count(ReportSchedule.id)).where(ReportSchedule.is_active.is_(True))) or 0
    avg = db.scalar(select(func.avg(Report.run_duration_seconds)).where(Report.run_duration_seconds.is_not(None))) or 0
    return {"total_reports": total, "completed": completed, "failed": failed, "scheduled": scheduled, "average_run_time_seconds": round(float(avg), 2)}

def get_status_percentages(db: Session):
    # Kept as parameterized SQL to demonstrate a clear aggregate query; values are bound parameters.
    sql = text("""
        SELECT status, COUNT(*) AS count,
               CASE WHEN (SELECT COUNT(*) FROM reports) = 0 THEN 0
                    ELSE ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM reports), 2)
               END AS percentage
        FROM reports
        WHERE status IN (:completed, :scheduled, :failed)
        GROUP BY status
    """)
    rows = db.execute(sql, {"completed": "Completed", "scheduled": "Scheduled", "failed": "Failed"}).mappings().all()
    by_status = {r["status"]: {"name": r["status"], "count": r["count"], "percentage": float(r["percentage"])} for r in rows}
    return [by_status.get(s, {"name": s, "count": 0, "percentage": 0.0}) for s in ("Completed", "Scheduled", "Failed")]

def get_type_distribution(db: Session):
    rows = db.execute(select(Report.report_type, func.count(Report.id)).group_by(Report.report_type)).all()
    return [{"name": r[0], "count": r[1]} for r in rows]

def recent_reports(db: Session, limit: int = 10):
    return db.scalars(select(Report).order_by(Report.created_at.desc()).limit(limit)).all()

def top_templates(db: Session, limit: int = 5):
    stmt = select(ReportTemplate, func.count(Report.id).label("usage_count")).outerjoin(Report, Report.template_id == ReportTemplate.id).group_by(ReportTemplate.id).order_by(func.count(Report.id).desc()).limit(limit)
    return [{"id": t.id, "template_name": t.template_name, "module": t.module, "usage_count": count} for t, count in db.execute(stmt).all()]

def list_activity(db: Session, page: int, size: int, search: str | None = None,
                  status_filter: str | None = None, date_from=None, date_to=None,
                  sort_by: str = "created_at", order: str = "desc"):
    allowed = {"id": ReportActivity.id, "status": ReportActivity.status, "created_at": ReportActivity.created_at, "report_id": ReportActivity.report_id}
    stmt = select(ReportActivity).join(Report, Report.id == ReportActivity.report_id)
    if search:
        stmt = stmt.where(Report.report_name.ilike(f"%{search}%"))
    if status_filter:
        stmt = stmt.where(ReportActivity.status == status_filter)
    if date_from:
        stmt = stmt.where(ReportActivity.created_at >= date_from)
    if date_to:
        stmt = stmt.where(ReportActivity.created_at <= date_to)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    col = allowed.get(sort_by, ReportActivity.created_at)
    stmt = stmt.order_by(col.asc() if order == "asc" else col.desc()).offset((page-1)*size).limit(size)
    return db.scalars(stmt).all(), total

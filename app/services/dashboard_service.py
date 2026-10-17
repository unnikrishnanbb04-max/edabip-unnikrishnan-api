
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import Report, ReportSchedule, ReportTemplate, ReportActivity


def get_dashboard(db: Session):
    total = db.query(Report).count()

    completed = db.query(Report).filter(
        Report.status == "Completed"
    ).count()

    failed = db.query(Report).filter(
        Report.status == "Failed"
    ).count()

    scheduled = db.query(ReportSchedule).filter(
        ReportSchedule.is_active.is_(True)
    ).count()

    average_run_time = db.query(
        func.avg(Report.run_time)
    ).filter(Report.last_run.isnot(None)).scalar()

    type_rows = db.query(
        Report.report_type,
        func.count(Report.id)
    ).group_by(Report.report_type).all()

    percentages = {
        "Completed": round(completed * 100 / total, 2) if total else 0,
        "Failed": round(failed * 100 / total, 2) if total else 0,
        "Scheduled": round(scheduled * 100 / total, 2) if total else 0,
    }

    recent = db.query(Report).order_by(
        Report.id.desc()
    ).limit(5).all()

    top_templates = db.query(
        ReportTemplate.id,
        ReportTemplate.template_name,
        func.count(Report.id).label("usage_count")
    ).outerjoin(
        Report, Report.template_id == ReportTemplate.id
    ).group_by(
        ReportTemplate.id, ReportTemplate.template_name
    ).order_by(
        func.count(Report.id).desc()
    ).limit(5).all()

    recent_activity = db.query(ReportActivity).order_by(
        ReportActivity.id.desc()
    ).limit(5).all()

    return {
        "summary": {
            "total_reports": total,
            "completed": completed,
            "failed": failed,
            "scheduled": scheduled,
            "average_run_time": round(average_run_time or 0, 4),
        },
        "type_distribution": {
            name: count for name, count in type_rows
        },
        "status_percentages": percentages,
        "recent_reports": recent,
        "top_templates": [
            {
                "id": row.id,
                "template_name": row.template_name,
                "usage_count": row.usage_count,
            }
            for row in top_templates
        ],
        "recent_activity": recent_activity,
    }

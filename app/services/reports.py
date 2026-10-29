from datetime import datetime, timezone
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.report import Report
from app.models.activity import ReportActivity

def run_report(db: Session, report: Report, action: str = "rerun"):
    # Placeholder work; replace with the actual report-generation function.
    status = "Failed" if report.id % 7 == 0 else "Completed"
    duration = float((report.id % 5) + 1)
    report.status = status
    report.last_run = datetime.now(timezone.utc)
    report.run_duration_seconds = duration
    db.add(ReportActivity(report_id=report.id, action=action, status=status,
                          message="Simulated report execution", duration_seconds=duration))
    db.commit()
    db.refresh(report)
    return report

def get_report_or_404(db: Session, report_id: int) -> Report:
    report = db.get(Report, report_id)
    if report is None:
        raise HTTPException(status_code=404, detail="Report not found")
    return report

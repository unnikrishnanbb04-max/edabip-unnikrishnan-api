
from datetime import datetime, timezone
from time import perf_counter

from sqlalchemy.orm import Session

from app.models import Report, ReportActivity, ReportTemplate, User
from app.exceptions import not_found
from app.repositories import report_repository as repo


def record_activity(
    db: Session,
    report_id: int | None,
    username: str,
    action: str,
    status: str,
    details: str | None = None
):
    activity = ReportActivity(
        report_id=report_id,
        username=username,
        action=action,
        status=status,
        details=details
    )
    db.add(activity)


def create_report(db: Session, data, user: User):
    if data.template_id is not None:
        template = db.query(ReportTemplate).filter(
            ReportTemplate.id == data.template_id
        ).first()

        if not template:
            raise not_found("Report template not found")

    report = Report(
        report_name=data.report_name,
        module=data.module,
        report_type=data.report_type,
        template_id=data.template_id,
        owner=user.username,
        status="Scheduled"
    )

    db.add(report)
    db.flush()

    record_activity(
        db, report.id, user.username,
        "Report created", "Completed",
        f"Created report: {report.report_name}"
    )

    db.commit()
    db.refresh(report)
    return report


def run_report(db: Session, report_id: int, user: User):
    report = repo.get_report(db, report_id)

    if not report:
        raise not_found("Report not found")

    started = perf_counter()

    try:
        # TODO: Execute the actual report-generation logic here.
        # This starter simulates a successful report run.
        report.status = "Completed"
        report.last_run = datetime.now(timezone.utc)
        report.run_time = round(perf_counter() - started, 4)

        record_activity(
            db, report.id, user.username,
            "Report run", "Completed",
            f"Ran report: {report.report_name}"
        )

        db.commit()
        db.refresh(report)
        return report

    except Exception:
        db.rollback()

        failed_report = repo.get_report(db, report_id)
        if failed_report:
            failed_report.status = "Failed"
            record_activity(
                db, report_id, user.username,
                "Report run", "Failed",
                "Report execution failed"
            )
            db.commit()

        raise


def update_report(db: Session, report_id: int, data, user: User):
    report = repo.get_report(db, report_id)

    if not report:
        raise not_found("Report not found")

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(report, field, value)

    record_activity(
        db, report.id, user.username,
        "Report updated", "Completed",
        f"Updated report: {report.report_name}"
    )

    db.commit()
    db.refresh(report)
    return report


def delete_report(db: Session, report_id: int, user: User):
    report = repo.get_report(db, report_id)

    if not report:
        raise not_found("Report not found")

    record_activity(
        db, report.id, user.username,
        "Report deleted", "Completed",
        f"Deleted report: {report.report_name}"
    )

    db.delete(report)
    db.commit()

    return {"message": "Report deleted successfully"}

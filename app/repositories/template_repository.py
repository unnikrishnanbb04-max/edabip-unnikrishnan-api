
from sqlalchemy.orm import Session

from app.models import ReportTemplate


def list_templates(db: Session):
    return db.query(ReportTemplate).order_by(
        ReportTemplate.id.desc()
    ).all()


def get_template(db: Session, template_id: int):
    return db.query(ReportTemplate).filter(
        ReportTemplate.id == template_id
    ).first()


def create_template(db: Session, template: ReportTemplate):
    db.add(template)
    db.commit()
    db.refresh(template)
    return template

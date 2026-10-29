
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import ReportTemplate


def list_templates(db: Session):
    statement = select(ReportTemplate).order_by(
        ReportTemplate.id.desc()
    )
    return db.scalars(statement).all()


def get_template(db: Session, template_id: int):
    statement = select(ReportTemplate).where(
        ReportTemplate.id == template_id
    )
    return db.scalars(statement).first()


def create_template(db: Session, template: ReportTemplate):
    db.add(template)
    db.commit()
    db.refresh(template)
    return template

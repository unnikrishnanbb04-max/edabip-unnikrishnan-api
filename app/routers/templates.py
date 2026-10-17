
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, ReportTemplate
from app.schemas.template import TemplateCreate, TemplateResponse
from app.repositories import template_repository as repo
from app.services.auth_service import get_current_user

router = APIRouter(prefix="/templates", tags=["Templates"])


@router.post("/", response_model=TemplateResponse, status_code=201)
def create_template(
    data: TemplateCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    template = ReportTemplate(**data.model_dump())
    return repo.create_template(db, template)


@router.get("/", response_model=list[TemplateResponse])
def get_templates(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    return repo.list_templates(db)


@router.get("/{template_id}", response_model=TemplateResponse)
def get_template(
    template_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user)
):
    from app.exceptions import not_found

    template = repo.get_template(db, template_id)
    if not template:
        raise not_found("Template not found")

    return template

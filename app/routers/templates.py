from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, require_admin
from app.models.report import ReportTemplate
from app.models.user import User

router = APIRouter(prefix="/templates", tags=["Report Templates"])

@router.get("", summary="List report templates")
def list_templates(page: int = Query(1, ge=1), size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    total = db.scalar(select(func.count(ReportTemplate.id))) or 0
    items = db.scalars(select(ReportTemplate).order_by(ReportTemplate.id).offset((page-1)*size).limit(size)).all()
    return {"items":[{"id":x.id,"template_name":x.template_name,"module":x.module,"description":x.description,"created_at":x.created_at} for x in items],"total":total,"page":page,"size":size}

@router.post("", status_code=201, summary="Create a report template")
def create_template(payload: dict, db: Session = Depends(get_db), user: User = Depends(require_admin)):
    name = payload.get("template_name"); module = payload.get("module")
    if not isinstance(name, str) or len(name.strip()) < 2 or not isinstance(module, str) or len(module.strip()) < 2:
        raise HTTPException(status_code=422, detail="template_name and module must be strings with at least 2 characters")
    item = ReportTemplate(template_name=name, module=module, description=payload.get("description"))
    db.add(item); db.commit(); db.refresh(item)
    return {"id":item.id,"template_name":item.template_name,"module":item.module,"description":item.description,"created_at":item.created_at}

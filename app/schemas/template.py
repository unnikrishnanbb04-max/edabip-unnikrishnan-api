
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TemplateCreate(BaseModel):
    template_name: str = Field(min_length=1, max_length=150)
    module: str = Field(min_length=1, max_length=100)
    description: str | None = None


class TemplateResponse(BaseModel):
    id: int
    template_name: str
    module: str
    description: str | None
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)

from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ScheduleCreate(BaseModel):
    report_id: int = Field(gt=0)
    frequency: Literal["Daily", "Weekly", "Monthly"]
    next_run: datetime


class ScheduleUpdate(BaseModel):
    frequency: Literal["Daily", "Weekly", "Monthly"] | None = None
    next_run: datetime | None = None


class ScheduleResponse(BaseModel):
    id: int
    report_id: int
    frequency: str
    next_run: datetime
    is_active: bool

    model_config = ConfigDict(from_attributes=True)
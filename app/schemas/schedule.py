from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class ScheduleCreate(BaseModel):
    report_id: int
    frequency: str = Field(pattern="^(Daily|Weekly|Monthly)$")
    next_run: datetime
    is_active: bool = True

class ScheduleUpdate(BaseModel):
    frequency: str | None = Field(default=None, pattern="^(Daily|Weekly|Monthly)$")
    next_run: datetime | None = None
    is_active: bool | None = None

class ScheduleResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    report_id: int
    frequency: str
    next_run: datetime
    is_active: bool
    created_at: datetime

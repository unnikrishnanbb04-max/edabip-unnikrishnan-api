
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class ReportCreate(BaseModel):
    report_name: str = Field(min_length=1, max_length=150)
    module: str = Field(min_length=1, max_length=100)
    report_type: Literal["Scheduled", "On Demand"]
    template_id: int | None = None


class ReportUpdate(BaseModel):
    report_name: str | None = Field(default=None, max_length=150)
    module: str | None = Field(default=None, max_length=100)
    report_type: Literal["Scheduled", "On Demand"] | None = None


class ReportResponse(BaseModel):
    id: int
    report_name: str
    module: str
    report_type: str
    template_id: int | None
    owner: str
    status: str
    last_run: datetime | None
    run_time: float

    model_config = ConfigDict(from_attributes=True)

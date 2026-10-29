from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

class ReportCreate(BaseModel):
    report_name: str = Field(min_length=2, max_length=200)
    module: str = Field(min_length=2, max_length=100)
    report_type: str = Field(pattern="^(Scheduled|On Demand)$")
    owner: str = Field(min_length=1, max_length=120)
    template_id: int | None = None

class ReportResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    report_name: str
    module: str
    report_type: str
    status: str
    owner: str
    last_run: datetime | None
    run_duration_seconds: float | None
    created_at: datetime
    template_id: int | None

class ActivityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    report_id: int
    schedule_id: int | None
    action: str
    status: str
    message: str | None
    duration_seconds: float | None
    created_at: datetime

class SummaryResponse(BaseModel):
    total_reports: int
    completed: int
    failed: int
    scheduled: int
    average_run_time_seconds: float

class DistributionItem(BaseModel):
    name: str
    count: int
    percentage: float | None = None

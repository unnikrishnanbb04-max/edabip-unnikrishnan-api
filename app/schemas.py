from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class ReportResponse(BaseModel):
    id: int
    report_name: str
    module: str
    report_type: str
    template_id: int | None = None
    owner: str
    status: str
    last_run: datetime | None = None
    run_time_seconds: Decimal
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ActivityResponse(BaseModel):
    id: int
    report_id: int
    action: str
    status: str
    message: Optional[str]
    started_at: datetime
    completed_at: Optional[datetime]
    run_time_seconds: float

    model_config = ConfigDict(from_attributes=True)


class SummaryResponse(BaseModel):
    total_reports: int
    completed: int
    failed: int
    scheduled: int
    average_run_time: float


class PaginationResponse(BaseModel):
    page: int
    limit: int
    total: int
    total_pages: int


class ActivityListResponse(BaseModel):
    items: list[ActivityResponse]
    pagination: PaginationResponse


class TypeDistributionItem(BaseModel):
    report_type: str
    count: int


class StatusDistributionItem(BaseModel):
    status: str
    count: int
    percentage: float


class TemplateRankingItem(BaseModel):
    template_id: int
    template_name: str
    report_count: int

class ReportListResponse(BaseModel):
    success: bool
    data: list[ReportResponse]
    pagination: PaginationResponse
    message: str
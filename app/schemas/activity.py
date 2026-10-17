
from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ActivityResponse(BaseModel):
    id: int
    report_id: int | None
    username: str
    action: str
    status: str
    details: str | None
    created_at: datetime | None

    model_config = ConfigDict(from_attributes=True)
